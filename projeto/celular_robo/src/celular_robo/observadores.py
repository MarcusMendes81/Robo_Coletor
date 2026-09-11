# Observer — EquipeDeTestes, RegistroAuditoria — enunciado, Seção 2.3.
#
# Herde de `Observador` (observadores_base.py — ABC com registro automático):
#
#   from celular_robo.observadores_base import Observador
#
# TODO: implemente aqui. EquipeDeTestes(Observador) reage a "bandeja_pronta";
# RegistroAuditoria(Observador) loga todo evento (coleta, bandeja pronta,
# pedido rejeitado), pensando em trilha de auditoria, não só depuração.
from abc import ABC, abstractmethod

from celular_robo.observadores_base import Observador




class AlertaBateria(Observador):
    def atualizar(self, evento, **dados):
        if evento == "bateria_critica":
            print(f"[ALERTA] bateria crítica: {dados['nivel']}%")


class RegistroEventos(Observador):
    def __init__(self):
        self.eventos = []

    def atualizar(self, evento, **dados):
        self.eventos.append((evento, dados))
