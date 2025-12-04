from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import logging

from agent import run_agent, stream_agent_response
from models import ChatMessage


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])

# In-memory session storage (replace with database in production)
sessions = {}

@router.get("/stream")
async def stream_chat(
    session_id: str = Query(..., description="Session ID for conversation history"),
    question: str = Query(..., description="User's question"),
):
    """
    Stream chat response with RAG integration.
    
    Args:
        session_id: Unique session identifier for conversation history.
        question: User's question/message.
        
    Yields:
        Response tokens/chunks streamed in real-time.
    """
    logger.info(f"Session: {session_id}, Question: {question}")
    
    try:
        if session_id not in sessions:
            sessions[session_id] = []
        
        conversation_history = sessions[session_id]
        run = run_agent(question, conversation_history)
        
        return StreamingResponse(run, media_type="text/event-stream")
        
    except Exception as e:
        logger.error(f"Chat streaming error: {str(e)}")
        return StreamingResponse(
            iter([f"Error: {str(e)}"]),
            status_code=500,
            media_type="text/plain"
        )
    
@router.get("/simple")
async def simple_chat(
    question: str = Query(..., description="User's question"),
):
    """
    Simple chat endpoint without streaming.
    
    Args:
        question: User's question/message.
        
    Returns:
        Full response string.
    """
    print("Simple chat called")
    logger.info(f"Simple Chat Question: {question}")
    
    try:
                
        full_response = await run_agent(question)
        
        return {"response": full_response}
        
    except Exception as e:
        logger.error(f"Simple chat error: {str(e)}")
        return {"error": str(e)}