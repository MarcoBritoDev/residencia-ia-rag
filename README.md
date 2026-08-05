Residência em IA Generativa & RAG — Instituto ECOA / PUC-Rio

Repositório com o desenvolvimento das atividades da Residência Trilhas em Tecnologia — Trilha de IA Generativa & RAG (Instituto ECOA, PUC-Rio). Cada aula é organizada em sua própria pasta, e o repositório acompanha a evolução do trabalho ao longo do programa.

Estrutura
residencia-ia-rag/
├── AULA_01/          # Primeira chamada a um LLM por código
│   └── hello_llm.py
├── AULA_02/          # Conversão de artigos científicos (PDF → Markdown)
│   ├── pdfs/         # Artigos de entrada
│   ├── markdown/     # Saída convertida
│   └── converter.py
├── .env.example      # Molde das variáveis de ambiente (sem a chave real)
├── .gitignore
├── requirements.txt
└── README.md
Aulas
Aula 01 — Primeira chamada a um LLM por código

Configuração do ambiente de desenvolvimento e primeira interação com um modelo de linguagem via código: ambiente virtual, gerenciamento seguro da chave de API com variáveis de ambiente, e uma chamada de chat que recebe e trata a resposta do modelo.

Aula 02 — Conversão de documentos (PDF → Markdown)

Ingestão de artigos científicos em PDF e conversão para Markdown usando a biblioteca Docling, que faz análise de layout, reconstrução da ordem de leitura e detecção de estrutura. Esta é a primeira etapa de um pipeline de RAG: transformar documentos em texto limpo, pronto para as etapas seguintes (chunking, embeddings, indexação).

Tecnologias
Python (ambiente virtual com venv)
python-dotenv — gerenciamento de chaves via variáveis de ambiente
SDK da OpenAI, apontado para o OpenRouter (Aula 01)
Docling — conversão de documentos para Markdown (Aula 02)
Notas técnicas
Provedor de LLM: as chamadas usam o OpenRouter (com a base_url do OpenRouter e modelos gratuitos com sufixo :free), e não a API paga da OpenAI diretamente. O SDK é o mesmo; muda apenas o endpoint. A escolha permite trabalhar sem depender de crédito pago durante os estudos.
Segurança da chave: a chave de API fica somente no arquivo .env (ignorado pelo Git via .gitignore) e nunca é versionada. O .env.example documenta apenas a estrutura esperada, sem valores reais.
Aula 02 — arquivo corrompido: um dos PDFs de entrada apresentava streams internos danificados, o que impedia a extração automática de texto. O caso serviu para reforçar a importância de validar os arquivos de entrada em um pipeline de ingestão de dados.
Como executar
Criar e ativar o ambiente virtual:
   python -m venv .venv
   .venv\Scripts\Activate.ps1     # Windows (PowerShell)
Instalar as dependências:
   pip install -r requirements.txt
Criar um arquivo .env na raiz (baseado no .env.example) com a chave:
   OPENROUTER_API_KEY=sua_chave_aqui
Executar a atividade desejada, por exemplo:
   python AULA_01/hello_llm.py
   python AULA_02/converter.py
