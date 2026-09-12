# State — ModoColetando, ModoAguardandoVerificacao — enunciado, Seção 2.3.
#
# Herde de `ModoOperacao` (modos_base.py — ABC com registro automático):
#
#   from celular_robo.modos_base import ModoOperacao
#
# TODO: implemente aqui. A transição ModoColetando -> ModoAguardandoVerificacao
# acontece via Observer (não é o próprio modo que decide sozinho), quando a
# bandeja completa.

from celular_robo.modos_base import ModoOperacao
from celular_robo.observadores_base import Observador
from celular_robo.robo import Bandeja

class ModoColetando(ModoOperacao):
   
    def mover(self, robo):
        return robo.estrategia.mover(robo)


class ModoAguardandoVerificacao(ModoOperacao):
   

    def mover(self, robo): # type: ignore
        print(f"{robo.nome} aguarda verificação da equipe de testes — não pode coletar agora.")
        return False

    def aprovar(self, robo):
       
        robo.bandeja = Bandeja()
        robo.notificar("retirada_aprovada")
        robo.modo = ModoColetando()

    def rejeitar(self, robo):
        robo.notificar("pedido_rejeitado")
        robo.modo = ModoColetando()


class MonitorColeta(Observador):

    def atualizar(self, evento, **dados):
        if evento == "bandeja_pronta":
            dados["robo"].modo = ModoAguardandoVerificacao()
