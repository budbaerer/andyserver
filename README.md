# andyserver
Lokal server med Ollama, Borealis, ChromaDB og Open WebUI

Prosjekt for en server som gjør at sluttbruker kan prompte Nasjonalbibliotekets 
norske språkmodell Borealis via et brukergrensesnitt i nettleser. Serveren kjører 
komponentene i separate Docker-containere.

## Komponenter

| Tjeneste | Beskrivelse | Port |
|----------|-------------|------|
| Ollama | Kjører språkmodeller lokalt | 11434 |
| Borealis 4b | Norsk språkmodell fra NbAiLab | - |
| Open WebUI | Nettlesergrensesnitt for chat | 3000 |
| ChromaDB | Vektordatabase for dokumentsøk | 8000 |

## Serveroppsett
- Ubuntu 24.04
- Intel Xeon E5-2620 v3 (12 kjerner)
- 15GB RAM
- Ingen GPU — kjører på CPU

## Prosjekt 2 — RAG-system

To Python-programmer for å søke i dokumenter med språkmodell:

- `last_inn_dokumenter.py` — leser en tekstfil og lagrer innholdet som vektorer i ChromaDB
- `rag.py` — tar imot et spørsmål fra bruker, henter de mest relevante avsnittene fra ChromaDB og sender dem til Borealis som svarer basert på innholdet
