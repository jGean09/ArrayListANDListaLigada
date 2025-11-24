# Este é o código da classe e funções de LISTA DE COMPRAS com LinkedList
# LISTA (LIST) usando LINKEDLIST
# CLASSE E FUNÇÕES

import time

class No:
    def __init__(self, dado):
        self.dado = dado
        self.prox = None

class ListaComprasLista:
    
    def __init__(self):
        self.cabeca = None
        self.tamanho = 0

        self.tempos_inserir_posicao = []
        self.tempos_remover_posicao = []
        self.tempos_aumentar = []
        self.tempos_diminuir = []

    def is_empty(self):
        return self.cabeca == None

    def quantidade_itens(self):
        return self.tamanho
    
    def tamanho_fisico(self):
        return self.tamanho

    def inserir_item_posicao(self, posicao, item):
         inicio = time.perf_counter()

         novo = No(item)
         
         if posicao <= 0: # Inserir no início
             novo.prox = self.cabeca
             self.cabeca = novo
         else:
             atual = self.cabeca
             indice_atual = 0
             # Navega até a posição anterior
             while atual is not None and indice_atual < posicao - 1:
                 atual = atual.prox
                 indice_atual += 1
             
             if atual is not None:
                 novo.prox = atual.prox
                 atual.prox = novo
             else:
                 # Se posição for maior que a lista, adiciona no final (se vazia)
                 if self.cabeca is None: self.cabeca = novo

         self.tamanho += 1

         fim = time.perf_counter()
         self.tempos_inserir_posicao.append(fim - inicio)

    def remover_item_posicao(self, posicao):
        inicio = time.perf_counter()

        if self.is_empty(): return None
        
        valor = None
        
        if posicao == 0:
            valor = self.cabeca.dado
            self.cabeca = self.cabeca.prox
        else:
            atual = self.cabeca
            indice_atual = 0
            while atual.prox is not None and indice_atual < posicao - 1:
                atual = atual.prox
                indice_atual += 1
            
            if atual.prox is not None:
                valor = atual.prox.dado
                atual.prox = atual.prox.prox

        if valor is not None:
            self.tamanho -= 1

        fim = time.perf_counter()
        self.tempos_remover_posicao.append(fim - inicio)

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