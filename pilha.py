from estrutura_base import Array, No

class PilhaArray:
    def __init__(self):
        self.dados = Array(capacidade=10)

    def empilhar(self, item):
        # Verifica se precisa crescer (Slide 1276)
        if self.dados.tamanho_logico == self.dados.capacidade:
            self.dados._aumentar_capacidade() # O(n) aqui
            
        self.dados.itens[self.dados.tamanho_logico] = item
        self.dados.tamanho_logico += 1

    def desempilhar(self):
        if self.dados.esta_vazia(): return None
        
        idx = self.dados.tamanho_logico - 1
        item = self.dados.itens[idx]
        self.dados.itens[idx] = None # Limpa referência
        self.dados.tamanho_logico -= 1
        
        # Otimização opcional (Slide 1309)
        if self.dados.tamanho_logico > 0 and \
           self.dados.tamanho_logico <= self.dados.capacidade // 4:
            self.dados._diminuir_capacidade()
            
        return item

class PilhaListaLigada:
    def __init__(self):
        self.topo = None # Head da lista

    def empilhar(self, item):
        # Inserção no início é O(1) (Slide 799)
        novo_no = No(item, self.topo)
        self.topo = novo_no

    def desempilhar(self):
        # Remoção no início é O(1) (Slide 854)
        if self.topo is None: return None
        item = self.topo.dado
        self.topo = self.topo.proximo
        return item