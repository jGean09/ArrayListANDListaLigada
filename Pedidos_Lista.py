# Este é o código da classe e funções de PEDIDOS DA LANCHONETE com LinkedList
# FILA (QUEUE) usando LINKEDLIST
# CLASSE E FUNÇÕES

import time

class No:
    def __init__(self, dado):
        self.dado = dado
        self.prox = None

class PedidosListaEncadeada:
    
    def __init__(self):
        self.cabeca = None # Onde atende (início)
        self.cauda = None  # Onde insere (fim)
        self.tamanho = 0

        #listas para medir tempos
        self.tempos_novo_pedido = []
        self.tempos_atender_pedido = []
        self.tempos_aumentar = []
        self.tempos_diminuir = []

    def is_empty(self):
        return self.cabeca == None

    def quantidade_itens(self):
        return self.tamanho
    
    def tamanho_fisico(self):
        return self.tamanho

    def novo_pedido(self, item): # Enqueue
         inicio = time.perf_counter()

         novo = No(item)
         
         if self.is_empty():
             self.cabeca = novo
             self.cauda = novo
         else:
             self.cauda.prox = novo # O atual último aponta para o novo
             self.cauda = novo      # O novo vira o último
             
         self.tamanho += 1

         fim = time.perf_counter()
         self.tempos_novo_pedido.append(fim - inicio)

    def atender_pedido(self): # Dequeue
        inicio = time.perf_counter()

        if self.is_empty():
            return None
        
        valor = self.cabeca.dado
        self.cabeca = self.cabeca.prox # A cabeça anda para o próximo
        
        if self.cabeca is None: # Se a fila ficou vazia, ajusta a cauda
            self.cauda = None
            
        self.tamanho -= 1

        fim = time.perf_counter()
        self.tempos_atender_pedido.append(fim - inicio)

        return valor
    
    def aumentar_tamanho(self):
        inicio = time.perf_counter()
        fim = time.perf_counter()
        self.tempos_aumentar.append(fim - inicio)
        return self.tamanho

    def diminuir_tamanho(self):
        inicio = time.perf_counter()
        fim = time.perf_counter()
        self.tempos_diminuir.append(fim - inicio)
        return self.tamanho