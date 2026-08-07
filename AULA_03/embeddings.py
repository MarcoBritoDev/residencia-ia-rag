import os
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def gerar_embedding(textos, model="openai/text-embedding-3-small"):
    """Recebe uma lista de textos e retorna a lista de vetores (embeddings)."""
    resposta = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": textos},
    )
    resposta.raise_for_status()  # levanta erro se a API recusar (402, 404, etc.)
    dados = resposta.json()
    return [item["embedding"] for item in dados["data"]]


def similaridade(a, b):
    """Similaridade do cosseno entre dois vetores: 1 = idênticos, 0 = sem relação."""
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


frases = [
    "bioética e inteligência artificial na medicina",
    "algoritmos e moderação de conteúdo em redes sociais",
    "escrita acadêmica assistida por IA",
]

vetores = gerar_embedding(frases)

print(f"Cada embedding tem {len(vetores[0])} dimensões.\n")

# compara a primeira frase com as outras duas
for i in range(1, len(frases)):
    s = similaridade(vetores[0], vetores[i])
    print(f"Similaridade entre frase 0 e frase {i}: {s:.4f}")
    print(f"   '{frases[0]}'")
    print(f"   '{frases[i]}'\n")