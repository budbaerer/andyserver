import chromadb

client = chromadb.HttpClient(host="192.168.68.103", port=8000)
collection = client.get_or_create_collection("arkiv")

with open("testdokument.txt", "r", encoding="utf-8") as f:
    tekst = f.read()

avsnitt = tekst.split("\n")
avsnitt = [a for a in avsnitt if a.strip()]

collection.add(
    documents=avsnitt,
    ids=[str(i) for i in range(len(avsnitt))]
)

print(f"Lastet inn {len(avsnitt)} avsnitt i ChromaDB")