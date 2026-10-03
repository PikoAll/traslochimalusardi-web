# traslochimalusardi-web

Sito vetrina statico di **F.LLI MALUSARDI** (traslochi, sgomberi e noleggio
autoscale a Milano), online su <https://www.traslochimalusardi.it/>.
Realizzato da Pikobit sul template *Alpha* di HTML5 UP (licenza CCA 3.0:
`LICENSE.txt`, crediti del template in `README.txt`).

## Struttura

- Pagine: `index.html`, `servizi.html`, `galleria.html`, `chi-siamo.html`,
  `contatti.html`.
- `assets/` — CSS, JS, sorgenti Sass e font del template; `images/` — foto.
- `robots.txt`, `sitemap.xml` — SEO (dominio canonico `www.`).
- `CNAME` — dominio personalizzato di GitHub Pages.
- `update_version.py` — cache busting: aggiunge/aggiorna `?v=<versione>` ai
  CSS/JS referenziati nelle pagine HTML.

## Come si avvia

Niente build e niente dipendenze: sono file statici, basta aprire
`index.html` nel browser. Pubblicazione: GitHub Pages dal ramo `main`,
cartella `/` (ogni merge su `main` va online).

Prima di un rilascio che cambia CSS o JS: aggiorna `NEW_VERSION` in
`update_version.py` (formato `AAAA.MM.GG[.N]`) e lancialo dalla radice:

```bash
python3 update_version.py
```

## Controlli

Nessun test e nessuna CI su GitHub. Prima della PR: apri le pagine toccate
nel browser e, se cambi URL o pagine, allinea
`sitemap.xml`.

## Regole git

- Mai lavorare su `main` (è il sito in produzione): ramo dedicato e PR.
- Merge solo dopo la verifica di Cowork (`Esito: OK`) e l'ok scritto di
  Giuseppe; mai `--delete-branch`, mai `push --force`.
- Commit piccoli: `tipo(scope): descrizione`. Niente si cancella (rename `.backup`).
- Lotto di card: non abilitato su questo repo.

## Passaggi di consegne

Mandati e resoconti Cowork <-> Claude Code: `~/Scrivania/prompt/<AAAA-MM-GG>_<task>/`
(`01-prompt`, `02-resoconto`, `03-verifica` con riga `Esito:`). Il repo non ha
`docs/5_stato_e_checkpoint.md`.
