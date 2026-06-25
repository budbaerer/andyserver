import chromadb
import ollama

client = chromadb.HttpClient(host="192.168.68.103", port=8000)
collection = client.get_collection("arkiv")

spørsmål = input("Still et spørsmål: ")

resultater = collection.query(
    query_texts=[spørsmål],
    n_results=7
)

kontekst = "\n".join(resultater["documents"][0])
print("\n--- KONTEKST FRA CHROMADB ---")
print(kontekst)
print("--- SLUTT KONTEKST ---\n")

client_ollama = ollama.Client(host="http://192.168.68.103:11434")
respons = client_ollama.chat(
    model="NbAiLab/borealis-instruct-preview:4b",
    messages=[
        {
            "role": "system",
            "content": "Du er en arkivfaglig assistent. Svar kun basert på informasjonen du får. Svar på norsk bokmål. Hvis svaret ikke finnes i informasjonen, si at du ikke vet."
        },
        {
            "role": "user",
            "content": f"Informasjon:\n{kontekst}\n\nSpørsmål: {spørsmål}"
        }
    ]
)

print(respons["message"]["content"])