/**
 * Minimal HTTP server for AICompared — something to actually run on a VM.
 * Dependency-free (Node's built-in http). Endpoints:
 *
 *   GET  /health     -> { status: "ok" }
 *   GET  /providers  -> { configured: [...] }
 *   POST /ask        -> body { prompt, model? } -> Gemini result
 *
 * Listens on $PORT (default 8080, the Google Cloud convention).
 */
import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { configuredProviders } from "./config.js";
import { GeminiClient } from "./providers/gemini.js";

const PORT = Number(process.env.PORT ?? 8080);

function json(res: ServerResponse, status: number, body: unknown): void {
  res.writeHead(status, { "content-type": "application/json" });
  res.end(JSON.stringify(body));
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
