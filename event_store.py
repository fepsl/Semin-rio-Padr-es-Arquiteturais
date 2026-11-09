"""Guarda e lê os eventos. Cada linha do arquivo representa um evento."""

import json
from pathlib import Path


def ler_eventos(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        return []
    with caminho.open(encoding="utf-8") as arquivo:
        return [json.loads(linha) for linha in arquivo if linha.strip()]


def salvar_evento(caminho, evento):
    # O modo "a" acrescenta uma linha, preservando os eventos anteriores.
    with Path(caminho).open("a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(evento, ensure_ascii=False) + "\n")
