# Observer — EquipeDeTestes, RegistroAuditoria — enunciado, Seção 2.3.
#
# Herde de `Observador` (observadores_base.py — ABC com registro automático):
#
#   from celular_robo.observadores_base import Observador
#
# TODO: implemente aqui. EquipeDeTestes(Observador) reage a "bandeja_pronta";
# RegistroAuditoria(Observador) loga todo evento (coleta, bandeja pronta,
# pedido rejeitado), pensando em trilha de auditoria, não só depuração.


from celular_robo.observadores_base import Observador

class EquipeDeTestes(Observador):

    def __init__(self):
        self.pendentes = []

    def atualizar(self, evento, **dados):
        if evento == "bandeja_pronta":
            robo = dados.get("robo")
            nome = robo.nome if robo is not None else "?"
            print(f"[EquipeDeTestes] bandeja de {nome} pronta pra retirada.")
            self.pendentes.append(dados)



class RegistroAuditoria(Observador):
    def __init__(self):
        self.eventos = []

    def atualizar(self, evento, **dados):
        self.eventos.append((evento, dados))
