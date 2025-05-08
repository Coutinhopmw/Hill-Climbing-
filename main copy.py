import random
import math
import csv
import matplotlib.pyplot as plt
import time

# FUNÇÃO DE CALCULO DA DISTÂNCIA ENTRE AS CIDADES
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
    rota_atual = list(range(len(cidades)))
    random.shuffle(rota_atual)
    custo_atual = funcao_objetivo(rota_atual, cidades)

    tempos = []
    custos = []
    inicio = time.time()
    
    print(f"Rota inicial: {rota_atual}, Custo: {custo_atual:.4f}")
    
    for i in range(max_iter):
        vizinhos = gerar_vizinhos(rota_atual)
        melhor_vizinho = None
        melhor_custo = custo_atual
        for vizinho in vizinhos:
            custo_vizinho = funcao_objetivo(vizinho, cidades)
            if custo_vizinho < melhor_custo:
                melhor_vizinho = vizinho
                melhor_custo = custo_vizinho
        
        if melhor_vizinho is not None and melhor_custo < custo_atual:
            rota_atual = melhor_vizinho
            custo_atual = melhor_custo
            tempo_atual = time.time() - inicio
            tempos.append(tempo_atual)
            custos.append(custo_atual)
            print(f"Iteração {i + 1}: Nova rota encontrada -> Custo: {custo_atual:.4f}, Tempo: {tempo_atual:.4f}s")
        else:
            print("Nenhuma melhoria encontrada. Parando o algoritmo.")
            break
    
    return rota_atual, custo_atual, tempos, custos

# FUNÇÃO PARA LER CIDADES DO CSV (COM NOME, X, Y)
def ler_cidades_csv(caminho_arquivo):
    cidades = []
    nomes = []
    with open(caminho_arquivo, newline='') as csvfile:
        leitor = csv.reader(csvfile)
        next(leitor)  # pula o cabeçalho
        for linha in leitor:
            nome = linha[0]
            x = float(linha[1])
            y = float(linha[2])
            cidades.append((x, y))
            nomes.append(nome)
    return cidades, nomes

# FUNÇÃO PARA PLOTAR O GRÁFICO DA ROTA
def plotar_rota(cidades, nomes, rota, custo_total):
    x_coords = [cidades[i][0] for i in rota] + [cidades[rota[0]][0]]
    y_coords = [cidades[i][1] for i in rota] + [cidades[rota[0]][1]]
    
    plt.figure(figsize=(10, 8))
    plt.plot(x_coords, y_coords, 'bo-', label='Rota')
    
    for i, nome in enumerate(nomes):
        plt.text(cidades[i][0], cidades[i][1], nome, fontsize=8)
    
    plt.title(f'Melhor Rota Encontrada (Custo Total: {custo_total:.2f})')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.legend()
    plt.grid(True)
    plt.show()

# FUNÇÃO PARA PLOTAR O GRÁFICO DE TEMPO E CUSTO
def plotar_tempo_custo(tempos, custos):
    plt.figure(figsize=(10, 6))
    plt.fill_between(tempos, custos, color='skyblue', alpha=0.5)
    plt.plot(tempos, custos, 'b-', linewidth=2)
    
    plt.title('Evolução do Custo ao Longo do Tempo')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('Custo da Rota')
    plt.grid(True)
    plt.show()

# Entrada principal
if __name__ == "__main__":
    caminho_arquivo = 'cidades.csv'  # Nome do arquivo CSV
    
    try:
        cidades, nomes = ler_cidades_csv(caminho_arquivo)
        print(f"{len(cidades)} cidades carregadas do arquivo '{caminho_arquivo}'.")
        
        melhor_rota, custo_total, tempos, custos = hill_climbing_tsp(cidades)
        
        print("\nResultado final:")
        print(f"Melhor rota: {melhor_rota}")
        print(f"Custo total: {custo_total:.4f}")
        
        # Gráfico da rota final
        plotar_rota(cidades, nomes, melhor_rota, custo_total)
        
        # Gráfico de tempo vs custo
        if tempos and custos:
            plotar_tempo_custo(tempos, custos)
        else:
            print("Nenhuma melhoria registrada para gerar o gráfico de tempo.")
        
    except FileNotFoundError:
        print(f"Arquivo '{caminho_arquivo}' não encontrado. Certifique-se de que ele está no mesmo diretório do script.")
