# Residência em IA Generativa & RAG — Instituto ECOA / PUC-Rio

Repositório com o desenvolvimento das atividades da **Residência Trilhas em Tecnologia — Trilha de IA Generativa & RAG** (Instituto ECOA, PUC-Rio). Cada aula é organizada em sua própria pasta, e o repositório acompanha a evolução do trabalho ao longo do programa.

## Estrutura

```
residencia-ia-rag/
├── AULA_01/            # Primeira chamada a um LLM por código
│   └── hello_llm.py
├── AULA_02/            # Conversão de artigos científicos (PDF → Markdown)
│   ├── pdfs/           # Artigos de entrada
│   ├── markdown/       # Saída convertida
│   └── converter.py
├── AULA_02.1/          # Extração de metadados dos Markdown (Structured Outputs)
│   ├── extrair.py
│   └── resultados.json
├── .env.example        # Molde das variáveis de ambiente (sem a chave real)
├── .gitignore
├── requirements.txt
└── README.md
```

## Aulas

### Aula 01 — Primeira chamada a um LLM por código

Configuração do ambiente de desenvolvimento e primeira interação com um modelo de linguagem via código: ambiente virtual, gerenciamento seguro da chave de API com variáveis de ambiente, e uma chamada de chat que recebe e trata a resposta do modelo.

### Aula 02 — Conversão de documentos (PDF → Markdown)

Ingestão de artigos científicos em PDF e conversão para Markdown usando a biblioteca **Docling**, que faz análise de layout, reconstrução da ordem de leitura e detecção de estrutura. Esta é a primeira etapa de um pipeline de RAG: transformar documentos em texto limpo, pronto para as etapas seguintes.

### Aula 02.1 — Extração de metadados (Structured Outputs)

A partir dos arquivos Markdown gerados na Aula 02, cada documento é processado por um LLM usando **Structured Outputs** (parâmetro `response_format` com `json_schema`), que obriga o modelo a responder em um formato JSON fixo. São extraídos, no mínimo, título, autores e ano de publicação — além de campos adicionais como método, amostra, métrica e limitações. O resultado é salvo em `resultados.json`, transformando documentos de texto em dados estruturados e consultáveis.

## Tecnologias

- **Python** (ambiente virtual com `venv`)
- **python-dotenv** — gerenciamento de chaves via variáveis de ambiente
- **SDK da OpenAI**, apontado para o **OpenRouter**
- **Docling** — conversão de documentos para Markdown
- **Structured Outputs** (JSON Schema) para extração de metadados

## Notas técnicas

- **Provedor de LLM:** as chamadas usam o **OpenRouter** (com a `base_url` do OpenRouter e modelos gratuitos), e não a API paga da OpenAI diretamente. O SDK é o mesmo; muda apenas o endpoint. Para a extração com Structured Outputs foi usado o roteador `openrouter/free`, que seleciona automaticamente um modelo gratuito compatível com o recurso.
- **Segurança da chave:** a chave de API fica somente no arquivo `.env` (ignorado pelo Git via `.gitignore`) e nunca é versionada. O `.env.example` documenta apenas a estrutura esperada, sem valores reais.
- **Qualidade de entrada:** um dos PDFs da Aula 02 estava corrompido (streams internos danificados), impedindo a extração automática de texto. Além disso, na Aula 02.1 alguns campos (como o ano de um dos artigos) retornaram "não informado" quando a informação não estava acessível no texto convertido. Ambos os casos reforçam a importância de validar a qualidade dos dados de entrada em um pipeline de ingestão.

## Como executar

1. Criar e ativar o ambiente virtual:

   ```
   python -m venv .venv
   .venv\Scripts\Activate.ps1     # Windows (PowerShell)
   ```

2. Instalar as dependências:

   ```
   pip install -r requirements.txt
   ```

3. Criar um arquivo `.env` na raiz (baseado no `.env.example`) com a chave:

   ```
   OPENROUTER_API_KEY=sua_chave_aqui
   ```

4. Executar as atividades:

   ```
   python AULA_01/hello_llm.py       # primeira chamada ao LLM
   python AULA_02/converter.py       # PDF -> Markdown
   python AULA_02.1/extrair.py       # extracao de metadados -> resultados.json
   ```
