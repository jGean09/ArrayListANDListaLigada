# Arquivo: fila.py
from estrutura_base import Array, No

class FilaArray:
    def __init__(self):
        self.dados = Array(capacidade=10)

    def enfileirar(self, item):
        # Adiciona no final (igual pilha)
        if self.dados.tamanho_logico == self.dados.capacidade:
            self.dados._aumentar_capacidade()
        self.dados.itens[self.dados.tamanho_logico] = item
        self.dados.tamanho_logico += 1

    def desenfileirar(self):
        # REMOÇÃO NO INÍCIO DE ARRAY É LENTA - O(n)
        # Slide 1260 - Requer deslocamento (Shift)
        if self.dados.esta_vazia(): return None
        item = self.dados.itens[0]
        
        # Desloca tudo para a esquerda (Shift up)
        for i in range(0, self.dados.tamanho_logico - 1):
            self.dados.itens[i] = self.dados.itens[i + 1]
            
        self.dados.itens[self.dados.tamanho_logico - 1] = None
        self.dados.tamanho_logico -= 1
        return item

class FilaListaLigada:
    def __init__(self):
        self.inicio = None # Head
        self.fim = None    # Tail

    def enfileirar(self, item):
        # Adiciona no fim (Slide 830)
        novo = No(item)
        if self.fim is None:
            self.inicio = self.fim = novo
        else:
            self.fim.proximo = novo
            self.fim = novo

    def desenfileirar(self):
        # Remove do início (Slide 854)
        if self.inicio is None: return None
        item = self.inicio.dado
        self.inicio = self.inicio.proximo
        if self.inicio is None: self.fim = None
        return item