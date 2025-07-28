# Intelligent Document Section Summarizer

This project provides a solution for intelligently extracting and summarizing relevant sections from a PDF document based on a user-defined persona and job description. It uses a hybrid approach, leveraging cloud services for robust PDF parsing and local machine learning models for efficient semantic analysis.

---

## Our Approach

The solution processes documents through a multi-stage pipeline to ensure accurate and relevant information extraction:

1.  **PDF Parsing**: The system first uses the **Adobe PDF Services SDK** to parse the input PDF. This cloud-based service accurately extracts text, tables, and structural elements from the document, preserving its layout and content fidelity.

2.  **Section Segmentation**: Using a provided `outline.json` file, the system identifies the document's primary headings. It then segments the parsed content, grouping text and tables under their corresponding headings.

3.  **Semantic Analysis**: This is the core of the intelligent extraction. The user's query (a persona and job description from `query.json`) and each document section are converted into vector embeddings using a local **Sentence Transformer model (`all-MiniLM-L6-v2`)**.

4.  **Relevance Scoring**: The system calculates the cosine similarity between the user query's vector and each section's vector. Sections with the highest similarity scores are deemed most relevant to the user's needs.

5.  **Output Generation**: The top N most relevant sections are compiled into a final `output.json` file, providing a focused and actionable summary of the document.

---

## Models and Libraries

### Key Libraries
* **Adobe PDF Services SDK**: The primary tool for robust, cloud-based extraction of content from PDF files.
* **Sentence-Transformers**: A Python framework for state-of-the-art sentence, text, and image embeddings.
* **PyTorch**: The backend framework used by Sentence-Transformers to run the ML model.
* **Scikit-learn**: Used for its efficient `cosine_similarity` function to compare vector embeddings.

### Machine Learning Model
* **`all-MiniLM-L6-v2`**: This is a lightweight and high-performance Sentence Transformer model. It excels at creating meaningful vector embeddings from text, making it ideal for semantic search and relevance scoring tasks. The model is included in the `/models` directory and runs entirely locally within the Docker container, requiring no internet connection for the analysis phase.

---

## How to Build and Run

### 1. Prerequisites
Before running the container, you must prepare the `app/input` directory. It must contain the following three files:

* **`document.pdf`**: The PDF file you want to analyze.
* **`outline.json`**: A JSON file that describes the heading structure of your PDF.
    ```json
    {
      "outline": [
        { "level": 1, "text": "Introduction", "page": 1 },
        { "level": 2, "text": "Market Analysis", "page": 2 }
      ]
    }
    ```
* **`query.json`**: A JSON file containing the persona and job description for the analysis.
    ```json
    {
      "persona": "A financial analyst",
      "job_description": "Looking for market growth projections and financial risks."
    }
    ```

### 2. Build the Docker Image
Navigate to the project's root directory (where the `Dockerfile` is located) and run the build command:
```bash
docker build -t adobe-summarizer .
```
### 3. Run the solution
Once the image is built, you can run the container using the following command. This command mounts your local `input` and `output` directories into the container.
```bash
docker run --rm -v "$(pwd)/app/input:/app/input" -v "$(pwd)/app/output:/app/output" adobe-summarizer
```
The program will start processing the files. Upon completion, the results will be saved to a new JSON file inside your `app/output` directory.