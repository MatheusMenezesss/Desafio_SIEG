import re
"""
   funcoes para padronizar os dados
"""

def parse_valor(valor_str: str) -> float:
    """
    Converte uma string de valor monetário em um float.
    Exemplo: "1.234,56" -> 1234.56
    """
    valor_str = valor_str.strip().replace('.', '').replace(',', '.')
    try:
        return float(valor_str)
    except ValueError:
        raise ValueError(f"Valor inválido: {valor_str}")
    

def parse_chave(chave_str: str) -> str:
    """
    Valida e retorna a chave como uma string.
    A chave deve ter exatamente 44 caracteres.
    """
    chave_str = re.sub(r'\D', '', chave_str)
    if len(chave_str) != 44:
        raise ValueError(f"Chave inválida: {chave_str}. Deve ter exatamente 44 caracteres.")
    return chave_str