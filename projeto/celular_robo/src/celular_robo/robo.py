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
from celular_robo.comandos import ComandoColeta
from celular_robo.excecoes import PedidoInvalido
from celular_robo.modelo_features import REQUER
from celular_robo.persistencia import validar_pedido


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

    def processar_pedido(self, pedido):
    
        validar_pedido(pedido)

        itens = pedido["itens"]
        for item in itens:
            for flag in ("fragil", "urgente"):
                if not item.get(flag):
                    continue
                exigido = REQUER.get(("item", flag), set())
                if exigido and ("estrategia", self.estrategia.apelido) not in exigido:
                    exigidas = sorted(valor for _, valor in exigido)
                    raise PedidoInvalido(
                        f"item {item['codinome']!r} tem {flag}=True, que exige "
                        f"estratégia {exigidas} — robô está configurado com "
                        f"{self.estrategia.apelido!r}"
                    )

        for item in itens:
            comando = ComandoColeta(item["codinome"], tuple(item["posicao"]), item["quantidade"])
            self.executar_comando(comando)

        completo = all(
            self.bandeja.quantidade_de(item["codinome"]) >= item["quantidade"]
            for item in itens
        )
        if completo:
            self.notificar("bandeja_pronta", lote=pedido.get("lote"))
        return completo

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
