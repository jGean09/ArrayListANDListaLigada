import os
import gc
import time
import matplotlib.pyplot as plt

from historico_array import HistoricoArray
from historico_lista import HistoricoListaEncadeada
from Pedidos_Array import PedidosArray
from Pedidos_Lista import PedidosListaEncadeada
from lista_compras_Array import ListaComprasArray
from lista_compras_Lista import ListaComprasLista

# ============================================================
#   UTILITÁRIOS GRÁFICOS
# ============================================================

def criar_pasta_graficos():
    if not os.path.exists("graficos"):
        os.makedirs("graficos")

def gerar_grafico(entradas, tempos, titulo, nome_arquivo):
    criar_pasta_graficos()
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
    criar_pasta_graficos()
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

# ============================================================
#   FUNÇÃO GENÉRICA DE TESTE (Funciona para Pilha, Fila e Lista)
# ============================================================

def executar_teste_generico(classe_estrutura, tipo_estrutura, operacao, n_elementos):
    """
    Roda um teste para uma estrutura específica e retorna os tempos.
    tipo_estrutura: 'pilha', 'fila', 'lista'
    """
    gc.collect()
    estrutura = classe_estrutura()
    
    # Medir Inserção (Push / Novo Pedido / Adicionar)
    t0 = time.perf_counter()
    for i in range(n_elementos):
        item = f"item_{i}"
        if tipo_estrutura == 'pilha':
            estrutura.inserir_item(item)
        elif tipo_estrutura == 'fila':
            estrutura.novo_pedido(item)
        elif tipo_estrutura == 'lista':
            # Teste crucial: Inserir no INÍCIO (0) para forçar o pior caso do Array
            estrutura.inserir_item_posicao(0, item)
    tempo_ins = time.perf_counter() - t0

    # Medir Remoção (Pop / Atender / Remover)
    t0 = time.perf_counter()
    for i in range(n_elementos):
        if tipo_estrutura == 'pilha':
            estrutura.remover_item()
        elif tipo_estrutura == 'fila':
            estrutura.atender_pedido()
        elif tipo_estrutura == 'lista':
            # Remove do início
            estrutura.remover_item_posicao(0)
    tempo_rem = time.perf_counter() - t0

    # Medir Aumentar (Resize) - Fake na Lista, Real no Array
    # Recriamos para testar o aumento isolado
    gc.collect()
    est_temp = classe_estrutura()
    t0 = time.perf_counter()
    # Força resize chamando método direto (se existir e for público) ou enchendo
    # No seu modelo, chamamos direto o método:
    est_temp.aumentar_tamanho()
    tempo_aum = time.perf_counter() - t0

    # Medir Diminuir
    t0 = time.perf_counter()
    est_temp.diminuir_tamanho()
    tempo_dim = time.perf_counter() - t0

    return tempo_ins, tempo_rem, tempo_aum, tempo_dim

# ============================================================
#   GERAR TODOS OS GRÁFICOS (LOOP PRINCIPAL)
# ============================================================

def gerar_todos_os_graficos():
    print("\n>>> Iniciando Bateria de Testes Completos...\n")
    
    # Configurações de Teste
    entradas = [100, 500, 1000, 2000] # Eixo X dos gráficos
    n_comp = 2000 # Tamanho para o comparativo direto

    # Definição dos cenários
    cenarios = [
        {
            "nome": "Historico Web (Pilha)",
            "tipo": "pilha",
            "cls_arr": HistoricoArray,
            "cls_lst": HistoricoListaEncadeada,
            "pasta": "graficos/pilha_"
        },
        {
            "nome": "Pedidos Lanchonete (Fila)",
            "tipo": "fila",
            "cls_arr": PedidosArray,
            "cls_lst": PedidosListaEncadeada,
            "pasta": "graficos/fila_"
        },
        {
            "nome": "Lista Compras (Lista)",
            "tipo": "lista",
            "cls_arr": ListaComprasArray,
            "cls_lst": ListaComprasLista,
            "pasta": "graficos/lista_"
        }
    ]

    for cenario in cenarios:
        print(f"--- Processando {cenario['nome']} ---")
        
        # Arrays para guardar dados dos gráficos individuais
        res_arr = {"ins": [], "rem": [], "aum": [], "dim": []}
        res_lst = {"ins": [], "rem": [], "aum": [], "dim": []}

        # 1. Rodar testes progressivos (para gráficos de linha x tamanho)
        for n in entradas:
            # Teste Array
            ta_ins, ta_rem, ta_aum, ta_dim = executar_teste_generico(cenario['cls_arr'], cenario['tipo'], "array", n)
            res_arr["ins"].append(ta_ins); res_arr["rem"].append(ta_rem)
            res_arr["aum"].append(ta_aum); res_arr["dim"].append(ta_dim)

            # Teste Lista
            tl_ins, tl_rem, tl_aum, tl_dim = executar_teste_generico(cenario['cls_lst'], cenario['tipo'], "lista", n)
            res_lst["ins"].append(tl_ins); res_lst["rem"].append(tl_rem)
            res_lst["aum"].append(tl_aum); res_lst["dim"].append(tl_dim)

        # 2. Gerar Gráficos Individuais
        pfx = cenario['pasta']
        gerar_grafico(entradas, res_arr["ins"], f"{cenario['nome']} - Array - Inserir", f"{pfx}array_inserir.png")
        gerar_grafico(entradas, res_arr["rem"], f"{cenario['nome']} - Array - Remover", f"{pfx}array_remover.png")
        gerar_grafico(entradas, res_lst["ins"], f"{cenario['nome']} - Lista - Inserir", f"{pfx}lista_inserir.png")
        
        # 3. Gerar Comparativos (Array vs Lista)
        # Usamos os dados coletados acima
        gerar_comparativo(entradas, res_arr["ins"], res_lst["ins"], f"Comparativo Inserir - {cenario['nome']}", f"{pfx}comparar_inserir.png")
        gerar_comparativo(entradas, res_arr["rem"], res_lst["rem"], f"Comparativo Remover - {cenario['nome']}", f"{pfx}comparar_remover.png")
        gerar_comparativo(entradas, res_arr["aum"], res_lst["aum"], f"Comparativo Aumentar - {cenario['nome']}", f"{pfx}comparar_aumentar.png")

    print("\n>>> Todos os gráficos gerados com sucesso!")

# ============================================================
#   INTERFACE DO USUÁRIO
# ============================================================

def menu():
    while True:
        print("\n" + "="*40)
        print(" SISTEMA DE ESTRUTURAS DE DADOS - UFRN")
        print("="*40)
        print("1. Executar Histórico Web (Pilha)")
        print("2. Executar Pedidos Lanchonete (Fila)")
        print("3. Executar Lista de Compras (Lista)")
        print("4. GERAR RELATÓRIO COMPLETO (Gráficos)")
        print("0. Sair")
        
        op = input("\nEscolha uma opção: ")

        if op == "1":
            # Exemplo simples de interação
            p = HistoricoArray()
            p.inserir_item("google.com")
            print("Visitou google.com (Pilha Array)")
        elif op == "2":
            f = PedidosArray()
            f.novo_pedido("X-Bacon")
            print("Pedido X-Bacon entrou na fila (Fila Array)")
        elif op == "3":
            l = ListaComprasArray()
            l.inserir_item_posicao(0, "Arroz")
            print("Arroz adicionado na lista (Lista Array)")
        elif op == "4":
            gerar_todos_os_graficos()
        elif op == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()