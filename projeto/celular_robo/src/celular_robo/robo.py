# RoboColetor + Bandeja + QuantidadeValida — enunciado, Seção 2.1.
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

from celular_robo.robo_base import Robo

class Bandeja:
   

    def __init__(self):
        self._itens = {}

    def __len__(self):
        return sum(self._itens.values())

    def __iter__(self):
        return iter(self._itens.items())

    def __contains__(self, codinome):
        return codinome in self._itens

    def __repr__(self):
        return f"Bandeja({dict(self._itens)!r})"

    def quantidade_de(self, codinome):
        
        return self._itens.get(codinome, 0)

    def adicionar(self, codinome, quantidade):
        
        self._itens[codinome] = self._itens.get(codinome, 0) + quantidade

    def remover(self, codinome, quantidade):
        
        atual = self._itens.get(codinome, 0)
        nova = atual - quantidade
        if nova <= 0:
            self._itens.pop(codinome, None)
        else:
            self._itens[codinome] = nova


class RoboColetor(Robo):
   

    def __init__(self, nome, **kwargs):
        super().__init__(nome, **kwargs)
        self.bandeja = Bandeja()
        self.historico_coleta = []

    def executar_comando(self, comando):
       
        sucesso = comando.executar(self)
        if sucesso:
            self.historico_coleta.append(comando)
        return sucesso

    def desfazer_ultimo(self):
       
        if not self.historico_coleta:
            return False
        comando = self.historico_coleta.pop()
        comando.desfazer(self)
        return True

    
    def __repr__(self):
        return (
            f"RoboColetor({self.nome!r}, x={self.x}, y={self.y}, "
            f"coletados={len(self.bandeja)})"
        )

    def __str__(self):
        return (
            f"{self.nome} em ({self.x}, {self.y}) — "
            f"{len(self.bandeja)} unidade(s) na bandeja"
        )
