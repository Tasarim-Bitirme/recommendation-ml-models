from fastapi import FastAPI
from pydantic import BaseModel
# from app.model.model import collaborative_filtering 
# from app.model.model import content_based_filtering
from app.model.model import __version__ as model_version
from app.model.model import hybrid_based_recommendation_bayesian_arpoach
from app.model.model import hybrid_based_recommendation_warp_aproach


import uvicorn
#import traceback


app = FastAPI(title="Bookshelf ML HYBRID BASED RECOMMENDATION SYSTE Model API", version="0.1.0", description="This is a simple API for the Bookshelf ML Model")





class BookNameInput(BaseModel):
    text: str

class RecommendationCountInput(BaseModel):
    count: int

class RecommendationOutput(BaseModel):
   #The recommentation output will be a list of book titles
    books: list


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}




# 

@app.post("/hybrid-bayesian-recommendation", response_model=RecommendationOutput)
def hybrid_based_recommendation_api(book_name: BookNameInput, recommendation_count: RecommendationCountInput):
    try:
        books = hybrid_based_recommendation_bayesian_arpoach(book_name.text, recommendation_count.count)
        return {"books": books}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/hybrid-warp-recommendation", response_model=RecommendationOutput)
def hybrid_based_recommendation_api(book_name: BookNameInput, recommendation_count: RecommendationCountInput):
    try:
        books = hybrid_based_recommendation_warp_aproach(book_name.text, recommendation_count.count)
        return {"books": books}
    except Exception as e:
        return {"error": str(e)}


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=4000)