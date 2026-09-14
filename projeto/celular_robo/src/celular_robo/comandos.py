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


class QuantidadeValida:
    

    def __init__(self, limite_attr):
        self.limite_attr = limite_attr

    def __set_name__(self, owner, name):
        self.nome_publico = name
        self.nome = "_" + name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.nome, 0)

    def __set__(self, instance, valor):
        if valor < 0:
            raise ValueError(f"{self.nome_publico}={valor} não pode ser negativo")
        limite = getattr(instance, self.limite_attr, None)
        if limite is not None and valor > limite:
            raise ValueError(
                f"{self.nome_publico}={valor} excede a quantidade pedida ({limite})"
            )
        instance.__dict__[self.nome] = valor


class ComandoColeta(Comando):
   

    quantidade_coletada = QuantidadeValida(limite_attr="quantidade")

    def __init__(self, codinome, posicao, quantidade):
        self.codinome = codinome
        self.posicao = tuple(posicao)
        self.quantidade = quantidade
        self.quantidade_coletada = 0


    def executar(self, robo):
        chegou = robo.estrategia.mover_ate(robo, self.posicao)
        if not chegou:
            robo.notificar("coleta_falhou", codinome=self.codinome, motivo="obstaculo")
            return False

        if not robo.estrategia.confirmar_coleta(robo, self.codinome):
            robo.notificar("coleta_falhou", codinome=self.codinome, motivo="revalidacao")
            return False

        robo.bandeja.adicionar(self.codinome, self.quantidade)
        self.quantidade_coletada = self.quantidade
        robo.notificar("item_coletado", codinome=self.codinome, quantidade=self.quantidade)
        return True

    def desfazer(self, robo):
        """Remove o item da bandeja e decrementa a contagem coletada."""
        robo.bandeja.remover(self.codinome, self.quantidade_coletada)
        robo.notificar(
            "coleta_desfeita", codinome=self.codinome, quantidade=self.quantidade_coletada
        )
        self.quantidade_coletada = 0

    def __repr__(self):
        return (
            f"ComandoColeta({self.codinome!r}, posicao={self.posicao}, "
            f"quantidade={self.quantidade}, coletada={self.quantidade_coletada})"
        )