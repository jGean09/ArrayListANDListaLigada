# Certifique-se de que o arquivo da classe se chama 'lista_compras_Array.py'
from lista_compras_Array import ListaComprasArray

def mostrar_estado(lista):
    # Função auxiliar para mostrar apenas a parte preenchida do array
    itens_visiveis = lista.array[:lista.quantidade]
    print(f"   Estado: {itens_visiveis} (Qtd: {lista.quantidade} | Cap: {lista.tamanho_fisico()})")

def auditoria_lista_array():
    print(">>> AUDITORIA: LISTA DE COMPRAS (ARRAY) <<<\n")
    lista = ListaComprasArray(tamanho_inicial=10)

    # ==========================================
    # TESTE 1: INSERÇÃO SEQUENCIAL (APPEND)
    # ==========================================
    print("1. Inserindo itens sequencialmente (A, B, C)...")
    lista.inserir_item_posicao(0, "A")
    lista.inserir_item_posicao(1, "B")
    lista.inserir_item_posicao(2, "C")
    
    mostrar_estado(lista)
    if lista.array[2] == "C":
        print("   ✅ SUCESSO: Inserção básica funcionando.")
    else:
        print("   ❌ ERRO: Falha na inserção básica.")

    # ==========================================
    # TESTE 2: O TESTE DE FOGO (INSERIR NO INÍCIO - SHIFT RIGHT)
    # ==========================================
    print("\n2. Inserindo 'X' na Posição 0 (Deve empurrar A, B, C)...")
    # Estado esperado: [X, A, B, C]
    lista.inserir_item_posicao(0, "X")
    
    mostrar_estado(lista)
    
    if lista.array[0] == "X" and lista.array[1] == "A":
        print("   ✅ SUCESSO: O deslocamento para a direita funcionou.")
    else:
        print("   ❌ ERRO: O deslocamento falhou (Verifique o loop for).")

    # ==========================================
    # TESTE 3: INSERIR NO MEIO (ÍNDICE 2)
    # ==========================================
    print("\n3. Inserindo 'Y' na Posição 2 (Entre A e B)...")
    # Atual: [X, A, B, C]
    # Esperado: [X, A, Y, B, C]
    lista.inserir_item_posicao(2, "Y")
    
    mostrar_estado(lista)
    if lista.array[2] == "Y" and lista.array[3] == "B":
        print("   ✅ SUCESSO: Inserção no meio correta.")
    else:
        print("   ❌ ERRO: Falha ao inserir no meio.")

    # ==========================================
    # TESTE 4: VALIDAÇÃO DE ÍNDICE (CLAMPING)
    # ==========================================
    print("\n4. Tentando inserir na posição 100 (Deve ir para o final)...")
    # Sua classe tem uma proteção: if posicao > quantidade: posicao = quantidade
    lista.inserir_item_posicao(100, "Z")
    
    mostrar_estado(lista)
    ultimo_indice = lista.quantidade - 1
    if lista.array[ultimo_indice] == "Z":
        print("   ✅ SUCESSO: O código corrigiu o índice e inseriu no final.")
    else:
        print("   ❌ ERRO: O item se perdeu ou foi inserido errado.")

    # ==========================================
    # TESTE 5: REMOÇÃO E SHIFT LEFT
    # ==========================================
    print("\n5. Removendo item da Posição 0 ('X')...")
    # Atual: [X, A, Y, B, C, Z]
    # Esperado: [A, Y, B, C, Z]
    removido = lista.remover_item_posicao(0)
    
    mostrar_estado(lista)
    
    if removido == "X" and lista.array[0] == "A":
        print("   ✅ SUCESSO: O item saiu e a fila andou para a esquerda.")
    else:
        print("   ❌ ERRO: Problema no deslocamento para esquerda.")

    # ==========================================
    # TESTE 6: EXPANSÃO AUTOMÁTICA
    # ==========================================
    print("\n6. Teste de Estouro (Forçar aumento de tamanho)...")
    # Vamos encher até passar de 10
    lista_temp = ListaComprasArray(tamanho_inicial=4)
    print("   Enchendo lista pequena...")
    lista_temp.inserir_item_posicao(0, "1")
    lista_temp.inserir_item_posicao(0, "2")
    lista_temp.inserir_item_posicao(0, "3")
    lista_temp.inserir_item_posicao(0, "4") # Cheia
    print(f"   Capacidade antes: {lista_temp.tamanho_fisico()}")
    
    lista_temp.inserir_item_posicao(0, "5") # Estouro
    print(f"   Capacidade depois: {lista_temp.tamanho_fisico()}")
    
    if lista_temp.tamanho_fisico() == 8:
        print("   ✅ SUCESSO: Array dobrou de tamanho (4 -> 8).")
    else:
        print("   ❌ ERRO: Resize falhou.")

    print("\n>>> AUDITORIA CONCLUÍDA <<<")

if __name__ == "__main__":
    auditoria_lista_array()