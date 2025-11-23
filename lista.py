from estrutura_base import Array, No

class ListaArray:
    def __init__(self):
        self.dados = Array(capacidade=10)

    def inserir_em(self, indice, item):
        if self.dados.tamanho_logico == self.dados.capacidade:
            self.dados._aumentar_capacidade()
        
        # Desloca para a direita para abrir espaço (Shift down - Slide 1325)
        # Começa do fim e vai até o índice
        for i in range(self.dados.tamanho_logico, indice, -1):
            self.dados.itens[i] = self.dados.itens[i - 1]
            
        self.dados.itens[indice] = item
        self.dados.tamanho_logico += 1

    def remover_em(self, indice):
        if not 0 <= indice < self.dados.tamanho_logico: return None
        item = self.dados.itens[indice]
        
        # Desloca para a esquerda (Shift up - Slide 1408)
        for i in range(indice, self.dados.tamanho_logico - 1):
            self.dados.itens[i] = self.dados.itens[i + 1]
            
        self.dados.tamanho_logico -= 1
        return item

class ListaListaLigada:
    def __init__(self):
        self.inicio = None # Head
        self.tamanho = 0

    def inserir_em(self, indice, item):
        # Slide 911
        if indice == 0:
            self.inicio = No(item, self.inicio)
        else:
            # Navega até o anterior
            atual = self.inicio
            for _ in range(indice - 1):
                if atual is None: break
                atual = atual.proximo
            if atual:
                atual.proximo = No(item, atual.proximo)
        self.tamanho += 1

    def remover_em(self, indice):
        # Slide 933
        if self.inicio is None: return None
        
        if indice == 0:
            valor = self.inicio.dado
            self.inicio = self.inicio.proximo
            self.tamanho -= 1
            return valor
            
        atual = self.inicio
        for _ in range(indice - 1):
            if atual.proximo is None: return None
            atual = atual.proximo
            
        if atual.proximo:
            valor = atual.proximo.dado
            atual.proximo = atual.proximo.proximo
            self.tamanho -= 1
            return valor
        return None