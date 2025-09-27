from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from src.api.manager.search_manager import SearchManager

router = APIRouter(prefix="/search", tags=["search"])
search_manager = SearchManager()


class SearchRequest(BaseModel):
    query: str


@router.post("/stream")
async def stream_search_results(request: SearchRequest):
    """Stream deep search results in real-time with AI thinking process"""
    try:
        query = request.query.strip()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty"
            )

        return StreamingResponse(
            search_manager.stream_search_results(query),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering
            },
        )
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg
        )


@router.post("/")
async def get_search_results(request: SearchRequest):
    """Traditional non-streaming search (for backward compatibility)"""
    try:
        query = request.query.strip()
        if not query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty"
            )

        # Collect all streaming results into a single response
        results = []
        async for data in search_manager.stream_search_results(query):
            # Parse the SSE data format
            if data.startswith("data: "):
                import json

                try:
                    parsed_data = json.loads(data[6:])  # Remove "data: " prefix
                    results.append(parsed_data)
                except json.JSONDecodeError:
                    continue

        return {"results": results}
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_msg
        )
