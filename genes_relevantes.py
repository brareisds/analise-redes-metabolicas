# Este script carrega dados de interações entre fármacos e genes de um arquivo TSV,
# cria um grafo dessas interações, e visualiza subgrafos contendo genes relevantes
# com base em diferentes métricas (centralidade de grau, intermediação e proximidade).
# A lista de genes relevantes foi obtida a partir do código "analise_geral.py".
# Os nós são coloridos de acordo com seu tipo e relevância.

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# Carregar os dados do grafo completo
file_path_network = 'ChG-Miner_miner-chem-gene.tsv'  

data_network = pd.read_csv(file_path_network, sep='\t', names=["Drug", "Gene"], skiprows=1)

# Criar o grafo
G = nx.Graph()

# Adicionar arestas ao grafo: Drug -> Gene
for _, row in data_network.iterrows():
    if pd.notna(row["Drug"]) and pd.notna(row["Gene"]):
        G.add_edge(row["Drug"], row["Gene"])

# Listas de genes relevantes
relevant_genes_centralidade = ["P08684", "P10635", "P11712", "P05177", "P33261", 
                               "P10632", "P20815", "DB00157", "P24941", "P20813"]
relevant_genes_intermediacao = ["P08684", "P05177", "P10635", "P11712", "DB00157", 
                                "P00734", "P24941", "P05181", "P23219", "P10632"]
relevant_genes_proximidade = ["P08684", "P11712", "P05177", "P10635", "P33261", 
                              "P10632", "P05181", "P20815", "P04798", "DB01136"]

# Função para criar e visualizar subgrafo
def plot_subgraph(relevant_genes, title):
    # Criar subgrafo contendo os genes relevantes e seus vizinhos
    subgraph = G.subgraph(
        set(relevant_genes) | set(
            neighbor for gene in relevant_genes for neighbor in G.neighbors(gene)
        )
    )
    
    # Aplicar cores: vermelho para P08684, laranja para outros genes relevantes, azul para genes gerais e verde para fármacos
    node_colors = []
    for node in subgraph.nodes():
        if node == "P08684":
            node_colors.append('red')  # Destacar P08684
        elif node in relevant_genes:
            node_colors.append('orange')  # Outros genes relevantes
        elif node.startswith('P'):
            node_colors.append('blue')  # Outros genes
        else:
            node_colors.append('green')  # Fármacos

    # Obter layout fixo com P08684 posicionado no centro para melhorar a visualização
    pos = nx.spring_layout(subgraph, seed=42)
    if "P08684" in pos:
        pos["P08684"] = [0, 0]  # Centralizar P08684

    # Visualizar o subgrafo
    plt.figure(figsize=(12, 12))
    nx.draw(subgraph, pos, node_color=node_colors, with_labels=False, node_size=100, font_size=10)

    # Adicionar legenda na parte inferior esquerda
    legend_elements = [
        mlines.Line2D([], [], color='red', marker='o', linestyle='None', markersize=10, label='P08684'),
        mlines.Line2D([], [], color='orange', marker='o', linestyle='None', markersize=10, label='Outros genes relevantes'),
        mlines.Line2D([], [], color='blue', marker='o', linestyle='None', markersize=10, label='Outros genes'),
        mlines.Line2D([], [], color='green', marker='o', linestyle='None', markersize=10, label='Fármacos'),
    ]
    plt.legend(handles=legend_elements, loc='lower left', fontsize=10)
    
    # Título do grafo
    plt.suptitle(title, fontsize=14)
    plt.axis("off")
    plt.show()

# Gerar gráficos para cada lista
plot_subgraph(relevant_genes_centralidade, "Subgrafo de Genes Relevantes (Centralidade de Grau)")
plot_subgraph(relevant_genes_intermediacao, "Subgrafo de Genes Relevantes (Intermediação)")
plot_subgraph(relevant_genes_proximidade, "Subgrafo de Genes Relevantes (Proximidade)")
