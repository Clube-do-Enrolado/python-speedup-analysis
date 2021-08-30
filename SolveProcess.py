import multiprocessing
import datetime
import Utils
from time import perf_counter_ns

def create_multiprocessing(data, qtdProcess):
    """
    Função que cria uma quantidade dada de processos para
    analisar os 250000 números dados.

    Parameters:
    data(list): Lista indexada através de .map com os números
    que foram lidos do arquivo .csv

    qtdProcess(int): Número de threads desejada para teste paralelo.

    Returns:
    (int): Quantidade de primos identificados por todos os processos.
    """
    

    list_size = len(data)

    # Retorna um objeto range, o qual pode ser acessado na notação de índice
    # [0]: primeiro índice
    # [1]: segundo índice considerando o 
    #      próximo índice com base no passo do range
    index = range(0, list_size+(list_size//qtdProcess), list_size//qtdProcess)

    primos = 0
    processos = []

    for i in range(qtdProcess):
        processos.append(data[index[i]:index[i+1]])

    with multiprocessing.Pool(qtdProcess) as p:
        primos = sum(p.map(Utils.countPrimes,processos))

    return primos

def results(data, qtdProcess):
    """
    Função que adquire o tempo de execução (relatório)
    ao identificar números primos através de múltiplos processos
    com o módulo multiprocessing.

    Parameters:
    data(list): Lista indexada através de .map com os números
    que foram lidos do arquivo .csv

    qtdProcess(int): Número de processos desejados para teste paralelo.

    Returns:
    (dictionary): Dicionário contendo:
    - número de primos lidos
    - o tempo de execução em segundos
    - o tempo de execução milissegundos.
    
    """
    
    start = datetime.datetime.now()
    start1 = perf_counter_ns()
    prime = create_multiprocessing(data,qtdProcess)
    finish = datetime.datetime.now()
    finish1 = perf_counter_ns()

    results = {
        'processes':qtdProcess,
        'primes':prime,
        'time_in_secs':(finish - start).total_seconds(),
        'time_in_ms':(finish1 - start1)/1000000
    }

    return results
