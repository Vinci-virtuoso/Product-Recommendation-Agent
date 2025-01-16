import logging
from fastapi import APIRouter, Depends, HTTPException
from src.app.models.chat_models import Query
from src.app.workflows.text2sql_workflow import text2sql_graph
from src.app.database import SessionLocal, User
from sqlalchemy.exc import SQLAlchemyError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

async def validate_user(user_id: str) -> bool:
    """Validate that the user exists in the database."""
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.id == int(user_id)).first()
        return user is not None
    except (ValueError, SQLAlchemyError) as e:
        logger.error(f"Error validating user: {str(e)}")
        return False
    finally:
        db.close()

@router.post("/query")
async def chat(query: Query, graph=Depends(text2sql_graph)):
    logger.info(f"Received query: {query.question} for user: {query.user_id}")
    
    try:
        # Validate user exists
        if not await validate_user(query.user_id):
            logger.error(f"User not found: {query.user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        # Initialize configuration
        config = {"configurable": {"current_user_id": query.user_id}}
        logger.info(f"Initializing graph with config: {config}")

        # Initialize state with all required fields
        initial_state = {
            "question": query.question,
        }
        logger.info(f"Initializing state: {initial_state}")

        # Invoke graph
        result = await graph.ainvoke(initial_state, config=config)
        logger.info(f"Graph execution completed. Result: {result}")
        
        if not result:
            raise HTTPException(status_code=500, detail="Graph execution failed to return a result")
            
        query_result = result.get("query_result")
        if not query_result:
            logger.error("No query_result in graph execution result")
            raise HTTPException(status_code=500, detail="Failed to generate response")
            
        return {"result": query_result}

    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
