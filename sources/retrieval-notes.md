# Lexical retrieval first

Start with [[BM25]] over markdown. You can print the score, you can explain a miss, and you can snapshot the index as "whatever files are in notes/".

A miss that you can explain is better than a near-miss from a black-box embedding.

## Query hygiene

Lowercase, drop stopwords, keep codes and versions (`k1`, `bm25`, `gpt`). Repeat the title in the searchable field so a note named "How agents remember things" wins the obvious query.

## When embeddings help

Use vectors when the user never shares tokens with the note. Until the corpus is large enough that lexical search collapses, do not add a model just to look modern.
