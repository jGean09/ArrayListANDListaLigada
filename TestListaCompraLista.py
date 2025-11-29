from lista_compras_Lista import ListaComprasLista  # Certifique-se que o nome do arquivo é esse mesmo

def auditoria():
    print(">>> INICIANDO AUDITORIA DA LISTA ENCADEADA <<<\n")
    lista = ListaComprasLista()

    # 1. TESTE BÁSICO: INSERIR 3 ITENS
    print("1. Inserindo 3 itens (Arroz, Feijão, Batata)...")
    lista.inserir_item_posicao(0, "Arroz")   # Pos 0
    lista.inserir_item_posicao(1, "Feijão")  # Pos 1
    lista.inserir_item_posicao(2, "Batata")  # Pos 2
    
    qtd = lista.quantidade_itens()
    print(f"   [Esperado: 3] -> [Real: {qtd}]")
    if qtd != 3: print("   ERRO GRAVE NA CONTAGEM!"); return

    # 2. O TESTE DA MENTIRA (BUG DA JÚLIA)
    print("\n2. Tentando inserir item 'Fantasma' na posição 99 (Inexistente)...")
    lista.inserir_item_posicao(99, "Fantasma")
    
    qtd = lista.quantidade_itens()
    print(f"   [Esperado: 3] -> [Real: {qtd}]")
    if qtd == 4:
        print("   ❌ FALHA: O código contou um item que não foi inserido!")
    else:
        print("   ✅ SUCESSO: O código ignorou a inserção inválida.")

    # 3. TESTE DA REMOÇÃO
    print("\n3. Removendo 1 item (Posição 0 - Arroz)...")
    removido = lista.remover_item_posicao(0)
    print(f"   Item removido: {removido}")
    
    qtd = lista.quantidade_itens()
    print(f"   [Esperado: 2] -> [Real: {qtd}]")
    
    if qtd == 2:
        print("   ✅ SUCESSO: A contagem foi atualizada corretamente.")
    else:
        print("   ❌ FALHA: A contagem não diminuiu.")

    # 4. TESTE REMOVER O QUE NÃO EXISTE
    print("\n4. Tentando remover de lista vazia ou índice errado...")
    lista.remover_item_posicao(50) # Índice não existe
    qtd = lista.quantidade_itens()
    print(f"   [Esperado: 2] -> [Real: {qtd}]")

    print("\n>>> AUDITORIA CONCLUÍDA <<<")

if __name__ == "__main__":
    auditoria()