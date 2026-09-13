# Referens (matplanering)

## Svenska receptkällor (prioritet)

**Användaren är proffskock — prioritera KVALITET över bekvämlighet**

1. **Bästa kvalitetskällor** (svenska eller internationella):
   - Köket.se (högkvalitativa svenska recept, kocktestade)
   - Arla (särskilt för mejeridominerade rätter)
   - Mitt Kök (autentisk nordisk mat)
   - Tasteline (professionella svenska kockar)
   - Landleys Kök (högkvalitativ husmanskost)
   - Internationella källor vid autenticitetsbehov (t.ex. asiatisk mat)

2. **Sekundära källor**:
   - ICA, Coop (bra basrecept men inte prioritet)
   - Matbloggar (om kvaliteten bevisligen är hög)

3. **Sökstrategi**:
   - Jämför flera källor för varje recept
   - Prioritera recept med professionell kockbakgrund
   - Leta tekniker och smakprofiler som höjer rätten
   - Balansera kvalitet med vardagsgenomförbarhet

4. **Ge alltid klickbara länkar**

Om ingen bra källa finns för en specifik rätt: använd andra pålitliga källor och förklara kort varför.

## Enheter & snabba konverteringar

- 1 msk = 15 ml
- 1 tsk = 5 ml
- 1 dl = 100 ml
- 10 dl = 1 l
- 1000 g = 1 kg

Praktiskt:
- Om totalsumman blir "stor", välj tydligare enhet (`1200 g` → `1,2 kg`).
- För "st"-varor: summera i `st` och lägg ev. "ca vikt" som notis om receptet kräver det.

## Normalisering av ingrediensnamn (butiksvänligt)

Använd konsekventa, vanliga namn:
- "kycklingfilé" (inte blandat med 3 varianter)
- "gul lök", "vitlök", "paprika", "morot"
- "matlagningsgrädde" vs "vispgrädde" (behåll som receptet anger)
- "ris (basmati/jasmin)" om sort spelar roll

## Skafferi-antaganden (fråga/flagga)

Gissa inte tyst. Lägg i "skafferi-antaganden" och markera som valbart:
- salt, svartpeppar
- neutral olja / olivolja
- sojasås, vinäger
- buljongtärning/fond

## Handlingslista-kategorier (standard)

- Grönsaker
- Frukt
- Mejeri & Ägg
- Kött & Fisk
- Skafferi
- Kryddor & Såser
- Fryst
- Bröd
- Övrigt

**Hushåll & hygien** — extra kategori som bara används för stapelvaror (från
`stapelvaror.md`), aldrig för receptingredienser. Används vid gruppering av stapelvaror
under "Stapelvaror (återkommande)" och i list-sök-blockets ordning.

## List-sök (Willys)

`03-handlingslista.md` inleds med ett kodblock (språk `text`) med en vara per rad, utan
mängder, parenteser eller receptnamn — tänkt att klistras in direkt i Willys list-sök.
Skriv korta sökord som man faktiskt söker med, inte receptets fraser (t.ex. "rödlök", inte
"2 st rödlökar").

Ordning: Grönsaker, Frukt, Mejeri & Ägg, Kött & Fisk, Skafferi, Kryddor & Såser, Fryst,
Bröd, Hushåll & hygien, Övrigt. Varje produkt tas med en gång, oavsett hur många recept den
förekommer i. Skafferi-antaganden (salt, peppar), vatten och obekräftade `vid behov`-varor
tas inte med. Fullständiga regler finns i `shopping-list-generator`.

## Stapelvaror

`stapelvaror.md` i projektroten listar återkommande hushållsvaror (frekvens `varje vecka`
eller `vid behov`) som inte hör till något recept. Fas 3 läser filen automatiskt och
sköter poolning, gruppering och eventuellt överlapp med receptingredienser ("+ stapelvara")
— se `shopping-list-generator` för detaljerna. Saknas filen hoppas steget över tyst.
