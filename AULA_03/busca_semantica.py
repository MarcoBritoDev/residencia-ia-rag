import os
import re
import glob
import requests
import numpy as np
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

def por_tamanho_fixo(texto, tamanho=500, overlap=50):
    """Chunk de tamanho fixo com sobreposição — o padrão de RAG de produção.
    Não depende da formatação do documento."""
    texto = " ".join(texto.split())          # normaliza espaços/quebras
    chunks = []
    i = 0
    while i < len(texto):
        chunks.append(texto[i:i + tamanho])
        i += tamanho - overlap                # avança, mas volta `overlap` pra trás
    return chunks


def gerar_embedding(textos, model="openai/text-embedding-3-small", lote=100):
    """Gera embeddings em lotes de `lote` para não estourar o limite da API."""
    vetores = []
    for i in range(0, len(textos), lote):
        pedaco = textos[i:i + lote]
        resposta = requests.post(
            "https://openrouter.ai/api/v1/embeddings",
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": model, "input": pedaco},
        )
        resposta.raise_for_status()
        vetores.extend(item["embedding"] for item in resposta.json()["data"])
    return vetores


def cosseno(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def carregar_texto(pasta="../AULA_02/markdown"):
    """Lê e concatena todos os .md da pasta."""
    caminhos = glob.glob(os.path.join(pasta, "*.md"))
    if not caminhos:
        raise FileNotFoundError(f"Nenhum .md em {pasta}. Rode de dentro de AULA_03.")
    partes = []
    for caminho in caminhos:
        with open(caminho, encoding="utf-8") as f:
            partes.append(f.read())
    return "\n\n".join(partes)


def por_linha(texto):
    return [l.strip() for l in texto.split("\n") if l.strip()]

def por_paragrafo(texto):
    blocos = re.split(r"\n\s*\n", texto)   
    paragrafos = []
    for bloco in blocos:
        p = " ".join(linha.strip() for linha in bloco.split("\n") if linha.strip())
        if p:
            paragrafos.append(p)
    return paragrafos

def por_capitulo(texto):
    partes = re.split(r"\n(?=#{1,6}\s)", texto)
    return [p.strip() for p in partes if p.strip()]


def buscar(query, trechos, top=3):
    """Embedda a query + todos os trechos e devolve os `top` de maior cosseno."""
    vetores = gerar_embedding([query] + trechos)
    v_query, v_trechos = vetores[0], vetores[1:]
    scores = [(cosseno(v_query, v), t) for v, t in zip(v_trechos, trechos)]
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores[:top]

def limpar_texto(texto):
    """Junta só palavras quebradas por hífen de fim de linha (com espaço antes do -)."""
    # "desenvolvi -mento" tem espaço antes do hífen; "médico-paciente" não tem
    texto = re.sub(r"(\w+)\s+-\s*(\w+)", r"\1\2", texto)
    return texto


query = "O que é 'Autonomia e opacidade algorítmica'?"
texto = carregar_texto()
texto = limpar_texto(texto)



print(f"QUERY: {query}\n")

for nome, funcao in [("LINHA", por_linha), ("PARÁGRAFO", por_paragrafo),
                     ("CAPÍTULO", por_capitulo), ("TAMANHO FIXO", por_tamanho_fixo)]:
    trechos = funcao(texto)
    print("=" * 75)
    print(f"ESTRATÉGIA: {nome}  —  {len(trechos)} trechos")
    print("=" * 75)
    for score, trecho in buscar(query, trechos):
        preview = " ".join(trecho.split())[:200]
        print(f"\n  score = {score:.4f}")
        print(f"  {preview}")
    print()