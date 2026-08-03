# Residência em IA Generativa & RAG — PUC-Rio / Instituto ECOA

Repositório com o desenvolvimento das atividades da Residência em Tecnologias
de IA Generativa e RAG. Cada aula fica organizada em sua própria pasta, e o
repositório acompanha a evolução do trabalho ao longo dos três meses do programa.

## Estrutura

- `AULA_01/` — Configuração inicial do ambiente e primeira chamada a um LLM por código.

## Tecnologias

- Python
- python-dotenv (gerenciamento de chaves via variáveis de ambiente)
- SDK da OpenAI, apontado para o OpenRouter

## Nota técnica

As chamadas aos modelos são feitas via OpenRouter, e não pela API da OpenAI
diretamente. O SDK da OpenAI é compatível, então basta ajustar a `base_url` e
usar um modelo com sufixo `:free`. Optei por essa abordagem para trabalhar sem
depender de crédito pago durante os estudos, mantendo o mesmo código que seria
usado com a API oficial.

## Configuração

1. Criar e ativar o ambiente virtual:

python -m venv .venv
.venv\Scripts\Activate.ps1

2. Instalar as dependências:

pip install -r requirements.txt

3. Criar um arquivo `.env` na raiz (baseado no `.env.example`) com a chave:

OPENROUTER_API_KEY=sua_chave_aqui

4. Rodar:

python AULA_01/hello_llm.py