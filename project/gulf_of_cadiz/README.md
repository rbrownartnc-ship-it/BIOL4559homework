# Gulf of Cadiz food web (Web of Life FW_005)

```bash
conda activate biol4559
python build_network.py
```

Rebuilds everything in `data/processed/` and `figures/` from `data/raw/`.

## Data
- `data/raw/FW_005.csv`: 44 x 44 diet matrix from the Web of Life download, no labels.
  Rows are prey, columns are predators, and each cell is the fraction of the predator's diet.
- `data/raw/FW_005_species_api.csv` and `FW_005_edges_api.json`: group names and the named edge list,
  from `web-of-life.es/get_species_info.php` and `get_networks.php?network_name=FW_005`.
  The matrix is in alphabetical name order, and the script checks that against all 413 edges.
- `data/raw/references.csv`, `README_weboflife.txt`: the citation and terms that came with the download.

Source: Torres, Coll, Heymans, Christensen & Sobrino (2013), *Ecological Modelling* 265:26–44,
doi:10.1016/j.ecolmodel.2013.05.019. Web of Life asks users to acknowledge
"This work has used the Web of Life database (www.web-of-life.es)".

## Outputs
- `data/processed/cadiz_edges.csv`: prey, predator, diet_share (411 edges)
- `data/processed/cadiz_nodes.csv`: group, prey/predator counts, summed diet share, trophic level, role
- `data/processed/cadiz_foodweb.graphml`: the weighted DiGraph (prey → predator)
- `data/processed/summary.txt`: every number the script prints
- `figures/cadiz_foodweb.png`, `figures/cadiz_diet_matrix.png`
