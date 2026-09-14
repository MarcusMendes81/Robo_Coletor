# TODO: teste da transição ModoColetando -> ModoAguardandoVerificacao
# disparada pelo Observer quando a bandeja completa — enunciado, Seção 2.7.


import pytest

from celular_robo.modos import ModoAguardandoVerificacao, ModoColetando, MonitorColeta
from celular_robo.observadores import EquipeDeTestes, RegistroAuditoria
from celular_robo.persistencia import processar_pedido


@pytest.fixture
def robo_pronto_pra_coletar(config_robo):
    robo = config_robo(estrategia_nome="direta")
    robo.adicionar_observador(MonitorColeta())
    return robo


def test_robo_comeca_em_modo_coletando(robo_pronto_pra_coletar):
    assert isinstance(robo_pronto_pra_coletar.modo, ModoColetando)


def test_bandeja_completa_dispara_transicao_para_aguardando_verificacao(
    robo_pronto_pra_coletar,
):
    pedido = {
        "lote": "Lote de teste",
        "itens": [{"codinome": "Projeto Kannon", "posicao": (3, 4), "quantidade": 2}],
    }
    completo = processar_pedido(robo_pronto_pra_coletar, pedido)
    assert completo is True
    assert isinstance(robo_pronto_pra_coletar.modo, ModoAguardandoVerificacao)