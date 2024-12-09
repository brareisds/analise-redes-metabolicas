# Este script carrega dados de interações entre fármacos e genes de um arquivo TSV,
# cria um grafo dessas interações, e visualiza o grafo com cores diferentes para
# fármacos (verde) e genes (azul).

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Caminho para os arquivos
file_path_network = 'ChG-Miner_miner-chem-gene.tsv'

# Carregar os dados
data_network = pd.read_csv(file_path_network, sep='\t', names=["Drug", "Gene"], skiprows=1)

# Criar o grafo
G = nx.Graph()

# Adicionar arestas ao grafo: Drug -> Gene
for _, row in data_network.iterrows():
    if pd.notna(row["Drug"]) and pd.notna(row["Gene"]):
        G.add_edge(row["Drug"], row["Gene"])

# Definir as cores com base no prefixo dos nós
def get_node_color(node):
    if node.startswith('DB'):
        return 'green'  # Fármacos ou compostos específicos
    else:
        return 'blue'  # Outros nós

node_colors = [get_node_color(node) for node in G.nodes()]

# Visualizar o grafo
plt.figure(figsize=(15, 15))
nx.draw(G, node_color=node_colors, with_labels=False, node_size=20, font_size=8)
plt.title("Grafo com Nós Coloridos por Tipo (DB: Verde, Outros: Azul)")

# Adicionar legenda
import matplotlib.patches as mpatches
blue_patch = mpatches.Patch(color='blue', label='Genes')
green_patch = mpatches.Patch(color='green', label='Fármacos ou compostos específicos')

plt.legend(handles=[blue_patch, green_patch], loc='upper right')

plt.show()