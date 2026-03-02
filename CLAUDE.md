# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a meal planning repository that implements a HelloFresh-like workflow for Swedish households. The system uses **multi-agent orchestration** to help with weekly meal planning through a structured 4-phase process: brainstorming → recipe selection → shopping list generation → meal prep planning.

## Repository Structure

```
YYYY-MM-DD/                          # Date-based meal planning folders
├── 01-brainstorming.md              # Meal preferences + candidate meals
├── 02-receptval.md                  # Selected recipes with links/sources
├── recept-*.md                      # Custom recipe files (when applicable)
├── 03-handlingslista.md             # Pooled shopping list (generated on request)
└── 04-meal-prep-plan.md             # Optimized prep timeline (generated on request)

.claude/
├── agents/
│   ├── meal-planning-orchestrator.md  # Top-level orchestrator (use with claude --agent)
│   ├── brainstorming-agent.md         # Phase 1: meal candidate generation
│   ├── recipe-researcher.md           # Phase 2: parallel recipe research (one per dish)
│   ├── recipe-creator.md              # Phase 2: custom recipe creation
│   ├── shopping-list-generator.md     # Phase 3: pooled shopping list
│   └── meal-prep-optimizer.md         # Phase 4: time-optimized prep plan
├── skills/
│   ├── meal-planning-hello-fresh/     # Main workflow skill
│   │   ├── SKILL.md                   # Orchestration instructions
│   │   ├── reference.md               # Sources, units, categories
│   │   └── examples.md                # Output format examples
│   └── create-recipe/                 # Custom recipe skill
│       └── SKILL.md                   # /create-recipe command
└── settings.local.json                # Local permission settings (gitignored)
```

## Multi-Agent Architecture

```
User
  ↓
[Main Conversation / Orchestrator]
  ├── Phase 1: brainstorming-agent (sonnet)
  ├── Phase 2: recipe-researcher × N (sonnet, PARALLEL — one per dish)
  │            + recipe-creator (on demand)
  ├── Phase 3: shopping-list-generator (sonnet)
  └── Phase 4: meal-prep-optimizer (inherit)
```

### Key Design Decisions

- **Parallel recipe research**: Phase 2 spawns one `recipe-researcher` agent per dish, all running in parallel. Each researcher compares 3-5 sources independently.
- **Subagents can't spawn subagents**: The main conversation acts as orchestrator. Alternatively, use `claude --agent meal-planning-orchestrator` for automated orchestration.
- **Skills preloaded into orchestrator**: The orchestrator agent has `meal-planning-hello-fresh` skill injected at startup via the `skills` field.

## Core Workflow & Architecture

### Phase-Gated Process (CRITICAL)

The workflow has **mandatory stop points** between phases. Never proceed to the next phase without explicit user approval:

1. **Phase 1 (Brainstorming)**: Generate meal candidates based on preferences
   - Stop and wait: User selects dishes or provides own recipes

2. **Phase 2 (Recipe Selection)**: Parallel recipe research + custom recipe creation
   - Stop and wait: Ask "Vill du att jag skapar handlingslista nu?"

3. **Phase 3 (Shopping List)**: Generate pooled, consolidated shopping list
   - Stop and wait: Ask "Vill du att jag skapar meal prep-plan nu?"

4. **Phase 4 (Meal Prep)**: Create optimized preparation timeline

### Language & Units

- **Language**: Swedish only
- **Units**: Metric (g, kg, ml, dl, l, msk, tsk, st)
- **Normalization**: Convert to clearer units when appropriate (1000g → 1kg, 10dl → 1l)

### Recipe Sources Priority

**User is a professional chef - prioritize QUALITY over convenience**

1. **Best quality sources** (Swedish or international):
   - Köket.se (high-quality Swedish recipes, chef-tested)
   - Arla (especially for dairy-based dishes)
   - Mitt Kök (authentic Nordic cuisine)
   - Tasteline (professional Swedish chefs)
   - Landleys Kök (high-quality home cooking)
   - International sources when authenticity matters (e.g., Asian cuisine from authentic sources)

2. **Secondary sources**:
   - ICA, Coop (good for basic recipes but not priority)
   - Food blogs (if quality is demonstrably high)

3. **Search strategy**:
   - Compare multiple sources for each recipe
   - Prioritize recipes with professional chef backgrounds
   - Look for techniques and flavor profiles that elevate the dish
   - Balance quality with weekday feasibility (not too advanced)

4. **Always provide clickable links**

### Default Parameters

- **Portions**: 6 per recipe (unless specified otherwise)
- **Meals**: Lunch + dinner
- **Protein focus**: High protein but varied (not low-carb, not vegan)
- **Vegetarian split**: **~80% vegetarian (or easily made vegetarian), ~20% meat/fish** — hard default
  - Vegetarian protein sources to rotate: lentils, chickpeas, tofu, tempeh, eggs, halloumi, beans, cheese, quorn
- **Scaling**: Calculate ingredient scaling factors when portions differ from recipe

### Shopping List Generation (Phase 3)

- **Pool ingredients** across all selected recipes
- **Normalize units** for clarity
- **Use butiksvänliga names** (Swedish grocery store names)
- **Categorize**: Grönsaker, Frukt, Mejeri & Ägg, Kött & Fisk, Skafferi, Kryddor & Såser, Fryst, Bröd, Övrigt
- **Pantry assumptions**: List separately (salt, pepper, oils) - don't assume silently
- **Mark uncertainties**: Use "(verifiera)" instead of guessing

### Custom Recipes

When creating custom recipes, save as `YYYY-MM-DD/recept-<slug>-<portioner>p.md` and reference from `02-receptval.md` as "Eget recept: `recept-<slug>.md`". Use `/create-recipe` or the `recipe-creator` agent.

### Meal Prep Planning (Phase 4)

Optimize for minimal total time by:
- Grouping similar tasks (chop all vegetables at once, cook all rice together)
- Parallelizing independent tasks (oven + stovetop + cold prep)
- Reusing bases/sauces when appropriate without sacrificing variety

## Specialized Agents

| Agent | Phase | Model | Purpose | Parallel? |
|---|---|---|---|---|
| `brainstorming-agent` | 1 | sonnet | Generate 10-20 meal candidates | No |
| `recipe-researcher` | 2 | sonnet | Find best recipe for ONE dish | **Yes — one per dish** |
| `recipe-creator` | 2 | inherit | Write custom recipe from scratch | Per recipe |
| `shopping-list-generator` | 3 | sonnet | Pool ingredients into shopping list | No |
| `meal-prep-optimizer` | 4 | inherit | Create time-optimized prep plan | No |
| `meal-planning-orchestrator` | All | inherit | Coordinate entire workflow | Top-level only |

## Skills

| Skill | Invocation | Purpose |
|---|---|---|
| `meal-planning-hello-fresh` | Auto or `/meal-planning-hello-fresh` | Main workflow with orchestration |
| `create-recipe` | `/create-recipe [dish] [portions]` | Create a custom recipe |

## Recipe Bank

`recept-bank.md` in the project root is a curated list of favorite recipes. The brainstorming agent reads this file at the start of Phase 1 and prioritizes those dishes as candidates, marking them with `★` in the output.

**Format**: Two sections (`Vegetariska favoriter` and `Kött & fisk`), each with columns: `Rätt | Källa/länk | Taggar | Portioner | Notering`

**Behavior**:
- Recipes in the bank are always considered first
- The agent fills remaining slots with fresh suggestions
- `★` markers help the user identify which candidates came from the bank

## Working with Date Folders

When starting a new week:
1. Create folder: `YYYY-MM-DD/` (use the Monday of that week)
2. Start with Phase 1 brainstorming
3. Follow the phase-gated workflow strictly
4. Reference previous weeks' folders for inspiration but start fresh each time
