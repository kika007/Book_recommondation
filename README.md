# Book Recommendation System

This project is a book recommendation system built from user ratings and book metadata. It prepares the Book-Crossing-style dataset, computes item-to-item similarity with collaborative filtering, and provides an interactive Streamlit interface for finding books similar to a selected title, with an author-based fallback for books that are not covered by the similarity model.

## Main Features
* Interactive Streamlit search by partial book title, followed by book selection and up to five recommendations.
* Item-based collaborative filtering using cosine similarity over an item-user rating matrix.
* Data preparation pipeline that merges ratings with book metadata, removes ratings of zero, and filters to active users and sufficiently rated books.
* Author-based fallback recommendations when the selected ISBN is missing from the trained similarity matrix.
* Jupyter notebook analysis with dataset diagnostics, activity distributions, sparsity checks, similarity examples, and pickle model export.

## Used Technologies
**User Interface:** Streamlit

**Data Processing:** pandas, NumPy

**Machine Learning:** scikit-learn (`cosine_similarity`)

**Sparse Computation:** SciPy (`csr_matrix`)

**Analysis and Visualization:** Jupyter Notebook, Matplotlib, Seaborn

**Model Serialization:** Python `pickle`

**Runtime:** Python 3.13 was used for the notebook kernel

## Installation and Setup

No `requirements.txt`, `environment.yml`, `pyproject.toml`, or other dependency lockfile is currently included, so create the environment and install the dependencies directly:

```bash
conda create -n book-recommender python=3.13 -y
conda activate book-recommender
python -m pip install pandas numpy matplotlib seaborn scipy scikit-learn streamlit jupyter
```

Run all commands from the project root, the directory containing `demo.py`, `analysis.ipynb`, and `archive/`.

## Data / Dataset Preparation

The project expects the following files under `archive/`:

```text
archive/
├── Books.csv
├── Ratings.csv
└── Users.csv
```

The files must be comma-separated CSV files with these columns:

* `Books.csv`: `ISBN`, `Book-Title`, `Book-Author` and the remaining book metadata columns.
* `Ratings.csv`: `User-ID`, `ISBN`, `Book-Rating`.
* `Users.csv`: `User-ID`, `Location`, `Age`.

The notebook loads the three files, joins ratings with books on `ISBN`, discards ratings whose ISBN is missing from `Books.csv`, and keeps only explicit ratings where `Book-Rating > 0`. For the similarity calculation it then keeps users with more than 40 ratings and books with at least 10 ratings. The resulting item-user matrix is converted to a SciPy CSR matrix and item-to-item cosine similarities are calculated.

The trained model is exported as `book_recommender_model.pkl` in the project root. Because pickle model files are ignored by Git, a fresh clone must generate this file locally before starting the app. The current Streamlit application loads this root-level path and also reads `archive/Books.csv`.

## Usage

1. Generate the similarity model:

   ```bash
   jupyter notebook analysis.ipynb
   ```

   Run the notebook cells in order. The export cell writes `book_recommender_model.pkl` to the project root.

2. Start the interactive application:

   ```bash
   streamlit run demo.py
   ```

3. In the app, enter part of a title, choose one of the matching books, and select **Find me books**. Recommendations are obtained from item similarity when available; otherwise, the app returns other books by the same author.