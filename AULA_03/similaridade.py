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


def euclidiana(a, b):
    a, b = np.array(a), np.array(b)
    return np.linalg.norm(a - b)          # MENOR = mais perto


def cosseno(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))  # MAIOR = mais perto


def ranquear(consulta, corpus, metrica=cosseno):
    """Ordena o corpus pela proximidade à consulta. Uma chamada de API só."""
    vetores = gerar_embedding([consulta] + corpus)
    v_consulta, v_corpus = vetores[0], vetores[1:]
    scores = [(termo, metrica(v_consulta, v)) for termo, v in zip(corpus, v_corpus)]
    scores.sort(key=lambda x: x[1], reverse=(metrica is cosseno))
    return scores


mapa = ["felino", "cachorro", "carro", "caminhão", "moto", "banana", "maçã", "goiaba"]

print("=== Consulta: 'gato' — por COSSENO (maior = mais perto) ===")
for termo, s in ranquear("gato", mapa, cosseno):
    print(f"  {s:.4f}  {termo}")

print("\n=== Consulta: 'gato' — por EUCLIDIANA (menor = mais perto) ===")
for termo, s in ranquear("gato", mapa, euclidiana):
    print(f"  {s:.4f}  {termo}")


# ---------- Lab 2: prova que cosseno pega SIGNIFICADO, não palavra igual ----------
pergunta = "como devolver um produto?"
trecho   = "política de reembolso em 7 dias"

va, vb = gerar_embedding([pergunta, trecho])
print(f"\ncosseno(pergunta, trecho) = {cosseno(va, vb):.4f}")
print(f"busca literal ('pergunta' está dentro do trecho?): {pergunta in trecho}")