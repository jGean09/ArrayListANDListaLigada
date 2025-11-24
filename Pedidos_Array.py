# Este é o código da classe e funções de PEDIDOS DA LANCHONETE com ArrayList
# FILA (QUEUE) usando ARRAYLIST
# CLASSE E FUNÇÕES

import time

class PedidosArray:
 
    def __init__(self, tamanho_inicial = 10):
    
        self.tamanho = tamanho_inicial    # o tamanho do array
        self.array = [None] * self.tamanho   # cria array com valores None
        self.fim = 0                       # aponta para a próxima posição vazia (final da fila)
    
        # listas para medir tempos 
        self.tempos_novo_pedido = [] # equivale ao push/enqueue
        self.tempos_atender_pedido = [] # equivale ao pop/dequeue
        self.tempos_aumentar = []
        self.tempos_diminuir = []

    def is_full(self):
        return self.fim == self.tamanho
      
    def is_empty(self):
        return self.fim == 0
   
    def quantidade_itens(self):
        return self.fim
    
    def tamanho_fisico(self):
        return self.tamanho
    
    def aumentar_tamanho(self):
        inicio = time.perf_counter()

        novo_tamanho = self.tamanho * 2
        novo_array = [None] * novo_tamanho

        for i in range(self.fim):
            novo_array[i] = self.array[i]

        self.array = novo_array
        self.tamanho = novo_tamanho

        fim = time.perf_counter()
        self.tempos_aumentar.append(fim - inicio)

        return self.tamanho

    def diminuir_tamanho(self):
        inicio = time.perf_counter()

        novo_tamanho = max(10, self.tamanho // 2)
        novo_array = [None] * novo_tamanho

        limite = min(self.fim, novo_tamanho)

        for i in range(limite):
            novo_array[i] = self.array[i]

        self.array = novo_array
        self.tamanho = novo_tamanho
        self.fim = limite

        fim = time.perf_counter()
        self.tempos_diminuir.append(fim - inicio)

        return self.tamanho

    def novo_pedido(self, item): # Enqueue
        inicio = time.perf_counter()

        if self.is_full():
            self.aumentar_tamanho()   
        
        self.array[self.fim] = item
        self.fim += 1

        fim = time.perf_counter()
        self.tempos_novo_pedido.append(fim - inicio)

    def atender_pedido(self): # Dequeue
        inicio = time.perf_counter()

        if self.is_empty():
            return None
        
        # Remove o primeiro elemento (índice 0)
        pedido_atendido = self.array[0]
        
        # DESLOCAMENTO (SHIFT): Move todos os elementos para a esquerda
        # Isso torna essa operação O(n), bem mais lenta que na Lista Encadeada
        for i in range(0, self.fim - 1):
            self.array[i] = self.array[i + 1]
            
        self.fim -= 1
        self.array[self.fim] = None # Limpa a última posição duplicada
        
        fim = time.perf_counter()
        self.tempos_atender_pedido.append(fim - inicio)

        if self.fim <= self.tamanho // 4:
            self.diminuir_tamanho()

        return pedido_atendido