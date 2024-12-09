# Este script analisa uma rede de interações droga-gene a partir de um arquivo TSV, 
# calcula métricas básicas da rede original fornecida
# (como grau médio, coeficiente de agrupamento e comprimento médio do caminho na maior componente conexa),
# e compara essas métricas com redes geradas a partir de modelos teóricos (Erdős-Rényi, Barabási-Albert, Watts-Strogatz e Grafo Regular).
# Com o objetivo de encontrar qual modelo melhor representa a rede.


import networkx as nx
import pandas as pd


# Caminho para o arquivo
file_path_network = 'ChG-Miner_miner-chem-gene.tsv'

# Carregar os dados
data_network = pd.read_csv(file_path_network, sep='\t', names=["Drug", "Gene"], skiprows=1)

# Criar o grafo a partir dos dados
G = nx.from_pandas_edgelist(data_network, source='Drug', target='Gene')

# Análise inicial do grafo
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

# Obter a maior componente conexa
largest_cc = max(nx.connected_components(G), key=len)
G_lcc = G.subgraph(largest_cc).copy()
num_nodes_lcc = G_lcc.number_of_nodes()
num_edges_lcc = G_lcc.number_of_edges()

# Distribuição de graus
degree_sequence = [d for n, d in G.degree()]
average_degree = sum(degree_sequence) / len(degree_sequence)

# Estatísticas da rede original
original_stats = {
    "Total Nodes": num_nodes,
    "Total Edges": num_edges,
    "Average Degree": average_degree,
    "Clustering Coefficient": nx.average_clustering(G),
    "Average Shortest Path (LCC)": nx.average_shortest_path_length(G_lcc),
}

# Comparação com modelos teóricos
models = {}

# 1. Erdős-Rényi (ER)
p = num_edges / (num_nodes * (num_nodes - 1))  # Probabilidade para o modelo ER
ER = nx.erdos_renyi_graph(num_nodes, p)
if nx.is_connected(ER):
    ER_lcc = ER
else:
    largest_cc_er = max(nx.connected_components(ER), key=len)
    ER_lcc = ER.subgraph(largest_cc_er).copy()
models["Erdős-Rényi"] = {
    "Clustering Coefficient": nx.average_clustering(ER),
    "Average Shortest Path (LCC)": nx.average_shortest_path_length(ER_lcc),
    "Average Degree": sum(dict(ER.degree()).values()) / num_nodes,
}

# 2. Barabási-Albert (BA)
m = max(1, round(num_edges / num_nodes))  # Número médio de arestas por nó, mínimo de 1
BA = nx.barabasi_albert_graph(num_nodes, m)
if nx.is_connected(BA):
    BA_lcc = BA
else:
    largest_cc_ba = max(nx.connected_components(BA), key=len)
    BA_lcc = BA.subgraph(largest_cc_ba).copy()
models["Barabási-Albert"] = {
    "Clustering Coefficient": nx.average_clustering(BA),
    "Average Shortest Path (LCC)": nx.average_shortest_path_length(BA_lcc),
    "Average Degree": sum(dict(BA.degree()).values()) / num_nodes,
}

# 3. Watts-Strogatz (WS) - Pequeno Mundo
k = max(2, round(2 * num_edges / num_nodes))  # Grau médio aproximado, mínimo de 2
if k % 2 != 0:
    k += 1  # Garantir que seja par
WS = nx.watts_strogatz_graph(num_nodes, k, 0.1)
if nx.is_connected(WS):
    WS_lcc = WS
else:
    largest_cc_ws = max(nx.connected_components(WS), key=len)
    WS_lcc = WS.subgraph(largest_cc_ws).copy()
models["Watts-Strogatz"] = {
    "Clustering Coefficient": nx.average_clustering(WS),
    "Average Shortest Path (LCC)": nx.average_shortest_path_length(WS_lcc),
    "Average Degree": sum(dict(WS.degree()).values()) / num_nodes,
}

# 4. Grafo Regular
k_reg = max(2, round(2 * num_edges / num_nodes))  # Grau regular, mínimo de 2
if k_reg % 2 != 0:
    k_reg += 1  # Garantir que seja par
Regular = nx.random_regular_graph(k_reg, num_nodes)
if nx.is_connected(Regular):
    Regular_lcc = Regular
else:
    largest_cc_regular = max(nx.connected_components(Regular), key=len)
    Regular_lcc = Regular.subgraph(largest_cc_regular).copy()
models["Regular"] = {
    "Clustering Coefficient": nx.average_clustering(Regular),
    "Average Shortest Path (LCC)": nx.average_shortest_path_length(Regular_lcc),
    "Average Degree": sum(dict(Regular.degree()).values()) / num_nodes,
}

# Resultados
comparison = {
    "Original": original_stats,
    "Models": models,
}

# Exibir resultados
for model, stats in comparison.items():
    print(f"\n{model} Network Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
