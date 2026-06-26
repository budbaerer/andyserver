import ollama
import os
import json
from pypdf import PdfReader
from docx import Document

MODELL = "NbAiLab/borealis-instruct-preview:4b"
client_ollama = ollama.Client(host="http://192.168.68.103:11434")

def les_fil(filsti):
    if filsti.endswith(".txt"):
        with open(filsti, "r", encoding="utf-8") as f:
            return f.read()
    elif filsti.endswith(".pdf"):
        leser = PdfReader(filsti)
        return "\n".join([side.extract_text() for side in leser.pages])
    elif filsti.endswith(".docx"):
        doc = Document(filsti)
        return "\n".join([avsnitt.text for avsnitt in doc.paragraphs])
    else:
        return None
    
def generer_metadata(tekst, filnavn):
        
    respons = client_ollama.chat(
        model=MODELL,
        messages=[
            {
                "role": "system",
                "content": "Du er en arkivfaglig assistent. Svar kun med gyldig JSON, ingen annen tekst."
            },
            {
                "role": "user",
                "content": f"""Analyser dette dokumentet og generer metadata i JSON-format med følgende felter:
- tittel
- dato (hvis funnet)
- emneord (liste)
- sakstype
- bevaringsverdi (bevares/kasseres)

Dokument: {tekst[:3000]}

Svar kun med JSON."""
            }
        ]
    )
    return respons["message"]["content"]

mappe = "dokumenter"
filer = os.listdir(mappe)

for filnavn in filer:
    filsti = os.path.join(mappe, filnavn)
    tekst = les_fil(filsti)

    if tekst is None:
        print(f"Hopper over {filnavn} — ukjent filtype")
        continue

    print(f"Genererer metadata for {filnavn}...")
    
    metadata_tekst = generer_metadata(tekst, filnavn)
    
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