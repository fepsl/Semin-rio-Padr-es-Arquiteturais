"""Regras do estoque e reconstrução do saldo a partir dos eventos."""


def reconstruir_saldo(eventos):
    saldo = 0
    for evento in eventos:
        if evento["tipo"] == "EntradaRegistrada":
            saldo += evento["quantidade"]
        elif evento["tipo"] == "SaidaRegistrada":
            saldo -= evento["quantidade"]
        else:
            raise ValueError("Tipo de evento desconhecido.")
    return saldo


def criar_evento(tipo, quantidade, saldo_atual):
    if tipo not in ("EntradaRegistrada", "SaidaRegistrada"):
        raise ValueError("Tipo de evento desconhecido.")
    if type(quantidade) is not int or quantidade <= 0:
        raise ValueError("A quantidade deve ser um número inteiro positivo.")
    if tipo == "SaidaRegistrada" and quantidade > saldo_atual:
        raise ValueError("Estoque insuficiente.")
    return {"tipo": tipo, "quantidade": quantidade}
