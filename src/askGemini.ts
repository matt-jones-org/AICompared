/**
 * Tiny CLI to sanity-check the Gemini client.
 * Run with: `npm run ask:gemini -- "your prompt here"`
 */
import { GeminiClient } from "./providers/gemini.js";

const prompt =
  process.argv.slice(2).join(" ").trim() ||
  "In one sentence, what is a good use for an AI model comparison tool?";

try {
  const client = new GeminiClient();
  const result = await client.generate(prompt);

  console.log(result.text);
  if (result.usage) {
    console.error(
      `\n[${result.model}] in=${result.usage.inputTokens ?? "?"} ` +
        `out=${result.usage.outputTokens ?? "?"} tokens`,
    );
  }
} catch (err) {
  console.error(
    `Gemini request failed: ${err instanceof Error ? err.message : String(err)}`,
  );
  process.exit(1);
}
