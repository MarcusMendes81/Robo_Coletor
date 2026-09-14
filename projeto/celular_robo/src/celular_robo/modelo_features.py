# TODO: implemente aqui. TIPOS_VALIDOS, ESTRATEGIAS_VALIDAS (derivados dos
# registros de Seção 2.2, não digitados à mão), REQUER/EXCLUI (4 dimensões: tipo,
# estratégia, área, urgência) e validar_configuracao levantando
# ConfiguracaoInvalida antes de qualquer robô ser instanciado.
# Modelo de features / LPS — enunciado, Seção 2.4.

from celular_robo.robo_base import Robo
from celular_robo import robo as _robo
from celular_robo.estrategias import RotaColeta
from celular_robo.excecoes import ConfiguracaoInvalida


TIPOS_VALIDOS = set(Robo._registro)
ESTRATEGIAS_VALIDAS = set(RotaColeta._registro_rotas)


AREAS_VALIDAS = {
    "centro_padrao": set(),
    "area_quarentena": {(5, 5), (5, 6), (5, 7), (5, 8)},
}

EXCLUI = {
    ("area", "area_quarentena"): {("estrategia", "direta")},
}


REQUER = {
    ("item", "fragil"): {("estrategia", "dupla_conferencia")},
    ("item", "urgente"): {("estrategia", "direta")},
}


def validar_configuracao(tipo_nome, estrategia_nome, area_nome=None):
   
    if tipo_nome not in TIPOS_VALIDOS:
        raise ConfiguracaoInvalida(
            f"tipo de robô inválido: {tipo_nome!r}. Válidos: {sorted(TIPOS_VALIDOS)}"
        )
    if estrategia_nome not in ESTRATEGIAS_VALIDAS:
        raise ConfiguracaoInvalida(
            f"estratégia inválida: {estrategia_nome!r}. Válidas: {sorted(ESTRATEGIAS_VALIDAS)}"
        )
    if area_nome is not None and area_nome not in AREAS_VALIDAS:
        raise ConfiguracaoInvalida(
            f"área inválida: {area_nome!r}. Válidas: {sorted(AREAS_VALIDAS)}"
        )

    if area_nome is not None:
        proibidos = EXCLUI.get(("area", area_nome), set())
        if ("estrategia", estrategia_nome) in proibidos:
            raise ConfiguracaoInvalida(
                f"área {area_nome!r} exclui a estratégia {estrategia_nome!r}"
            )
