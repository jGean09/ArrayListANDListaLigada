# Este é o código da classe e funções de HISTÓRICO WEB com LinkedList
# PILHA usando LINKEDLIST
# CLASSE E FUNÇÕES

import time

class No:

    def __init__(self, dado):
        self.dado = dado          # cada nó contém o dado (valor a ser guardado)
        self.prox = None          # cada nó possui o "prox" que aponta pro próximo nó

class HistoricoListaEncadeada:
    
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

        #listas para medir tempos
        self.tempos_push = []
        self.tempos_pop = []
        self.tempos_aumentar = []
        self.tempos_diminuir = []

    def is_empty(self):
        return self.cabeca == None    #verifica se a cabeca está vazia, indicando que a lista está vazia

    def quantidade_links_lista(self):       # retorna tamanho lógico, a quantidade de dados inseridos
        return self.tamanho
    
    def tamanho_fisico_hist_lista(self):        #retorna tamanho físico da lista
        return self.tamanho

    def inserir_item_hist_lista(self, item):
         inicio = time.perf_counter()  #início de contagem de tempo

         novo = No(item)              #o novo nó é do tipo Nó, recebendo item
         novo.prox = self.cabeca      #a cabeça agora é o prox do novo nó inserido
         self.cabeca = novo           #a cabeça recebe novo, aponta pro último item a ser inserido no topo da pilha
         self.tamanho += 1            #tamanho da lista cresce, incrementando 1

         fim = time.perf_counter()     #fim de contagem de tempo
         self.tempos_push.append(fim - inicio)    #guarda tempo transcorrido

    def remover_item_hist_lista(self):
        inicio = time.perf_counter()

        if self.is_empty():              #se a pilha estiver vazia, é retornado None (sem intens)        
            return None
        
        valor = self.cabeca.dado           #valor é o dado do self.cabeca
        self.cabeca = self.cabeca.prox     #self.cabeça é o prox que aponta para posição anterior
        self.tamanho -= 1                  #tamanho da lista diminui

        fim = time.perf_counter()
        self.tempos_pop.append(fim - inicio)

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


