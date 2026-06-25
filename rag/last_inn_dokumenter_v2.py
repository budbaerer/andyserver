import chromadb
import os
from pypdf import PdfReader
from docx import Document

client = chromadb.HttpClient(host="192.168.68.103", port=8000)
collection = client.get_or_create_collection("arkiv")

eksisterende = collection.get()["ids"]

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

mappe = "dokumenter"
filer = os.listdir(mappe)

for filnavn in filer:
    filsti = os.path.join(mappe, filnavn)
    tekst = les_fil(filsti)

    if tekst is None:
        print(f"Hopper over {filnavn} — ukjent filtype")
        continue

    avsnitt = tekst.split("\n")
    avsnitt = [a for a in avsnitt if a.strip()]

    ids = [f"{filnavn}_{i}" for i in range(len(avsnitt))]

    nye_avsnitt = []
    nye_ids = []

    for avsnitt_tekst, id in zip(avsnitt, ids):
        if id not in eksisterende:
            nye_avsnitt.append(avsnitt_tekst)
            nye_ids.append(id)

    if nye_avsnitt:
        collection.add(
            documents=nye_avsnitt,
            ids=nye_ids
        )
        print(f"Lastet inn {len(nye_avsnitt)} avsnitt fra {filnavn}")
    else:
        print(f"{filnavn} er allerede lastet inn — hopper over")