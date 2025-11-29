# Certifique-se de que o nome do arquivo da classe está correto aqui:
from Pedidos_Array import PedidosArray

def mostrar_fila(fila):
    # Mostra apenas os itens válidos (até self.fim)
    itens = fila.array[:fila.fim]
    print(f"   Fila: {itens} | Próxima Vaga (Fim): {fila.fim} | Capacidade: {fila.tamanho_fisico()}")

def auditoria_fila_array():
    print(">>> AUDITORIA: PEDIDOS LANCHONETE (FILA ARRAY) <<<\n")
    fila = PedidosArray(tamanho_inicial=10)

    # ==========================================
    # TESTE 1: LÓGICA FIFO (O PRIMEIRO QUE ENTRA É O PRIMEIRO QUE SAI)
    # ==========================================
    print("1. Inserindo Pedidos (X-Bacon, Coca, Batata)...")
    fila.novo_pedido("X-Bacon") # 0
    fila.novo_pedido("Coca")    # 1
    fila.novo_pedido("Batata")  # 2

    mostrar_fila(fila)

    print("\n   Atendendo o primeiro pedido...")
    atendido = fila.atender_pedido()
    print(f"   Saiu: {atendido}")

    if atendido == "X-Bacon":
        print("   ✅ SUCESSO: FIFO respeitado (X-Bacon saiu primeiro).")
    else:
        print(f"   ❌ ERRO: Ordem errada. Saiu '{atendido}'.")

    # ==========================================
    # TESTE 2: O GRANDE DESLOCAMENTO (SHIFT LEFT)
    # ==========================================
    print("\n2. Verificando se a fila 'andou' (Coca virou o 1º?)...")
    # Estado esperado: ["Coca", "Batata"]
    # Coca deve estar no índice 0 agora
    
    mostrar_fila(fila)
    
    primeiro_da_fila = fila.array[0]
    segundo_da_fila = fila.array[1]

    if primeiro_da_fila == "Coca" and segundo_da_fila == "Batata":
        print("   ✅ SUCESSO: Todo mundo andou uma casa para a frente.")
    else:
        print(f"   ❌ ERRO: Falha no deslocamento. Pos 0 tem '{primeiro_da_fila}'.")

    # ==========================================
    # TESTE 3: LIMPEZA DE RASTROS (DUPLICAÇÃO)
    # ==========================================
    print("\n3. Verificando se o último item foi limpo...")
    # Quando a fila anda, a posição antiga da Batata (índice 2) deve virar None
    # Seu código tem a linha: self.array[self.fim] = None. Vamos testar.
    
    lixo = fila.array[2] # Onde estava a batata antes
    if lixo is None:
        print("   ✅ SUCESSO: A posição antiga foi limpa (None).")
    else:
        print(f"   ⚠️ ALERTA: A posição antiga ainda tem lixo: {lixo}")

    # ==========================================
    # TESTE 4: EXPANSÃO DA FILA
    # ==========================================
    print("\n4. Teste de Lotação (Novo Pedido em Fila Cheia)...")
    # Vamos criar uma fila pequena para estourar rápido
    fila_peq = PedidosArray(tamanho_inicial=3)
    fila_peq.novo_pedido("1")
    fila_peq.novo_pedido("2")
    fila_peq.novo_pedido("3")
    print(f"   Capacidade antes: {fila_peq.tamanho_fisico()}")
    
    fila_peq.novo_pedido("4") # Estouro
    print(f"   Capacidade depois: {fila_peq.tamanho_fisico()}")

    if fila_peq.tamanho_fisico() == 6:
        print("   ✅ SUCESSO: A fila dobrou de tamanho corretamente.")
    else:
        print("   ❌ ERRO: Resize falhou.")

    # ==========================================
    # TESTE 5: FIM DA FILA (ÍNDICES)
    # ==========================================
    print("\n5. Teste de consistência do ponteiro 'fim'...")
    # Na fila original, temos [Coca, Batata]. Fim deve ser 2.
    print(f"   Valor de self.fim: {fila.fim}")
    
    fila.novo_pedido("Pastel")
    # Agora: [Coca, Batata, Pastel]. Fim deve ser 3.
    
    if fila.array[2] == "Pastel" and fila.fim == 3:
        print("   ✅ SUCESSO: O novo pedido entrou no final correto.")
    else:
        print("   ❌ ERRO: O ponteiro 'fim' está perdido.")

    # ==========================================
    # TESTE 6: FILA VAZIA
    # ==========================================
    print("\n6. Esvaziando a fila e tentando atender vento...")
    fila.atender_pedido() # Sai Coca
    fila.atender_pedido() # Sai Batata
    fila.atender_pedido() # Sai Pastel
    
    atendido = fila.atender_pedido() # Fila vazia
    if atendido is None and fila.fim == 0:
         print("   ✅ SUCESSO: Retornou None e fim zerado.")
    else:
         print("   ❌ ERRO: Comportamento estranho na fila vazia.")

    print("\n>>> AUDITORIA CONCLUÍDA <<<")

if __name__ == "__main__":
    auditoria_fila_array()