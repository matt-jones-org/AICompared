/**
 * Shared shapes for model providers. AICompared compares output across
 * providers, so each one implements the same `ModelClient` contract.
 */

/** Per-request generation options. Not every provider honors every field. */
export interface GenerateOptions {
  /** Override the client's default model. */
  model?: string;
  /** System / developer instruction, if the provider supports one. */
  system?: string;
  /** Sampling temperature. */
  temperature?: number;
  /** Cap on tokens generated in the response. */
  maxOutputTokens?: number;
}

/** Token accounting, when the provider reports it. */
export interface Usage {
  inputTokens?: number;
  outputTokens?: number;
}

/** A single model response, normalized across providers. */
export interface GenerateResult {
  provider: string;
  model: string;
  text: string;
  usage?: Usage;
}

/** A provider client capable of producing a completion for a prompt. */
export interface ModelClient {
  readonly provider: string;
  generate(prompt: string, options?: GenerateOptions): Promise<GenerateResult>;
}
