# README - Análise de Redes Complexas

## Autoras

- Barbara Reis dos Santos
- Mayara Lessnau de Figueiredo Neves

## Descrição do Repositório

Este repositório contém scripts e ferramentas para análise de redes complexas com foco em interações droga-gene, utilizando a rede disponível no banco de dados [ChG-Miner](https://snap.stanford.edu/biodata/datasets/10004/10004-DCh-Miner.html). A rede representa associações entre fármacos e genes, permitindo a análise de propriedades estruturais e a comparação com modelos teóricos de redes.

## Descrição da Rede

A rede analisada é uma **rede de associação doença-droga**, contendo informações sobre relações entre fármacos, doenças e substâncias químicas. Os nós representam doenças, drogas e compostos químicos, enquanto as arestas indicam associações conhecidas entre eles. Exemplos incluem interações entre compostos como arsênico e doenças como neoplasias prostáticas, doenças de pele e isquemia miocárdica. Essa rede é valiosa para entender mecanismos pelos quais medicamentos tratam doenças e para formular hipóteses sobre os mecanismos subjacentes às doenças ambientais.

## Scripts Disponíveis

### 1. **grafo_colorido.py**

Carrega os dados da rede e cria um grafo onde os nós são coloridos de acordo com seus tipos (fármacos em verde e genes em azul). Gera uma visualização completa da rede com uma legenda destacando as categorias dos nós.

### 2. **genes_relevantes.py**

Foca em subgrafos contendo genes relevantes identificados com base em métricas como centralidade de grau, proximidade e intermediação. Os genes e seus vizinhos são destacados em diferentes cores para facilitar a interpretação.

### 3. **comp_modelos.py**

Compara as métricas estruturais da rede original com modelos teóricos de redes, incluindo:

- **Erdős-Rényi:** Rede aleatória.
- **Barabási-Albert:** Rede com hubs baseada em crescimento preferencial.
- **Watts-Strogatz:** Rede do tipo pequeno mundo.
- **Grafo Regular:** Rede homogênea com grau fixo.

Os resultados incluem coeficiente de agrupamento, comprimento médio do caminho e grau médio.

### 4. **analise_geral.py**

Realiza uma análise abrangente da rede, calculando métricas estruturais como número de componentes conexas, centralidades, ciclos, cliques e distribuição de graus. Inclui visualizações detalhadas do grafo completo e da maior componente conexa.

## Dataset Utilizado

O arquivo de entrada utilizado é o `ChG-Miner_miner-chem-gene.tsv`, contendo interações entre fármacos e genes. Este arquivo está disponível no repositório e é carregado pelos scripts para construção da rede.

- **Dataset:** Fornecido pelo projeto [ChG-Miner](https://snap.stanford.edu/biodata/datasets/10004/10004-DCh-Miner.html).
