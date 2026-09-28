"""Gulf of Cadiz food web (Web of Life FW_005): clean, build, and profile
a weighted directed predator-prey network.

Source: Torres et al. 2013, Ecological Modelling 265:26-44, via the Web of
Life database (www.web-of-life.es). Run from this folder:

    python build_network.py
"""
import json
from itertools import combinations
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap, to_rgb
from matplotlib.patches import Rectangle
from matplotlib.transforms import Bbox
from matplotlib.lines import Line2D
from mpl_toolkits.axes_grid1 import make_axes_locatable

RAW = "data/raw"
OUT = "data/processed"
FIG = "figures"

# ---------------------------------------------------------------- load
# FW_005.csv is a bare 44x44 matrix: no header, no row names. Rows are prey
# (resources), columns are predators (consumers), cells are the fraction of
# the column group's diet made up of the row group.
M = np.loadtxt(f"{RAW}/FW_005.csv", delimiter=",")
assert M.shape == (44, 44)

# Names come from the Web of Life API. The matrix is in alphabetical order;
# that is checked cell by cell against the API's named edge list below.
species = pd.read_csv(f"{RAW}/FW_005_species_api.csv")["species"]
names = sorted(species)
idx = {n: i for i, n in enumerate(names)}

api = pd.DataFrame(json.load(open(f"{RAW}/FW_005_edges_api.json")))
api["w"] = api["connection_strength"].astype(float)
assert len(api) == (M > 0).sum() == 413
for r in api.itertuples():
    assert M[idx[r.species1], idx[r.species2]] == r.w, (r.species1, r.species2)

report = []
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    report.append(line)

log("== raw ==")
log(f"groups: {len(names)}   links (nonzero cells): {(M > 0).sum()}")
log("name <-> matrix mapping verified on all 413 links")

# every consumer's diet should sum to 1
colsum = M.sum(axis=0)
consumers = [n for n in names if colsum[idx[n]] > 0]
dev = max(abs(colsum[idx[n]] - 1) for n in consumers)
log(f"consumers: {len(consumers)}   max |diet sum - 1| = {dev:.4f}")

# ---------------------------------------------------------------- clean
# "Import" is not a functional group. In Ecopath it is the share of a
# predator's diet eaten outside the model area. The paper's model has 43
# groups; Import is the 44th row.
imp = M[idx["Import"]]
log("\n== cleaning ==")
for n in names:
    if imp[idx[n]] > 0:
        log(f"Import in diet of {n}: {imp[idx[n]]:.3f}")
keep = [n for n in names if n != "Import"]
M = M[np.ix_([idx[n] for n in keep], [idx[n] for n in keep])]
names = keep
idx = {n: i for i, n in enumerate(names)}
log(f"dropped Import -> {len(names)} groups, {(M > 0).sum()} links")

NONLIVING = {"Detritus", "Discard"}
VERTEBRATES = {"Seabirds", "Killer whales", "Dolphins", "Loggerhead turtles"}
FISHES = {"Sharks", "Demersal piscivores", "Anglerfishes", "Skates",
          "Adult hake", "Juvenile hake", "Mackerels", "Horse mackerels",
          "Deep-sea fishes", "Large benthopelagic fishes",
          "Small benthopelagic fishes", "Flatfishes", "Demersal fishes",
          "Mullets", "Commercial sparids 1", "Commercial sparids 2",
          "Blue whiting", "Small demersal fishes", "Anchovy", "Sardine"}
def group(n):
    if n in NONLIVING:   return "non-living"
    if n in VERTEBRATES: return "marine mammals, birds, turtles"
    if n in FISHES:      return "fishes"
    return "invertebrates & plankton"
assert sum(group(n) == "invertebrates & plankton" for n in names) == 17

# ---------------------------------------------------------------- build
# Edge direction prey -> predator, i.e. the direction energy flows.
# Reverse the graph (G.reverse()) for the "who eats whom" convention.
G = nx.DiGraph()
for n in names:
    G.add_node(n, group=group(n))
for i, j in zip(*np.nonzero(M)):
    G.add_edge(names[i], names[j], weight=float(M[i, j]))

N, L = G.number_of_nodes(), G.number_of_edges()
loops = sorted(nx.nodes_with_selfloops(G))
log("\n== network ==")
log(f"nodes {N}   edges {L}   self-loops (cannibalism) {len(loops)}")
log("cannibals:", ", ".join(loops))
log(f"isolates: {list(nx.isolates(G)) or 'none'}")
log(f"weakly connected components: {nx.number_weakly_connected_components(G)}")
scc = max(nx.strongly_connected_components(G), key=len)
log(f"largest strongly connected component: {len(scc)} of {N}")
log(f"directed connectance L/N^2 = {L / N**2:.3f}   "
    f"(Web of Life's 0.437 uses L/(S(S-1)/2) with S=44)")

w = np.array([d["weight"] for *_, d in G.edges(data=True)])
log(f"weights: min {w.min():g}  median {np.median(w):.3f}  max {w.max():g}")
log(f"links < 0.01: {(w < 0.01).sum()}   < 0.001: {(w < 0.001).sum()}")

# ---------------------------------------------------------------- nodes
# Trophic level, Ecopath style: TL = 1 + sum(diet share x prey TL), basal
# groups = 1. Diets are renormalised without Import for the two groups
# that had it.
D = M / np.where(M.sum(axis=0) > 0, M.sum(axis=0), 1)   # columns sum to 1
TL = np.linalg.solve(np.eye(N) - D.T, np.ones(N))

nodes = pd.DataFrame({
    "group": [group(n) for n in names],
    # generality / vulnerability, not counting the self-loop
    "n_prey": [G.in_degree(n) - (n in loops) for n in names],
    "n_predators": [G.out_degree(n) - (n in loops) for n in names],
    # out-strength: summed share of predator diets this group makes up
    "diet_share_sum": [G.out_degree(n, weight="weight") for n in names],
    "cannibal": [n in loops for n in names],
    "trophic_level": TL.round(3),
}, index=pd.Index(names, name="group_name"))
nodes["role"] = np.select(
    [nodes.n_prey == 0, nodes.n_predators == 0],
    ["basal", "top predator"], "intermediate")

log("\nbasal:", ", ".join(nodes.index[nodes.role == "basal"]))
log("top predators (eaten by no other group):",
    ", ".join(nodes.index[nodes.role == "top predator"]))
log("\nmost prey groups (generalists):")
for n, r in nodes.nlargest(5, "n_prey").iterrows():
    log(f"  {n:28s} {r.n_prey}")
log("most predator groups:")
for n, r in nodes.nlargest(5, "n_predators").iterrows():
    log(f"  {n:28s} {r.n_predators}")
log("largest summed diet share (out-strength):")
for n, r in nodes.nlargest(5, "diet_share_sum").iterrows():
    log(f"  {n:28s} {r.diet_share_sum:.2f}")
log("highest trophic level:")
for n, r in nodes.nlargest(5, "trophic_level").iterrows():
    log(f"  {n:28s} {r.trophic_level:.2f}")

# How fragile is the web to the modelling choice of keeping detritus?
H = G.copy()
H.remove_nodes_from(NONLIVING)
log(f"\nwithout Detritus/Discard: {H.number_of_nodes()} nodes, "
    f"{H.number_of_edges()} edges, isolates {list(nx.isolates(H)) or 'none'}, "
    f"weak components {nx.number_weakly_connected_components(H)}")

# ---------------------------------------------------------------- save
edges = pd.DataFrame([(u, v, d["weight"]) for u, v, d in G.edges(data=True)],
                     columns=["prey", "predator", "diet_share"])
edges.sort_values(["predator", "diet_share"], ascending=[True, False]) \
     .to_csv(f"{OUT}/cadiz_edges.csv", index=False)
nodes.to_csv(f"{OUT}/cadiz_nodes.csv")
for n in G:
    G.nodes[n]["trophic_level"] = float(nodes.at[n, "trophic_level"])
nx.write_graphml(G, f"{OUT}/cadiz_foodweb.graphml")
with open(f"{OUT}/summary.txt", "w") as f:
    f.write("\n".join(report) + "\n")

# ---------------------------------------------------------------- figures
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e1e0d9"
GROUP_COLOR = {"invertebrates & plankton": "#2a78d6", "fishes": "#eb6834",
               "marine mammals, birds, turtles": "#1baf7a",
               "non-living": "#898781"}
plt.rcParams.update({"font.family": "sans-serif", "font.size": 9,
                     "text.color": INK, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2})
group_handles = [Line2D([], [], marker="s", ls="", color=c, markersize=8, label=g)
                 for g, c in GROUP_COLOR.items()]

# 1. Diet matrix, both axes ordered by trophic level. Group identity sits in
# a colour strip beside each axis so the labels can stay in ink.
order = list(nodes.sort_values("trophic_level").index)
A = M[np.ix_([idx[n] for n in order], [idx[n] for n in order])]
cmap = LinearSegmentedColormap.from_list(
    "blue", ["#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
strip = np.array([[to_rgb(GROUP_COLOR[group(n)])] for n in order])

fig, ax = plt.subplots(figsize=(10.5, 10))
im = ax.imshow(np.ma.masked_equal(A, 0), cmap=cmap,
               norm=LogNorm(vmin=1e-4, vmax=1), interpolation="none")
div = make_axes_locatable(ax)
sl = div.append_axes("left", size="1.6%", pad=0.04, sharey=ax)
sb = div.append_axes("bottom", size="1.6%", pad=0.04, sharex=ax)
sl.imshow(strip, aspect="auto", interpolation="none")
sb.imshow(strip.transpose(1, 0, 2), aspect="auto", interpolation="none")
sl.set_yticks(range(N), order)
sl.set_xticks([])
sb.set_xticks(range(N), order, rotation=90)
sb.set_yticks([])
sl.set_ylabel("prey (resource)")
sb.set_xlabel("predator (consumer)")
ax.tick_params(labelleft=False, labelbottom=False, left=False, bottom=False)
for a in (sl, sb):
    a.tick_params(length=0)
    for sp in a.spines.values():
        sp.set_visible(False)
ax.set_xticks(np.arange(-.5, N), minor=True)
ax.set_yticks(np.arange(-.5, N), minor=True)
ax.grid(which="minor", color=GRID, lw=0.4)
ax.tick_params(which="minor", length=0)
for sp in ax.spines.values():
    sp.set_color(GRID)
for k, n in enumerate(order):               # outline cannibalism cells
    if n in loops:
        ax.add_patch(Rectangle((k - .5, k - .5), 1, 1, fill=False,
                               edgecolor=INK, lw=0.9))
cax = div.append_axes("right", size="2.2%", pad=0.2)
cb = fig.colorbar(im, cax=cax)
cb.set_label("share of predator's diet (log scale; < 1e-4 drawn at floor)")
cb.outline.set_visible(False)
handles = group_handles + [Line2D([], [], marker="s", ls="", markersize=9,
                                  markerfacecolor="none", markeredgecolor=INK,
                                  label="cannibalism (diagonal)")]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False,
           fontsize=8.5, handletextpad=0.3)
fig.subplots_adjust(left=0.24, right=0.9, top=0.98, bottom=0.25)
fig.savefig(f"{FIG}/cadiz_diet_matrix.png", dpi=200)
plt.close(fig)

# 2. Food web: y = trophic level, x from a 1-D force layout (y held fixed),
# then nodes are pushed sideways until no two labels overlap.
rng = np.random.default_rng(4)
y = {n: TL[idx[n]] for n in G}
x = {n: rng.uniform(-1, 1) for n in G}
U = G.to_undirected()
for _ in range(400):
    for n in G:
        pull = np.mean([x[m] for m in U[n] if m != n])
        push = sum(np.sign(x[n] - x[m]) * 0.012 / (abs(x[n] - x[m]) + 0.05)
                   for m in G if m != n and abs(y[n] - y[m]) < 0.35)
        x[n] = 0.85 * x[n] + 0.15 * pull + push
xs = np.array(list(x.values()))
x = {n: (x[n] - xs.min()) / (xs.max() - xs.min()) for n in G}

size = 40 + 260 * np.sqrt(nodes["diet_share_sum"] / nodes["diet_share_sum"].max())
fig, ax = plt.subplots(figsize=(12, 9.5))
fig.subplots_adjust(left=0.06, right=0.98, top=0.98, bottom=0.1)
ax.set_xlim(-0.35, 1.35)
ax.set_ylim(0.8, TL.max() + 0.25)
labels = {n: ax.annotate(n, (x[n], y[n]), xytext=(0, 10 if n in loops else 7),
                         textcoords="offset points", ha="center",
                         va="bottom", fontsize=7.5, color=INK, zorder=4)
          for n in G}
px_per_x = ax.transData.transform((1, 0))[0] - ax.transData.transform((0, 0))[0]
def node_box(n):
    r = (np.sqrt(size[n] + (110 if n in loops else 0)) / 2 + 2) * fig.dpi / 72
    cx, cy = ax.transData.transform((x[n], y[n]))
    return Bbox.from_extents(cx - r, cy - r, cx + r, cy + r)

for _ in range(300):
    fig.canvas.draw()
    # each node owns its marker and its label; no box may touch another node's
    box = {n: [labels[n].get_window_extent().expanded(1.06, 1.25), node_box(n)]
           for n in G}
    moved = False
    for a, b in combinations(G, 2):
        for ba in box[a]:
            for bb in box[b]:
                if ba.overlaps(bb):
                    gap = min(ba.x1, bb.x1) - max(ba.x0, bb.x0)
                    d = (gap / 2 + 1) / px_per_x
                    lo, hi = (a, b) if (x[a], a) < (x[b], b) else (b, a)
                    x[lo] -= d
                    x[hi] += d
                    moved = True
                    break
            else:
                continue
            break
    for n in G:
        labels[n].xy = (x[n], y[n])
    if not moved:
        break
assert not moved, "labels still overlap"
pos = {n: (x[n], y[n]) for n in G}

for u, v, d in sorted(G.edges(data=True), key=lambda e: e[2]["weight"]):
    if u == v:
        continue
    wt = d["weight"]
    ax.annotate("", xy=pos[v], xytext=pos[u],
                arrowprops=dict(arrowstyle="-|>", mutation_scale=6 + 6 * wt,
                                lw=0.25 + 3.2 * wt, color=INK2,
                                alpha=0.07 + 0.6 * wt, shrinkA=6, shrinkB=6,
                                connectionstyle="arc3,rad=0.08"))
for n in G:
    ax.scatter(*pos[n], s=size[n], color=GROUP_COLOR[group(n)],
               edgecolor="white", linewidth=1.2, zorder=3)
    if n in loops:                          # ring marks cannibalism
        ax.scatter(*pos[n], s=size[n] + 110, facecolor="none",
                   edgecolor=INK, linewidth=0.9, zorder=2)
ax.set_ylabel("trophic level")
ax.set_xticks([])
for s in ("top", "right", "bottom"):
    ax.spines[s].set_visible(False)
ax.spines["left"].set_color(GRID)
ax.grid(axis="y", color=GRID, lw=0.5)
ax.set_axisbelow(True)
xs = np.array([p[0] for p in pos.values()])
ax.set_xlim(xs.min() - 0.08, xs.max() + 0.08)   # zooming in only adds space
handles = [Line2D([], [], marker="o", ls="", color=c, markersize=8, label=g)
           for g, c in GROUP_COLOR.items()]
handles += [Line2D([], [], marker="o", ls="", markerfacecolor="none",
                   markeredgecolor=INK, markersize=10,
                   label="cannibalism (self-loop)"),
            Line2D([], [], color=INK2, lw=2.5, alpha=0.6,
                   label="prey → predator, width = diet share")]
fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False,
           fontsize=8.5)
fig.savefig(f"{FIG}/cadiz_foodweb.png", dpi=200)
plt.close(fig)
