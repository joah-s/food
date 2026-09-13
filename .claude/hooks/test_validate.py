#!/usr/bin/env python3
"""Regressionstest for receptvalidatorn.

Kor: python3 .claude/hooks/test_validate.py

Testerna tacker det som ar heuristiskt och darmed skort: normaliseringen,
karnordsutvinningen, matchningen av ingredienser mot instruktionssteg och
korskontrollen av handlingslistan (list-sok och stapelvaror).
"""

from __future__ import annotations

import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_recipe import (  # noqa: E402
    extract_headwords,
    find_mention,
    normalize,
    validate,
)
from validate_week import (  # noqa: E402
    collect_list_items,
    collect_search_terms,
    main as validate_week_main,
    read_weekly_staples,
)

failures: list[str] = []


def check(label: str, actual: object, expected: object) -> None:
    if actual != expected:
        failures.append(f"{label}\n    förväntat: {expected!r}\n    faktiskt:  {actual!r}")


# --------------------------------------------------------------------------
# Normalisering
# --------------------------------------------------------------------------

NORMALIZE_CASES = [
    ("- 1.2 kg kycklingfilé", "- 1,2 kg kycklingfilé"),
    ("- 2 burkar majs (à 340g)", "- 2 burkar majs (à 340 g)"),
    ("- 1/2 dl ströbröd", "- ½ dl ströbröd"),
    ("**1 dl**mjölk", "**1 dl** mjölk"),
    ("**1/2 dl**ströbröd", "**½ dl** ströbröd"),
    ("Grädda i 180°C i 25-30 minuter.", "Grädda i 180 °C i 25–30 minuter."),
    ("- 1000 g blandfärs", "- 1 kg blandfärs"),
    ("- 10 dl vatten", "- 1 l vatten"),
    ("- Mjölk — 1,5 dl", "- 1,5 dl mjölk"),
    ("- Blandfärs (50/50 nöt och fläsk) — 800 g", "- 800 g blandfärs (50/50 nöt och fläsk)"),
    ("- Gul lök — 1 st (finriven)", "- 1 st gul lök (finriven)"),
    # Far INTE roras:
    ("- Pensla med **2 msk** olja, strö över **2 tsk** salt", None),
    ("- Källa: https://example.se/recept-1.2-kg", None),
    ("- 1,5 dl mjölk", None),
    ("Vecka 2026-06-08", None),
]

for source, expected in NORMALIZE_CASES:
    result, _ = normalize(source)
    check(f"normalize({source!r})", result, expected if expected is not None else source)

# Normaliseringen ska vara idempotent.
for source, _ in NORMALIZE_CASES:
    once, _ = normalize(source)
    twice, fixes = normalize(once)
    check(f"normalize idempotent för {source!r}", (twice, fixes), (once, []))


# --------------------------------------------------------------------------
# Karnord
# --------------------------------------------------------------------------

HEADWORD_CASES = [
    ("mjölk", ["mjölk"]),
    ("gul lök", ["lök"]),
    ("stor bit ingefära", ["ingefära"]),
    ("vatten för konsistens", ["vatten"]),
    ("kycklinglår med ben och skinn", ["kycklinglår"]),
    ("rostade jordnötter", ["jordnötter"]),
    ("sriracha/chili", ["sriracha", "chili"]),
    ("crème fraiche", ["crème"]),
]

for name, expected in HEADWORD_CASES:
    check(f"extract_headwords({name!r})", extract_headwords(name), expected)


# --------------------------------------------------------------------------
# Matchning ingrediens -> steg (bojningar och sammansatta ord)
# --------------------------------------------------------------------------

MENTION_CASES = [
    ("Koka riset 12 min", ["jasminris"], True),          # efterled i sammansatt ord
    ("Krydda med salt och peppar", ["svartpeppar"], True),
    ("Fräs löken mjuk", ["lök"], True),                  # bestamd form
    ("Riv moroten grovt", ["morötter"], True),           # omljud i plural
    ("Vänd ner smöret", ["smör"], True),
    ("Blanda alla ingredienser", ["kokosmjölk"], False),  # ska INTE matcha
    ("Stek kycklingen", ["kycklinglårfilé"], True),
]

for step, heads, should_match in MENTION_CASES:
    found = find_mention(step, heads) is not None
    check(f"find_mention({step!r}, {heads!r})", found, should_match)


# --------------------------------------------------------------------------
# Hela filen
# --------------------------------------------------------------------------

GOOD = """# Recept — Testrätt för 4 portioner

En testrätt som följer standarden.

## Ingredienser (4 portioner)

### Bas
- 1,5 dl mjölk
- 500 g blandfärs
- salt och svartpeppar efter smak

## Gör så här

### 1) Blanda
- Häll **1,5 dl** mjölk över **500 g** blandfärs och rör ihop.
- Smaka av med salt och svartpeppar.

## Matlåda / förvaring
- Kyl: 3 dagar.

## Källor
- Test: https://example.com
"""

BAD_MISSING_AMOUNT = GOOD.replace(
    "- Häll **1,5 dl** mjölk över **500 g** blandfärs och rör ihop.",
    "- Häll mjölken över blandfärsen och rör ihop.",
)

BAD_UNUSED = GOOD.replace("- 500 g blandfärs", "- 500 g blandfärs\n- 2 msk tomatpuré")

BAD_PORTIONS = GOOD.replace("## Ingredienser (4 portioner)", "## Ingredienser (6 portioner)")


def errors_for(text: str, name: str = "recept-test-4p.md") -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / name
        path.write_text(text, encoding="utf-8")
        return validate(path, fix=False).errors


check("giltigt recept ger inga fel", errors_for(GOOD), [])
check("saknad mängd i steg upptäcks", len(errors_for(BAD_MISSING_AMOUNT)), 2)
check("oanvänd ingrediens upptäcks", len(errors_for(BAD_UNUSED)), 1)
check("portionsavvikelse upptäcks", len(errors_for(BAD_PORTIONS)), 1)

# no-check-markoren ska tysta Regel 2.
silenced = GOOD.replace(
    "- 500 g blandfärs", "- 500 g blandfärs\n- 2 msk tomatpuré <!-- no-check -->"
)
check("no-check-markören tystar Regel 2", errors_for(silenced), [])


# --------------------------------------------------------------------------
# Handlingslistan: kodblock, stapelvaror och list-sok
# --------------------------------------------------------------------------

WEEK_RECIPES = """# Steg 4 — Alla recept

## Testwok

### Ingredienser (6 portioner)
- 2 st rödlökar
- 2 st röda paprikor
- 2 st gula lökar
- 5 dl jasminris
- 2 msk risvinäger
- 2 msk olivolja
- 1 dl vatten
- salt efter smak
"""

LIST_SEARCH = """## List-sök (Willys)
Kopiera blocket och klistra in i butikens list-sök.
```text
{terms}
```
"""

WEEK_SHOPPING = """# Steg 3 — Handlingslista (poolad)
> header

{list_search}
---

## Grönsaker
- 2 st rödlökar
- 2 st röda paprikor
- 2 st gula lökar

## Skafferi
- 5 dl jasminris
- 2 msk risvinäger
- 2 msk olivolja

## Stapelvaror (återkommande)
Från `stapelvaror.md`, hör inte till något recept.
### Frukt
- Banan
### Hushåll & hygien
- Toalettpapper
### Kolla hemma (vid behov)
- [ ] Schampoo

---

## Skafferi-antaganden (verifiera om du har hemma)
- salt
- vatten
"""

FULL_TERMS = "rödlök\nröd paprika\ngul lök\njasminris\nrisvinäger\nbanan\ntoalettpapper"

STAPLES = """# Stapelvaror

## Format

```
| Vara | Kategori | Frekvens | Mängd | Notering |
| Kodblock | Frukt | varje vecka | – | ska inte räknas |
```

## Varor

| Vara | Kategori | Frekvens | Mängd | Notering |
|---|---|---|---|---|
| Banan | Frukt | varje vecka | – | |
| Toalettpapper | Hushåll & hygien | varje vecka | – | |
| Schampoo | Hushåll & hygien | vid behov | – | |
"""


def shopping_with(terms: str | None) -> str:
    block = LIST_SEARCH.format(terms=terms) if terms is not None else ""
    return WEEK_SHOPPING.format(list_search=block)


def run_week(shopping: str, staples: str | None = None) -> tuple[int, str]:
    """Kor validate_week pa en temporar veckomapp. Returnerar (exitkod, utdata)."""
    with tempfile.TemporaryDirectory() as tmp:
        week = Path(tmp) / "2026-01-05"
        week.mkdir()
        (week / "03-handlingslista.md").write_text(shopping, encoding="utf-8")
        (week / "04-alla-recept.md").write_text(WEEK_RECIPES, encoding="utf-8")
        if staples is not None:
            (Path(tmp) / "stapelvaror.md").write_text(staples, encoding="utf-8")
        out = io.StringIO()
        with redirect_stdout(out):
            code = validate_week_main([str(week)])
        return code, out.getvalue()


def list_search_tips(output: str) -> list[str]:
    return [line.strip() for line in output.splitlines() if "list-sök" in line]


def items_in(text: str) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "03-handlingslista.md"
        path.write_text(text, encoding="utf-8")
        return [item.name for item in collect_list_items(path)]


def terms_in(text: str) -> list[str] | None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "03-handlingslista.md"
        path.write_text(text, encoding="utf-8")
        return collect_search_terms(path)


# Kodblock ska inte ge punkter, aven om raderna ser ut som punkter.
check(
    "punkter i kodblock ignoreras",
    items_in("## Grönsaker\n- 1 st gurka\n```text\n- 2 st tomater\npotatis\n```\n"),
    ["gurka"],
)

# Stapelvaror hoppas over fram till nasta '## '-rubrik, ocksa under '###'.
names = items_in(shopping_with(FULL_TERMS))
staple_names = [n for n in names if n in ("Banan", "Toalettpapper", "[ ] Schampoo")]
check("Stapelvaror-sektionen ignoreras", staple_names, [])
check("punkter efter Stapelvaror räknas igen", "salt" in names and "rödlökar" in names, True)

check("list-sök-blocket läses", terms_in(shopping_with("potatis\n\ngul lök")),
      ["potatis", "gul lök"])
check("bara första kodblocket under List-sök läses",
      terms_in(shopping_with("potatis") + "\n## List-sök igen\n```\nbanan\n```\n"), ["potatis"])
check("saknat list-sök-block ger None", terms_in(shopping_with(None)), None)

code, output = run_week(shopping_with(None))
check("saknat list-sök-block ger exit 0", code, 0)
check("saknat list-sök-block ger TIPS",
      any("saknar list-sök-block" in t for t in list_search_tips(output)), True)
_, output = run_week(shopping_with(None), STAPLES)
check("saknat list-sök-block ger inga stapelvaru-TIPS",
      any("stapelvaran" in t for t in list_search_tips(output)), False)

code, output = run_week(shopping_with(FULL_TERMS), STAPLES)
check("full täckning ger exit 0", code, 0)
check("full täckning ger inga list-sök-TIPS", list_search_tips(output), [])
check("stapelvaror ger inga 'matchar ingen ingrediens'-TIPS", "matchar ingen" in output, False)

# Plural i receptet mot singular i list-sok, bade prefixnyckel ('rodlo')
# och kort karnord med bojningsandelse ('lok' mot 'lokar').
_, output = run_week(shopping_with("rödlök\nröd paprika\ngul lök\njasminris\nrisvinäger"))
check("pluralformer matchar list-sök", list_search_tips(output), [])

code, output = run_week(shopping_with(FULL_TERMS.replace("röd paprika\n", "")))
tips = list_search_tips(output)
check("saknad receptingrediens ger exit 0", code, 0)
check("saknad receptingrediens ger ett TIPS", len(tips), 1)
check("TIPS nämner ingrediensen", "'röda paprikor'" in (tips[0] if tips else ""), True)

# Kort karnord far bara bojningsandelse, inte ett helt efterled: 'ris' != 'risvinager'.
_, output = run_week(shopping_with(FULL_TERMS.replace("jasminris\nrisvinäger", "ris")))
tips = list_search_tips(output)
check("'ris' täcker inte 'risvinäger' eller 'jasminris'", len(tips), 2)

with tempfile.TemporaryDirectory() as tmp:
    staples_path = Path(tmp) / "stapelvaror.md"
    staples_path.write_text(STAPLES, encoding="utf-8")
    check("varje vecka-varor läses, kodblock och vid behov hoppas över",
          read_weekly_staples(staples_path), ["Banan", "Toalettpapper"])

code, output = run_week(shopping_with(FULL_TERMS.replace("\ntoalettpapper", "")), STAPLES)
tips = list_search_tips(output)
check("saknad varje vecka-stapelvara ger exit 0", code, 0)
check("saknad varje vecka-stapelvara ger ett TIPS", len(tips), 1)
check("TIPS nämner stapelvaran", "stapelvaran 'Toalettpapper'" in (tips[0] if tips else ""), True)

# Utan stapelvaror.md i foraldrakatalogen kontrolleras inga stapelvaror.
_, output = run_week(shopping_with(FULL_TERMS.replace("\ntoalettpapper", "")))
check("utan stapelvaror.md ges inga stapelvaru-TIPS", list_search_tips(output), [])


# --------------------------------------------------------------------------

if failures:
    print(f"{len(failures)} test misslyckades:\n")
    for f in failures:
        print(f"  ✗ {f}")
    sys.exit(1)

print("Alla test godkända.")
