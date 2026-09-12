# Strategy — RotaDireta, RotaComDuplaConferencia — enunciado, Seção 2.3.
# (Não confundir com estrategias_base.py — genérico do curso, não editar. Ao
# contrário de Command/Observer/State, aqui você NÃO herda de `Estrategia`:
# escreva sua própria base, ver TODO abaixo — motivo em estrategias_base.py.)
#
# TODO: implemente aqui. Considere uma base comum (RotaColeta) com
# __init_subclass__ registrando cada rota, ver Seção 2.2 (metaprogramação
# aplicada a uma segunda hierarquia).

from abc import ABC, abstractmethod

from celular_robo.robo_base import Direcao


class RotaColeta(ABC):
    _registro_rotas = {}

    def __init_subclass__(cls, apelido=None, **kwargs):
        super().__init_subclass__(**kwargs)
        chave = apelido or cls.__name__
        RotaColeta._registro_rotas[chave] = cls
        cls.apelido = chave

    @abstractmethod
    def mover_ate(self, robo, posicao):
        ...

    @abstractmethod
    def confirmar_coleta(self, robo, codinome):
        ...

    def mover(self, robo):
        return robo.avancar()


def _navegar_ate(robo, destino):
    
    tx, ty = destino
    if tx != robo.x:
        robo.girar_ate(Direcao.LESTE if tx > robo.x else Direcao.OESTE)
        robo.avancar_n(abs(tx - robo.x))
    if ty != robo.y:
        robo.girar_ate(Direcao.NORTE if ty > robo.y else Direcao.SUL)
        robo.avancar_n(abs(ty - robo.y))
    return (robo.x, robo.y) == destino


class RotaDireta(RotaColeta, apelido="direta"):

    def mover_ate(self, robo, posicao):
        return _navegar_ate(robo, posicao)

    def confirmar_coleta(self, robo, codinome):
        return True


class RotaComDuplaConferencia(RotaColeta, apelido="dupla_conferencia"):
   

    def mover_ate(self, robo, posicao):
        return _navegar_ate(robo, posicao)

    def confirmar_coleta(self, robo, codinome):
        return self._revalidar(robo, codinome) and self._revalidar(robo, codinome)

    def _revalidar(self, robo, codinome):
        print(f"[dupla conferência] revalidando {codinome!r} em {robo.posicao}...")
        return True
