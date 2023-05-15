from fastapi import FastAPI
from pydantic import BaseModel
from app.model.model import recommend_books_pipeline as recommend_books
from app.model.model import __version__ as model_version
# from model.model import get_book_titles
# from model.model import get_book_ISBNs

#import uvicorn
#import traceback


app = FastAPI(title="Bookshelf ML Model API", version="0.1.0", description="This is a simple API for the Bookshelf ML Model")





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

# #get function to get all the book titles
# @app.get("/titles")
# def all_books_titles():
#     books = get_book_titles()
#     return {"isbns": books}

# #get function to get all the book ISBNs
# @app.get("/ISBNs")
# def all_books_ISBNs():
#     books = get_book_ISBNs()
#     return {"titles": books}

@app.post("/recommend", response_model = RecommendationOutput)
def recommend(title: BookNameInput, number: RecommendationCountInput):
    books = recommend_books(title.text, number.count)
    return {"books": books}





# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=4000)