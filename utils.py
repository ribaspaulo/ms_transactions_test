from functools import partial
import shutil

def change_column(matrix, column, function):
    """
    Modifica os valores de uma coluna em uma matriz.

    Args:
        matrix: A matriz a ser modificada.
        column: O índice da coluna a ser modificada.
        function: Uma função que recebe um valor antigo e retorna o novo valor.
    """
    for row in matrix:
        row[column] = function(row[column])

def value_switch(matrix: list, value_column: int, new_value_column: int, value: str):
    """
    Identifica o índice de um valor na matriz, considerando sua coluna e retorna o valor de outra coluna conforme o índice.

    Args:
        matrix: A matriz a ser pesquisada.
        value_column: O índice da coluna onde o valor conhecido se encontra.
        new_value_column: O índice da coluna do valor a ser retornado.
    """
    try:
        return matrix[new_value_column][matrix[value_column].index(value)]
    except:
        return value

def move_file(origin, destiny):
    msg = ""
    try:
        # Move o arquivo da origem para o destino
        shutil.move(origin, destiny)
        msg = f"Arquivo movido com sucesso de {origin} para {destiny}."
    except FileNotFoundError:
        msg = f"Arquivo {origin} não encontrado."
    except IOError:
        msg = f"Erro ao mover o arquivo {destiny}."
    return msg

def del_folder(folder):
    msg = ""
    try:
        # Deleta a pasta temporária
        shutil.rmtree(folder)
        msg = f"A pasta {folder} foi excluída com sucesso."
    except FileNotFoundError:
        msg = f"A pasta {folder} não encontrado."
    except IOError:
        msg = f"Erro ao excluír a pasta {folder}."
    return msg    