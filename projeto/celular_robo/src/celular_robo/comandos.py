# Command — ComandoColeta — enunciado, Seção 2.3.
#
# Herde de `Comando` (comandos_base.py — ABC com registro automático):
#
#   from celular_robo.comandos_base import Comando
#
# TODO: implemente aqui. ComandoColeta(Comando): __init__(codinome, posicao,
# quantidade), com .executar(robo) e .desfazer(robo) (remove o item da
# bandeja, decrementa a contagem coletada).

from celular_robo.comandos_base import Comando


class ComandoColeta(Comando):
    def __init__(self, codinome, posicao, quantidade, fragil=False, urgente=False):
        self.codinome = codinome
        self.posicao = tuple(posicao)
        self.quantidade = quantidade
        self.fragil = bool(fragil)
        self.urgente = bool(urgente)
        self._executado = 0

    def executar(self, robo): # type: ignore
        if not getattr(robo, "pedido", None):
            raise ValueError("robô não possui pedido carregado")
        if not isinstance(robo.modo, __import__("celular_robo.modos", fromlist=["ModoColetando"]).ModoColetando):
            raise RuntimeError("robô não está no modo de coleta")
        robo._comando_atual = self
        try:
            robo.estrategia.mover(robo, self)
            robo.adicionar_na_bandeja(self.codinome, self.quantidade)
            self._executado = self.quantidade
            robo.notificar(
                "coleta",
                codinome=self.codinome,
                quantidade=self.quantidade,
                posicao=self.posicao,
            )
            if robo.bandeja_completa():
                robo.notificar("bandeja_pronta", pedido=robo.pedido)
            return True
        finally:
            robo.__dict__.pop("_comando_atual", None)

    def desfazer(self, robo):
        if self._executado <= 0:
            return False
        robo.remover_da_bandeja(self.codinome, self._executado)
        robo.notificar(
            "coleta_desfeita",
            codinome=self.codinome,
            quantidade=self._executado,
        )
        self._executado = 0
        return True

    def __repr__(self):
        return f"ComandoColeta({self.codinome!r}, {self.posicao!r}, {self.quantidade})"
