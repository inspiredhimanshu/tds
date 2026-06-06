# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "vaderSentiment",
# ]
# ///

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()

class SentimentRequest(BaseModel):
    sentences: List[str]

class SentimentResult(BaseModel):
    sentence: str
    sentiment: Literal["happy", "sad", "neutral"]

class SentimentResponse(BaseModel):
    results: List[SentimentResult]

def get_sentiment(sentence: str) -> str:
    score = analyzer.polarity_scores(sentence)["compound"]

    if score >= 0.05:
        return "happy"
    elif score <= -0.05:
        return "sad"
    else:
        return "neutral"

@app.post("/sentiment", response_model=SentimentResponse)
async def analyze_sentiment(data: SentimentRequest):
    if not data.sentences:
        raise HTTPException(status_code=400, detail="sentences list cannot be empty")

    results = []
    for sentence in data.sentences:
        results.append({
            "sentence": sentence,
            "sentiment": get_sentiment(sentence)
        })

    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)