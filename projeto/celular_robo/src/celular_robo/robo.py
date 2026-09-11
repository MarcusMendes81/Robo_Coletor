# RoboColetor + QuantidadeValida — enunciado, Seção 2.1.
#
# `Robo` (posição, __init_subclass__/_registro, avancar/girar, estrategia/modo,
# Observer) já vem pronto em robo_base.py — não precisa reescrever, só importar:
#
#   from celular_robo.robo_base import Robo, Coordenada
#
# TODO: implemente aqui.
# - RoboColetor(Robo): reaproveita Coordenada (x, y) por herança — não precisa
#   redeclarar. Adicione o que for específico da coleta (ex.: bandeja).
# - QuantidadeValida: descriptor novo (mesmo protocolo de Coordenada/Percentual
#   em robo_base.py), validando que a quantidade coletada de um item nunca é
#   negativa nem passa do pedido.
# - __str__/__repr__ (robô) e __len__ (bandeja — quantos itens já coletados).

from celular_robo.modos import ModoColetando
from celular_robo.robo_base import Robo
from celular_robo.excecoes import PedidoInvalido
from celular_robo.excecoes import PedidoInvalido


class QuantidadeValida:

    def __set_name__(self, owner, name):
        self.nome = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.nome, 0)

    def __set__(self, instance, valor):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise TypeError("quantidade precisa ser um inteiro")
        if valor < 0:
            raise ValueError("quantidade não pode ser negativa")
        codinome = getattr(instance, "_item_em_validacao", None)
        limite = getattr(instance, "_limite_total", None)
        if limite is not None and valor > limite:
            raise ValueError(
                f"quantidade coletada excede o total do pedido ({limite})"
            )
        instance.__dict__[self.nome] = valor

        
class RoboColetor(Robo):
    quantidade_coletada = QuantidadeValida()

    def __init__(self, nome, **kwargs):
        catalogo = kwargs.pop("catalogo", None)
        super().__init__(nome, **kwargs)
        self.bandeja = {}
        self.modo = ModoColetando()
        self.pedido = None
        self._limites_quantidade = {}
        self._limite_total = None
        self._item_em_validacao = None
        self._historico_coleta = []
        self._aprovado = False
        self.catalogo = catalogo

    def carregar_pedido(self, pedido):
        if self.catalogo is not None:
            desconhecidos = {item.codinome for item in pedido.itens} - set(self.catalogo)
            if desconhecidos:
                raise PedidoInvalido(f"codinome não encontrado: {sorted(desconhecidos)}")
        estrategia_nome = type(self.estrategia).__name__
        for item in pedido.itens:
            if item.fragil and estrategia_nome != "RotaComDuplaConferencia":
                raise PedidoInvalido(f"item frágil exige dupla conferência: {item.codinome!r}")
            if item.urgente and estrategia_nome != "RotaDireta":
                raise PedidoInvalido(f"item urgente exige rota direta: {item.codinome!r}")
        self.pedido = pedido
        self._limites_quantidade = {
            item.codinome: item.quantidade for item in pedido.itens
        }
        self._limite_total = sum(self._limites_quantidade.values())
        self.bandeja.clear()
        self.quantidade_coletada = 0
        self._aprovado = False

    def quantidade_do_item(self, codinome):
        return self.bandeja.get(codinome, 0)

    def adicionar_na_bandeja(self, codinome, quantidade):
        limite = self._limites_quantidade.get(codinome)
        if limite is None:
            raise ValueError(f"item não pertence ao pedido: {codinome!r}")
        atual = self.bandeja.get(codinome, 0)
        nova = atual + quantidade
        self._item_em_validacao = codinome
        try:
            self.quantidade_coletada = nova
        finally:
            self._item_em_validacao = None
        self.bandeja[codinome] = nova
        self._historico_coleta.append((codinome, quantidade))