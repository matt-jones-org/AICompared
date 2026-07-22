/**
 * Minimal HTTP server for AICompared — something to actually run on a VM.
 * Dependency-free (Node's built-in http). Endpoints:
 *
 *   GET  /health                 -> { status: "ok" }
 *   GET  /providers              -> { configured: [...] }
 *   POST /ask                    -> body { prompt, model? } -> Gemini result
 *   GET  /auth/google/login      -> 302 redirect to Google's consent screen
 *   GET  /auth/google/callback   -> exchanges the code, returns sign-in summary
 *
 * Listens on $PORT (default 8080, the Google Cloud convention).
 */
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { randomBytes } from "node:crypto";
import { configuredProviders } from "./config.js";
import { GeminiClient } from "./providers/gemini.js";
import {
  buildAuthUrl,
  decodeIdToken,
  exchangeCodeForTokens,
} from "./oauth/google.js";

const PORT = Number(process.env.PORT ?? 8080);

/** Name of the cookie that carries the anti-CSRF OAuth `state` value. */
const STATE_COOKIE = "g_oauth_state";

function json(res: ServerResponse, status: number, body: unknown): void {
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
}

/** Parse a Cookie header into a plain name->value map. */
function parseCookies(header: string | undefined): Record<string, string> {
  const out: Record<string, string> = {};
  if (!header) return out;
  for (const pair of header.split(";")) {
    const eq = pair.indexOf("=");
    if (eq === -1) continue;
    const name = pair.slice(0, eq).trim();
    if (name) out[name] = decodeURIComponent(pair.slice(eq + 1).trim());
  }
  return out;
}

/** Build a Set-Cookie value with sane security defaults. maxAge is in seconds. */
function cookie(name: string, value: string, maxAge: number): string {
  const attrs = [
    `${name}=${encodeURIComponent(value)}`,
    "Path=/",
    "HttpOnly",
    "SameSite=Lax",
    `Max-Age=${maxAge}`,
  ];
  return attrs.join("; ");
}

async function readBody(req: IncomingMessage): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of req) chunks.push(chunk as Buffer);
  return Buffer.concat(chunks).toString("utf8");
}

const server = createServer(async (req: IncomingMessage, res: ServerResponse) => {
  try {
    const url = new URL(req.url ?? "/", `http://${req.headers.host ?? "localhost"}`);

    if (req.method === "GET" && url.pathname === "/health") {
      return json(res, 200, { status: "ok" });
    }

    if (req.method === "GET" && url.pathname === "/providers") {
      return json(res, 200, { configured: configuredProviders() });
    }

    if (req.method === "POST" && url.pathname === "/ask") {
      const raw = await readBody(req);
      let parsed: { prompt?: unknown; model?: unknown };
      try {
        parsed = raw ? JSON.parse(raw) : {};
      } catch {
        return json(res, 400, { error: "Request body must be valid JSON." });
      }
      const prompt = typeof parsed.prompt === "string" ? parsed.prompt.trim() : "";
      if (!prompt) {
        return json(res, 400, { error: "Field 'prompt' (non-empty string) is required." });
      }
      const client = new GeminiClient();
      const result = await client.generate(prompt, {
        model: typeof parsed.model === "string" ? parsed.model : undefined,
      });
      return json(res, 200, result);
    }

    // --- Google OAuth: step 1, send the user to the consent screen. ---
    if (req.method === "GET" && url.pathname === "/auth/google/login") {
      let authUrl: string;
      const state = randomBytes(16).toString("hex");
      try {
        authUrl = buildAuthUrl({ state });
      } catch (err) {
        // Misconfiguration (missing client id/secret or redirect URI).
        return json(res, 503, {
          error: err instanceof Error ? err.message : String(err),
        });
      }
      res.writeHead(302, {
        location: authUrl,
        // Bind the state to this browser so we can verify it on callback.
        "set-cookie": cookie(STATE_COOKIE, state, 600),
      });
      return res.end();
    }

    // --- Google OAuth: step 2, Google redirects back here with a code. ---
    if (req.method === "GET" && url.pathname === "/auth/google/callback") {
      const error = url.searchParams.get("error");
      if (error) {
        return json(res, 400, { error: `Authorization was denied: ${error}` });
      }

      const code = url.searchParams.get("code");
      const state = url.searchParams.get("state");
      const expectedState = parseCookies(req.headers.cookie)[STATE_COOKIE];

      if (!code || !state) {
        return json(res, 400, { error: "Missing 'code' or 'state' parameter." });
      }
      // Constant work either way; reject on any state mismatch (CSRF guard).
      if (!expectedState || state !== expectedState) {
        return json(res, 400, {
          error: "Invalid OAuth state — possible CSRF, or the login expired.",
        });
      }

      let tokens;
      try {
        tokens = await exchangeCodeForTokens(code);
      } catch (err) {
        return json(res, 502, {
          error: err instanceof Error ? err.message : String(err),
        });
      }

      const claims = tokens.idToken ? decodeIdToken(tokens.idToken) : undefined;

      // Clear the one-time state cookie now that the flow is complete.
      res.setHeader("set-cookie", cookie(STATE_COOKIE, "", 0));
      // Return a summary only — never echo the access/refresh tokens to the
      // browser. In a real app you'd persist them server-side against a session.
      return json(res, 200, {
        signedIn: true,
        user: claims ? { email: claims.email, name: claims.name } : undefined,
        grantedScopes: tokens.scope,
        accessTokenExpiresIn: tokens.expiresIn,
        refreshTokenGranted: Boolean(tokens.refreshToken),
      });
    }

    return json(res, 404, { error: `No route for ${req.method} ${url.pathname}` });
  } catch (err) {
    return json(res, 500, {
      error: err instanceof Error ? err.message : String(err),
    });
  }
});

server.listen(PORT, () => {
  console.log(`AICompared server listening on :${PORT}`);
});
