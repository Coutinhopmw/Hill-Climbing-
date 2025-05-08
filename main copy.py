import random
import math

# FUNÇÃO DE CALCULO DA DISTANCIA ENTRE AS CIDADES
def distancia(cidade1, cidade2):
    return math.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)

# FUNÇÃO DO CUSTO DA ROTA
def funcao_objetivo(rota, cidades):
    custo = 0
    for i in range(len(rota)):
        cidade_atual = cidades[rota[i]]
        proxima_cidade = cidades[rota[(i + 1) % len(rota)]]  # Volta ao início no final
        custo += distancia(cidade_atual, proxima_cidade)
    return custo

# FUNÇÃO PARA GERAR VIZINHOS (TROCA DE CIDADES)
def gerar_vizinhos(rota):
    vizinhos = []
    for i in range(len(rota)):
        for j in range(i + 1, len(rota)):
            novo_vizinho = rota[:]
            novo_vizinho[i], novo_vizinho[j] = novo_vizinho[j], novo_vizinho[i]
            vizinhos.append(novo_vizinho)
    return vizinhos

# FUNÇÃO HILL CLIMBING
def hill_climbing_tsp(cidades, max_iter=1000):
    # Inicializa com uma solução aleatória (permutação das cidades)
    rota_atual = list(range(len(cidades)))
    random.shuffle(rota_atual)
    custo_atual = funcao_objetivo(rota_atual, cidades)
    
    print(f"Rota inicial: {rota_atual}, Custo: {custo_atual:.4f}")
    
    for i in range(max_iter):
        # Gera os vizinhos da rota atual
        vizinhos = gerar_vizinhos(rota_atual)
        
        # Avalia os vizinhos e encontra o melhor
        melhor_vizinho = None
        melhor_custo = custo_atual
        for vizinho in vizinhos:
            custo_vizinho = funcao_objetivo(vizinho, cidades)
            if custo_vizinho < melhor_custo:  # Minimização
                melhor_vizinho = vizinho
                melhor_custo = custo_vizinho
        
        # Verifica se encontrou uma melhoria
        if melhor_vizinho is not None and melhor_custo < custo_atual:
            rota_atual = melhor_vizinho
            custo_atual = melhor_custo
            print(f"Iteração {i + 1}: Nova rota encontrada -> {rota_atual}, Custo: {custo_atual:.4f}")
        else:
            print("Nenhuma melhoria encontrada. Parando o algoritmo.")
            break
    
    return rota_atual, custo_atual

# Entrada principal
if __name__ == "__main__":
    # Define as coordenadas das cidades (x, y)
    cidades = [
        (0, 0),  # Cidade 0
        (2, 3),  # Cidade 1
        (5, 2),  # Cidade 2
        (6, 6),  # Cidade 3
        (8, 3)   # Cidade 4
    ]
    
    resultado = hill_climbing_tsp(cidades)
    print("\nResultado final:")
    print(f"Melhor rota: {resultado[0]}")
    print(f"Custo total: {resultado[1]:.4f}")