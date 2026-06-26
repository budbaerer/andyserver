import ollama
import os
import json
import base64

MODELL = "llava:7b"
client_ollama = ollama.Client(host="http://192.168.68.103:11434")

def les_bilde(filsti):
    with open(filsti, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
def generer_metadata(filsti, filnavn):
    bilde_data = les_bilde(filsti)
    
    respons = client_ollama.chat(
        model=MODELL,
        messages=[
            {
                "role": "user",
                "content": """Analyser dette bildet og generer metadata i JSON-format med følgende felter:
- tittel
- beskrivelse
- emneord (liste)
- dato (hvis synlig)
- personer (hvis synlige)
- steder (hvis gjenkjennelig)

Svar kun med gyldig JSON, ingen annen tekst.""",
                "images": [bilde_data]
            }
        ]
    )
    return respons["message"]["content"]

mappe = "dokumenter"
filer = os.listdir(mappe)

for filnavn in filer:
    filsti = os.path.join(mappe, filnavn)
    
    if not filnavn.lower().endswith((".jpg", ".jpeg", ".png", ".tiff")):
        print(f"Hopper over {filnavn} — ikke et bilde")
        continue
    
    print(f"Analyserer bilde: {filnavn}...")
    
    metadata_tekst = generer_metadata(filsti, filnavn)
    
    try:
        renset = metadata_tekst.strip()
        renset = renset.replace("```json", "").replace("```", "").strip()
        renset = renset.replace("«", '"').replace("»", '"')
        metadata = json.loads(renset)
        metadata["filnavn"] = filnavn
        
        ut_fil = filnavn + "_metadata.json"
        with open(ut_fil, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"Lagret metadata til {ut_fil}")
    except:
        print(f"Klarte ikke å parse JSON for {filnavn}")
        print(metadata_tekst)

