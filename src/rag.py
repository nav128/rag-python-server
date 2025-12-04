from embeddings import get_embedding
import vector_store


async def you_know_what(text: str): # relavant vector db results
    # embed
    queryembedding = get_embedding(text)
    # search vector db
    results = await vector_store.searchsimilar(queryembedding, top_k=5)
    # unify chunks into files 
    # each result.metadata has documentid, sourcefile, chunk_index
    documents_map = {}
    for res in results:
        doc_id = res.metadata.get("documentid", "unknown")
        source_file = res.metadata.get("sourcefile", "unknown")
        if doc_id not in documents_map:
            documents_map[doc_id] = {
                "source_file": source_file,
                "chunks": []
            }
        documents_map[doc_id]["chunks"].append(res)
    # sort by chunk_index
    for doc in documents_map.values():
        doc["chunks"].sort(key=lambda x: x.metadata.get("chunk_index", 0))
    return documents_map


if __name__ == "__main__":
    import asyncio
    sample_text = "moshe is short shmuel is tall"
    results = asyncio.run(you_know_what(sample_text))
    for res in results:
        print(f"Score: {res.score}, Text: {res.text}, Metadata: {res.metadata}")