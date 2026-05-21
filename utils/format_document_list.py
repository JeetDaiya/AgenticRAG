from langchain_core.documents import Document

def format_document_list(docs : list[Document]):
    """Gives a formatted string based on given {docs}, the string contains the metadata with content"""
    formatted_chunks = []
    for i, doc in enumerate(docs):
        metadata = doc.metadata
        dl_meta = metadata.get("dl_meta", {})
        
        # --- Extract Heading ---
        headings = dl_meta.get("headings", [])
        section = headings[0] if headings else "Unknown Section"
        
        # --- Extract Page Numbers ---
        pages = set()
        for item in dl_meta.get("doc_items", []):
            for prov in item.get("prov", []):
                if "page_no" in prov:
                    pages.add(prov["page_no"])
        
        # Format the page string (e.g., "54" or "54-55")
        if len(pages) == 1:
            page_str = str(list(pages)[0])
        elif len(pages) > 1:
            sorted_pages = sorted(list(pages))
            page_str = f"{sorted_pages[0]}-{sorted_pages[-1]}"
        else:
            page_str = "Unknown"
            
        # --- Build Final String ---
        header = f"--- Source {i+1} | Page(s): {page_str} | Section: {section} ---"
        formatted_chunks.append(f"{header}\n{doc.page_content}")
    
    formatted_string = "\n\n".join(formatted_chunks)
    
    return formatted_string
