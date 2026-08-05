import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

base = Path(__file__).parent
pasta_md = base.parent / "AULA_02" / "markdown"
saida = base / "resultados.json"

schema = {
    "name": "extracao_artigo",
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            "titulo":      {"type": "string", "description": "Título do artigo"},
            "autores":     {"type": "array", "items": {"type": "string"},
                            "description": "Lista dos nomes dos autores"},
            "ano":         {"type": "string", "description": "Ano de publicação"},
            "metodo":      {"type": "string", "description": "Método ou abordagem metodológica usada"},
            "amostra":     {"type": "string", "description": "Amostra, corpus ou dados analisados; 'não informado' se não houver"},
            "metrica":     {"type": "string", "description": "Métricas ou formas de avaliação usadas; 'não informado' se não houver"},
            "limitacoes":  {"type": "string", "description": "Limitações apontadas pelo estudo; 'não informado' se não houver"},
        },
        "required": ["titulo", "autores", "ano", "metodo", "amostra", "metrica", "limitacoes"],
        "additionalProperties": False,
    },
}

resultados = []

for md in sorted(pasta_md.glob("*.md")):
    print(f"Extraindo de: {md.name}...")
    texto = md.read_text(encoding="utf-8")[:12000]

    resposta = client.chat.completions.create(
        model="google/gemma-4-26b-a4b-it:free",  # <-- 
        messages=[
            {"role": "system", "content": "Você extrai metadados de artigos científicos. Responda apenas com JSON, com base no texto fornecido. Se algo não estiver no texto, use 'não informado'."},
            {"role": "user", "content": f"Extraia as informações deste artigo:\n\n{texto}"},
        ],
        response_format={"type": "json_schema", "json_schema": schema},
    )

    conteudo = resposta.choices[0].message.content.strip()

    
    if conteudo.startswith("```"):
        conteudo = conteudo.split("```")[1]
        if conteudo.startswith("json"):
            conteudo = conteudo[4:]
        conteudo = conteudo.strip()

    dados = json.loads(conteudo)
    dados["arquivo"] = md.name
    resultados.append(dados)
    print(f"  -> {dados['titulo'][:60]}...")

saida.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nConcluído. {len(resultados)} artigos salvos em {saida.name}")