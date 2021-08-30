import sympy

def read_data(filename):
    """Lê os dados do arquivo indicado.

    Parameters:
    filename(string): Nome do arquivo com extensão.

    Returns:
    list: Dados lidos e indexados em tupla por um index e pelo valor
    do arquivo, como um dicionário.
    """
    with open(filename) as file:
        # Salva os dados .csv em uma lista retirando todos os
        # espaços para cada linha do arquivo.
        data = [line.strip() for line in file]
        # Conversão necessária para classificação do sympy.isprime
        data = list(map(int, data))

    return data

def countPrimes(numbers):
    """
    Método para contar a quantidade de números primos identificados.
    
    Parameters:
    numbers(list): Lista de tuplas indexadas com os valores lidos
    da base .csv.

    Returns:
    int: Número de primos identificados.
    """
    primos = 0
    for i in range(len(numbers)):
        if sympy.isprime(numbers[i]):
            primos += 1
    return primos
