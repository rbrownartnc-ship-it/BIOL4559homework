# BIOL4559 Homework

Coursework repository for BIOL 4559 (University of Virginia).

## Environment setup

This repo uses a conda environment named `biol4559` running Python 3.13.

```bash
conda create -n biol4559 python=3.13
conda activate biol4559
pip install -r requirements.txt
python -m ipykernel install --user --name biol4559 --display-name "Python (BIOL4559)"
```

Then launch the notebook server:

```bash
jupyter notebook
```

Select the **Python (BIOL4559)** kernel when opening a notebook.

## Contents

- `requirements.txt` — package list for the course environment
- Lab notebook — see below

