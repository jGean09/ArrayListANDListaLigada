# Certifique-se de que o arquivo da classe se chama 'Pedidos_Lista.py'
from Pedidos_Lista import PedidosListaEncadeada 

def auditoria_fila_lista():
    print(">>> AUDITORIA: PEDIDOS LANCHONETE (LINKED LIST) <<<\n")
    fila = PedidosListaEncadeada()

    # ==========================================
    # TESTE 1: INSERÇÃO E PONTEIROS (CABEÇA E CAUDA)
    # ==========================================
    print("1. Inserindo 2 pedidos (Hambúrguer e Suco)...")
    fila.novo_pedido("Hambúrguer") # Primeiro
    fila.novo_pedido("Suco")       # Segundo (Último)

    # Verificação interna dos ponteiros (Cirúrgica)
    cabeca_real = fila.cabeca.dado
    cauda_real = fila.cauda.dado
    
    print(f"   Cabeça (Próximo a sair): {cabeca_real}")
    print(f"   Cauda (Último que entrou): {cauda_real}")

    if cabeca_real == "Hambúrguer" and cauda_real == "Suco":
        print("   ✅ SUCESSO: Ponteiros Head/Tail configurados corretamente.")
    else:
        print("   ❌ ERRO: Ponteiros bagunçados.")

    # ==========================================
    # TESTE 2: LÓGICA FIFO (ATENDER PEDIDO)
    # ==========================================
    print("\n2. Atendendo o primeiro pedido...")
    atendido = fila.atender_pedido()
    print(f"   Pedido atendido: {atendido}")
    
    if atendido == "Hambúrguer":
        print("   ✅ SUCESSO: O primeiro da fila foi atendido.")
    else:
        print(f"   ❌ ERRO: FIFO violado. Saiu '{atendido}'.")

    # ==========================================
    # TESTE 3: ATUALIZAÇÃO DA CABEÇA
    # ==========================================
    print("\n3. Verificando quem é o próximo...")
    # Agora o Suco deve ter virado a Cabeça
    nova_cabeca = fila.cabeca.dado
    
    if nova_cabeca == "Suco":
        print("   ✅ SUCESSO: A fila andou. 'Suco' agora é a cabeça.")
    else:
        print(f"   ❌ ERRO: Cabeça incorreta ({nova_cabeca}).")

    # ==========================================
    # TESTE 4: ESVAZIAMENTO TOTAL (RESET DE CAUDA)
    # ==========================================
    print("\n4. Esvaziando a fila (Teste Crítico de Ponteiro)...")
    fila.atender_pedido() # Sai Suco. Fila fica vazia.
    
    print(f"   Está vazia? {fila.is_empty()}")
    
    # O PULO DO GATO: Se a fila está vazia, a CAUDA tem que ser None também.
    if fila.cauda is None:
        print("   ✅ SUCESSO: A Cauda foi resetada para None (Evitou bugs futuros).")
    else:
        print(f"   ❌ ERRO GRAVE: A fila está vazia mas a Cauda aponta para lixo ({fila.cauda.dado}).")

    # ==========================================
    # TESTE 5: RESSURREIÇÃO (INSERIR APÓS ESVAZIAR)
    # ==========================================
    print("\n5. Inserindo pedido em fila que foi esvaziada...")
    try:
        fila.novo_pedido("Sobremesa")
        print(f"   Inseriu: {fila.cabeca.dado}")
        if fila.cabeca.dado == "Sobremesa" and fila.cauda.dado == "Sobremesa":
            print("   ✅ SUCESSO: A fila voltou a funcionar corretamente.")
        else:
            print("   ❌ ERRO: Inconsistência após reuso da fila.")
    except Exception as e:
        print(f"   ❌ ERRO CRÍTICO: O código quebrou ao reinserir ({e}).")

    # ==========================================
    # TESTE 6: FUNÇÕES FAKE
    # ==========================================
    print("\n6. Testando funções dummy (Aumentar/Diminuir)...")
    res_a = fila.aumentar_tamanho()
    res_d = fila.diminuir_tamanho()
    
    if res_a == 1 and res_d == 1: # Tamanho atual é 1 (Sobremesa)
        print("   ✅ SUCESSO: Retornaram o tamanho correto.")
    else:
        print("   ⚠️ ALERTA: Retorno inesperado.")

    print("\n>>> AUDITORIA CONCLUÍDA <<<")

if __name__ == "__main__":
    auditoria_fila_lista()