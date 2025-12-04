import uuid

from models import Chunk


def split_text(text: str, document_id: str, source_file: str, chunk_size: int = 500, overlap: int = 50) -> list[dict]:
    """
    Split the input text into chunks of specified size with overlap.
    
    Args:
        text (str): The input text to be split.
        document_id (str): The ID of the document.
        source_file (str): The source file name.
        chunk_size (int): The size of each chunk.
        overlap (int): The number of overlapping characters between chunks.
        
    Returns:
        list[dict]: A list of dictionaries containing chunk text and metadata.
    """
    chunks = []
    start = 0
    chunk_index = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk_text = text[start:end]
        
        chunks.append(Chunk(
            text=chunk_text,
            metadata= {
                "documentid": document_id,
                "sourcefile": source_file,
                "chunk_index": chunk_index
            }
        ))
        
        chunk_index += 1
        start += chunk_size - overlap  # Move start forward with overlap
    
    return chunks