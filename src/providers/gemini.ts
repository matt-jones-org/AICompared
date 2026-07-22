/**
 * Gemini (Google AI Studio) model client.
 *
 * Uses the official `@google/genai` SDK with a GOOGLE_API_KEY — the standard,
 * recommended path for calling Gemini models. See `.env.example`.
 */
import { GoogleGenAI } from "@google/genai";
import { requireApiKey } from "../config.js";
import type { GenerateOptions, GenerateResult, ModelClient } from "./types.js";

/** Sensible default model — fast and inexpensive for comparisons. */
export const DEFAULT_GEMINI_MODEL = "gemini-2.5-flash";

export interface GeminiClientOptions {
  /** API key override; defaults to GOOGLE_API_KEY from the environment. */
  apiKey?: string;
  /** Default model to use when a request doesn't specify one. */
  defaultModel?: string;
}

export class GeminiClient implements ModelClient {
  readonly provider = "google";
  private readonly client: GoogleGenAI;
  private readonly defaultModel: string;

  constructor(options: GeminiClientOptions = {}) {
    const apiKey = options.apiKey ?? requireApiKey("google");
    this.client = new GoogleGenAI({ apiKey });
    this.defaultModel = options.defaultModel ?? DEFAULT_GEMINI_MODEL;
  }

  async generate(
    prompt: string,
    options: GenerateOptions = {},
  ): Promise<GenerateResult> {
    const model = options.model ?? this.defaultModel;

    const response = await this.client.models.generateContent({
      model,
      contents: prompt,
      config: {
        ...(options.system !== undefined
          ? { systemInstruction: options.system }
          : {}),
        ...(options.temperature !== undefined
          ? { temperature: options.temperature }
          : {}),
        ...(options.maxOutputTokens !== undefined
          ? { maxOutputTokens: options.maxOutputTokens }
          : {}),
      },
    });

    const usage = response.usageMetadata;
    return {
      provider: this.provider,
      model,
      text: response.text ?? "",
      usage: usage
        ? {
            inputTokens: usage.promptTokenCount,
            outputTokens: usage.candidatesTokenCount,
          }
        : undefined,
    };
  }
}
