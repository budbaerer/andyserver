import chromadb
import ollama

client = chromadb.HttpClient(host="192.168.68.103", port=8000)
collection = client.get_collection("arkiv")

spørsmål = input("Still et spørsmål: ")

resultater = collection.query(
    query_texts=[spørsmål],
    n_results=2
)

kontekst = "\n".join(resultater["documents"][0])

client_ollama = ollama.Client(host="http://192.168.68.103:11434")
respons = client_ollama.chat(
    model="NbAiLab/borealis-instruct-preview:4b",
    messages=[
        {
            "role": "system",
            "content": "Svar kun basert på informasjonen du får. Svar på norsk."
        },
        {
            "role": "user",
            "content": f"Informasjon:\n{kontekst}\n\nSpørsmål: {spørsmål}"
        }
    ]
)

print(respons["message"]["content"])