---
name: meal-planning-hello-fresh
description: Skapar HelloFresh-liknande matplanering för veckan. Använd när användaren nämner matplan, veckomeny, handlingslista, meal prep, matlådor eller HelloFresh. Orkestrerar specialiserade agenter genom 4 faser med obligatoriska stoppunkter.
---

# Matplanering (HelloFresh-stil) — Multi-Agent Workflow

## Quick start

När användaren vill planera mat för kommande vecka:

1. Skapa datum-mapp i projektroten: `YYYY-MM-DD/` (måndagen för veckan).
2. Följ faserna nedan — delegera till specialiserade agenter.
3. **Gå aldrig vidare utan användarens uttryckliga godkännande.**

## Antaganden (default)

- **Språk**: svenska
- **Vecka**: lunch + middag
- **Standardportioner**: 6 portioner per recept (om inget annat anges)
- **Preferens**: högre protein, varierat (inte low carb, inte veganskt) — **ca 80% vegetarisk, ca 20% kött/fisk**
- **Receptkällor**: prioritera kvalitet — Köket, Tasteline, Arla, Landleys Kök, internationella vid autenticitet

## Agentarkitektur

```
Användare
    ↓
[Orchestrator / Huvudkonversation]
    ├── Fas 1: brainstorming-agent
    ├── Fas 2: recipe-researcher × N (PARALLELLT, en per rätt)
    │         + recipe-creator (vid behov)
    ├── Fas 3: shopping-list-generator
    └── Fas 4: meal-prep-optimizer
```

## Fas 1 — Brainstorming

**Delegera till `brainstorming-agent`.**

Ge agenten:
- Användarens preferenser (protein, tid, utrustning, smaker)
- Antal måltider/dagar
- Datum-mapp

Agenten skriver `01-brainstorming.md` med 10-20 kandidater.

### STOPP
Presentera listan. Be användaren välja rätter och/eller klistra in egna recept.

## Fas 2 — Receptval (PARALLELL FORSKNING)

**Spawna EN `recipe-researcher` per vald rätt — alla i bakgrunden, parallellt.**

Varje researcher:
- Söker 3-5 källor för sin specifika rätt
- Jämför kvalitet (inte bara första träff)
- Returnerar: bästa länk, alternativ, originalportioner, kvalitetsbedömning

**Exempel:**
```
5 valda rätter (80% veg, 20% kött/fisk) → 5 parallella recipe-researcher-agenter:
  Agent 1: "Hitta bästa recept för kikärtscurry, 6 portioner"         (vegetarisk)
  Agent 2: "Hitta bästa recept för halloumigryta, 6 portioner"        (vegetarisk)
  Agent 3: "Hitta bästa recept för tofuwok, 6 portioner"              (vegetarisk)
  Agent 4: "Hitta bästa recept för pasta med zucchini & pesto, 6 port" (vegetarisk)
  Agent 5: "Hitta bästa recept för laxpasta, 6 portioner"             (kött/fisk)
```

Efter alla researchers returnerat:
1. Syntetisera resultat till `02-receptval.md`
2. Beräkna skalningsfaktorer
3. Om eget recept behövs: spawna `recipe-creator`

### STOPP (obligatorisk)
Fråga: **"Vill du att jag skapar handlingslista nu?"**

## Fas 3 — Handlingslista

**Delegera till `shopping-list-generator`.**

Ge agenten:
- Alla recept med portioner och skalningsfaktorer
- Referens till `02-receptval.md` och `recept-*.md`-filer

Agenten skriver `03-handlingslista.md`.

### STOPP (obligatorisk)
Fråga: **"Vill du att jag skapar meal prep-plan nu?"**

## Fas 4 — Meal prep-plan

**Delegera till `meal-prep-optimizer`.**

Ge agenten alla recept. Agenten skapar tidsoptimerad tillagningsplan i `04-meal-prep-plan.md`.

Klart! Ingen stoppunkt efter detta.

## Ytterligare skills

- `/create-recipe [rätt] [portioner]` — Skapa ett eget recept från grunden

## Referens

För källor och konverteringar, se [reference.md](reference.md).
För exempel på format, se [examples.md](examples.md).
