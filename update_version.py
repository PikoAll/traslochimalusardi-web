import os
import re

# Definizione della nuova versione (Aggiornare manualmente prima del push)
# Il formato è Anno.Mese.Giorno.Revisione
# Per esempio: 2025.10.17.1
NEW_VERSION = "2025.12.01.1" 
HTML_DIRECTORY = "./"

# Espressioni regolari per trovare i riferimenti a CSS e JS
# Rileva riferimenti a /assets/css/main.css e /assets/js/main.js
# Rileva anche riferimenti a librerie come slick.min.js se hanno il ?v=
ASSET_REGEX = r'(href|src)="(assets/.*?(\.css|\.js))(\?v=[\d\.]+)?(\"|>)'

def update_version_in_html(file_path, version):
    """Aggiorna il parametro di versione in tutti i file CSS/JS trovati nel file HTML."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            
        # Funzione di sostituzione: aggiunge o aggiorna il parametro ?v=
        def replacer(match):
            tag, asset_path, file_extension, old_version, quote_or_end = match.groups()
            
            # Se c'era già un parametro di versione, lo ignora, altrimenti lo aggiunge
            return f'{tag}="{asset_path}?v={version}{quote_or_end}'
        
        new_content = re.sub(ASSET_REGEX, replacer, content)

        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(new_content)
            print(f"[SUCCESS] Aggiornato {file_path} a v{version}")
        # else:
            # print(f"[SKIP] Nessuna modifica necessaria in {file_path}")

    except Exception as e:
        print(f"[ERROR] Errore nell'elaborazione di {file_path}: {e}")

# --- Inizio Esecuzione ---
print(f"Inizio aggiornamento assets alla versione: {NEW_VERSION}")
for filename in os.listdir(HTML_DIRECTORY):
    if filename.endswith(".html"):
        file_path = os.path.join(HTML_DIRECTORY, filename)
        update_version_in_html(file_path, NEW_VERSION)

print("Aggiornamento Cache Busting completato!")
