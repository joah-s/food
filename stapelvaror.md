# Stapelvaror — återkommande varor

Varor som köps regelbundet men inte hör till något recept (hushåll, hygien, frukost,
mellanmål). `shopping-list-generator` läser filen i Fas 3 och lägger till varorna i
`03-handlingslista.md` och i list-sök-listan.

## Format

```
| Vara | Kategori | Frekvens | Mängd | Notering |
```

- **Vara**: butiksvänligt namn, så som du söker efter det i butiken.
- **Kategori**: en av butikskategorierna i handlingslistan, till exempel Frukt, Mejeri & Ägg,
  Kött & Fisk, Skafferi, Fryst, Bröd eller Hushåll & hygien.
- **Frekvens**:
  - `varje vecka` läggs alltid till i handlingslistan och i list-sök.
  - `vid behov` listas som en kryssruta under "Kolla hemma" och kommer bara med i list-sök om
    du säger att du behöver varan den veckan.
- **Mängd**: valfri, till exempel `1 förp` eller `2 l`. Lämna `–` om du inte bryr dig.
- **Notering**: valfri, till exempel märke eller sort.

Ändra frekvensen här när en vara inte behövs varje vecka, eller lägg till nya rader.

---

## Varor

| Vara | Kategori | Frekvens | Mängd | Notering |
|---|---|---|---|---|
| Banan | Frukt | varje vecka | – | |
| Havredryck | Mejeri & Ägg | varje vecka | – | |
| Kaviar | Kött & Fisk | varje vecka | – | |
| Äppelmos | Skafferi | varje vecka | – | |
| Havregryn | Skafferi | varje vecka | – | |
| Kaffe | Skafferi | varje vecka | – | |
| Corny bar / Flapjack | Skafferi | varje vecka | – | Bars |
| Frysta bär | Fryst | varje vecka | – | |
| Bröd | Bröd | varje vecka | – | |
| Toalettpapper | Hushåll & hygien | varje vecka | – | |
| Hushållspapper | Hushåll & hygien | varje vecka | – | |
| Schampoo | Hushåll & hygien | varje vecka | – | |
| Balsam | Hushåll & hygien | varje vecka | – | |
| Tvål | Hushåll & hygien | varje vecka | – | |
| Tandkräm | Hushåll & hygien | varje vecka | – | |
