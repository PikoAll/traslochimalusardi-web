# Stato e checkpoint

## 2026-10-09 - setup azienda
- Aggiunti `docs/` (5 file + nota di rilascio), `docs/mappa.md`, `CLAUDE.md`.
- Creati board GitHub, label, epic (milestone) e card.
- Noto: alcune pagine referenziano file non presenti nel repo (icona, un foglio di stile
  `custom-fixes.css`, alcune immagini): da verificare e correggere (card dedicata).
- Nessuna CI ne' test automatici ancora.

## 2026-10-10 - TRM-001 controllo riferimenti locali
- Aggiunto `scripts/check-links.py [ROOT]`: controlla `href`/`src` locali delle `*.html` in radice
  e gli URL di `sitemap.xml`; ignora link esterni, `tel:`, `mailto:`, `#`, `data:`, `javascript:`.
  Exit 0 se tutto risolve, 1 altrimenti (stampa `pagina.html -> percorso`). Solo stdlib Python.
- Aggiunti test in `scripts/test_check_links.py` (unittest, stesso stile TDD: prima rossi, poi verdi).
- Lo script segnala i file mancanti noti (icona, `custom-fixes.css`, immagini): la correzione
  resta nella card dedicata. Nessuna modifica a pagine o CI (script non ancora agganciato a CI).
- Fix cancello: i mancanti noti sono nella baseline `scripts/check-links.known` (tollerati);
  lo script fallisce solo sui riferimenti NUOVI. Togliere la riga quando il file viene sistemato.
