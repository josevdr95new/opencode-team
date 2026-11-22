# 🤖 OpenCode Team — Multi-Agent Team with SDD

[![Español](https://img.shields.io/badge/docs-Espa%C3%B1ol-blue)](README.md) [![English](https://img.shields.io/badge/docs-English-blue)](README.en.md) ![License](https://img.shields.io/badge/license-MIT-blue.svg) [![Skills](https://skills.sh/b/josevdr95new/opencode-team)](https://skills.sh/josevdr95new/opencode-team)

> 🇪🇸 **Versión en español:** [README.md](README.md)

A multi-agent development team for [OpenCode](https://opencode.ai) led by an **orchestrator**: you talk only to him, he analyzes, decides, delegates to the specialists, verifies quality, and reports back to you.

Inspired by public best practices in agent engineering: Anthropic's *orchestrator-worker* pattern (multi-agent research system) and GitHub Spec Kit's **SDD (Spec-Driven Development)** workflow.

## Architecture

```
                       YOU (any language)
                           │
                    ┌──────▼──────┐
                    │ ORCHESTRATOR │  ← default agent, decides and arbitrates
                    └──────┬──────┘
      ┌─────────┬─────────┬────────┼────────┬──────────┐
      ▼         ▼         ▼        ▼        ▼          ▼
  designer  frontend  backend  developer  debugger  security-auditor
  (impeccable)                  (fixes)  (systematic-  (security-audit,
                                           debugging +    read-only)
                                            browser)
      └─────────┴─────────┴────────┴─── everyone reports to the orchestrator ──┘
```

## The Team

| Agent | Role | Skills it uses |
|---|---|---|
| `orchestrator` | Boss: decides, delegates, arbitrates, consolidates. Does small tweaks himself; anything bigger is always delegated | `sdd`, `delegation` |
| `designer` | UI/UX: design specs, tokens and visual audit | `impeccable` (always; third-party, installed separately) |
| `frontend` | Builds interfaces with accessibility and complete states | — |
| `backend` | APIs, data, tests, input validation | — |
| `developer` | General development: mid-size changes, refactors, scripts, config | — |
| `debugger` | Root cause + minimal fix + regression test; reviews code | `systematic-debugging`, `browser`, `code-review` |
| `security-auditor` | Read-only OWASP audit with severity-ranked findings | `security-audit` (by Cloudflare, installed separately) |

*Also available to the orchestrator without installing anything — OpenCode built-ins: `explore` (code/web research, read-only) and `general` (multi-step research).*

All agents have `websearch` + `webfetch` to research the internet whenever they need to.

## Quality gates

Nothing is "done" without passing the gates: code → `debugger` (code-review) + `security-auditor` (security-audit); UI → `designer` (impeccable). The orchestrator verifies `git diff` and tests himself before reporting success.

## SDD Workflow (for non-trivial features)

```
constitution (.team/constitution.md)  ← once per project
   → spec (.team/spec/<slug>/spec.md) → clarify (max 5 questions)
   → plan (plan.md) → tasks (tasks.md, one owner + acceptance per task)
   → implement (delegate per task)
   → converge (verify acceptance criteria + quality gates)
```

Templates for every artifact live in [`skills/sdd/references/`](skills/sdd/references/).

## Installation

Requirements: [OpenCode V2](https://opencode.ai/docs/).

> **✅ You do NOT need to install the third-party skills manually.** The first time you work on a project, the orchestrator checks whether `security-audit` and `impeccable` are installed and, if one is missing, **downloads and installs it automatically** using the official commands below. It only asks for your approval the first time (requires Node.js). The result is recorded in `.team/skills-check.md` and it won't check again in that project.

### Option A — Global (recommended)

Copy the contents to your global config and you'll have the team in **all** your projects:

```bash
git clone https://github.com/josevdr95new/opencode-team.git
cd opencode-team

# Linux / macOS
cp -r agents skills commands ~/.config/opencode/

# Windows (PowerShell)
copy -Recurse agents, skills, commands "$HOME\.config\opencode\"
```

If you already have an `opencode.json`, just add `"default_agent": "orchestrator"` (don't overwrite the file). Otherwise copy the one from this repo.

No restart needed: OpenCode reloads its config on save.

### Option B — Per project

Copy the same folders into the project's `.opencode/` directory.

### Manual install of third-party skills (optional)

- **`security-audit`** (used by `security-auditor`) — by [Cloudflare](https://github.com/cloudflare/security-audit-skill), MIT:

  ```bash
  npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit --global
  ```

- **`impeccable`** (used by `designer`) — design skill by [Paul Bakaus](https://github.com/pbakaus/impeccable) ([impeccable.style](https://impeccable.style)), official OpenCode support:

  ```bash
  npx impeccable install
  ```

Without them the `designer` or `security-auditor` keep working in degraded mode (they lose their design standard or full audit method), but the team doesn't break.

> **Note:** the skills that ship with this repo (`sdd`, `delegation`, `code-review`, `systematic-debugging`) install by copying the folders as explained above. The two third-party ones are installed separately because we can't redistribute them.

## Usage

Talk to the orchestrator directly (it's the default agent), or use the commands:

| Command | What it does |
|---|---|
| `/team <mission>` | Free-form mission for the team |
| `/spec <feature>` | Full SDD flow; shows spec and plan before implementing |
| `/debug <bug>` | Systematic debugging (with browser if it's frontend) |
| `/audit <scope>` | Security audit with severity-ranked report |
| `/review <scope>` | Code review + security audit in parallel |

## Repository structure

```
├── opencode.json          ← default_agent: orchestrator
├── agents/                ← 1 orchestrator + 6 subagents
├── skills/
│   ├── sdd/               ← SDD workflow + templates in references/
│   ├── delegation/        ← orchestrator's delegation playbook
│   ├── code-review/       ← severity-ranked review checklist
│   └── systematic-debugging/ ← 4-phase method (reproduce → isolate → fix → verify)
└── commands/              ← /team /spec /debug /audit /review
```

## Customization

- **Model per agent**: add `model: provider/model#variant` to the agent's frontmatter.
- **More restrictions**: edit each agent's `permissions` (last matching rule wins).
- **New agent**: create `agents/<name>.md` with `mode: subagent` and add it to the `subagent` `allow` list in `orchestrator.md`.
- **Revert**: remove `"default_agent"` from your config and you're back to OpenCode's default `build` agent.

## Credits & references

- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic (orchestrator-worker pattern, briefings, effort scaling, quality gates)
- [GitHub Spec Kit](https://github.com/github/spec-kit) — Spec-Driven Development workflow (constitution → spec → plan → tasks → implement → converge)
- [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) — the security audit skill used by `security-auditor`
- [Impeccable](https://github.com/pbakaus/impeccable) ([impeccable.style](https://impeccable.style)) by Paul Bakaus — the design skill used by `designer`
- [OpenCode V2 docs](https://opencode.ai/docs/) — agents, skills, permissions and commands

## Keywords

`multi-agent team` · `opencode agents` · `orchestrator subagents` · `spec driven development` · `spec kit workflow` · `agent skills team` · `code review agent` · `security audit skill` · `AI coding team`

## License

[MIT](LICENSE)
