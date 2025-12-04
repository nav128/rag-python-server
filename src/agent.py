
import os
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRequest, RunContext
import logging
from typing import Optional

from vector_store import searchsimilar
from models import ChatMessage, AgentState, MyOutput, SearchResult

logger = logging.getLogger(__name__)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
MAX_HISTORY_MESSAGES_INCLUDE = 20


# Define the agent
rag_agent = Agent(
    model=LLM_PROVIDER,
    system_prompt="""You MUST always begin by calling the search_docs tool.
Do NOT perform reasoning or answer before the search.
Do Not return before searching.
The information is in the text of the result.
If for any reason there were no docs or you werent able to find relevant information in the docs, say you don't know.
Always cite your sources from the search results.
Be concise and accurate in your responses. """,
    output_type=MyOutput,
# validation_context=ensure_search_first,
)


@rag_agent.tool
async def search_docs(ctx: RunContext[AgentState], query: str, top_k: int = 5) -> str:
    """
    Search the document database for relevant chunks.
    
    Args:
        ctx: Agent execution context with conversation history.
        query: Search query string.
        top_k: Number of top results to return.
        
    Returns:
        Formatted search results as a string.
    """
    logger.info(f"Searching docs with query: '{query}'")
    
    try:
        # Get embedding for the query
        from embeddings import get_embedding
        query_embedding = get_embedding(query)
        
        # Search vector store
        results = await searchsimilar(query_embedding, top_k=top_k)
        
        # Format results
        formatted_results = []
        for i, result in enumerate(results, 1):
            search_result = SearchResult(
                chunk_id=result.id,
                text=result.text,
                relevance_score=result.score,
                source_file=result.metadata["sourcefile"]
            )
            # ctx.state.search_results.append(search_result)
            formatted_results.append(
                f"{i}. [{search_result.source_file}] Score: {search_result.relevance_score:.2f}\n"
                f"   {search_result.text[:200]}..."
            )
        
        logger.info(f"Found {len(formatted_results)} results")
        return "\n\n".join(formatted_results) if formatted_results else "No relevant documents found."
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        return f"Error searching documents: {str(e)}"


async def run_agent(
    user_message: str,
    conversation_history: Optional[list[ChatMessage]] = None,
) :
    """
    Run the RAG agent with conversation history.
    
    Args:
        user_message: User's input message.
        conversation_history: Previous chat messages.
        provider: LLM provider to use.
        
    Returns:
        Tuple of (agent_response, updated_conversation_history).
    """
    if conversation_history is None:
        conversation_history = []
    
    # Add user message to history
    conversation_history.append(ChatMessage(role="user", content=user_message))
        

    try:
        # Run agent with PydanticAI
        agent_response = ""  
  
        async with rag_agent.run_stream(
            user_prompt=user_message,
            message_history=conversation_history[-MAX_HISTORY_MESSAGES_INCLUDE:],
            instructions="first search the docs, then answer the question based on the search results.",
        ) as r:
            async for event in r.stream_output():
                if isinstance(event, MyOutput):
                    agent_response += event.message
                    logger.info(f"Agent output chunk: {event.message}")
                    format = event.message.replace('\n', '\\n')
                    yield f"data: {format}\n\n"
              

        yield "data: [end]\n\n" 
        
        # Add agent response to history
        conversation_history.append(ChatMessage(role="assistant", content=agent_response))
        return
        
    except Exception as e:
        logger.error(f"Agent execution error: {str(e)}")
        error_msg = f"Error: {str(e)}"
        conversation_history.append(ChatMessage(role="assistant", content=error_msg))
        yield error_msg
        return


if __name__ == "__main__":
    import asyncio
    async def test_agent():
        user_query = "What can you tell me about moshe and a?"
        response, history = await run_agent(user_query)
        print("Agent Response:", response)


    asyncio.run(test_agent())