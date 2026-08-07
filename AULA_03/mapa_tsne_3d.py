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

# n_components=3 → agora projeta em 3 dimensões em vez de 2
coords = TSNE(n_components=3, perplexity=5, random_state=42,
              init="pca").fit_transform(vetores)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection="3d")          # eixo 3D
ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=cores, s=80)

# em 3D o rótulo usa ax.text com três coordenadas
for (x, y, z), termo in zip(coords, termos):
    ax.text(x, y, z, termo, fontsize=9)

ax.set_title("Embeddings reduzidos para 3D (via t-SNE)")
plt.tight_layout()
plt.savefig("mapa_tsne_3d.png", dpi=120)
plt.show()