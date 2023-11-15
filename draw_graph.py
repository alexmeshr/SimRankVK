import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm
import PIL
from SimRank import simrank


def print_graph(matr, photos, images_dir, spring_k=0.3, similarity_C=0.8, image_scale_factor=0.01, edge_scale_factor=1):
    images = {i: PIL.Image.open(images_dir+"/image_{}.png".format(i)) for i in range(photos.size)}
    #labels = {i:str(users[i]) for i in range(users.size)}
    rows, cols = np.where(matr==1)
    edges = zip(rows.tolist(), cols.tolist())
    G = nx.Graph()
    for i in range(photos.size):
        G.add_node(i, image=images[i])
    G.add_edges_from(edges)
    pos = nx.spring_layout(G, seed=3113794652, k=spring_k)

    print("running the simrank algorithm")
    S = simrank(matr, C=similarity_C)
    print("simrank completed, drawing graph")

    ax = plt.gca()
    fig = plt.gcf()
    tr_figure = ax.transData.transform
    tr_axes = fig.transFigure.inverted().transform
    M = G.number_of_edges()
    edge_colors = np.zeros(M, dtype=float)
    for i, e in enumerate(G.edges):
        edge_colors[i] = S[e]
    edge_widths = edge_colors / edge_colors.max()*edge_scale_factor
    cmap = mpl.cm.get_cmap('viridis')
    nx.draw_networkx_edges(
        G,
        pos=pos,
        ax=ax,
        min_source_margin=0,
        min_target_margin=0,
        width=edge_widths,
        edge_color=edge_colors,
        edge_cmap=cmap,
    )
    pc = mpl.collections.PatchCollection(edges, cmap=cmap)
    pc.set_array(edge_colors)
    plt.colorbar(pc, ax=ax)
    #nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="purple")
    pos_lower = {}
    icon_size_x = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.01
    icon_size_y = (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.01
    icon_center = icon_size_x / 2.0
    for i, n in enumerate(G.nodes):
        size_coef =np.sqrt(matr[i].sum()*image_scale_factor)
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))
        # get overlapped axes and plot icon
        a = plt.axes([xa - icon_center*size_coef, ya - icon_center*size_coef, icon_size_x*size_coef, icon_size_y*size_coef])
        pos_lower[i] = (pos[n][0], pos[n][1] - 0.001*size_coef)
        a.imshow(G.nodes[n]["image"], aspect='auto', )
        a.axis("off")


#plt.savefig('MSU_Sarov_2000dpi.png', dpi=2000, bbox_inches='tight', pad_inches=0)
#plt.show()


"""


"""
