# Receptbank — favoritrecept

Lägg till rätter här som du vill att brainstorming-agenten ska föreslå.
Agenten läser den här filen och prioriterar dessa rätter som kandidater varje vecka.

## Format

```
| Rätt | Källa/länk | Taggar | Portioner | Notering |
```

- **Källa/länk**: URL till recept, eller "Eget recept" / "Utantill"
- **Taggar**: kombinera fritt — `vegetarisk`, `kött/fisk`, `snabb`, `batch`, `frys`, `helg`, `asiatisk`, `medelhav`, etc.
- **Portioner**: originalportioner i receptet (agenten skalar till 6 om inget annat anges)
- **Notering**: egna kommentarer, t.ex. "byt ut feta mot halloumi", "gillar dubbel chili"

---

## Vegetariska favoriter

| Rätt | Källa/länk | Taggar | Portioner | Notering |
|---|---|---|---:|---|
| Halloumiburgare | [HelloFresh](https://www.hellofresh.se/recipes/halloumiburgare-5ef1b2d34369b54e605a48e7) | vegetarisk, snabb, vardag | 2 | Med pommes, picklad lök och gurksalsa |
| Ugnsbakade rotfrukter med kikärtor och fetaost | [ICA](https://www.ica.se/recept/ugnsbakade-rotfrukter-399456/) | vegetarisk, batch, proteinrik | 4 | Egen version — kompletterad med rostade kikärtor, fetaost och tahiniyoghurt så den är en hel rätt |
| Halloumistroganoff | [ICA](https://www.ica.se/recept/halloumistroganoff-722769/) | vegetarisk, vardag, batch | 4 | Serveras med ris, gryn eller pasta |
| Marinerad tofu i ugn | [ICA](https://www.ica.se/recept/marinerad-tofu-i-ugn-727690/) | vegetarisk, proteinrik, batch | 8 | Bra meal prep-protein till bowls och wraps |
| Krämig vegetarisk gryta med quorn och dijonsenap | [Köket](https://www.koket.se/kramig-vegetarisk-gryta-med-quorn-och-dijonsenap) | vegetarisk, gryta, vardag | 4 | Med dijon och soltorkad tomat — ingen dragon |
| TikTok-pasta med fetaost och tomater | [Coop](https://www.coop.se/recept/pasta-med-fetaost-och-tomater/) | vegetarisk, snabb, pasta | 4 (verifiera) | Kontrollera portionsantal i källan |
| Tofu teriyaki med ris | [Quorn](https://www.quorn.se/recept/quorn-vegetarisk-teriyaki-med-ris) | vegetarisk, asiatisk, proteinrik | 4 | Snabb vardagsrätt — görs med stekt tofu i stället för quorn |
| Linsgryta med kokosmjölk | [ICA](https://www.ica.se/recept/linsgryta-med-kokosmjolk-724788/) | vegetarisk, gryta, batch | 4 | Klimatsmart och bra matlåda |
| Tofu stroganoff | [ICA](https://www.ica.se/recept/tofu-stroganoff-728908/) | vegetarisk, vardag, proteinrik | 4 | Krämig stroganoff med tofu |

## Kött & fisk

| Rätt | Källa/länk | Taggar | Portioner | Notering |
|---|---|---|---:|---|
| Pasta salsiccia classico | [Köket](https://www.koket.se/pasta-salsiccia-classico) | kött/fisk, pasta, snabb | 4 | Krämig tomat- och gräddsås med salsiccia |
| Spaghetti och köttfärssås | [ICA](https://www.ica.se/recept/spaghetti-och-kottfarssas-712805/) | kött/fisk, pasta, vardag, batch | 4 | Klassisk vardagsrätt |
| Köttbullar | [Arla](https://www.arla.se/recept/kottbullar/) | kött/fisk, husman, vardag | 4 | Klassiska hemgjorda köttbullar |
| Korvstroganoff med ris | [ICA](https://www.ica.se/recept/korvstroganoff-med-ris-533512/) | kött/fisk, vardag, snabb | 4 | Enkel vardagsgryta |
| Klassisk lasagne | [ICA](https://www.ica.se/recept/klassisk-lasagne-679675/) | kött/fisk, batch, helg | 4 | Bra till matlådor |
| Tacos | [ICA](https://www.ica.se/recept/tacos-722416/) | kött/fisk, snabb, fredagsmat | 4 | Basrecept för klassisk taco |

---

## Instruktioner till agenten

När du läser den här filen:
1. Inkludera alltid relevanta rätter från receptbanken i kandidatlistan
2. Markera dem med `★` i brainstorming-tabellen så användaren vet att det är ett favorit-recept
3. Välj rätter som passar veckans constraints (tid, utrustning, säsong)
4. Blanda fritt med egna förslag — receptbanken är ett komplement, inte en begränsning
