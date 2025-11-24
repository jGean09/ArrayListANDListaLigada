import os
import gc
import time
import matplotlib.pyplot as plt

from historico_array import HistoricoArray
from historico_lista import HistoricoListaEncadeada


# ============================================================
#   GERAR PASTA DE GRÁFICOS
# ============================================================

def criar_pasta_graficos():
    if not os.path.exists("graficos"):
        os.makedirs("graficos")


# ============================================================
#   TESTES AUTOMÁTICOS – ARRAY
# ============================================================

def testes_automaticos_array(n):
    arr = HistoricoArray()

    # Inserção automática
    inicio = time.time()
    for i in range(n):
        arr.inserir_item(f"url_{i}")
    tempo_insercao = time.time() - inicio

    # Remoção automática
    inicio = time.time()
    for i in range(n):
        arr.remover_item()
    tempo_remocao = time.time() - inicio

    # Aumentar capacidade repetidamente
    inicio = time.time()
    for _ in range(1000):
        arr.aumentar_tamanho()
    tempo_aumentar = time.time() - inicio

    # Diminuir capacidade repetidamente
    inicio = time.time()
    for _ in range(1000):
        arr.diminuir_tamanho()
    tempo_diminuir = time.time() - inicio

    return tempo_insercao, tempo_remocao, tempo_aumentar, tempo_diminuir


# ============================================================
#   TESTES AUTOMÁTICOS – LISTA ENCADEADA
# ============================================================

def testes_automaticos_lista(n):
    lista = HistoricoListaEncadeada()

    # Inserção
    inicio = time.time()
    for i in range(n):
        lista.inserir_item(f"url_{i}")
    tempo_insercao = time.time() - inicio

    # Remoção
    inicio = time.time()
    for i in range(n):
        lista.remover_item()
    tempo_remocao = time.time() - inicio

    # "Aumentar" (função fake)
    inicio = time.time()
    for _ in range(1000):
        lista.aumentar_tamanho()
    tempo_aumentar = time.time() - inicio

    # "Diminuir" (função fake)
    inicio = time.time()
    for _ in range(1000):
        lista.diminuir_tamanho()
    tempo_diminuir = time.time() - inicio

    return tempo_insercao, tempo_remocao, tempo_aumentar, tempo_diminuir

# ===========================================================
#   FUNÇÕES PARA GERAR GRÁFICOS
# ===========================================================

def gerar_grafico(entradas, tempos, titulo, nome_arquivo):
    """
    Plota e salva um gráfico simples.
    entradas: lista de valores do eixo x (ex: [100,500,1000])
    tempos: lista de tempos correspondentes (mesma ordem/len que entradas)
    titulo: título do gráfico
    nome_arquivo: caminho do arquivo para salvar (ex: "graficos/array_inserir.png")
    """
    # garante pasta
    pasta = os.path.dirname(nome_arquivo) or "."
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    plt.figure()
    plt.plot(entradas, tempos, marker="o", linestyle="-")
    plt.xlabel("Tamanho da entrada")
    plt.ylabel("Tempo (s)")
    plt.title(titulo)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()
    print(f">> Gráfico salvo: {nome_arquivo}")


def gerar_comparativo(entradas, tempos_array, tempos_lista, titulo, nome_arquivo):
    """
    Plota e salva um gráfico comparativo (Array vs Lista).
    entradas: lista de valores do eixo x
    tempos_array: lista de tempos do array (mesma len de entradas)
    tempos_lista: lista de tempos da lista (mesma len de entradas)
    """
    # garante pasta
    pasta = os.path.dirname(nome_arquivo) or "."
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    plt.figure()
    plt.plot(entradas, tempos_array, marker="o", linestyle="-", label="Array")
    plt.plot(entradas, tempos_lista, marker="s", linestyle="--", label="Lista Encadeada")
    plt.xlabel("Tamanho da entrada")
    plt.ylabel("Tempo (s)")
    plt.title(titulo)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(nome_arquivo)
    plt.close()
    print(f">> Gráfico salvo: {nome_arquivo}")

# ===========================================================
#   GERAÇÃO DE GRÁFICOS
# ===========================================================

def gerar_todos_os_graficos():
    print("\nGerando gráficos (modo seguro)...\n")
    criar_pasta_graficos()

    # ENTRADAS REDUZIDAS E SEGUROS
    entradas = [100, 500, 1000, 2000]   # para gráficos individuais
    n_comp = 2000                        # para comparativos (único valor)

    # listas para armazenar resultados
    ins_arr, rem_arr, aum_arr, dim_arr = [], [], [], []
    ins_lst, rem_lst, aum_lst, dim_lst = [], [], [], []

    # ---------- Array: individuais ----------
    for n in entradas:
        print(f"Array: testando n={n} (inserir/remover/aumentar/diminuir)")
        gc.collect()
        arr = HistoricoArray(tamanho_inicial=10)

        # Inserir n (medir tempo total -> média por inserção se quiser)
        t0 = time.perf_counter()
        for i in range(n):
            arr.inserir_item("x")
        t_ins = time.perf_counter() - t0
        ins_arr.append(t_ins)

        # Remover n (recriar para garantir estado)
        t0 = time.perf_counter()
        for i in range(n):
            arr.remover_item()
        t_rem = time.perf_counter() - t0
        rem_arr.append(t_rem)

        # Aumentar capacidade (medir chamada única)
        gc.collect()
        arr = HistoricoArray(tamanho_inicial=max(10, n))
        t0 = time.perf_counter()
        arr.aumentar_tamanho()   # se seu método recebe novo tamanho, adapte
        t_aum = time.perf_counter() - t0
        aum_arr.append(t_aum)

        # Diminuir capacidade
        gc.collect()
        arr = HistoricoArray(tamanho_inicial=max(10, n))
        for _ in range(n):
            arr.inserir_item("x")
        t0 = time.perf_counter()
        arr.diminuir_tamanho()
        t_dim = time.perf_counter() - t0
        dim_arr.append(t_dim)

        # liberar antes do próximo n
        del arr
        gc.collect()

    # ---------- Lista encadeada: individuais ----------
    for n in entradas:
        print(f"Lista: testando n={n} (inserir/remover/aumentar/diminuir)")
        gc.collect()
        lst = HistoricoListaEncadeada()

        t0 = time.perf_counter()
        for i in range(n):
            lst.inserir_item("x")
        t_ins = time.perf_counter() - t0
        ins_lst.append(t_ins)

        # Remover
        t0 = time.perf_counter()
        for i in range(n):
            lst.remover_item()
        t_rem = time.perf_counter() - t0
        rem_lst.append(t_rem)

        # Aumentar (fake)
        t0 = time.perf_counter()
        lst.aumentar_tamanho()
        t_aum = time.perf_counter() - t0
        aum_lst.append(t_aum)

        # Diminuir (fake)
        t0 = time.perf_counter()
        lst.diminuir_tamanho()
        t_dim = time.perf_counter() - t0
        dim_lst.append(t_dim)

        del lst
        gc.collect()

    # ---------- Comparativos (um n_comp razoável) ----------
    print(f"\nExecutando comparativos com n_comp = {n_comp}")
    gc.collect()
    arr = HistoricoArray(tamanho_inicial=10)
    t0 = time.perf_counter()
    for i in range(n_comp):
        arr.inserir_item("x")
    t_ins_arr_comp = time.perf_counter() - t0

    gc.collect()
    lst = HistoricoListaEncadeada()
    t0 = time.perf_counter()
    for i in range(n_comp):
        lst.inserir_item("x")
    t_ins_lst_comp = time.perf_counter() - t0

    # remover comparativo
    gc.collect()
    arr2 = HistoricoArray(tamanho_inicial=n_comp)
    for i in range(n_comp):
        arr2.inserir_item("x")
    t0 = time.perf_counter()
    for i in range(n_comp):
        arr2.remover_item()
    t_rem_arr_comp = time.perf_counter() - t0

    gc.collect()
    lst2 = HistoricoListaEncadeada()
    for i in range(n_comp):
        lst2.inserir_item("x")
    t0 = time.perf_counter()
    for i in range(n_comp):
        lst2.remover_item()
    t_rem_lst_comp = time.perf_counter() - t0

    # Aumentar/diminuir comparativos (chamada única)
    gc.collect()
    arr3 = HistoricoArray(tamanho_inicial=n_comp)
    t0 = time.perf_counter()
    arr3.aumentar_tamanho()
    t_aum_arr_comp = time.perf_counter() - t0

    gc.collect()
    lst3 = HistoricoListaEncadeada()
    t0 = time.perf_counter()
    lst3.aumentar_tamanho()
    t_aum_lst_comp = time.perf_counter() - t0

    gc.collect()
    arr4 = HistoricoArray(tamanho_inicial=n_comp)
    for i in range(n_comp):
        arr4.inserir_item("x")
    t0 = time.perf_counter()
    arr4.diminuir_tamanho()
    t_dim_arr_comp = time.perf_counter() - t0

    gc.collect()
    lst4 = HistoricoListaEncadeada()
    for i in range(n_comp):
        lst4.inserir_item("x")
    t0 = time.perf_counter()
    lst4.diminuir_tamanho()
    t_dim_lst_comp = time.perf_counter() - t0

    # salvar gráficos (você já tem funções que fazem isso; aqui apenas um exemplo)
    gerar_grafico(entradas, ins_arr, "Inserir - Array", "graficos/array_inserir.png")
    gerar_grafico(entradas, rem_arr, "Remover - Array", "graficos/array_remover.png")
    gerar_grafico(entradas, aum_arr, "Aumentar - Array", "graficos/array_aumentar.png")
    gerar_grafico(entradas, dim_arr, "Diminuir - Array", "graficos/array_diminuir.png")

    gerar_grafico(entradas, ins_lst, "Inserir - Lista", "graficos/lista_inserir.png")
    gerar_grafico(entradas, rem_lst, "Remover - Lista", "graficos/lista_remover.png")
    gerar_grafico(entradas, aum_lst, "Aumentar - Lista", "graficos/lista_aumentar.png")
    gerar_grafico(entradas, dim_lst, "Diminuir - Lista", "graficos/lista_diminuir.png")

    gerar_comparativo([n_comp], [t_ins_arr_comp], [t_ins_lst_comp], "Comparativo Inserir", "graficos/comparar_inserir.png")
    gerar_comparativo([n_comp], [t_rem_arr_comp], [t_rem_lst_comp], "Comparativo Remover", "graficos/comparar_remover.png")
    gerar_comparativo([n_comp], [t_aum_arr_comp], [t_aum_lst_comp], "Comparativo Aumentar", "graficos/comparar_aumentar.png")
    gerar_comparativo([n_comp], [t_dim_arr_comp], [t_dim_lst_comp], "Comparativo Diminuir", "graficos/comparar_diminuir.png")

    print("Gráficos gerados em modo seguro em 'graficos/'")


# ============================================================
#   MENUS INTERATIVOS
# ============================================================

def menu_array():
    estrutura = HistoricoArray()

    while True:
        print("\n===== MENU ARRAY =====")
        print("1 - Inserir item")
        print("2 - Remover item")
        print("3 - Ver quantidade de itens")
        print("4 - Ver tamanho físico (capacidade)")
        print("5 - Aumentar tamanho físico")
        print("6 - Diminuir tamanho físico")
        print("7 - Testes automáticos")
        print("8 - Voltarao Menu Principal")
        op = input("Escolha: ")

        if op == "1":
            valor = input("Digite o item: ")
            estrutura.inserir_item(valor)

        elif op == "2":
            print("Removido:", estrutura.remover_item())

        elif op == "3":
            print("Quantidade:", estrutura.quantidade_itens())

        elif op == "4":
            print("Tamanho físico:", estrutura.tamanho_fisico())

        elif op == "5":
            print("Novo tamanho:", estrutura.aumentar_tamanho())

        elif op == "6":
            print("Novo tamanho:", estrutura.diminuir_tamanho())

        elif op == "7":
            n = int(input("Quantidade de operações automáticas: "))
            tempos = testes_automaticos_array(n)
            print("Tempos:", tempos)

        elif op == "8":
            break

        else:
            print("Inválido.")


def menu_lista():
    estrutura = HistoricoListaEncadeada()

    while True:
        print("\n===== MENU LISTA ENCADEADA =====")
        print("1 - Inserir item")
        print("2 - Remover item")
        print("3 - Ver quantidade de itens")
        print("4 - Ver tamanho lógico")
        print("5 - Aumentar tamanho (fake)")
        print("6 - Diminuir tamanho (fake)")
        print("7 - Testes automáticos")
        print("8 - Voltar ao Menu Principal")
        op = input("Escolha: ")

        if op == "1":
            valor = input("Digite o item: ")
            estrutura.inserir_item(valor)

        elif op == "2":
            print("Removido:", estrutura.remover_item())

        elif op == "3":
            print("Quantidade:", estrutura.quantidade_itens())

        elif op == "4":
            print("Tamanho (lógico):", estrutura.tamanho_fisico())

        elif op == "5":
            print("Tamanho:", estrutura.aumentar_tamanho())

        elif op == "6":
            print("Tamanho:", estrutura.diminuir_tamanho())

        elif op == "7":
            n = int(input("Quantidade de operações automáticas: "))
            tempos = testes_automaticos_lista(n)
            print("Tempos:", tempos)

        elif op == "8":
            break

        else:
            print("Inválido.")


# ============================================================
#   MAIN
# ============================================================

def main():
    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Usar Histórico com Array")
        print("2 - Usar Histórico com Lista Encadeada")
        print("3 - Gerar todos os gráficos automáticos")
        print("0 - Sair")
        op = input("Escolha: ")

        if op == "1":
            menu_array()

        elif op == "2":
            menu_lista()

        elif op == "3":
            gerar_todos_os_graficos()

        elif op == "0":
            print("Encerrando...")
            return

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
