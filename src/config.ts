/**
 * Central configuration for AICompared.
 *
 * Loads provider API keys from the environment (via a local `.env` file in
 * development, or real environment variables in production) and exposes them
 * through a small typed API. Keys are never hardcoded — see `.env.example`.
 */
import "dotenv/config";

/** Providers AICompared knows how to talk to. */
export type Provider =
  | "anthropic"
  | "openai"
  | "google"
  | "mistral"
  | "cohere";

/** The environment variable that holds each provider's API key. */
const ENV_VAR: Record<Provider, string> = {
  anthropic: "ANTHROPIC_API_KEY",
  openai: "OPENAI_API_KEY",
  google: "GOOGLE_API_KEY",
  mistral: "MISTRAL_API_KEY",
  cohere: "COHERE_API_KEY",
};

/** All providers, in a stable order. */
export const PROVIDERS = Object.keys(ENV_VAR) as Provider[];

/**
 * Return the API key for a provider, or `undefined` if it isn't configured.
 * A blank/whitespace-only value is treated as unconfigured.
 */
export function getApiKey(provider: Provider): string | undefined {
  const value = process.env[ENV_VAR[provider]]?.trim();
  return value ? value : undefined;
}

/**
 * Return the API key for a provider, throwing a clear error if it's missing.
 * Use this at the point where a provider is actually invoked.
 */
export function requireApiKey(provider: Provider): string {
  const key = getApiKey(provider);
  if (!key) {
    throw new Error(
      `Missing API key for "${provider}". Set ${ENV_VAR[provider]} in your ` +
        `.env file (see .env.example for where to obtain it).`,
    );
  }
  return key;
}

/** Whether a provider has a usable API key configured. */
export function isConfigured(provider: Provider): boolean {
  return getApiKey(provider) !== undefined;
}

/** The subset of providers that currently have a key configured. */
export function configuredProviders(): Provider[] {
  return PROVIDERS.filter(isConfigured);
}

/** Google OAuth client credentials, for a user-delegated authorization flow. */
export interface GoogleOAuthConfig {
  clientId: string;
  clientSecret: string;
}

/**
 * Return the Google OAuth client credentials, or `undefined` if either the
 * client ID or client secret is missing. This is for a user-delegated OAuth
 * flow only — for standard Gemini model calls, use `getApiKey("google")`.
 */
export function getGoogleOAuthConfig(): GoogleOAuthConfig | undefined {
  const clientId = process.env.GOOGLE_OAUTH_CLIENT_ID?.trim();
  const clientSecret = process.env.GOOGLE_OAUTH_CLIENT_SECRET?.trim();
  if (!clientId || !clientSecret) return undefined;
  return { clientId, clientSecret };
}
