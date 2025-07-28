from collections import Counter

def analyze_and_find_headings(spans):
    """
    Analyzes text spans to identify the Title and H1, H2, H3 headings.
    """
    if not spans:
        return {"title": "No text found in document", "outline": []}

    # Find the most common font size to identify the body text.
    font_sizes = [s["size"] for s in spans]
    most_common_size = Counter(font_sizes).most_common(1)[0][0]

    # Identify all potential headings (larger than body text or bold).
    heading_candidates = [s for s in spans if s["size"] > (most_common_size + 1) or "bold" in s["font"].lower()]
    if not heading_candidates:
        return {"title": "Could not identify a title", "outline": []}

    # Assume the title is the largest text on the first page.
    first_page_candidates = [s for s in heading_candidates if s["page"] == 1]
    title_span = max(first_page_candidates, key=lambda x: x["size"]) if first_page_candidates else max(heading_candidates, key=lambda x: x["size"])
    
    # Cluster the *other* headings by font size to determine their level.
    outline = []
    other_headings = [s for s in heading_candidates if s != title_span]
    
    unique_heading_sizes = sorted(list(set([s["size"] for s in other_headings])), reverse=True)
    
    size_to_level = {}
    if len(unique_heading_sizes) > 0: size_to_level[unique_heading_sizes[0]] = "H1"
    if len(unique_heading_sizes) > 1: size_to_level[unique_heading_sizes[1]] = "H2"
    if len(unique_heading_sizes) > 2: size_to_level[unique_heading_sizes[2]] = "H3"
    
    for s in other_headings:
        if s["size"] in size_to_level:
            outline.append({
                "level": size_to_level[s["size"]],
                "text": s["text"],
                "page": s["page"]
            })

    # Return the final object in the required format.
    return {
        "title": title_span["text"],
        "outline": sorted(outline, key=lambda x: x["page"]) 
    }