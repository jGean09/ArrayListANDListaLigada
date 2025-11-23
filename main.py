import time
import matplotlib.pyplot as plt
from pilha import PilhaArray, PilhaListaLigada
from fila import FilaArray, FilaListaLigada
from lista import ListaArray, ListaListaLigada

def benchmark(estrutura_arr, estrutura_list, operacao_nome, qtd_elementos):
    print(f"--- Iniciando Teste de Desempenho: {operacao_nome} ---")
    tempos_arr = []
    tempos_list = []
    indices = []

    # Executa o teste
    for i in range(qtd_elementos):
        # Teste Implementação Array
        inicio = time.perf_counter_ns()
        if operacao_nome == "Pilha - Empilhar": 
            estrutura_arr.empilhar(i)
        elif operacao_nome == "Fila - Desenfileirar": 
            estrutura_arr.desenfileirar()
        elif operacao_nome == "Lista - Inserir no Inicio": 
            estrutura_arr.inserir_em(0, i)
        fim = time.perf_counter_ns()
        tempos_arr.append(fim - inicio)

        # Teste Implementação Lista Ligada
        inicio = time.perf_counter_ns()
        if operacao_nome == "Pilha - Empilhar": 
            estrutura_list.empilhar(i)
        elif operacao_nome == "Fila - Desenfileirar": 
            estrutura_list.desenfileirar()
        elif operacao_nome == "Lista - Inserir no Inicio": 
            estrutura_list.inserir_em(0, i)
        fim = time.perf_counter_ns()
        tempos_list.append(fim - inicio)
        
        indices.append(i)

    # Geração do Gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(indices, tempos_arr, label='Array (Contíguo)', color='red', alpha=0.6, linewidth=0.8)
    plt.plot(indices, tempos_list, label='Lista Ligada (Nós)', color='blue', alpha=0.6, linewidth=0.8)
    
    plt.title(f'Comparativo de Tempo: {operacao_nome}')
    plt.xlabel('Quantidade de Operações')
    plt.ylabel('Tempo (nanosegundos)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    nome_arquivo = f"grafico_{operacao_nome.replace(' ', '_').lower()}.png"
    plt.savefig(nome_arquivo)
    print(f"Gráfico gerado e salvo como: {nome_arquivo}\n")
    plt.close() 

def menu():
    while True:
        print("\n=== TRABALHO ESTRUTURA DE DADOS II (UFRN) ===")
        print("1. Teste PILHA (Empilhar - Mostra Resize do Array)")
        print("2. Teste FILA (Desenfileirar - Mostra lentidão do Array)")
        print("3. Teste LISTA (Inserir no Início - Mostra lentidão do Array)")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        # N para Pilha pode ser alto (resize é rápido na média)
        N_PILHA = 20000 
        # N para Fila/Lista deve ser menor pois Array é O(n) (muito lento)
        N_LENTO = 5000   

        if opcao == '1':
            p_arr = PilhaArray()
            p_list = PilhaListaLigada()
            benchmark(p_arr, p_list, "Pilha - Empilhar", N_PILHA)
            
        elif opcao == '2':
            f_arr = FilaArray()
            f_list = FilaListaLigada()
            print("Preenchendo filas antes de remover...")
            for i in range(N_LENTO): 
                f_arr.enfileirar(i)
                f_list.enfileirar(i)
            
            benchmark(f_arr, f_list, "Fila - Desenfileirar", N_LENTO)

        elif opcao == '3':
            l_arr = ListaArray()
            l_list = ListaListaLigada()
            benchmark(l_arr, l_list, "Lista - Inserir no Inicio", N_LENTO) 

        elif opcao == '4':
            print("Encerrando...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()