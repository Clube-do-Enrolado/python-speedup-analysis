import Utils
import SolveThreads
import SolveProcess
import SolveSequential
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    
    data = Utils.read_data('data.csv')
    parallel_numbers = [2,3,4,5,6,7,8,9,10,11,12]
    number_of_tests = 50
    seq_info = []
    thr_info = []
    prc_info = []
    s_thr = []
    s_prc = []
    thr_total = []
    prc_total = []

    print(f'----> Inicio de simulação com {len(data)} valores')
    for i in parallel_numbers: 
        print(f'\n----> Utilizando {i} Threads/Processos')
        for j in range(number_of_tests):
            seq = SolveSequential.results(data)['time_in_secs']
            thr = SolveThreads.results(data,i)['time_in_secs']
            prc = SolveProcess.results(data,i)['time_in_secs']
            seq_info.append(seq)
            thr_info.append(thr)
            prc_info.append(prc)
            s_thr.append(seq/thr)
            s_prc.append(seq/prc)

        seq_mean = np.mean(seq_info)
        thr_mean = np.mean(thr_info)
        prc_mean = np.mean(prc_info)

        print("\n======= RESULTADOS =======\n")
        print(f'Tempo sequencial médio (s): {seq_mean}')
        print(f'Tempo paralelo com threads médio (s): {thr_mean}')
        print(f'Tempo paralelo com processos médio (s): {prc_mean}')
        print(f'Speedup(S) entre sequencial e threads: {seq_mean/thr_mean}')
        print(f'Speedup(S) entre sequencial e processos: {seq_mean/prc_mean}')
        
        plot1 = plt.figure(1)
        plt.plot(seq_info, label = "Sequêncial")
        plt.plot(thr_info, label = "Paralelo(Thread)")
        plt.plot(prc_info, label = "Paralelo(Processos)")
        plt.xlabel('Execuções')
        plt.ylabel('Tempo Gasto (ms)')
        plt.title(f'Comparação de tempos: utilizando {i} Threads/Processos')
        plt.legend()

        plot2 = plt.figure(2)
        plt.scatter(thr_info, s_thr, label="Threads", color="orange")
        plt.scatter(prc_info, s_prc, label="Processos", color="green")
        plt.xlabel('Tempo gasto (segundos)')
        plt.ylabel('SpeedUp') 
        plt.legend()
        
        plt.show()
        
        thr_total.append(seq_mean/thr_mean)
        prc_total.append(seq_mean/prc_mean)
        
        seq_info = []
        thr_info = []
        prc_info = []
        s_thr = []
        s_prc = []
        

    plot3 = plt.figure(3)
    plt.plot(parallel_numbers, thr_total,label="Thread")
    plt.plot(parallel_numbers, prc_total,label="Processos")
    plt.xlabel('Número de threads/processos utilizados')
    plt.ylabel('SpeedUp')
    plt.legend()
    plt.title("Comparação de SpeedUp entre Threads e Processos")
    plt.show()
