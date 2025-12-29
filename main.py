from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from parser import DiscourseParser
from schemas import ParseRequest, ParseResponse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading RST Parser model...")
    try:
        models["parser"] = DiscourseParser()
        logger.info("RST Parser model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load RST Parser model: {e}")
    yield
    models.clear()

app = FastAPI(title="RST Discourse Parser API", lifespan=lifespan)

@app.post("/parse", response_model=ParseResponse)
async def parse_text(request: ParseRequest):
    parser = models.get("parser")
    if not parser:
        raise HTTPException(status_code=503, detail="Parser not initialized or failed to load")
    
    try:
        tree = parser.parse(request.text)
        if not tree:
             raise HTTPException(status_code=400, detail="Could not parse text or empty result")
        return ParseResponse(tree=tree)
    except Exception as e:
        logger.error(f"Parsing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "RST Discourse Parser API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
