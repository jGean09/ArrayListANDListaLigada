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
        gerar_grafico(entradas, res_lst["rem"], f"{cenario['nome']} - Lista - Remover", f"{pfx}lista_remover.png")
        
        # 3. Gerar Comparativos (Array vs Lista)
        # Usamos os dados coletados acima
        gerar_comparativo(entradas, res_arr["ins"], res_lst["ins"], f"Comparativo Inserir - {cenario['nome']}", f"{pfx}comparar_inserir.png")
        gerar_comparativo(entradas, res_arr["rem"], res_lst["rem"], f"Comparativo Remover - {cenario['nome']}", f"{pfx}comparar_remover.png")
        gerar_comparativo(entradas, res_arr["aum"], res_lst["aum"], f"Comparativo Aumentar - {cenario['nome']}", f"{pfx}comparar_aumentar.png")

    print("\n>>> Todos os gráficos gerados com sucesso!")

# ============================================================
#   INTERFACE DO USUÁRIO
# ============================================================

# MENUS PARA EXECUÇÃO DO ALGORITMO HISTÓRICO WEB

def menu_historico_array():

    historico = HistoricoArray()    #instancia objeto do tipo HistoricoArray

    while True:
        print("="*60)
        print(" HISTORICO WEB - FUNÇÕES NO ARRAY")
        print("="*60)
        print("1.  Inserir Novo Link")
        print("2.  Verificar Qtdd Links Inseridos")
        print("3.  Verificar Tamanho Total do Array")
        print("4.  Remover Link")
        print("5.  Aumentar Tamanho Físico")
        print("6.  Diminuir Tamanho Físico")
        print("0.  Voltar ao Menu Principal")

        op = int(input("Escolha sua opção: "))

        if op == 1:

            link = input("Digite o site que deseja visitar: ")     #insere novo item (link)
            historico.inserir_item_hist_array(link)        #chama método para inserir link no historico

            print(f"Novo item inserido: {link}")
        elif op == 2:

            links_totais = historico.quantidade_links()     #retorna total de links
            print(f"Quantidade de itens inseridos: {links_totais}")

        elif op == 3:     

            tamanho_total_array = historico.tamanho_fisico_hist_array()  #pré-alocado
            print(f"O tamanho físico do array é: {tamanho_total_array}")

        elif op == 4:

            item_removido = historico.remover_item_hist_array()   #remove último link inserido
            print(f"Item removido: {item_removido}")

        elif op == 5:

            novo_tamanho_fisico = historico.aumentar_tamanho()   #aumenta tamanho físico
            print(f"Após o aumento, o novo tamanho físico array é: {novo_tamanho_fisico}")

        elif op == 6:

            tamanho_fisico_reduzido = historico.diminuir_tamanho_hist_array()   #diminui tamanho físico
            print(f"Após a diminuição, o novo tamanho físico do array é: {tamanho_fisico_reduzido}")

        elif op == 0:
            break

        else:
            print("Opção inválida!")

def menu_historico_lista_encadeada():

    historico = HistoricoListaEncadeada()    #instancia objeto do tipo HistoricoListaEncadeada

    while True:
        print("="*60)
        print(" HISTORICO WEB - FUNÇÕES NA LISTA ENCADEADA")
        print("="*60)
        print("1.  Inserir Novo Link")
        print("2.  Verificar Qtdd Links Inseridos")
        print("3.  Verificar Tamanho Total da Lista Encadeada")
        print("4.  Remover Link")
        print("5.  Aumentar Tamanho Físico")
        print("6.  Diminuir Tamanho Físico")
        print("0.  Voltar ao Menu Principal")

        op = int(input("Escolha sua opção: "))

        if op == 1:

            link = input("Digite o site que deseja visitar: ")     #insere novo valor (link)
            historico.inserir_item_hist_lista(link)         #chama método para inserir

            print(f"Novo item inserido: {link}")
        elif op == 2:

            links_totais = historico.quantidade_links_lista()    #retorna links totais inseridos
            print(f"Quantidade de itens inseridos: {links_totais}")

        elif op == 3:     

            tamanho_total_lista = historico.tamanho_fisico_hist_lista() #tamanho físico atual
            print(f"O tamanho físico da lista encadeada é: {tamanho_total_lista}")

        elif op == 4:

            item_removido = historico.remover_item_hist_lista()   #remove último link inserido
            print(f"Item removido: {item_removido}")

        elif op == 5:

            novo_tamanho_fisico = historico.aumentar_tamanho()    #dobra tamanho físico
            print(f"Após o aumento, o novo tamanho físico da lista encadeada é: {novo_tamanho_fisico}")

        elif op == 6:

            tamanho_fisico_reduzido = historico.diminuir_tamanho()  #diminui tamanho físico na metade
            print(f"Após a diminuição, o novo tamanho físico da lista encadeada é: {tamanho_fisico_reduzido}")

        elif op == 0:
            break

        else:
            print("Opção inválida!")

def menu_historico_estruturas():
    while True:
        print("\n" + "="*40)
        print(" MENU ALGORITMO HISTORICO WEB ")
        print("="*40)
        print("1. Executar com ARRAY")
        print("2. Executar com LISTA ENCADEADA")
        print("0. Voltar ao Menu Principal")

        op = int(input("\nEscolha uma opção de estrutura: "))

        if op == 1:
            menu_historico_array()

        elif op == 2:
            menu_historico_lista_encadeada()

        elif op == 0:
            break
        else:
            print("Opção inválida!")

# MENUS PARA EXECUÇÃO DO ALGORITMO PEDIDOS DE LANCHONETE   

def menu_pedidos_array():
    pedidos = PedidosArray()     #instancia objeto "pedido" do tipo PedidosArray, que é a sua classe

    while True:
        print("="*60)
        print(" PEDIDOS DE LANCHONETE - FUNÇÕES NO ARRAY")
        print("="*60)
        print("1.  Fazer Novo Pedido")
        print("2.  Verificar Qtdd Pedidos Feitos")
        print("3.  Verificar Tamanho Total do Array de Pedidos")
        print("4.  Atender Pedido (Remover)")
        print("5.  Aumentar Tamanho Físico")
        print("6.  Diminuir Tamanho Físico")
        print("0.  Voltar ao Menu Principal")

        op = int(input("Escolha sua opção: "))

        if op == 1:

            pedido = input("Digite o pedido que deseja fazer: ")     #insere novo valor (pedido)
            pedidos.novo_pedido(pedido)         #chama método para inserir/fazer pedido

            print(f"Novo pedido feito: {pedido}")
        elif op == 2:

            pedidos_totais = pedidos.quantidade_itens()   #retorna total de pedidos feitos
            print(f"Quantidade de pedidos inseridos: {pedidos_totais}")

        elif op == 3:     

            tamanho_total_array = pedidos.tamanho_fisico()   #pré-alocado
            print(f"O tamanho físico do array é: {tamanho_total_array}")

        elif op == 4:

            pedido_removido = pedidos.atender_pedido()       #remove primeiro pedido inserido ("atende")
            print(f"Item removido: {pedido_removido}")

        elif op == 5:

            novo_tamanho_fisico = pedidos.aumentar_tamanho()  #aumenta tamanho físico (dobro)
            print(f"Após o aumento, o novo tamanho físico do array é: {novo_tamanho_fisico}")

        elif op == 6:

            tamanho_fisico_reduzido = pedidos.diminuir_tamanho()
            print(f"Após a diminuição, o novo tamanho físico do array é: {tamanho_fisico_reduzido}")

        elif op == 0:
            break

        else:
            print("Opção inválida!")

def menu_pedidos_lista_encadeada():

    pedidos = PedidosListaEncadeada()

    while True:
        print("="*60)
        print(" PEDIDOS DE LANCHONETE - FUNÇÕES NA LISTA ENCADEADA")
        print("="*60)
        print("1.  Fazer Novo Pedido")
        print("2.  Verificar Qtdd Pedidos Feitos")
        print("3.  Verificar Tamanho Total da Lista Encadeada")
        print("4.  Atender Pedido (Remover)")
        print("5.  Aumentar Tamanho Físico")
        print("6.  Diminuir Tamanho Físico")
        print("0.  Voltar ao Menu Principal")

        op = int(input("Escolha sua opção: "))

        if op == 1:

            pedido = input("Digite o pedido que deseja fazer: ")     #insere novo valor (pedido)
            pedidos.novo_pedido(pedido)         #chama método para inserir/fazer pedido

            print(f"Novo pedido feito: {pedido}")
        elif op == 2:

            pedidos_totais = pedidos.quantidade_itens()
            print(f"Quantidade de pedidos inseridos: {pedidos_totais}")

        elif op == 3:     

            tamanho_total_lista = pedidos.tamanho_fisico()
            print(f"O tamanho físico da lista encadeada é: {tamanho_total_lista}")

        elif op == 4:

            pedido_removido = pedidos.atender_pedido()
            print(f"Item removido: {pedido_removido}")

        elif op == 5:

            novo_tamanho_fisico = pedidos.aumentar_tamanho()
            print(f"Após o aumento, o novo tamanho físico da lista encadaeada é: {novo_tamanho_fisico}")

        elif op == 6:

            tamanho_fisico_reduzido = pedidos.diminuir_tamanho()
            print(f"Após a diminuição, o novo tamanho físico da lista encadeada é: {tamanho_fisico_reduzido}")

        elif op == 0:
            break

        else:
            print("Opção inválida!")



def menu_pedidos_estruturas():
    while True:
        print("\n" + "="*40)
        print(" MENU ALGORITMO PEDIDOS DE LANCHONETE ")
        print("="*40)
        print("1. Executar com ARRAY")
        print("2. Executar com LISTA ENCADEADA")
        print("0. Voltar ao Menu Principal")

        op = int(input("\nEscolha uma opção: "))

        if op == 1:
            menu_pedidos_array()

        elif op == 2:
            menu_pedidos_lista_encadeada()

        elif op == 0:
            break
        else:
            print("Opção inválida!")

# MENUS PARA EXECUÇÃO DO ALGORITMO LISTA DE TAREFAS

def menu_compras_array():

    itens = ListaComprasArray()           #instancia objeto (lista) do tipo ListaComprasArray (classe)

    while True:
        print("="*60)
        print(" LISTA DE COMPRAS DE ITENS - FUNÇÕES NO ARRAY")
        print("="*60)
        print("1.  Inserir Novo Item")
        print("2.  Verificar Qtdd Itens Inseridos")
        print("3.  Verificar Tamanho Total do Array")
        print("4.  Comprar Item (Remover)")
        print("5.  Aumentar Tamanho Físico")
        print("6.  Diminuir Tamanho Físico")
        print("0.  Voltar ao Menu Principal")

        op = int(input("Escolha sua opção: "))

        if op == 1:

            item = input("Digite o item que deseja inserir na lista de compras: ")     #insere novo valor (compras)
            posicao = int(input("Digite a posição que deseja inserir o item na lista: "))
            itens.inserir_item_posicao(posicao, item)         #chama método para inserir/fazer pedido

            print(f"Novo item inserido: {item}")
        elif op == 2:

            itens_totais = itens.quantidade_itens()
            print(f"Quantidade de itens inseridos: {itens_totais}")

        elif op == 3:     

            tamanho_total_array = itens.tamanho_fisico()
            print(f"O tamanho físico do array é: {tamanho_total_array}")

        elif op == 4:

            posicao_item = int(input("Digite o valor da posição do item que deseja remover: "))
            item_removido = itens.remover_item_posicao(posicao_item)
            print(f"Item removido: {item_removido}")

        elif op == 5:

            novo_tamanho_fisico = itens.aumentar_tamanho()
            print(f"Após o aumento, o novo tamanho físico do array é: {novo_tamanho_fisico}")

        elif op == 6:

            tamanho_fisico_reduzido = itens.diminuir_tamanho()
            print(f"Após a diminuição, o novo tamanho físico do array é: {tamanho_fisico_reduzido}")
    # =======================================================
    #TESTE TESTE TESTE TESTE TESTE
        elif op == 7:
            item = input("Digite o item pra retornar posicao: ")
            item_removido = itens.retorna_posicao(item)
            print(f"A posicao do item removido eh: {item_removido}")
    # ===========================================================
        elif op == 0:
            break

        else:
            print("Opção inválida!")

def menu_compras_lista_encadeada():

    itens = ListaComprasLista()

    while True:
        print("="*60)
        print(" PEDIDOS DE LANCHONETE - FUNÇÕES NA LISTA ENCADEADA")
        print("="*60)
        print("1.  Fazer Novo Pedido")
        print("2.  Verificar Qtdd Pedidos Feitos")
        print("3.  Verificar Tamanho Total da Lista Encadeada")
        print("4.  Atender Pedido (Remover)")
        print("5.  Aumentar Tamanho Físico")
        print("6.  Diminuir Tamanho Físico")
        print("0.  Voltar ao Menu Principal")

        op = int(input("Escolha sua opção: "))

        if op == 1:

            item = input("Digite o item que deseja inserir: ")     #insere novo valor (item)
            itens.inserir_item_posicao(item)         #chama método para inserir item na lista de compras

            print(f"Novo item inserido: {item}")
        elif op == 2:

            pedidos_totais = itens.quantidade_itens()
            print(f"Quantidade de itens inseridos: {pedidos_totais}")

        elif op == 3:     

            tamanho_total_lista = itens.tamanho_fisico()
            print(f"O tamanho físico da lista encadeada é: {tamanho_total_lista}")

        elif op == 4:

            posicao = int(input("Digite a posição do item que deseja remover: "))
            pedido_removido = itens.remover_item_posicao()
            print(f"Item removido: {pedido_removido}")

        elif op == 5:

            novo_tamanho_fisico = itens.aumentar_tamanho()
            print(f"Após o aumento, o novo tamanho físico da lista encadaeada é: {novo_tamanho_fisico}")

        elif op == 6:

            tamanho_fisico_reduzido = itens.diminuir_tamanho()
            print(f"Após a diminuição, o novo tamanho físico da lista encadeada é: {tamanho_fisico_reduzido}")

        elif op == 0:
            break

        else:
            print("Opção inválida!")

def menu_compras_estruturas():
    while True:
        print("\n" + "="*40)
        print(" MENU ALGORITMO LISTA DE TAREFAS ")
        print("="*40)
        print("1. Executar com ARRAY")
        print("2. Executar com LISTA ENCADEADA")
        print("0. Voltar ao Menu Principal")

        op = int(input("\nEscolha uma opção: "))

        if op == 1:
            menu_compras_array()

        elif op == 2:
            menu_compras_lista_encadeada()

        elif op == 0:
            break
        else:
            print("Opção inválida!")


# MENU PRINCIPAL (ESCOLHER ALGORITMOS)
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
            menu_historico_estruturas()

        elif op == "2":
            menu_pedidos_estruturas()

        elif op == "3":
            menu_compras_estruturas()

        elif op == "4":
            gerar_todos_os_graficos()

        elif op == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()