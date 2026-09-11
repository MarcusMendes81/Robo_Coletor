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


class ModoColetando(ModoOperacao):
    def mover(self, robo):
        comando = getattr(robo, "_comando_atual", None)
        return robo.estrategia.mover(robo, comando)

    def iniciar_coleta(self, robo, comando):
        robo._comando_atual = comando
        try:
            return self.mover(robo)
        finally:
            robo.__dict__.pop("_comando_atual", None)


class ModoAguardarVerificacao(ModoOperacao):
    def mover(self, robo):
        print(f"{robo.nome} aguarda a verificação da equipe de testes.")
        return False

    def iniciar_coleta(self, robo, comando):
        raise RuntimeError("não é possível iniciar nova coleta antes da aprovação da bandeja")
