from fastapi import APIRouter

router = APIRouter()

@router.post("/sentiment_analysis")
def sentiment_analysis(text: str):
    """
    Perform sentiment analysis on the provided text.
    """
    return {"message": "Sentiment analysis result"}