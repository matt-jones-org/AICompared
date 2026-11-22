# AICompared

An early-stage tool for comparing responses across AI providers. Right now it is
only the groundwork: a typed module that loads API keys for Anthropic, OpenAI,
Google, Mistral and Cohere from the environment, and a script that reports which
ones are configured. No provider is called yet.

## Setup

Requires Node.js and npm. The TypeScript sources run directly with `tsx`.

```sh
npm install
cp .env.example .env      # then add keys for the providers you want
npm run config:check
```

`config:check` lists each provider as configured or not. It only checks that a
key is present; it does not validate the key against the provider. `.env` is
gitignored, and anything already set in your real environment takes precedence
over it.

Other scripts:

- `npm run typecheck` runs `tsc --noEmit`.
- `npm run build` compiles `src/` to `dist/`.

## Layout

- `src/config.ts`: provider list, key lookup (`getApiKey`, `requireApiKey`,
  `isConfigured`, `configuredProviders`). Blank values count as unconfigured.
- `src/checkConfig.ts`: the `config:check` script.
- `.claude/`: a SessionStart hook that installs dependencies in Claude Code web
  sessions.

## Status

Scaffolding only. The next step is sending the same prompt to each configured
provider and showing the answers side by side; none of that exists yet.

## matt-jones-site/

Not part of this project. It is a temporary staged copy of the static site for
www.matt-jones.org, kept here until the site has its own repository. See its own
README.
