# Este script analisa a rede complexa https://snap.stanford.edu/biodata/datasets/10004/10004-DCh-Miner.html 
# utilizando NetworkX e Matplotlib. 
# Ele carrega a rede e calcula métricas estruturais (componentes conexas, centralidades, ciclos, etc.), 
# exibe os resultados no terminal e gera visualizações, incluindo distribuição de graus e subgrafos relevantes.


import networkx as nx
import matplotlib.pyplot as plt
import argparse

# Função para carregar a rede de um arquivo .tsv
def load_network(file_path):
    try:
        # Lendo o arquivo como lista de arestas com separador de tabulação
        G = nx.read_edgelist(file_path, delimiter='\t', nodetype=str)
        return G
    except Exception as e:
        print(f"Erro ao carregar a rede: {e}")
        return None

# Função para calcular as métricas básicas da rede
def analyze_network(G):
    analysis = {}

    # Número de nós e arestas
    analysis["num_nodes"] = G.number_of_nodes()
    analysis["num_edges"] = G.number_of_edges()

    # Componentes conectadas
    analysis["connected_components"] = nx.number_connected_components(G)
    largest_cc_nodes = max(nx.connected_components(G), key=len)
    analysis["largest_component_size"] = len(largest_cc_nodes)

    # Raio e diâmetro (da maior componente conexa)
    largest_cc_subgraph = G.subgraph(largest_cc_nodes)
    analysis["radius"] = nx.radius(largest_cc_subgraph)
    analysis["diameter"] = nx.diameter(largest_cc_subgraph)

    # Ciclos (atenção para grafos grandes)
    try:
        cycles = list(nx.cycle_basis(largest_cc_subgraph))
        analysis["num_cycles"] = len(cycles)
    except Exception as e:
        analysis["num_cycles"] = f"Erro ao calcular ciclos: {e}"

    # Centralidades
    degree_centrality = nx.degree_centrality(G)
    closeness_centrality = nx.closeness_centrality(G)
    betweenness_centrality = nx.betweenness_centrality(G)

    # 10 vértices mais centrais
    analysis["top_10_degree"] = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    analysis["top_10_closeness"] = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    analysis["top_10_betweenness"] = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]

    # Número de cliques e tamanhos
    try:
        cliques = list(nx.find_cliques(G))
        analysis["num_cliques"] = len(cliques)
        clique_sizes = [len(clique) for clique in cliques]
        analysis["clique_sizes"] = clique_sizes
        analysis["max_clique_size"] = max(clique_sizes)
    except Exception as e:
        analysis["num_cliques"] = f"Erro ao calcular cliques: {e}"
        analysis["clique_sizes"] = []
        analysis["max_clique_size"] = "Não aplicável"

    return analysis

# Função para obter as cores dos nós
def get_node_colors(G):
    colors = []
    for node in G.nodes():
        if node.startswith('D'):
            colors.append('red')
        elif node.startswith('P'):
            colors.append('blue')
        elif node.startswith('Q'):
            colors.append('yellow')
        else:
            colors.append('gray')  # cor padrão
    return colors

# Função para plotar a distribuição de graus
def plot_degree_distribution(degrees):
    counts, bins, patches = plt.hist(degrees, bins=range(min(degrees), max(degrees) + 2), align='left', edgecolor='black')
    plt.xlabel("Grau")
    plt.ylabel("Frequência")
    plt.title("Distribuição de Graus")
    plt.xlim(0, max(degrees)+1)
    plt.ylim(0, max(counts)+1)
    plt.show()

# Função para desenhar o grafo
def draw_network(G, title, sample_size=None, node_colors=None, figsize=(10, 10), layout_func=nx.spring_layout):
    plt.figure(figsize=figsize)

    # Subamostragem para redes grandes
    if sample_size and sample_size < len(G.nodes):
        sampled_nodes = list(G.nodes)[:sample_size]
        G = G.subgraph(sampled_nodes)

    # Recalcular as cores após a subamostragem
    if node_colors is None or len(node_colors) != len(G.nodes):
        node_colors = get_node_colors(G)
    
    # Gerar layout (use um layout mais rápido ou pré-calcule)
    pos = layout_func(G)
    
    # Renderizar o grafo
    nx.draw(
        G, pos,
        with_labels=False, node_size=20, edge_color='black', node_color=node_colors, alpha=0.8
    )
    plt.title(title)
    plt.show()

# Função para exibir a análise de forma organizada
def print_analysis(analysis):
    print("\n===== Análise da Rede =====")
    print(f"Quantidade de nós: {analysis['num_nodes']}")
    print(f"Quantidade de arestas: {analysis['num_edges']}")
    print(f"Quantidade de componentes conexas: {analysis['connected_components']}")
    print(f"Tamanho da maior componente conexa: {analysis['largest_component_size']}")
    print(f"Raio: {analysis['radius']}")
    print(f"Diâmetro: {analysis['diameter']}")
    print(f"Quantidade de ciclos: {analysis['num_cycles']}")
    print(f"Número de cliques encontrados: {analysis['num_cliques']}")
    print(f"Tamanho máximo de clique: {analysis['max_clique_size']}\n")

    print("10 vértices mais centrais:")
    print("  Grau:")
    for node, centrality in analysis["top_10_degree"]:
        print(f"    {node}: {centrality:.4f}")
    print("  Proximidade:")
    for node, centrality in analysis["top_10_closeness"]:
        print(f"    {node}: {centrality:.4f}")
    print("  Intermediação:")
    for node, centrality in analysis["top_10_betweenness"]:
        print(f"    {node}: {centrality:.4f}")
    print("===========================")

# Função principal
def main():
    # Configurando argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Análise de redes complexas.")
    parser.add_argument(
        "file_path",
        type=str,
        help="Caminho para o arquivo da rede em formato .tsv"
    )
    args = parser.parse_args()

    # Carregar o arquivo especificado
    file_path = args.file_path
    G = load_network(file_path)

    if G is not None:
        analysis = analyze_network(G)
        print_analysis(analysis)

        # Exemplo de visualização
        degrees = [deg for _, deg in G.degree()]
        plot_degree_distribution(degrees)


        # Visualização do grafo completo (com subamostragem para redes grandes)
        print("Plotando a rede completa...")
        draw_network(G, "Visualização da Rede Completa", sample_size=1000, node_colors=get_node_colors(G), layout_func=nx.random_layout)

        # Visualização da maior componente conexa
        print("Plotando a maior componente conexa...")
        largest_cc_nodes = max(nx.connected_components(G), key=len)
        largest_cc_subgraph = G.subgraph(largest_cc_nodes)
        draw_network(largest_cc_subgraph, "Maior Componente Conexa", node_colors=get_node_colors(largest_cc_subgraph), layout_func=nx.spring_layout)

if __name__ == "__main__":
    main()