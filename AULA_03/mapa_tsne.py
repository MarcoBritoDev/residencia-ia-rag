import os
import requests
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


def gerar_embedding(textos, model="openai/text-embedding-3-small"):
    resposta = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": model, "input": textos},
    )
    resposta.raise_for_status()
    return [item["embedding"] for item in resposta.json()["data"]]


termos = [
    "gato", "felino", "cachorro", "leão", "cavalo", "coelho",      # animais
    "carro", "caminhão", "moto", "ônibus", "avião", "bicicleta",   # veículos
    "banana", "maçã", "goiaba", "uva", "manga", "abacaxi",         # frutas
]
cores = ["blue"]*6 + ["red"]*6 + ["green"]*6

vetores = np.array(gerar_embedding(termos))

coords = TSNE(n_components=2, perplexity=5, random_state=42,
              init="pca").fit_transform(vetores)

plt.figure(figsize=(9, 7))
plt.scatter(coords[:, 0], coords[:, 1], c=cores, s=80)
for (x, y), termo in zip(coords, termos):
    plt.annotate(termo, (x, y), fontsize=10, xytext=(6, 4),
                 textcoords="offset points")
plt.title("Embeddings reduzidos para 2D (via t-SNE)")
plt.tight_layout()
plt.savefig("mapa_tsne.png", dpi=120)
plt.show()