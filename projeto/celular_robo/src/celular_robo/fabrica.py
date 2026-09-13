# Factory — criar_robo_coletor, criar_robo_configurado — enunciado, Seção 2.3.
# (Ver fabrica_base.py — genérico do curso, não editar: criar_robo("RoboColetor",
# ...) já funciona, pode chamar direto ou usar como modelo.)
#
# TODO: implemente aqui. criar_robo_coletor(tipo_nome, ...) a partir do
# _registro (Seção 2.2); criar_robo_configurado combina isso com a validação do
# modelo de features (Seção 2.4).
#
# Contrato mínimo exigido por tests/test_00_fornecido.py (não altere a
# assinatura abaixo sem também atualizar aquele arquivo):
#
#   criar_robo_configurado(tipo_nome, nome, estrategia_nome=..., area_nome=...)
from celular_robo.fabrica_base import criar_robo
from celular_robo.modelo_features import validar_configuracao, AREAS_VALIDAS
from celular_robo.estrategias import RotaColeta


def criar_robo_coletor(tipo_nome, nome, **kwargs):
 
    return criar_robo(tipo_nome, nome, **kwargs)


def criar_robo_configurado(tipo_nome, nome, estrategia_nome, area_nome=None, **kwargs):
 
    validar_configuracao(tipo_nome, estrategia_nome, area_nome=area_nome)

    estrategia_cls = RotaColeta._registro_rotas[estrategia_nome]
    kwargs.setdefault("estrategia", estrategia_cls())
    if area_nome is not None:
      
        kwargs.setdefault("obstaculos", set(AREAS_VALIDAS[area_nome]))
    return criar_robo_coletor(tipo_nome, nome, **kwargs)
