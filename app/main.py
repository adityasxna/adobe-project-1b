# app/main.py (Updated for Round 1B)
import os
import json
from section_extractor import extract_sections_from_pdf
from semantic_analyzer import rank_sections_by_relevance

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def process_for_round1b():
    print("Starting Round 1B processing...")
    
    # In Round 1B, the input directory has a specific structure
    pdf_path = os.path.join(INPUT_DIR, "document.pdf")
    json_outline_path = os.path.join(INPUT_DIR, "outline.json")
    query_path = os.path.join(INPUT_DIR, "query.json")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # 1. Load the query
    with open(query_path, 'r') as f:
        query_data = json.load(f)
    persona = query_data["persona"]
    job_description = query_data["job_description"]

    # 2. Extract content for each section using the PDF and the 1A outline
    print("Extracting sections from PDF...")
    sections = extract_sections_from_pdf(pdf_path, json_outline_path)

    # 3. Rank the sections semantically
    print("Ranking sections by relevance...")
    ranked_sections = rank_sections_by_relevance(sections, persona, job_description)

    # 4. Generate the final JSON output
    final_output = {"ranked_sections": []}
    for section in ranked_sections:
        final_output["ranked_sections"].append({
            "importance_rank": section["importance_rank"],
            "level": section["level"],
            "page": section["page"],
            "heading": section["heading_text"],
            "relevance_score": section["relevance_score"]
        })

    output_path = os.path.join(OUTPUT_DIR, "result.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4)
        
    print(f"Successfully generated Round 1B result at {output_path}")

if __name__ == "__main__":
    # You would switch between these functions based on which round you're submitting for.
    # For Round 1B submission, you'd only call process_for_round1b().
    process_for_round1b()