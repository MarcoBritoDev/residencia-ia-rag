import os
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


def gerar_embedding(textos, model="openai/text-embedding-3-small"):
    resposta = requests.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        json={"model": model, "input": textos},
    )
    resposta.raise_for_status()
    return [item["embedding"] for item in resposta.json()["data"]]


def cosseno(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


frase_ancora = "O cachorro correu no parque e brincou com a bola."
frases_comparacao = [
    ("Similar (mesmo sentido, palavras diferentes)", "Um cão estava correndo no jardim e brincando com seu brinquedo."),
    ("Relacionado (mesmo contexto de animais)", "O gato dormiu na almofada da sala durante toda a tarde."),
    ("Diferente (outro domínio - economia)", "A taxa de juros do banco central subiu dois pontos percentuais."),
    ("Oposto/Negação", "Nenhum animal esteve no parque e o cão permaneceu preso em casa."),
]

# uma chamada só: âncora na posição 0
todas = [frase_ancora] + [f for _, f in frases_comparacao]
vetores = gerar_embedding(todas)
v_ancora, v_resto = vetores[0], vetores[1:]

print(f"Âncora: {frase_ancora}\n")
for (rotulo, frase), v in zip(frases_comparacao, v_resto):
    s = cosseno(v_ancora, v)
    print(f"  {s:.4f}  [{rotulo}]")
    print(f"          {frase}\n")