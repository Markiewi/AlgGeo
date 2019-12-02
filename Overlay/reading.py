"""
    Parser przyjmuje pliki tekstowe gdzie pierwsza linia zawiera odpowiednio
    ilosc punktow (n1), ilosc krawedzi (e1) pierwszego grafu planarnego,
    a nastepna linia zawiera odpowiednio ilosc punktow (n2), ilosc krawedzi (e2) drugiego
    grafu planarnego.
    Nastepne n1 linii zawiera po jednym punkcie pierwszego grafu, a pozniej e1 linii kazda
    zawierajaca krawedz pierwszego grafu.
    Nastepne linie zawieraja to samo dla grafu drugiego.
    Punkty sa jako dwie wspolrzedne (najpierw x) oddzielone spacja.
    Krawedzie sa w postaci indeksow do przyszlo powstalej listy punkow (rowniez oddzielone spacja).
"""


def reading(file):
    f = [int(x) for x in open(file).read().split()]
    f = [tuple(f[i:i + 2]) for i in range(0, len(f), 2)]

    g1_nodes_index = f[0][0] + 2
    g1_edges_index = f[0][1] + g1_nodes_index

    g2_nodes_index = f[1][0] + g1_edges_index
    g2_edges_index = f[1][1] + g2_nodes_index

    g1_nodes = f[2:g1_nodes_index]
    g1_edges = f[g1_nodes_index:g1_edges_index]

    g2_nodes = f[g1_edges_index:g2_nodes_index]
    g2_edges = f[g2_nodes_index:g2_edges_index]

    nodes = g1_nodes.copy() + g2_nodes.copy()
    edges = g1_edges.copy() + g2_edges.copy()

    return nodes, edges, g1_nodes, g1_edges, g2_nodes, g2_edges
