# Este é o código da classe e funções de HISTÓRICO WEB com Arraylist
# PILHA usando ARRAYLIST
# CLASSE E FUNÇÕES

import time

class HistoricoArray:
 
    def __init__(self, tamanho_inicial = 10):
    
        self.tamanho = tamanho_inicial    # o tamanho do array é de 10 (tamanho_inicial)
        self.array = [None] * self.tamanho   #está criando array com tamanho igual a 10 com valores None em cada posição
        self.topo = 0                           # esse atributo indicará o topo da pilha (próxima posição a ser preenchida)
    
        # listas para medir tempos 
        self.tempos_push = []
        self.tempos_pop = []
        self.tempos_aumentar = []
        self.tempos_diminuir = []

    def is_full(self):
        return self.topo == self.tamanho      # verifica se pilha está cheia com atributo topo
      
    def is_empty(self):
        return self.topo == 0                    # verifica se pilha está vazia com atributo topo
   
    def quantidade_links(self):          #retorna tamanho lógico, a quantidade de dados inseridos
        return self.topo
    
    def tamanho_fisico_hist_array(self):            #retorna tamanho físico do array, posições pré-alocadas
        return self.tamanho
    
    def aumentar_tamanho(self):
        inicio = time.perf_counter()

        novo_tamanho = self.tamanho * 2    # recomendado dobrar tamanho
        novo_array = [None] * novo_tamanho    # cria novo array com tamanho do novo tamanho

        for i in range(self.topo):               # self.topo indica a última posição preenchida 
            novo_array[i] = self.array[i]        # os dados são copiados para o novo array até o self.topo

        self.array = novo_array                  # o array da classe é o novo array com os dados copiados
        self.tamanho = novo_tamanho        # o tamanho do array recebe o novo tamanho

        fim = time.perf_counter()
        self.tempos_aumentar.append(fim - inicio)

        return self.tamanho

    def diminuir_tamanho_hist_array(self):
        inicio = time.perf_counter()

        novo_tamanho = max(10, self.tamanho // 2)   #reduz tamanho pela metade, sem deixar ficar menor que 10
        novo_array = [None] * novo_tamanho             #cria novo array com novo tamanho e dados vazios

        limite = min(self.topo, novo_tamanho)       # limita self.topo ao novo tamanho

        # copia apenas o que existe (até self.topo)
        for i in range(limite):
            novo_array[i] = self.array[i]

        self.array = novo_array                          #o array é o novo array
        self.tamanho = novo_tamanho                #o tamanho é alterada para um novo tamanho

        # topo não fica maior do que o novo tamanho
        self.topo = limite

        fim = time.perf_counter()
        self.tempos_diminuir.append(fim - inicio)

        return self.tamanho

    def inserir_item_hist_array(self, item):
        inicio = time.perf_counter()

        if self.is_full():               # se a pilha estiver cheia, é preciso aumentar seu tamanho
            self.aumentar_tamanho()   
        
        self.array[self.topo] = item     # a posição "topo" (vazia) do array receeb o novo dado
        self.topo += 1                   # posição "topo" incrementa mais 1

        fim = time.perf_counter()
        self.tempos_push.append(fim - inicio)

    def remover_item_hist_array(self):
        inicio = time.perf_counter()

        if self.is_empty():              #se a pilha estiver vazia (sem dados), retorna None
            return None
        
        self.topo -= 1                   # o topo volta a ser a última posição preenchida
        valor = self.array[self.topo]    # valor recebe o dado que está na posição "topo" do array
        self.array[self.topo] = None     # apaga dado que estava na posição "topo" do array
        
        fim = time.perf_counter()
        self.tempos_pop.append(fim - inicio)

        if self.topo <= self.tamanho // 4:  #se a qtdd de dados preenchidos for menor que 1/4 da tamanho
            self.diminuir_tamanho_hist_array()         #então, o tamanho será reduzido

        return valor  #retorna dado que foi removido
        
        
