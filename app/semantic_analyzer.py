# app/semantic_analyzer.py
from sentence_transformers import SentenceTransformer, util
import torch

# Load the model from the local path inside the Docker container
MODEL_PATH = "/app/models/all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_PATH)

def rank_sections_by_relevance(sections, persona, job_description):
    """
    Ranks document sections based on semantic similarity to a persona and job description.
    """
    if not sections:
        return []

    # Combine persona and job description into a single query for better context
    query = f"Persona: {persona}. Job Description: {job_description}"
    
    # Generate embeddings
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    section_contents = [s["section_content"] for s in sections]
    section_embeddings = model.encode(section_contents, convert_to_tensor=True)
    
    # Calculate cosine similarity
    cosine_scores = util.cos_sim(query_embedding, section_embeddings)
    
    # Pair sections with their scores and rank them
    ranked_sections = []
    for i, section in enumerate(sections):
        section["relevance_score"] = round(cosine_scores[0][i].item(), 4)
        ranked_sections.append(section)
        
    # Sort by relevance score in descending order
    ranked_sections.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    # Add the importance_rank
    for rank, section in enumerate(ranked_sections):
        section["importance_rank"] = rank + 1
        
    return ranked_sections