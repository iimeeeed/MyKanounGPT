# KanounGPT

KanounGPT is an early retrieval-augmented generation (RAG) experiment for Algerian law. Its goal is to make issues of the *Journal officiel de la République algérienne* easier to search and, eventually, to question in natural language.

The repository currently covers the data pipeline: downloading Arabic editions of the official journal, extracting their text with OCR, preparing the documents, generating embeddings, and storing those embeddings in a FAISS index. The conversational answer-generation layer is not implemented yet, so this should be treated as a research prototype rather than a finished legal assistant.

## How it works

The pipeline is split into a few small scripts and notebooks:

1. `scrape.ipynb` downloads Arabic PDF issues from `joradp.dz` and stores them by year under `joradp/`.
2. `model.py` renders each PDF as images and runs Arabic Tesseract OCR. The resulting text files are written to `extracted_texts/`.
3. `remove_pages.py` removes the cover and table-of-contents material by keeping text from `Page 2` onward.
4. `add_info.py` adds the year and issue number inferred from filenames such as `A1995001.txt`.
5. `json_converter.py` can split OCR output into page-level JSON. `correct_json.py` is an optional Arabic correction experiment.
6. `rag.ipynb` embeds each complete text file with `all-MiniLM-L6-v2`, normalizes the vectors, and inserts them into a FAISS `IndexFlatIP`.

After normalization, inner-product search is equivalent to cosine similarity. `IndexFlatIP` was chosen because it is simple and exact: it does not require training and is a reasonable baseline for a corpus of this size. The tradeoff is that search time and memory use grow linearly with the number of documents.

The repository includes `vector_index_cosine.faiss`, a generated index with 384-dimensional vectors.

## Why these choices

- **The official journal as the source.** It gives the project a primary, authoritative corpus instead of relying on summaries or third-party legal websites.
- **OCR instead of PDF text extraction.** Many journal issues are scans, so there is no dependable embedded text layer to parse.
- **One vector per issue.** This keeps indexing straightforward and preserves document-level context. It is a useful first baseline, although it is too coarse for precise article-level retrieval.
- **Local embeddings and FAISS.** Embedding and retrieval can run locally without sending the legal corpus to an external service.
- **Notebooks for exploration.** The project is still experimental, and notebooks make each stage easy to inspect and change.

## Running the project

Python 3.10 or 3.11 is recommended. To reproduce the complete pipeline, you also need:

- Tesseract OCR with the Arabic language data;
- Poppler, used by `pdf2image` to render PDF pages;
- Jupyter Notebook or JupyterLab.

From the project directory, create an environment and install the Python dependencies:

```bash
cd KanounGPT
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Then install the packages used by the pipeline:

```bash
python -m pip install jupyter requests pytesseract pdf2image pillow numpy sentence-transformers faiss-cpu ar-corrector
```

Open the notebooks with:

```bash
jupyter lab
```

Run `scrape.ipynb` to download the source PDFs. This may take a long time and use significant disk space because the notebook scans issues from 1964 through 2024.

Before running the OCR stage, edit these two values near the top of `model.py` so they match your installation:

```python
pytesseract.pytesseract.tesseract_cmd = "/path/to/tesseract"
poppler_path = "/path/to/poppler/bin"
```

The checked-in values are Homebrew paths from one macOS machine and will not work everywhere. Once configured, run:

```bash
python model.py
python remove_pages.py
python add_info.py
```

The page-level JSON path is optional:

```bash
python json_converter.py
python correct_json.py
```

Finally, open `rag.ipynb` and run its vectorization and FAISS cells. This reads `extracted_texts/`, creates intermediate `.npy` files under `vectorized_texts/`, and writes `vector_index_cosine.faiss`.

To check that the included index can be loaded:

```bash
python -c "import faiss; i = faiss.read_index('vector_index_cosine.faiss'); print(i.ntotal, i.d)"
```

There is currently no command that starts a chat interface. The section intended to connect retrieval to LangChain and Gemini is empty.

## Repository layout

```text
KanounGPT/
├── scrape.ipynb                 # Download official-journal PDFs
├── model.py                     # PDF rendering and Arabic OCR
├── remove_pages.py              # Remove material before page 2
├── add_info.py                  # Add year and issue metadata
├── json_converter.py            # Convert page-marked text to JSON
├── correct_json.py              # Experimental Arabic text correction
├── preprocessing.ipynb          # One-document correction experiment
├── rag.ipynb                    # Embedding and FAISS index construction
├── test.ipynb                   # Unrelated LangChain/RAG experiment
├── output_file.txt              # Example corrected OCR output
└── vector_index_cosine.faiss    # Generated vector index
```

The downloaded PDFs, extracted text, JSON files, and intermediate vectors are not included in the repository.

## Current limitations

- **No question-answering layer.** Retrieval is prepared, but query embedding, source lookup, prompt construction, answer generation, and a user interface are still missing.
- **The index is not self-describing.** The ordered `file_ids` list used while building FAISS is kept only in notebook memory and is not saved beside the index. The included index therefore cannot reliably map a result back to its source document.
- **Retrieval units are too large.** A whole journal issue is represented by one vector. Long issues can cover unrelated subjects, making relevant articles hard to retrieve.
- **The embedding model is not Arabic-specific.** `all-MiniLM-L6-v2` is a compact English-oriented baseline. A multilingual or Arabic legal-domain model should give more meaningful similarity scores.
- **OCR quality varies.** Scans, Arabic typography, tables, page layout, and older print quality introduce errors. The sample output also shows encoding artifacts that need to be resolved before dependable retrieval.
- **Preprocessing is destructive and heuristic.** `remove_pages.py` overwrites files and assumes that useful content begins at `Page 2`. `add_info.py` also modifies files in place.
- **The scripts are machine-specific.** OCR paths are hard-coded for macOS, directory names are fixed, and `model.py` currently filters filenames to the 2005–2015 range.
- **The downloader is brittle.** It stops processing a year at the first `404`, assumes issue numbers are contiguous, and does not implement retries, rate limiting, or resumable downloads.
- **There is no evaluation set.** Retrieval accuracy and OCR quality have not been measured against labelled legal questions or verified transcriptions.
- **Legal reliability is not established.** Generated answers would need citations, date/version handling, and review by a qualified person. This project must not be used as a substitute for professional legal advice.

## Sensible next steps

The next useful milestone is a small retrieval-only command that chunks issues by page or article, saves metadata next to every vector, embeds Arabic queries with a multilingual model, and returns the best passages with issue and page references. An LLM can be added after that retrieval path has been evaluated.

Before publishing or sharing the repository, remove any credentials from experimental notebooks and rotate credentials that may already have been exposed.
