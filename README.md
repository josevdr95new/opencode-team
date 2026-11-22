# 🤖 OpenCode Team — Equipo multi-agente con SDD

Sistema de equipo de desarrollo para [OpenCode](https://opencode.ai) dirigido por un **orquestador**: tú le escribes solo a él, él analiza, decide, delega en los especialistas, verifica la calidad y te reporta.

Inspirado en las mejores prácticas públicas de ingeniería de agentes: el patrón *orchestrator-worker* de Anthropic (multi-agent research system) y el flujo **SDD (Spec-Driven Development)** de GitHub Spec Kit.

## Arquitectura

```
                         TÚ (español)
                           │
                    ┌──────▼──────┐
                    │ ORCHESTRATOR │  ← agente por defecto, decide y arbitra
                    └──────┬──────┘
      ┌─────────┬─────────┬────────┼────────┬──────────┐
      ▼         ▼         ▼        ▼        ▼          ▼
  designer  frontend  backend  developer  debugger  security-auditor
  (impeccable)                  (ajustes) (systematic-  (security-audit,
                                           debugging +    solo lectura)
                                            browser)
      └─────────┴─────────┴────────┴─── todos reportan al orquestador ──┘
```

## Equipo

| Agente | Rol | Skills que usa |
|---|---|---|
| `orchestrator` | Jefe: decide, delega, arbitra, consolida. Los ajustes pequeños los hace él mismo; lo grande siempre se delega | `sdd`, `delegation` |
| `designer` | UI/UX: specs, tokens de diseño y auditoría visual | `impeccable` (siempre; de terceros, se instala aparte) |
| `frontend` | Implementa interfaces con accesibilidad y estados completos | — |
| `backend` | APIs, datos, tests, validación de entradas | — |
| `developer` | Desarrollo general: ajustes medianos, refactors, scripts, config | — |
| `debugger` | Causa raíz + fix mínimo + test de regresión; revisa código | `systematic-debugging`, `browser`, `code-review` |
| `security-auditor` | Auditoría OWASP de solo lectura con hallazgos por severidad | `security-audit` (de Cloudflare, se instala aparte) |

Todos los agentes tienen `websearch` + `webfetch` para investigar en internet cuando lo necesitan.

## Instalación

### Requisitos

- [OpenCode V2](https://opencode.ai/docs/)

> **✅ NO hace falta instalar las skills de terceros manualmente.** La primera vez que trabajes en un proyecto, el orquestador verifica si `security-audit` e `impeccable` están instaladas y, si falta alguna, **la descarga e instala automáticamente** con los comandos oficiales de abajo. Solo pide tu aprobación la primera vez (y requiere Node.js). El resultado queda registrado en `.team/skills-check.md` y no vuelve a verificar en ese proyecto. Los comandos manuales de abajo son solo una alternativa si prefieres hacerlo tú.

### Instalación manual (opcional)

- **`security-audit`** (la usa el `security-auditor`) — skill de [Cloudflare](https://github.com/cloudflare/security-audit-skill), licencia MIT:

  ```bash
  npx skills add https://github.com/cloudflare/security-audit-skill --skill security-audit --global
  ```

- **`impeccable`** (la usa el `designer`) — skill de diseño de [Paul Bakaus](https://github.com/pbakaus/impeccable) ([impeccable.style](https://impeccable.style)), con soporte oficial para OpenCode:

  ```bash
  npx impeccable install
  ```

Sin ellas el `designer` o el `security-auditor` siguen trabajando en modo degradado (pierden su estándar de diseño o su método completo de auditoría), pero el equipo no se bloquea.

> **Nota:** las skills del propio repo (`sdd`, `delegation`, `code-review`, `systematic-debugging`) sí viajan con él: se instalan copiando las carpetas como se explica abajo. Las dos de terceros se instalan aparte porque no podemos redistribuirlas.

### Opción A — Global (recomendado)

Copia el contenido a tu config global y tendrás el equipo en **todos** tus proyectos:

```bash
git clone https://github.com/josevdr95new/opencode-team.git
cd opencode-team

# Linux / macOS
cp -r agents skills commands ~/.config/opencode/

# Windows (PowerShell)
copy -Recurse agents, skills, commands "$HOME\.config\opencode\"
```

Si ya tienes un `opencode.json`, añádele solo `"default_agent": "orchestrator"` (no lo sobrescribas). Si no, copia el de este repo.

No hace falta reiniciar OpenCode: recarga la config sola al guardar.

### Opción B — Por proyecto

Copia las mismas carpetas dentro de `.opencode/` del proyecto:

```bash
cp -r agents skills commands  tu-proyecto/.opencode/
```

## Uso

Escribe directamente al orquestador (es el agente por defecto). Él solo:

- decide si un ajuste pequeño lo hace él o se delega,
- reparte tareas medianas/grandes entre especialistas con briefings completos,
- lanza en paralelo lo independiente (máx. 3–4),
- **nunca da nada por terminado sin las compuertas de calidad**: `debugger` (code-review) + `security-auditor` (security-audit) para código, `designer` (impeccable) para UI,
- verifica `git diff` y tests él mismo antes de reportarte éxito.

| Comando | Qué hace |
|---|---|
| `/team <misión>` | Misión libre para el equipo |
| `/spec <feature>` | Flujo SDD completo; muestra spec y plan antes de implementar |
| `/debug <bug>` | Depuración sistemática (con navegador si es frontend) |
| `/audit <ámbito>` | Auditoría de seguridad con informe por severidad |
| `/review <ámbito>` | Revisión de código + seguridad en paralelo |

## Flujo SDD (para features no triviales)

```
constitución (.team/constitution.md)  ← una vez por proyecto
   → spec (.team/spec/<slug>/spec.md) → clarificar (máx. 5 preguntas)
   → plan (plan.md) → tasks (tasks.md, agente y aceptación por tarea)
   → implementar (delegación por tareas)
   → converger (verificar criterios de aceptación + compuertas de calidad)
```

Las plantillas de cada artefacto están en [`skills/sdd/references/`](skills/sdd/references/).

## Estructura

```
├── opencode.json          ← default_agent: orchestrator
├── agents/                ← 1 orquestador + 6 subagentes
├── skills/
│   ├── sdd/               ← flujo SDD + plantillas en references/
│   ├── delegation/        ← playbook de delegación del orquestador
│   ├── code-review/       ← checklist de revisión por severidad
│   └── systematic-debugging/ ← método de 4 fases (reproducir → aislar → arreglar → verificar)
└── commands/              ← /team /spec /debug /audit /review
```

## Personalización

- **Modelo por agente**: añade `model: provider/model#variante` al frontmatter del agente.
- **Más restricciones**: edita `permissions` en cada agente (la última regla que coincide gana).
- **Nuevo agente**: crea `agents/<nombre>.md` con `mode: subagent` y añádelo a los `allow` de `subagent` en `orchestrator.md`.
- **Revertir**: quita `"default_agent"` de tu config y vuelves al agente `build` de siempre.

## Créditos y referencias

- [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) — Anthropic (patrón orchestrator-worker, briefings, escalado de esfuerzo, compuertas)
- [GitHub Spec Kit](https://github.com/github/spec-kit) — flujo Spec-Driven Development (constitución → spec → plan → tasks → implement → converge)
- [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill) — la skill de auditoría de seguridad que usa el `security-auditor`
- [Impeccable](https://github.com/pbakaus/impeccable) ([impeccable.style](https://impeccable.style)) de Paul Bakaus — la skill de diseño que usa el `designer`
- [Documentación de OpenCode V2](https://opencode.ai/docs/) — agentes, skills, permisos y comandos

## Licencia

[MIT](LICENSE)
