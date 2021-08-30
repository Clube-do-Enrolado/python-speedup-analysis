import Utils
import datetime
import concurrent.futures
from time import perf_counter_ns

def create_threads(data,qtdThread):
    """
    Função que cria uma quantidade dada de threads para
    analisar os 250000 números dados.

    Parameters:
    data(list): Lista indexada através de .map com os números
    que foram lidos do arquivo .csv

    qtdThread(int): Número de threads desejada para teste paralelo.

    Returns:
    (int): Quantidade de primos identificados por todas as threads.
    """
    list_size = len(data)

    # Retorna um objeto range, o qual pode ser acessado na notação de índice
    # [0]: primeiro índice
    # [1]: segundo índice considerando o 
    #      próximo índice com base no passo do range
    index = range(0, list_size+(list_size//qtdThread), list_size//qtdThread)

    primos = 0

    # Executa as chamadas da função (countPrimes) de maneira assíncrona
    # o executor encapsula a chamada assíncrona.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        chamadas = []
        for i in range(qtdThread):
            # Salva em uma lista de objetos Future (threads) o "agendamento"
            # da execução da função countPrimes e passa como parâmetro os números
            # que cada thread irá analisar, ou seja, corta a lista original em 
            # vários pedaços para cada thread.
            chamadas.append(executor.submit(Utils.countPrimes, numbers=data[index[i]:index[i+1]]))

        # Aguarda o término das funções assíncronas e une os resultados.
        for chamada in concurrent.futures.as_completed(chamadas):
            primos += chamada.result()

    return primos


def results(data,qtdThread):
    """
    Função que adquire o tempo de execução (relatório)
    ao identificar números primos através de threads
    com o módulo concurrent.futures.

    Parameters:
    data(list): Lista indexada através de .map com os números
    que foram lidos do arquivo .csv

    qtdThread(int): Número de threads desejada para teste paralelo.

    Returns:
    (dictionary): Dicionário contendo:
    - número de primos lidos
    - o tempo de execução em segundos
    - o tempo de execução milissegundos.

    """
    start = datetime.datetime.now()
    start1 = perf_counter_ns()
    prime = create_threads(data,qtdThread)
    finish = datetime.datetime.now()
    finish1 = perf_counter_ns()

    diff_time = finish - start
    
    results = {
        'threads':qtdThread,
        'primes':prime,
        'time_in_secs':(finish - start).total_seconds(),
        'time_in_ms':(finish1 - start1)/1000000
    }

    return results
