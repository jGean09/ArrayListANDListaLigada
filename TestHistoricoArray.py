# Certifique-se de que o arquivo da classe se chama 'historico_array.py'
from historico_array import HistoricoArray 

def auditoria_pilha():
    print(">>> INICIANDO AUDITORIA DA PILHA (ARRAY) <<<\n")
    pilha = HistoricoArray(tamanho_inicial=10)

    # ==========================================
    # TESTE 1: LÓGICA BÁSICA (EMPILHAR/DESEMPILHAR)
    # ==========================================
    print("1. Teste de Lógica LIFO (Last In, First Out)...")
    pilha.inserir_item("Site A")
    pilha.inserir_item("Site B")
    pilha.inserir_item("Site C") # <--- Último (Topo)

    topo = pilha.remover_item()
    print(f"   Inseriu A, B, C. Removeu: {topo}")
    
    if topo == "Site C":
        print("   ✅ SUCESSO: O último item foi o primeiro a sair.")
    else:
        print(f"   ❌ ERRO: Esperava 'Site C', veio '{topo}'.")
        return

    # Limpar pilha para próximos testes
    pilha.remover_item() # Tira B
    pilha.remover_item() # Tira A

    # ==========================================
    # TESTE 2: EXPANSÃO (AUMENTAR TAMANHO)
    # ==========================================
    print("\n2. Teste de Expansão (Estourar capacidade inicial)...")
    print(f"   Capacidade atual: {pilha.tamanho_fisico()} (Esperado: 10)")
    
    # Vamos encher até o limite (10 itens)
    for i in range(10):
        pilha.inserir_item(f"Dado {i}")
    
    print("   Pilha cheia (10 itens). Inserindo o 11º item...")
    pilha.inserir_item("Dado Ouro") # <--- Aqui deve dobrar

    cap_nova = pilha.tamanho_fisico()
    print(f"   Nova capacidade: {cap_nova}")

    if cap_nova == 20:
        print("   ✅ SUCESSO: O array dobrou de tamanho (10 -> 20).")
    else:
        print(f"   ❌ ERRO: O array não expandiu corretamente (Deu {cap_nova}).")

    # ==========================================
    # TESTE 3: CONTRAÇÃO (DIMINUIR TAMANHO)
    # ==========================================
    print("\n3. Teste de Contração (Esvaziar para economizar memória)...")
    # Atualmente temos 11 itens e capacidade 20.
    # A regra do seu código é: diminuir se topo <= tamanho // 4
    # 20 // 4 = 5. Precisamos ter 5 ou menos itens para ele reduzir.
    
    print("   Removendo itens até sobrar 4...")
    qtd_atual = pilha.quantidade_itens() # deve ser 11
    
    # Remover até sobrar 4 itens
    while qtd_atual > 4:
        pilha.remover_item()
        qtd_atual = pilha.quantidade_itens()

    # O último remover_item (quando caiu para 5 ou 4) deve ter disparado a redução
    # Novo tamanho deve ser metade de 20 -> 10.
    cap_final = pilha.tamanho_fisico()
    print(f"   Itens restantes: {qtd_atual}")
    print(f"   Capacidade final: {cap_final}")

    if cap_final == 10:
        print("   ✅ SUCESSO: O array encolheu de volta para 10.")
    elif cap_final == 20:
        print("   ❌ ERRO: O array continuou grande (Desperdício de memória).")
    else:
        print(f"   ⚠️ ALERTA: Tamanho inesperado ({cap_final}).")

    # ==========================================
    # TESTE 4: REMOVER DE PILHA VAZIA
    # ==========================================
    print("\n4. Teste de Segurança (Remover de pilha vazia)...")
    pilha = HistoricoArray() # Nova pilha limpa
    resultado = pilha.remover_item()
    
    if resultado is None:
        print("   ✅ SUCESSO: Retornou None corretamente.")
    else:
        print("   ❌ ERRO: Quebrou ou retornou lixo.")

    print("\n>>> AUDITORIA CONCLUÍDA <<<")

if __name__ == "__main__":
    auditoria_pilha()