from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from src.api.controller.search_controller import router as search_router
from src.config.app_config import config

API_PREFIX = "/api"

app = FastAPI(
    title="Deep Search Agent API",
    description="API for the Deep Search Agent using LangGraph",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router, prefix=API_PREFIX, tags=["search"])


@app.get("/deep-search", response_class=HTMLResponse)
def deep_search():
    try:
        with open("index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="HTML file not found")


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=1122, reload=True, log_level="info")
