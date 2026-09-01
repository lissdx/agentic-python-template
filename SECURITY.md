# Security

## Reporting a vulnerability

Open a [private security advisory](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)
on this repository rather than a public issue.

## What this repository must never contain

- **Credentials of any kind.** `.env` is ignored; `.env.example` carries variable
  names and never values. API keys, OAuth clients, refresh tokens and private
  keys are excluded by `.gitignore` — deliberately, before the first commit,
  because a public repository is a poor place to discover the gap.
- **Real data.** Inputs drawn from a production system carry whatever that system
  carried. Fixtures and eval sets are synthetic or redacted. Deleting a file does
  not remove it from history.

## Agent-specific surfaces worth stating

- **Prompt injection is an input, not an accident.** Content a tool retrieves —
  a page, a document, a message — reaches the model as text, and text can carry
  instructions. Treat it as untrusted input, not as context.
- **A tool is a capability boundary.** Whatever a tool can do, the model can be
  argued into doing. Scope credentials to the tool, not to the process.
