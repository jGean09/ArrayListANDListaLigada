# Arquivo: estrutura_base.py

class Array:
    """
    Simula um Array de tamanho fixo com redimensionamento manual.
    Baseado na Aula 09.
    """
    def __init__(self, capacidade=10):
        self.capacidade = capacidade      # Tamanho Físico
        self.tamanho_logico = 0           # Tamanho Lógico (slide 1235)
        self.itens = [None] * capacidade  # Alocação fixa simulada

    def esta_vazia(self):
        return self.tamanho_logico == 0

    def __len__(self):
        return self.tamanho_logico

    def __getitem__(self, indice):
        if not 0 <= indice < self.tamanho_logico:
            raise IndexError("Índice fora do limite")
        return self.itens[indice]

    def _aumentar_capacidade(self):
        """
        Duplica o tamanho físico. Custo O(n).
        Slide 1279: Cria novo array, copia dados, redefini variável.
        """
        nova_cap = self.capacidade * 2
        novo_array = [None] * nova_cap
        # Copia os elementos (O custo computacional real)
        for i in range(self.tamanho_logico):
            novo_array[i] = self.itens[i]
        
        self.itens = novo_array
        self.capacidade = nova_cap

    def _diminuir_capacidade(self):
        """
        Reduz pela metade se uso < 25%. Custo O(n).
        Slide 1309.
        """
        if self.capacidade <= 10: return # Limite mínimo
        
        nova_cap = self.capacidade // 2
        novo_array = [None] * nova_cap
        for i in range(self.tamanho_logico):
            novo_array[i] = self.itens[i]
            
        self.itens = novo_array
        self.capacidade = nova_cap

class No:
    """
    Nó simples para estruturas encadeadas.
    Baseado na Aula 10 - Slide 655.
    """
    def __init__(self, dado, proximo_no=None):
        self.dado = dado
        self.proximo = proximo_no