---
description: Revisión de calidad completa (código + seguridad en paralelo)
agent: orchestrator
---

Revisión de calidad de: $ARGUMENTS

Lanza en paralelo a `debugger` (skill `code-review`) y a `security-auditor` (skill `security-audit`). Consolida los hallazgos de ambos en una sola tabla por severidad con `archivo:línea`, resuelve solapamientos decidiendo tú, y dime qué corregir primero y por qué.
