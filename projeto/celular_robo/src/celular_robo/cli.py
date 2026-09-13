# CLI — enunciado, Seção 4.
#
# TODO: implemente aqui. Menu interativo (ou argparse, à sua escolha):
# listar pedido carregado, processar pedido, ver estado da bandeja,
# aprovar/rejeitar retirada da equipe de testes.

from celular_robo.persistencia import montar_robo_de_config, montar_pedido_de_json, processar_pedido
from celular_robo.observadores import RegistroAuditoria,  EquipeDeTestes
from celular_robo.modos import MonitorColeta, ModoAguardandoVerificacao
from celular_robo.excecoes import ErroColeta

CONFIG_PADRAO = "dados/robo_padrao.json"
PEDIDO_PADRAO = "dados/pedido_exemplo.json"

MENU = """
=== Robô Coletor — {nome} ===
1) Listar pedido carregado
2) Processar pedido
3) Ver estado da bandeja
4) Aprovar retirada (equipe de testes)
5) Rejeitar retirada (equipe de testes)
6) Carregar outro pedido (JSON)
0) Sair
"""


def _montar_robo(caminho_config):
    import json

    with open(caminho_config, encoding="utf-8") as arquivo:
        config = json.load(arquivo)
    robo = montar_robo_de_config(config)
    robo._equipe_testes = EquipeDeTestes()
    robo.adicionar_observador(robo._equipe_testes)
    robo.adicionar_observador(RegistroAuditoria())
    robo.adicionar_observador(MonitorColeta())
    return robo


def _listar_pedido(pedido):
    if pedido is None:
        print("Nenhum pedido carregado.")
        return
    print(f"Lote: {pedido.get('lote', '(sem nome)')}")
    for item in pedido["itens"]:
        flags = []
        if item.get("fragil"):
            flags.append("frágil")
        if item.get("urgente"):
            flags.append("urgente")
        flags_txt = f" [{', '.join(flags)}]" if flags else ""
        print(
            f"  - {item['codinome']}: {item['quantidade']} unidade(s) "
            f"em {tuple(item['posicao'])}{flags_txt}"
        )


def _processar_pedido(robo, pedido):
    if pedido is None:
        print("Nenhum pedido carregado — use a opção 6 primeiro.")
        return
    try:
        completo = processar_pedido(robo, pedido)
    except ErroColeta as erro:
        print(f"Pedido rejeitado: {erro}")
        return
    if completo:
        print("Pedido processado com sucesso — bandeja completa, aguardando verificação.")
    else:
        print("Pedido processado, mas a bandeja não ficou completa (algum item bloqueado).")


def _ver_bandeja(robo):
    print(robo)
    print(f"Modo atual: {type(robo.modo).__name__}")


def _aprovar(robo):
    if not isinstance(robo.modo, ModoAguardandoVerificacao):
        print("Não há retirada pendente de aprovação no momento.")
        return
    robo.modo.aprovar(robo)
    print("Retirada aprovada — bandeja esvaziada, robô livre pra um pedido novo.")


def _rejeitar(robo):
    if not isinstance(robo.modo, ModoAguardandoVerificacao):
        print("Não há retirada pendente de rejeição no momento.")
        return
    robo.modo.rejeitar(robo)
    print("Retirada rejeitada — robô volta a coletar o MESMO pedido (bandeja intacta).")


def main():
    robo = _montar_robo(CONFIG_PADRAO)
    try:
        pedido = montar_pedido_de_json(PEDIDO_PADRAO)
    except (ErroColeta, FileNotFoundError):
        pedido = None

    while True:
        print(MENU.format(nome=robo.nome))
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            _listar_pedido(pedido)
        elif escolha == "2":
            _processar_pedido(robo, pedido)
        elif escolha == "3":
            _ver_bandeja(robo)
        elif escolha == "4":
            _aprovar(robo)
        elif escolha == "5":
            _rejeitar(robo)
        elif escolha == "6":
            caminho = input(f"Caminho do JSON do pedido [{PEDIDO_PADRAO}]: ").strip()
            caminho = caminho or PEDIDO_PADRAO
            try:
                pedido = montar_pedido_de_json(caminho)
                print("Pedido carregado.")
            except ErroColeta as erro:
                print(f"Não foi possível carregar o pedido: {erro}")
            except FileNotFoundError:
                print(f"Arquivo não encontrado: {caminho}")
        elif escolha == "0":
            print("Até mais!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
