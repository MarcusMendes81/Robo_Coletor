# Hierarquia de exceções — enunciado, Seção 2.5.
#
# TODO: implemente aqui. ErroColeta(Exception) como base;
# ConfiguracaoInvalida(ErroColeta) e PedidoInvalido(ErroColeta) como as duas
# subclasses (ver Seção 2.5 pra critério de qual usar em cada caso).
class ErroColeta(Exception):
    """Erro base do domínio de coleta."""


class ConfiguracaoInvalida(ErroColeta):
    """Configuração incompatível de robô, rota ou área."""


class PedidoInvalido(ErroColeta):
    """Pedido com conteúdo inválido."""
