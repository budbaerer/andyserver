# andyserver
Lokal server med Ollama, Borealis og Open WebUI

Prosjekt for en server som gjør at sluttbruker kan prompte Nasjonalbibliotekets 
norske språkmodell Borealis via et brukergrensesnitt i nettleser. Serveren kjører 
komponentene i separate Docker-containere.

## Komponenter

| Tjeneste | Beskrivelse | Port |
|----------|-------------|------|
| Ollama | Kjører språkmodeller lokalt | 11434 |
| Borealis 4b | Norsk språkmodell fra NbAiLab | - |
| Open WebUI | Nettlesergrensesnitt for chat | 3000 |

## Serveroppsett
- Ubuntu 24.04
- Intel Xeon E5-2620 v3 (12 kjerner)
- 15GB RAM
- Ingen GPU — kjører på CPU

