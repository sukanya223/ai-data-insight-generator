from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve_columns(query, columns):
    corpus = list(columns) + [query]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(corpus)

    query_vec = vectors[-1]
    col_vecs = vectors[:-1]

    sims = cosine_similarity(query_vec, col_vecs).flatten()
    top_idx = sims.argsort()[-3:][::-1]

    return [columns[i] for i in top_idx]


def retrieve_rows(df, query, top_k=5):
    row_text = df.astype(str).agg(" ".join, axis=1)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(list(row_text) + [query])

    query_vec = vectors[-1]
    row_vecs = vectors[:-1]

    sims = cosine_similarity(query_vec, row_vecs).flatten()
    top_idx = sims.argsort()[-top_k:][::-1]

    return df.iloc[top_idx]