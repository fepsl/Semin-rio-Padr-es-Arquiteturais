"""Execute: python app.py. Demonstração automática: python app.py --demo."""

import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from estoque import criar_evento, reconstruir_saldo
from event_store import ler_eventos, salvar_evento


ARQUIVO = Path(__file__).with_name("eventos.jsonl")


def registrar(caminho, tipo, quantidade):
    eventos = ler_eventos(caminho)
    saldo = reconstruir_saldo(eventos)
    evento = criar_evento(tipo, quantidade, saldo)
    salvar_evento(caminho, evento)


def mostrar_historico(caminho):
    eventos = ler_eventos(caminho)
    if not eventos:
        print("Nenhum evento registrado.")
    for numero, evento in enumerate(eventos, start=1):
        print(f'{numero}. {evento["tipo"]}: {evento["quantidade"]}')


def demonstrar():
    # A demonstração usa um arquivo temporário e não altera o estoque do menu.
    with TemporaryDirectory() as pasta:
        caminho = Path(pasta) / "eventos.jsonl"
        registrar(caminho, "EntradaRegistrada", 10)
        print("Entrada de 10 registrada.")
        registrar(caminho, "SaidaRegistrada", 3)
        print("Saída de 3 registrada.")
        mostrar_historico(caminho)
        print("Saldo reconstruído:", reconstruir_saldo(ler_eventos(caminho)))
        try:
            registrar(caminho, "SaidaRegistrada", 100)
        except ValueError as erro:
            print("Saída de 100 rejeitada:", erro)
        print("Total de eventos salvos:", len(ler_eventos(caminho)))


def executar_menu():
    print("CONTROLE DE ESTOQUE: CADERNOS")
    while True:
        print("\n1 - Entrada\n2 - Saída\n3 - Histórico\n4 - Reconstruir saldo\n0 - Sair")
        opcao = input("Escolha: ").strip()
        if opcao == "0":
            break
        try:
            if opcao in ("1", "2"):
                quantidade = int(input("Quantidade: "))
                tipo = "EntradaRegistrada" if opcao == "1" else "SaidaRegistrada"
                registrar(ARQUIVO, tipo, quantidade)
                print("Evento salvo.")
            elif opcao == "3":
                mostrar_historico(ARQUIVO)
            elif opcao == "4":
                print("Saldo reconstruído:", reconstruir_saldo(ler_eventos(ARQUIVO)))
            else:
                print("Opção inválida.")
        except ValueError as erro:
            print("Erro:", erro)


if __name__ == "__main__":
    if sys.argv[1:] == ["--demo"]:
        demonstrar()
    elif sys.argv[1:]:
        print("Uso: python app.py [--demo]")
        raise SystemExit(2)
    else:
        executar_menu()
