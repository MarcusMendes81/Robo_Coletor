# Fixtures compartilhadas entre seus test_*.py — TODO, à sua escolha.
# (A fixture usada por test_00_fornecido.py já vem definida nele mesmo —
# não precisa duplicar aqui.)

import pytest

from celular_robo.fabrica import criar_robo_configurado
from celular_robo.modos import ModoColetando
from celular_robo.robo import RoboColetor

@pytest.fixture
def config_robo():

    def criar_robo(estrategia_nome="direta", area_nome="centro_padrao", **kwargs):
        kwargs.setdefault("modo", ModoColetando())
        return criar_robo_configurado("RoboColetor", "Coletor-Teste", estrategia_nome=estrategia_nome, area_nome=area_nome,**kwargs)

    return criar_robo