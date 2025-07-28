# app/section_extractor.py
import fitz
import json

def extract_sections_from_pdf(pdf_path, json_outline_path):
    """
    Extracts the full text content for each section defined in the JSON outline.
    """
    with open(json_outline_path, 'r') as f:
        outline = json.load(f)["outline"]
    
    doc = fitz.open(pdf_path)
    sections = []

    for i, heading in enumerate(outline):
        start_page = heading["page"]
        
        # Find the text block for the current heading to get its y-coordinate
        heading_text_instances = doc[start_page - 1].search_for(heading["text"])
        if not heading_text_instances:
            continue
        start_bbox = heading_text_instances[0]
        
        # Determine the end of the section
        if i + 1 < len(outline):
            next_heading = outline[i+1]
            end_page = next_heading["page"]
            next_heading_instances = doc[end_page - 1].search_for(next_heading["text"])
            end_bbox = next_heading_instances[0] if next_heading_instances else None
        else:
            # Last section goes to the end of the document
            end_page = len(doc)
            end_bbox = None

        # Extract text within the bounds
        section_text = ""
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num - 1]
            # Define the clipping rectangle for text extraction
            clip_rect = fitz.Rect(page.rect.tl, page.rect.br) # Full page initially

            if page_num == start_page:
                clip_rect.y0 = start_bbox.y1 # Start after the heading

            if page_num == end_page and end_bbox:
                clip_rect.y1 = end_bbox.y0 # End before the next heading
            
            # If start and end are on the same page, combine the y-bounds
            if start_page == end_page and end_bbox:
                clip_rect = fitz.Rect(start_bbox.bl, end_bbox.tr)

            text = page.get_text("text", clip=clip_rect)
            section_text += text
            
        sections.append({
            "level": heading["level"],
            "heading_text": heading["text"],
            "page": heading["page"],
            "section_content": section_text.strip().replace("\n", " ")
        })

    doc.close()
    return sections
