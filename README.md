# Residência em IA Generativa & RAG

Projeto da residência em IA Generativa e RAG (Retrieval-Augmented Generation), promovida pelo **Instituto ECOA** em parceria com a **PUC-Rio**. O repositório acompanha as atividades práticas aula a aula, do primeiro contato com LLMs por código até a construção de um pipeline de RAG.

## Stack

- **Python 3.11** em ambiente virtual (`.venv`)
- **OpenRouter** como provedor de modelos (via SDK da OpenAI e chamadas HTTP diretas)
- **Docling** — conversão de PDF para Markdown
- **LangChain** (`langchain-text-splitters`) — estratégias de chunking
- **NumPy**, **scikit-learn**, **Matplotlib** — cálculo vetorial e visualização

## Estrutura

```
residencia-rag/
├── AULA_01/       # primeira chamada a um LLM por código
├── AULA_02/       # conversão de PDF→Markdown e extração estruturada
├── AULA_03/       # embeddings, distâncias e busca semântica
├── AULA_04/       # chunking com LangChain sobre base ampliada
├── documentos/    # base de dados central do projeto
│   ├── pdfs/      # PDFs de origem (NÃO versionados)
│   └── markdown/  # documentos convertidos (versionados)
├── .env           # chaves de API (NÃO versionado)
├── .gitignore
└── requirements.txt
```

## Setup

```
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz com sua chave (veja o modelo em `.env.example`):

```
OPENROUTER_API_KEY=sua_chave_aqui
```

---

## AULA_01 — Primeira chamada a um LLM

Primeiro contato com um modelo de linguagem por código, usando o SDK da OpenAI apontado para o endpoint do OpenRouter (`https://openrouter.ai/api/v1`) com modelos gratuitos. Configuração de ambiente virtual, `.env` e `.gitignore`.

## AULA_02 — PDF para Markdown e extração estruturada

- `converter.py` — converte três artigos científicos de PDF para Markdown com a biblioteca Docling (rodando localmente).
- `extrair.py` — lê cada `.md` e usa o modelo com um schema JSON para extrair campos estruturados (título, autores, ano, método, amostra, métrica, limitações).
- `resultados.json` — saída consolidada da extração.

## AULA_03 — Embeddings, distâncias e busca semântica

O núcleo conceitual do RAG: transformar texto em vetores, medir proximidade de significado e recuperar trechos relevantes.

- **`embeddings.py`** — primeiro teste de embedding: gera vetores de três frases e calcula a similaridade de cosseno entre elas, provando que o modelo captura significado.
- **`distancias.py`** — funções `distancia_euclidiana()` e `distancia_cosseno()` (esta última como `1 - similaridade`), validadas contra vetores simples de resultado conhecido.
- **`similaridade.py`** — ranqueia termos por proximidade a uma consulta usando as duas métricas, e demonstra que embedding recupera por sentido, não por palavra igual (busca literal falha onde a semântica acerta).
- **`ancora.py`** — testa os limites do embedding comparando uma frase-âncora com variações (equivalente, relacionada, de outro domínio e negação), evidenciando a conhecida fraqueza dos embeddings com **negação**.
- **`busca_semantica.py`** — busca semântica sobre os artigos da AULA_02, comparando quatro estratégias de chunking (linha, parágrafo, capítulo e tamanho fixo com sobreposição) e incluindo limpeza do texto herdado da conversão de PDF.
- **`mapa_tsne_3d.py`** — reduz os embeddings a 3D com t-SNE para visualizar o agrupamento por categoria (animais, veículos, frutas).

**Principais aprendizados da aula:**

- Embeddings da OpenAI são normalizados, então distância euclidiana e de cosseno concordam na ordenação; divergência indicaria vetores não-normalizados.
- Visualizações 2D/3D (PCA, t-SNE) ilustram a intuição, mas o ranking no espaço completo (1536 dimensões) é a fonte da verdade.
- A escolha do tamanho do chunk é decisiva: o chunking por tamanho fixo com sobreposição recupera os trechos mais úteis, mesmo com score de topo mais baixo — **score alto não é sinônimo de trecho útil**.
- Pré-processamento (limpeza de hifenização e ruído da extração) impacta diretamente a qualidade da recuperação.

## AULA_04 — Chunking com LangChain sobre base ampliada

Reimplementação das estratégias de chunking com a biblioteca **LangChain**, agora sobre uma base expandida de 12 documentos (os 3 artigos anteriores mais 9 papers fundadores de LLMs e RAG: *Attention Is All You Need*, *BERT*, *GPT-3/4*, *InstructGPT*, *LoRA*, *RAG*, *LLaMA*, *Scaling Laws*).

- `documentos/converter.py` — versão do conversor Docling que lê de `documentos/pdfs/`, escreve em `documentos/markdown/` e **pula arquivos já convertidos**, com tratamento de erro por documento.
- `chunking_langchain.py` — compara 10 estratégias de chunking isolando uma variável por vez (tamanho, sobreposição, estrutura), usando `CharacterTextSplitter`, `RecursiveCharacterTextSplitter` e `MarkdownHeaderTextSplitter`.

**Principais aprendizados da aula:**

- **A busca semântica discrimina assunto, não palavra:** para uma consulta sobre ética algorítmica, todos os trechos de topo vieram dos documentos de ética, mesmo com 9 papers técnicos (que também citam "algoritmo") competindo na base.
- **Existe um ponto ideal de tamanho de chunk:** trechos pequenos maximizam o score mas cortam contexto; trechos grandes preservam contexto mas diluem o score.
- **O `RecursiveCharacterTextSplitter` produz trechos mais limpos** que o corte de tamanho fixo, por respeitar fronteiras de parágrafo e frase — é o padrão recomendado.
- **Chunking por estrutura (seção) é inviável em base heterogênea:** um paper sem subtítulos gerou um chunk de 52.313 caracteres, muito acima do limite da API de embedding. Estratégias de tamanho fixo e recursivo são mais seguras por garantirem um teto de tamanho.

---

## Segurança

O arquivo `.env` contém a chave de API e **nunca** é versionado — está no `.gitignore`, junto com o `.venv` e os PDFs de origem (`documentos/pdfs/`), que são pesados e reproduzíveis a partir dos scripts. Apenas os markdowns convertidos são versionados. Antes de cada commit, o `git status` é verificado para garantir que nenhuma credencial seja enviada ao repositório.