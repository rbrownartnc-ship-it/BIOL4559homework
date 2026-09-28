"""Can the data test "higher consumers are more connected / have more diverse
diets"? Rank-correlates trophic level with each kind of degree and with
weighted diet diversity, across the 40 consumers. Run build_network.py first.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

nodes = pd.read_csv("data/processed/cadiz_nodes.csv", index_col=0)
edges = pd.read_csv("data/processed/cadiz_edges.csv")
edges = edges[edges.prey != edges.predator]          # cannibalism excluded


def effective_prey(g):
    """exp(Shannon entropy) of the diet: 'how many equally used prey'."""
    p = g.diet_share / g.diet_share.sum()
    return np.exp(-(p * np.log(p)).sum())


nodes["effective_prey"] = edges.groupby("predator").apply(effective_prey)
nodes["total_degree"] = nodes.n_prey + nodes.n_predators
consumers = nodes[nodes.n_prey > 0]                   # basal groups have no diet

print(f"consumers: {len(consumers)}")
for col in ["n_prey", "n_predators", "total_degree", "effective_prey"]:
    rho, p = spearmanr(consumers.trophic_level, consumers[col])
    print(f"trophic level vs {col:15s} rho = {rho:+.2f}   p = {p:.2g}")

print("\nhighest total degree:")
print(nodes.nlargest(5, "total_degree")
      [["trophic_level", "n_prey", "n_predators", "total_degree"]])
