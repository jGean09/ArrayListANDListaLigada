# Este é o código da classe e funções de LISTA DE COMPRAS com Arraylist
# LISTA (LIST) usando ARRAYLIST
# CLASSE E FUNÇÕES

import time

class ListaComprasArray:
 
    def __init__(self, tamanho_inicial = 10):
        self.tamanho = tamanho_inicial
        self.array = [None] * self.tamanho
        self.quantidade = 0 # Quantidade lógica
    
        # Listas para gráficos
        self.tempos_inserir_posicao = []
        self.tempos_remover_posicao = []
        self.tempos_aumentar = []
        self.tempos_diminuir = []

    def is_full(self):
        return self.quantidade == self.tamanho
      
    def is_empty(self):
        return self.quantidade == 0
   
    def quantidade_itens(self):
        return self.quantidade
    
    def tamanho_fisico(self):
        return self.tamanho
    
    def aumentar_tamanho(self):
        inicio = time.perf_counter()
        novo_tamanho = self.tamanho * 2
        novo_array = [None] * novo_tamanho
        for i in range(self.quantidade):
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
        limite = min(self.quantidade, novo_tamanho)
        for i in range(limite):
            novo_array[i] = self.array[i]
        self.array = novo_array
        self.tamanho = novo_tamanho
        self.quantidade = limite
        fim = time.perf_counter()
        self.tempos_diminuir.append(fim - inicio)
        return self.tamanho

    def inserir_item_posicao(self, posicao, item):
        inicio = time.perf_counter()      

        if self.is_full():             #se estiver cheio, aumenta o tamanho
            self.aumentar_tamanho()

        # Validação básica
        if posicao < 0: posicao = 0      #se posicao passada for menor que 0, automaticamente será 0
        if posicao > self.quantidade: posicao = self.quantidade    #se a posicao > self.quantidade, posicao passa a ser quantidade

        # Desloca elementos para a direita para abrir espaço
        for i in range(self.quantidade, posicao, -1):
            self.array[i] = self.array[i-1]
            
        self.array[posicao] = item
        self.quantidade += 1

        fim = time.perf_counter()
        self.tempos_inserir_posicao.append(fim - inicio)

    def remover_item_posicao(self, posicao):   
        inicio = time.perf_counter()

        if self.is_empty(): return None    
        if posicao < 0 or posicao >= self.quantidade: return None   

        valor = self.array[posicao]

        # Desloca elementos para a esquerda para fechar o buraco
        for i in range(posicao, self.quantidade - 1):
            self.array[i] = self.array[i+1]
            
        self.quantidade -= 1
        self.array[self.quantidade] = None

        fim = time.perf_counter()
        self.tempos_remover_posicao.append(fim - inicio)

        if self.quantidade <= self.tamanho // 4:
            self.diminuir_tamanho()

        return valor