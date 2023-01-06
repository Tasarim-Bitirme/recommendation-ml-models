from fastapi import FastAPI
from pydantic import BaseModel
from app.model.model import collaborative_filtering 
from app.model.model import content_based_filtering
from app.model.model import __version__ as model_version
# from model.model import get_book_titles
# from model.model import get_book_ISBNs

#import uvicorn
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




@app.post("/recommend", response_model = RecommendationOutput)
def recommend(title: BookNameInput, number: RecommendationCountInput):
    #books = recommend_books(title.text, number.count)

    #Get collaborative filtering recommendations
    books_collaborative_filtering = collaborative_filtering(title.text, number.count//2)
    #Get content based filtering recommendations
    books_content_based_filtering = content_based_filtering(title.text, number.count//2)

    #if the recommended books are 5 I want to return 5 books from the collaborative filtering and 5 books from the content based filtering  
    #put  a copy of the duplicate books on the front of the list
    #Combine the two lists
    books = books_collaborative_filtering + books_content_based_filtering

    #Remove duplicates
    #books = list(dict.fromkeys(books))
    #if there's duplicates in the list
    #put a copy of the duplicate books on the front of the list
    #then remove the other copies
    #then return the list
    if len(books) != len(set(books)):
        for i in range(len(books)):
            if books[i] in books[i+1:]:
                books.insert(0, books[i])
        books = list(dict.fromkeys(books))
    
    return {"books": books}




# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=4000)