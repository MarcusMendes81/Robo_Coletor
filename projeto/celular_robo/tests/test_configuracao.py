# TODO: seus testes de configuração/LPS — enunciado, Seção 2.7 (pytest.raises,
# @pytest.mark.parametrize cobrindo estratégia×área).

import pytest
from celular_robo.excecoes import ConfiguracaoInvalida
from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modelo_features import AREAS_VALIDAS, ESTRATEGIAS_VALIDAS, TIPOS_VALIDOS


def test_tipos_validos_contem_robocoletor():
    assert "RoboColetor" in TIPOS_VALIDOS


def test_estrategias_validas_contem_direta_e_dupla_conferencia():
    assert {"direta", "dupla_conferencia"} <= ESTRATEGIAS_VALIDAS


def test_areas_validas_contem_centro_padrao_e_area_quarentena():
    assert {"centro_padrao", "area_quarentena"} <= set(AREAS_VALIDAS)


def test_tipo_invalido_levanta_configuracao_invalida():
    with pytest.raises(ConfiguracaoInvalida):
        criar_robo_configurado("RoboFantasma", "X", estrategia_nome="direta")


def test_estrategia_invalida_levanta_configuracao_invalida():
    with pytest.raises(ConfiguracaoInvalida):
        criar_robo_configurado("RoboColetor", "X", estrategia_nome="voadora")


def test_area_invalida_levanta_configuracao_invalida():
    with pytest.raises(ConfiguracaoInvalida):
        criar_robo_configurado(
            "RoboColetor", "X", estrategia_nome="direta", area_nome="lua"
        )