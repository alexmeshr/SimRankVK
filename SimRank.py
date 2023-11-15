import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm

def simrank(A, Xi=0.1, C=0.6):
    N = A.shape[0]
    EPS = 0.000001
    A_ = A / A.sum(axis=0)
    A_f = ((1-Xi)*A_ + Xi/N * np.ones((N, N)))
    S = np.eye(N,N)
    cur_d = S.sum()
    prev_d = 0
    i = 1
    while(abs(cur_d-prev_d) > EPS):
        F = A_f.transpose() @ S @ A_f
        S = C * F - C * np.diag(F.diagonal()) + np.eye(N,N)
        i+=1
        if i % 10==0:
            prev_d = cur_d
            cur_d = S.sum()
            #print(cur_d)
    return S

import networkx as nx
if __name__ == '__main__':
    matr = np.load("files/prepared_sarov_matrix.npy")
    S = simrank(matr)
    rows, cols = np.where(matr==1)
    edges = zip(rows.tolist(), cols.tolist())
    G = nx.Graph()
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=3113794652, k=0.3)

    M = G.number_of_edges()
    edge_colors = np.zeros(M, dtype=float)
    for i, e in enumerate(G.edges):
        edge_colors[i] = S[e]
    edge_widths = edge_colors/edge_colors.max()
    print(edge_widths.min())
    cmap = mpl.cm.get_cmap('viridis')

    nodes = nx.draw_networkx_nodes(G, pos, node_color="indigo",node_size = 15,)
    G_edges = nx.draw_networkx_edges(
        G,
        pos,
        node_size=15,
        width=edge_widths*10,
        edge_color=edge_colors,
        edge_cmap=cmap,
    )
    pc = mpl.collections.PatchCollection(edges, cmap=cmap)
    pc.set_array(edge_colors)

    ax = plt.gca()
    ax.set_axis_off()
    plt.colorbar(pc, ax=ax)
    plt.show()