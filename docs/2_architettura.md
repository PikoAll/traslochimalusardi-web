# Architettura

Sito statico, nessun backend.

| Parte | Cosa e' |
|---|---|
| Pagine | `index.html`, `servizi.html`, `galleria.html`, `chi-siamo.html`, `contatti.html` |
| Stile e script | `assets/` (template Alpha di HTML5 UP, licenza CCA 3.0, vedi `LICENSE.txt`) |
| Immagini | `images/` |
| SEO | `robots.txt`, `sitemap.xml`, dati strutturati JSON-LD nelle pagine |
| Dominio | `CNAME` (GitHub Pages) |
| Cache busting | `update_version.py`: aggiunge/aggiorna `?v=<versione>` ai CSS/JS referenziati |

## Pubblicazione
GitHub Pages dal ramo `main`, cartella `/`: ogni merge su `main` va online.

## Controlli
Oggi: nessuna CI. Controllo minimo locale: compilazione di `update_version.py`
(`python3 -m py_compile update_version.py`). Il controllo dei riferimenti locali delle pagine
e' pianificato nell'epic "qualita-sito".
