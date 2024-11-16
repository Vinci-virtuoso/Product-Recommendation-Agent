from fastapi import APIRouter, Depends, HTTPException

from app.models.chat_models import ChatRequest, ChatResponse
from app.workflows.rag_workflow import create_rag_graph

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, graph=Depends(create_rag_graph)):
    try:

        initial_state = {
            "question": request.question,
        }

        result_state = await graph.ainvoke(input=initial_state)

        answer = result_state.get("answer", "Sorry, I couldn't find an answer.")
        return ChatResponse(answer=answer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
