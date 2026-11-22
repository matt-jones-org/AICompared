/**
 * Prints which provider API keys are currently configured.
 * Run with: `npm run config:check`
 *
 * Only reports whether each key is present; never print key values here.
 */
// ".js" is deliberate: this is an ES module and the specifier names the emitted file.
import { PROVIDERS, isConfigured, configuredProviders } from "./config.js";

console.log("AICompared — API key status\n");

for (const provider of PROVIDERS) {
  const ok = isConfigured(provider);
  console.log(`  ${ok ? "✓" : "✗"} ${provider}${ok ? "" : "  (not configured)"}`);
}

const configured = configuredProviders();
console.log(
  `\n${configured.length} of ${PROVIDERS.length} providers configured.` +
    (configured.length === 0
      ? " Copy .env.example to .env and add at least one key."
      : ""),
);
