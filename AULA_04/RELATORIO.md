## [https://drive.google.com/drive/folders/1OvtUfbhoOjppGK9T\_pmH7bYsGbj2Tu9i?usp=sharing](https://drive.google.com/drive/folders/1OvtUfbhoOjppGK9T_pmH7bYsGbj2Tu9i?usp=sharing)

alternativa para modelo de embeddings:
 [https://huggingface.co/blog/getting-started-with-embeddings](https://huggingface.co/blog/getting-started-with-embeddings)

# Avaliação de Estratégias de Chunking com LangChain

## Objetivo

Implementar e comparar **10 estratégias diferentes de divisão de documentos (chunking)** utilizando os splitters disponíveis no **LangChain**, gerando embeddings para cada chunk e salvando os resultados em arquivos JSON.

O objetivo é avaliar como diferentes estratégias de chunking influenciam:

- quantidade de chunks gerados;
- tamanho dos chunks;
- preservação do contexto;
- sobreposição entre chunks;
- representação semântica dos documentos;
- qualidade da estrutura resultante para utilização posterior em sistemas de RAG.

Documentação de referência:

[https://docs.langchain.com/oss/python/integrations/splitters](https://docs.langchain.com/oss/python/integrations/splitters)

---

# 1. Base de documentos

Utilizar **todos os documentos PDF disponíveis na pasta do Google Drive**:

[https://drive.google.com/drive/folders/1OvtUfbhoOjppGK9T\_pmH7bYsGbj2Tu9i](https://drive.google.com/drive/folders/1OvtUfbhoOjppGK9T_pmH7bYsGbj2Tu9i)

Para cada PDF, o pipeline deverá executar as etapas:

```
PDF
 ↓
Extração do conteúdo
 ↓
Markdown
 ↓
Chunking
 ↓
Embeddings
 ↓
JSON

```

A implementação deverá ser capaz de processar todos os documentos da pasta de forma automatizada.

---

# 2. Extração dos PDFs para Markdown

Antes do processo de chunking, os PDFs deverão ser convertidos para **Markdown estruturado**.

A extração deve preservar, sempre que possível:

- títulos e headings;
- parágrafos;
- listas;
- tabelas;
- imagens;
- legendas;
- referências;
- ordem dos elementos no documento;
- informações de página.

### Questão importante

Durante a extração, deve ser avaliado **como cada tipo de conteúdo do PDF é representado no Markdown**.

Especial atenção deverá ser dada a:

### Imagens

Verificar se:

- a imagem é descartada;
- é inserida como referência;
- é convertida para descrição textual;
- é armazenada separadamente;
- possui alguma informação associada à sua posição no documento.

### Tabelas

Verificar se são convertidas para:

```
| Coluna A | Coluna B |
|----------|----------|
| Valor 1  | Valor 2  |

```

ou para outra representação.

Também deve ser analisado se a estrutura e o significado das tabelas são preservados após a conversão.

### Resultado esperado

Para cada PDF, deverá existir uma versão Markdown intermediária que possa ser utilizada pelos diferentes splitters.

---

# 3. Estratégias de Chunking

Utilizar os **splitters do LangChain** para realizar os 10 experimentos abaixo. para os itens 4, 5, 6, 7 e 8 pode usar apenas os três arquivos .md das aulas anteriores. Depois que definir as melhores estrategias aplicar para todos os documentos

| Teste Estratégia Configuração Variável isolada  |                |                               |                       |
| ----------------------------------------------- | -------------- | ----------------------------- | --------------------- |
| 1                                               | Fixo           | 200 caracteres, sem overlap   | Tamanho extremo baixo |
| 2                                               | Fixo           | 500 caracteres, sem overlap   | Tamanho               |
| 3                                               | Fixo           | 1000 caracteres, sem overlap  | Tamanho               |
| 4                                               | Fixo           | 2000 caracteres, sem overlap  | Tamanho extremo alto  |
| 5                                               | Fixo + overlap | 500 caracteres, overlap 50    | Overlap leve          |
| 6                                               | Fixo + overlap | 500 caracteres, overlap 200   | Overlap pesado        |
| 7                                               | Por parágrafo  | Separação por parágrafos      | Estrutura natural     |
| 8                                               | Por sentença   | Sentenças agrupadas em 3      | Estrutura natural     |
| 9                                               | Recursivo      | Separadores hierárquicos      | Estratégia composta   |
| 10                                              | Markdown       | Separação por headings/seções | Estrutura semântica   |

### Observação

Os testes devem ser implementados utilizando os componentes equivalentes disponíveis no LangChain, evitando implementar manualmente os algoritmos de split quando existir um splitter apropriado na biblioteca.

---

# 4. Testes 1 a 6 - Chunking por tamanho

Nos primeiros seis experimentos, o objetivo é avaliar o impacto do tamanho dos chunks e do overlap.

### Teste 1

```
chunk_size = 200
chunk_overlap = 0

```

### Teste 2

```
chunk_size = 500
chunk_overlap = 0

```

### Teste 3

```
chunk_size = 1000
chunk_overlap = 0

```

### Teste 4

```
chunk_size = 2000
chunk_overlap = 0

```

### Teste 5

```
chunk_size = 500
chunk_overlap = 50

```

### Teste 6

```
chunk_size = 500
chunk_overlap = 200

```

Para esses testes, documentar:

- número total de chunks;
- tamanho médio;
- tamanho mínimo;
- tamanho máximo;
- quantidade de chunks sobrepostos;
- percentual de overlap;
- número de tokens, se possível.

---

# 5. Teste 7 - Por parágrafo

Utilizar uma estratégia que preserve os **parágrafos como unidade de contexto**.

O objetivo é verificar se a estrutura natural do documento produz chunks semanticamente mais coerentes do que a divisão puramente baseada em caracteres.

Registrar:

- quantidade de chunks;
- tamanho médio;
- tamanho mínimo/máximo;
- exemplos de chunks;
- metadados associados.

---

# 6. Teste 8 - Sentenças agrupadas

Dividir o documento em sentenças e agrupar **3 sentenças por chunk**.

Exemplo:

```
Sentença 1
Sentença 2
Sentença 3
    ↓
Chunk 1

Sentença 4
Sentença 5
Sentença 6
    ↓
Chunk 2

```

O objetivo é comparar uma unidade de contexto baseada em sentenças com as estratégias baseadas em caracteres.

---

# 7. Teste 9 - Recursive Chunking

Utilizar o **Recursive Character Text Splitter**, explorando a ideia de separadores hierárquicos.

A estratégia deverá priorizar a preservação da estrutura do texto, utilizando separadores como:

```
parágrafos
↓
linhas
↓
espaços
↓
caracteres

```

Registrar a configuração utilizada e justificar a escolha dos parâmetros.

---

# 8. Teste 10 - Markdown / estrutura semântica

Utilizar um splitter específico para documentos Markdown, buscando preservar a estrutura definida pelos headings:

```
# Seção 1

## Subseção 1.1

Texto...

## Subseção 1.2

Texto...

# Seção 2

Texto...

```

O objetivo é avaliar se a estrutura semântica do documento pode produzir chunks mais adequados para recuperação de informação.

Sempre que possível, preservar nos metadados informações como:

```
heading
nível do heading
seção
subseção

```

---

# 9. Geração dos Embeddings

Após a divisão dos documentos, gerar um embedding para **cada chunk**.

O modelo de embedding deverá ser escolhido entre as alternativas avaliadas na tarefa anterior (openrouter ou então usando o embeddings do huggingface como alternativa).

Como referência sobre modelos e utilização de embeddings:

[https://huggingface.co/blog/getting-started-with-embeddings](https://huggingface.co/blog/getting-started-with-embeddings)

A implementação deve deixar o modelo configurável, por exemplo:

```
EMBEDDING_MODEL = "..."

```

Dessa forma, a estratégia de chunking pode ser comparada mantendo o mesmo modelo de embedding.

### Importante

Para que os experimentos sejam comparáveis, **os 10 testes devem utilizar o mesmo modelo de embedding**.

---

# 10. Estrutura dos dados

Cada chunk deverá possuir, no mínimo:

```
{
  "chunk_id": "doc01_test05_chunk001",
  "document_id": "doc01",
  "document_name": "documento.pdf",
  "test_id": 5,
  "strategy": "fixed_with_overlap",
  "chunk_size": 500,
  "chunk_overlap": 50,
  "text": "Conteúdo do chunk...",
  "embedding": [0.0123, -0.0345, "..."],
  "metadata": {
    "page": 10,
    "section": "Introdução"
  }
}

```

Os campos podem ser adaptados de acordo com os metadados efetivamente disponíveis na etapa de extração.

---

# 11. Organização dos arquivos

Os resultados deverão ser organizados de forma que seja possível identificar facilmente:

- documento;
- estratégia utilizada;
- chunks;
- embeddings;
- configuração do experimento.

Uma sugestão de estrutura:

```
results/
├── documento_01/
│   ├── markdown/
│   │   └── documento_01.md
│   │
│   ├── test_01/
│   │   └── chunks_embeddings.json
│   │
│   ├── test_02/
│   │   └── chunks_embeddings.json
│   │
│   ├── test_03/
│   │   └── chunks_embeddings.json
│   │
│   ├── ...
│   │
│   └── test_10/
│       └── chunks_embeddings.json
│
├── documento_02/
│   └── ...
│
└── summary.json

```

---

# 12. Resumo dos experimentos

Além dos arquivos individuais, gerar um `summary.json` contendo informações comparativas dos 10 testes.

Exemplo:

```
{
  "document": "documento_01.pdf",
  "experiments": [
    {
      "test_id": 1,
      "strategy": "fixed",
      "chunk_size": 200,
      "chunk_overlap": 0,
      "num_chunks": 1520,
      "avg_chunk_size": 198.4,
      "embedding_dimension": 768
    }
  ]
}

```

---

# 13. Análise obrigatória

Ao final, produzir uma análise comparando as 10 estratégias.

Responder e analisar:

1. Qual estratégia gerou mais chunks?
2. Qual gerou menos chunks?
3. Como o tamanho dos chunks variou?
4. Qual estratégia preservou melhor a estrutura dos documentos?
5. Como tabelas foram tratadas?
6. Como imagens foram tratadas?
7. Quais informações foram perdidas durante a conversão PDF → Markdown?
8. O chunking por caracteres fragmentou conceitos ou estruturas importantes?
9. O chunking por parágrafo produziu chunks muito grandes?
10. O chunking por sentença conseguiu preservar melhor o contexto?
11. O Recursive Splitter apresentou vantagens?
12. O Markdown Splitter conseguiu preservar a estrutura semântica?
13. Qual estratégia parece mais adequada para um sistema de RAG?
14. Quais estratégias devem ser descartadas?
15. Quais estratégias você acha que devem ser utilizadas nos próximos experimentos?

---

# 14. Entregar

Ao final da atividade, deverão ser entregues pelo github (pasta aula\_04 ou equivalante):

### Código

Pipeline completo responsável por:

```
PDF
 ↓
Markdown
 ↓
10 estratégias de chunking
 ↓
Embeddings
 ↓
JSON

```

### Dados

Para cada documento:

- Markdown gerado;
- chunks dos 10 experimentos;
- embeddings dos 10 experimentos;
- metadados.

### Relatório

Documento contendo:

- configurações dos 10 testes;
- estatísticas;
- exemplos de chunks;
- análise da conversão PDF → Markdown;
- análise de tabelas e imagens;
- comparação das estratégias;
- conclusão sobre as melhores estratégias.

---

# Resultado esperado

Ao final da tarefa, deverá ser possível responder experimentalmente:

> **Qual estratégia de chunking produz a melhor representação dos documentos para utilização em um sistema de RAG?**

A escolha não deve ser baseada apenas no número de chunks. Deve considerar também a **preservação de contexto, estrutura semântica, integridade de tabelas e informações relevantes, tamanho dos chunks e qualidade da representação vetorial**.