# Ajuste o nome do arquivo se necessário
from historico_lista import HistoricoListaEncadeada 

def auditoria_pilha_lista():
    print(">>> AUDITORIA: HISTÓRICO WEB (LINKED LIST) <<<\n")
    pilha = HistoricoListaEncadeada()

    # ==========================================
    # TESTE 1: INSERÇÃO E CONTAGEM (PUSH)
    # ==========================================
    print("1. Inserindo 3 sites (Google, Youtube, UFRN)...")
    pilha.inserir_item("Google")
    pilha.inserir_item("Youtube")
    pilha.inserir_item("UFRN") # <--- Este é o Topo (Cabeça)

    qtd = pilha.quantidade_itens()
    print(f"   Itens na pilha: {qtd} (Esperado: 3)")
    
    if qtd == 3:
        print("   ✅ SUCESSO: Contagem correta.")
    else:
        print("   ❌ ERRO: Contagem incorreta.")

    # ==========================================
    # TESTE 2: VERIFICAR LIFO (LAST IN, FIRST OUT)
    # ==========================================
    print("\n2. Removendo item do topo (POP)...")
    removido = pilha.remover_item()
    print(f"   Site removido: {removido}")

    # Como "UFRN" foi o último a entrar, ele tem que ser o primeiro a sair
    if removido == "UFRN":
        print("   ✅ SUCESSO: O comportamento de Pilha (LIFO) funcionou.")
    else:
        print(f"   ❌ ERRO: Ordem errada! Esperava 'UFRN', veio '{removido}'.")

    # ==========================================
    # TESTE 3: CONSISTÊNCIA APÓS REMOÇÃO
    # ==========================================
    print("\n3. Verificando o novo topo...")
    # O próximo tem que ser Youtube
    # Como não temos método 'peek' (espiar), vamos remover de novo para ver
    topo_novo = pilha.remover_item()
    
    if topo_novo == "Youtube":
         print("   ✅ SUCESSO: O ponteiro 'prox' estava correto (Youtube era o segundo).")
    else:
         print(f"   ❌ ERRO: Ponteiro perdido. Esperava 'Youtube', veio '{topo_novo}'.")

    # ==========================================
    # TESTE 4: REMOVER ATÉ ESVAZIAR
    # ==========================================
    print("\n4. Esvaziando a lista completamente...")
    pilha.remover_item() # Remove Google
    
    # Agora deve estar vazia
    vazia = pilha.is_empty()
    qtd_final = pilha.quantidade_itens()
    
    print(f"   Está vazia? {vazia}")
    print(f"   Quantidade: {qtd_final}")

    if vazia is True and qtd_final == 0:
        print("   ✅ SUCESSO: Lista limpa corretamente.")
    else:
        print("   ❌ ERRO: Lista diz que tem itens mas deveria estar vazia.")

    # ==========================================
    # TESTE 5: REMOVER DE LISTA VAZIA (SEGURANÇA)
    # ==========================================
    print("\n5. Tentando remover de lista vazia...")
    resultado = pilha.remover_item()
    
    if resultado is None:
        print("   ✅ SUCESSO: Retornou None e não quebrou o código.")
    else:
        print("   ❌ ERRO: Comportamento inesperado.")

    # ==========================================
    # TESTE 6: FUNÇÕES FAKE (AUMENTAR/DIMINUIR)
    # ==========================================
    print("\n6. Testando funções 'Fake' (Aumentar/Diminuir)...")
    # Elas não devem fazer nada além de retornar o tamanho atual
    tam_a = pilha.aumentar_tamanho()
    tam_d = pilha.diminuir_tamanho()
    
    if tam_a == 0 and tam_d == 0:
        print("   ✅ SUCESSO: Funções existem e não quebraram a lógica.")
    else:
        print("   ⚠️ ALERTA: As funções mudaram algo que não deveriam.")

    print("\n>>> AUDITORIA CONCLUÍDA <<<")

if __name__ == "__main__":
    auditoria_pilha_lista()