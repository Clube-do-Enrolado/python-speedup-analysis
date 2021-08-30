import datetime
import multiprocessing
from time import perf_counter_ns
import sympy
import concurrent.futures

class SimulationThreads:
  def __init__(self, filename):
    self.data = self.read_data(filename)

  def read_data(self,filename):
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

  def create_threads(self, qtdThread):
    list_size = len(self.data)

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
            chamadas.append(executor.submit(self.countPrimes, numbers=self.data[index[i]:index[i+1]]))

        for chamada in concurrent.futures.as_completed(chamadas):
            primos += chamada.result()

    return primos

  def countPrimes(self,numbers):
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

  def solve_sequential(self):
    print('\nClassificação de %d valores (Sequêncial)\n'%(len(self.data)))
    start = datetime.datetime.now()
    start1 = perf_counter_ns()
    prime = self.countPrimes(self.data)
    finish = datetime.datetime.now()
    finish1 = perf_counter_ns()

    diff_time = finish - start
    print("Primos encontrados: ", prime)
    print("Tempo (em segundos): ",diff_time.total_seconds())
    print("Tempo em ms: ",(finish1-start1)/1000000)

  def solve_threads(self, qtdThread):
    print('\nClassificação de %d valores (Paralelo)\n'%(len(self.data)))
    start = datetime.datetime.now()
    start1 = perf_counter_ns()
    prime = self.create_threads(qtdThread)
    finish = datetime.datetime.now()
    finish1 = perf_counter_ns()

    diff_time = finish - start
    print("Primos encontrados: ", prime)
    print("Tempo (em segundos): ",diff_time.total_seconds())
    print("Tempo em ms: ",(finish1-start1)/1000000)

class SimulationProcesses:
  def __init__(self, filename):
    self.data = self.read_data(filename)

  def read_data(self,filename):
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

  def countPrimes(self,numbers):
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

  def create_multiprocessing(self, qtdThread):
    list_size = len(self.data)

    # Retorna um objeto range, o qual pode ser acessado na notação de índice
    # [0]: primeiro índice
    # [1]: segundo índice considerando o 
    #      próximo índice com base no passo do range
    index = range(0, list_size+(list_size//qtdThread), list_size//qtdThread)

    primos = 0
    processos = []

    for i in range(qtdThread):
        processos.append(self.data[index[i]:index[i+1]])

    with multiprocessing.Pool(qtdThread) as p:
        primos = sum(p.map(self.countPrimes,processos))

    

    return primos
    
  def solve_multiprocessing(self, qtdThread):
    print('\nClassificação de %d valores (Paralelo - multiprocessing)\n'%(len(self.data)))
    start = datetime.datetime.now()
    start1 = perf_counter_ns()
    prime = self.create_multiprocessing(qtdThread)
    finish = datetime.datetime.now()
    finish1 = perf_counter_ns()

    diff_time = finish - start
    print("Primos encontrados: ", prime)
    print("Tempo (em segundos): ",diff_time.total_seconds())
    print("Tempo em ms: ",(finish1-start1)/1000000)


if __name__ == "__main__":
  sm = SimulationThreads('data.csv')
  sm.solve_sequential() 
  sm.solve_threads(5)
  sm2 =SimulationProcesses('data.csv')
  sm2.solve_multiprocessing(5)
