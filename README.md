# ImageRip 🖼️

Estrai logo, immagini di copertina e galleria da qualsiasi sito web, senza problemi CORS.

## Requisiti

- Python 3.6+ (già installato su Mac e Linux; su Windows scaricalo da python.org)
- Nessuna libreria esterna da installare

## Avvio

1. Metti `server.py` e `index.html` nella **stessa cartella**
2. Apri il terminale in quella cartella
3. Esegui:

```bash
python server.py
```

4. Il browser si apre automaticamente su `http://localhost:7771`

## Uso

1. Incolla l'URL del sito nel campo di testo
2. Premi **Analizza →**
3. Le immagini vengono estratte in tre categorie:
   - **Logo** — immagini rilevate come logo del sito
   - **Copertina** — Open Graph image, hero, banner
   - **Galleria** — tutte le altre immagini della pagina
4. Clicca le immagini per selezionarle (o usa "Seleziona tutto")
5. Premi **Scarica ZIP** → file `imagerip_nomesito.zip` con tre sottocartelle

## Note

- Il server gira solo in locale (localhost), non è accessibile da Internet
- Funziona con qualsiasi sito, inclusi quelli con protezioni CORS
- Per fermare il server: `Ctrl+C` nel terminale
