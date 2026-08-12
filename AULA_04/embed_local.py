from sentence_transformers import SentenceTransformer

EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# carrega uma vez só (na primeira execução, baixa ~400 MB; depois usa cache local)
print(f"Carregando modelo {EMBEDDING_MODEL}...")
modelo = SentenceTransformer(EMBEDDING_MODEL)
print("Modelo carregado.\n")


def gerar_embedding(textos, lote=64):
    """Gera embeddings LOCALMENTE — sem API, sem custo, sem 402."""
    vetores = modelo.encode(textos, batch_size=lote, show_progress_bar=True)
    return vetores.tolist()


# --- teste rápido: prova que funciona e mostra a dimensão ---
if __name__ == "__main__":
    frases = [
        "gato",
        "felino",
        "carro",
    ]
    vetores = gerar_embedding(frases)
    print(f"\nGerados {len(vetores)} embeddings.")
    print(f"Dimensão de cada embedding: {len(vetores[0])}")

    # sanity check: gato deve estar mais perto de felino que de carro
    import numpy as np
    def cos(a, b):
        a, b = np.array(a), np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    print(f"\ncosseno(gato, felino) = {cos(vetores[0], vetores[1]):.4f}")
    print(f"cosseno(gato, carro)  = {cos(vetores[0], vetores[2]):.4f}")
    print("(o primeiro deve ser MAIOR — gato é mais parecido com felino)")
