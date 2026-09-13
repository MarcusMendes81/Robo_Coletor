# Configuração e persistência — enunciado, Seção 2.6.
#
# TODO: implemente aqui. montar_robo_de_config(config) e
# montar_pedido_de_json(caminho) — mesmo par de funções do capstone do curso
# (montar_robo_de_config/montar_frota_de_json), adaptado: um arquivo
# configura o robô (tipo, estratégia, área), outro traz o pedido de coleta.
import json
from celular_robo.comandos import ComandoColeta
from celular_robo.fabrica import criar_robo_configurado

from celular_robo.excecoes import ConfiguracaoInvalida, PedidoInvalido
from celular_robo.modelo_features import REQUER

CATALOGO_DISPOSITIVOS = {
    "Projeto Kanon": {"posicao": (3, 4), "estoque": 5},
    "Projeto Dhoko": {"posicao": (7, 2), "estoque": 3},
    "Projeto Shaka": {"posicao": (2, 8), "estoque": 10},
}

def validar_pedido(pedido):
   
    itens = pedido.get("itens", [])
    if not itens:
        raise PedidoInvalido("pedido vazio — nenhum item pra coletar")

    tem_urgente = False
    tem_fragil = False

    for item in itens:
        codinome = item.get("codinome")
        quantidade = item.get("quantidade", 0)
        fragil = bool(item.get("fragil", False))
        urgente = bool(item.get("urgente", False))

        if codinome not in CATALOGO_DISPOSITIVOS:
            raise PedidoInvalido()

        estoque = CATALOGO_DISPOSITIVOS[codinome]["estoque"]
        if quantidade > estoque:
            raise PedidoInvalido()

        if fragil and urgente:
            raise PedidoInvalido(
                f"item {codinome!r} não pode ser frágil e urgente ao mesmo tempo"
            )

        tem_fragil = tem_fragil or fragil
        tem_urgente = tem_urgente or urgente

    if tem_fragil and tem_urgente:
        raise PedidoInvalido()


def montar_robo_de_config(config):
   

    try:
        tipo = config["tipo"]
        nome = config["nome"]
        estrategia_nome = config["estrategia"]
    except KeyError as erro:
        raise ConfiguracaoInvalida(f"chave obrigatória faltando na config: {erro}") from erro

    return criar_robo_configurado(
        tipo, nome, estrategia_nome=estrategia_nome, area_nome=config.get("area")
    )


def montar_pedido_de_json(caminho):
    
    with open(caminho, encoding="utf-8") as arquivo:
        pedido = json.load(arquivo)

    for item in pedido.get("itens", []):
        if "posicao" in item:
            item["posicao"] = tuple(item["posicao"])

    validar_pedido(pedido)
    return pedido

def processar_pedido(robo, pedido):
   
    validar_pedido(pedido)

    itens = pedido["itens"]
    for item in itens:
        for flag in ("fragil", "urgente"):
            if not item.get(flag):
                continue
            exigido = REQUER.get(("item", flag), set())
            if exigido and ("estrategia", robo.estrategia.apelido) not in exigido:
                exigidas = sorted(valor for _, valor in exigido)
                raise PedidoInvalido(
                    f"item {item['codinome']!r} tem {flag}=True, que exige "
                    f"estratégia {exigidas} — robô está configurado com "
                    f"{robo.estrategia.apelido!r}"
                )

    for item in itens:
        comando = ComandoColeta(item["codinome"], tuple(item["posicao"]), item["quantidade"])
        robo.executar_comando(comando)

    completo = all(
        robo.bandeja.quantidade_de(item["codinome"]) >= item["quantidade"] for item in itens
    )
    if completo:
        robo.notificar("bandeja_pronta", lote=pedido.get("lote"))
    return completo
