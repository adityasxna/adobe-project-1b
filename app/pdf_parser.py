import pdfplumber

def parse_pdf(pdf_path):
    """
    Opens a PDF and extracts a list of text spans by grouping words.
    This version uses the pdfplumber library.
    """
    all_spans = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                # Extract words and group them into lines/spans
                words = page.extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False, use_text_flow=True, extra_attrs=["size", "fontname"])

                if not words:
                    continue

                # Group words with the same properties into a single span
                current_span = words[0]
                current_span['page'] = i + 1

                for w in words[1:]:
                    # Check if the next word has the same font and size, and is on the same line
                    if (w['fontname'] == current_span['fontname'] and 
                        abs(w['size'] - current_span['size']) < 0.1 and 
                        abs(w['top'] - current_span['top']) < 5):
                        current_span['text'] += ' ' + w['text'] # Merge text
                    else:
                        # End of the current span, save it
                        all_spans.append({
                            "text": current_span.get("text"),
                            "size": current_span.get("size"),
                            "font": current_span.get("fontname"),
                            "page": current_span.get("page"),
                        })
                        # Start a new span
                        current_span = w
                        current_span['page'] = i + 1

                # Add the very last span
                all_spans.append({
                    "text": current_span.get("text"),
                    "size": current_span.get("size"),
                    "font": current_span.get("fontname"),
                    "page": current_span.get("page"),
                })

    except Exception as e:
        print(f"---! ERROR USING PDFPLUMBER !---")
        print(f"The error is: {e}")
        print("---------------------------------")
        return []

    return all_spans