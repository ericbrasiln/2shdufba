#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
read_doc.py

Script educativo para analisar o conteúdo de um arquivo .txt com um modelo local do Ollama.

O que ele faz:
1) Checa se o servidor do Ollama está ativo em http://localhost:11434
2) Lista modelos já baixados localmente (API /api/tags)
3) Pede ao usuário um arquivo .txt e um prompt
4) Envia tudo ao modelo escolhido (API /api/generate) e exibe a resposta

Requisitos:
- Python 3.8+
- Ollama instalado e em execução (https://ollama.com)
  Inicie o servidor antes de rodar: `ollama serve` (ou abra o app no Windows)

Uso:
    python read_doc.py

Observações:
- Para arquivos muito grandes, o script faz um corte conservador (ex.: 15.000 caracteres)
  para evitar estouro de contexto em modelos pequenos.
- Este script é propositalmente simples e didático.
"""

from __future__ import annotations
import sys
import json
import requests
from pathlib import Path

OLLAMA_HOST = "http://localhost:11434" # Host padrão do Ollama local

# Limite simples de caracteres do documento a ser enviado no prompt.
# Ajuste se necessário, conforme o modelo (quanto menor o modelo, menor deve ser o contexto).
DOC_CHAR_LIMIT = 25000


def check_server() -> None:
    """Verifica se o servidor do Ollama está acessível."""
    url = f"{OLLAMA_HOST}/api/version"
    try:
        r = requests.get(url, timeout=5) # Verifica se o servidor responde
        r.raise_for_status()
    except requests.exceptions.RequestException as exc:
        print(
            "\n[ERRO] Não consegui falar com o servidor do Ollama em "
            f"{OLLAMA_HOST}.\n"
            "Dicas:\n"
            "  • Verifique se o Ollama está instalado.\n"
            "  • Inicie o servidor (ex.: `ollama serve`) ou abra o aplicativo (Windows/macOS).\n"
            f"Detalhes técnicos: {exc}\n"
        )
        sys.exit(1)


def list_local_models() -> list[dict]:
    """
    Retorna a lista de modelos disponíveis localmente (baixados).
    Usa /api/tags. Cada item contém campos como 'name' e 'size'.
    """
    url = f"{OLLAMA_HOST}/api/tags"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        models = data.get("models", [])
        return models
    except requests.exceptions.RequestException as exc:
        print(f"[ERRO] Falha ao listar modelos locais: {exc}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("[ERRO] Resposta inesperada do servidor ao consultar /api/tags.")
        sys.exit(1)


def choose_model(models: list[dict]) -> str:
    """
    Exibe os modelos com numeração e retorna o 'name' do modelo escolhido.
    Pede ao usuário para escolher um número.
    """
    if not models:
        print(
            "\n[AVISO] Nenhum modelo encontrado localmente.\n"
            "Baixe ao menos um modelo antes de continuar, por exemplo:\n"
            "  ollama pull phi3:mini\n"
        )
        sys.exit(1)

    print("\nModelos locais encontrados:")
    for idx, m in enumerate(models, start=1):
        name = m.get("name", "desconhecido")
        size_bytes = m.get("size", 0)
        # Tenta converter tamanho para MB/GB de forma amigável
        human = _human_readable_size(size_bytes)
        print(f"  {idx}. {name} ({human})")

    while True:
        choice = input("\nEscolha o número do modelo que deseja usar: ").strip()
        if not choice.isdigit():
            print("Por favor, digite um número válido (ex.: 1, 2, 3...).")
            continue
        choice_i = int(choice)
        if 1 <= choice_i <= len(models):
            return models[choice_i - 1].get("name", "")
        print(f"Escolha um número entre 1 e {len(models)}.")


def _human_readable_size(num_bytes: int) -> str:
    """
    Função para converter tamanho em bytes para string legível (KB/MB/GB).
    """
    try:
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if num_bytes < 1024.0:
                return f"{num_bytes:.1f} {unit}"
            num_bytes /= 1024.0
        return f"{num_bytes:.1f} PB"
    except Exception:
        return "tamanho desconhecido"


def ask_file_path() -> Path:
    """
    Pede ao usuário o caminho de um arquivo .txt e valida a existência.
    """
    while True:
        p = input("\nDigite o caminho do arquivo .txt: ").strip().strip('"').strip("'")
        path = Path(p).expanduser()
        if not path.exists():
            print("[ERRO] Caminho não encontrado. Tente novamente.")
            continue
        if not path.is_file():
            print("[ERRO] O caminho informado não é um arquivo. Tente novamente.")
            continue
        if path.suffix.lower() != ".txt":
            print("[AVISO] O arquivo não é .txt. Vou tentar ler mesmo assim.")
        return path


def read_text_file(path: Path) -> str:
    """
    Lê o conteúdo de um arquivo de texto com fallback de codificação.
    """
    # Tentamos UTF-8 primeiro; se falhar, tentamos latin-1 (Windows com acentos)
    encodings = ["utf-8", "latin-1"]
    for enc in encodings:
        try:
            return path.read_text(encoding=enc, errors="replace")
        except Exception:
            continue
    print("[ERRO] Não foi possível ler o arquivo de texto.")
    sys.exit(1)


def ask_user_prompt() -> str:
    """
    Pede o prompt do usuário.
    """
    print("\nAgora escreva o prompt (o que você quer saber sobre o documento):")
    prompt = input("> ").strip()
    if not prompt:
        print("[ERRO] Prompt vazio. Tente novamente executando o script.")
        sys.exit(1)
    return prompt


def build_instruction(user_prompt: str, doc_text: str) -> str:
    """
    Monta a instrução final a ser enviada ao modelo.
    Inclui um cabeçalho simples + recorte do documento.
    """
    doc_for_context = doc_text
    trimmed = "" # Mensagem de aviso se o documento for recortado
    if len(doc_text) > DOC_CHAR_LIMIT:
        doc_for_context = doc_text[:DOC_CHAR_LIMIT]
        trimmed = (
            f"\n\n[AVISO] Documento original tinha {len(doc_text)} caracteres. "
            f"Recortado para {DOC_CHAR_LIMIT} caracteres para caber no contexto."
        )

    instruction = (
        "Você é um assistente que responde com base EXCLUSIVAMENTE no documento fornecido.\n"
        "Se a informação não estiver claramente no documento, diga que não encontrou.\n\n"
        "=== DOCUMENTO INÍCIO ===\n"
        f"{doc_for_context}\n"
        "=== DOCUMENTO FIM ===\n\n"
        "Pergunta do usuário:\n"
        f"{user_prompt}\n"
    )

    if trimmed:
        print(trimmed)
    return instruction


def generate_with_ollama(model_name: str, instruction: str) -> str:
    """
    Chama a API /api/generate do Ollama com streaming e concatena as respostas.
    Retorna a resposta final como string.
    """
    url = f"{OLLAMA_HOST}/api/generate"
    payload = {
        "model": model_name,
        "prompt": instruction,
        # temperature baixa para respostas mais “coladas” ao documento
        "options": {"temperature": 0.2},
        # stream=True faz o servidor enviar pedaços incrementais
        "stream": True,
    }

    try:
        with requests.post(url, json=payload, stream=True, timeout=120) as r:
            r.raise_for_status()
            result_parts = []
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                # Cada linha é um JSON com o campo "response" (ou "done": true)
                try:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        result_parts.append(chunk["response"])
                except json.JSONDecodeError:
                    # Em casos raros, pode vir algo não-JSON; ignoramos
                    continue
            return "".join(result_parts).strip()
    except requests.exceptions.RequestException as exc:
        print(f"[ERRO] Falha ao gerar resposta com o modelo '{model_name}': {exc}")
        sys.exit(1)


def main() -> None:
    print("\n=== Analisador de docs simples com Ollama ===")

    # 1) Servidor ativo?
    check_server()

    # 2) Modelos locais
    models = list_local_models()
    model_name = choose_model(models)
    print(f"\n[OK] Modelo selecionado: {model_name}")

    # 3) Arquivo de texto
    path = ask_file_path()
    doc_text = read_text_file(path)
    print(f"[OK] Arquivo lido: {path} ({len(doc_text)} caracteres)")

    # 4) Prompt do usuário
    user_prompt = ask_user_prompt()

    # 5) Monta instrução e gera resposta
    instruction = build_instruction(user_prompt, doc_text)
    print("\n[INFO] Gerando resposta... (isso pode levar alguns segundos)\n")
    answer = generate_with_ollama(model_name, instruction)

    print("\n=== RESPOSTA DO MODELO ===\n")
    print(answer)
    print("\n===========================\n")


if __name__ == "__main__":
    main()
