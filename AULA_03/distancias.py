import os
import requests
import numpy as np
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


def distancia_euclidiana(a, b):
    """Distância euclidiana: 0 = idênticos, quanto maior, mais diferentes."""
    a, b = np.array(a), np.array(b)
    return np.linalg.norm(a - b)


def distancia_cosseno(a, b):
    """Distância de cosseno = 1 - similaridade. 0 = mesma direção, 2 = opostos."""
    a, b = np.array(a), np.array(b)
    similaridade = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    return 1 - similaridade


# ---------- Parte 3: teste com vetores simples do enunciado ----------
embedding_a = [1, 0, 0]
embedding_b = [0, 1, 0]
embedding_c = [1, 0, 0]

print("=== Vetores de teste (enunciado) ===")
print(f"euclidiana(a, b) = {distancia_euclidiana(embedding_a, embedding_b):.4f}   cosseno(a, b) = {distancia_cosseno(embedding_a, embedding_b):.4f}")
print(f"euclidiana(a, c) = {distancia_euclidiana(embedding_a, embedding_c):.4f}   cosseno(a, c) = {distancia_cosseno(embedding_a, embedding_c):.4f}")
print(f"euclidiana(b, c) = {distancia_euclidiana(embedding_b, embedding_c):.4f}   cosseno(b, c) = {distancia_cosseno(embedding_b, embedding_c):.4f}")


# ---------- Termos reais: embeddings de verdade ----------
termos = ["gato", "felino", "cachorro", "carro", "caminhão", "moto",
          "banana", "maçã", "goiaba"]

vetores = gerar_embedding(termos)

print("\n=== Termos reais — consulta: 'gato' ===")
gato = vetores[0]
for termo, v in zip(termos[1:], vetores[1:]):
    de = distancia_euclidiana(gato, v)
    dc = distancia_cosseno(gato, v)
    print(f"  euclidiana={de:.4f}  cosseno={dc:.4f}  {termo}")