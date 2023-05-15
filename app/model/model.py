import pickle
import re
from pathlib import Path
#import traceback
# import streamlit as st
import pandas as pd





__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent

#Load the books model:

books_dictionary = pickle.load(open(f"{BASE_DIR}/final_books.pkl", "rb"))

books_model = pd.DataFrame(books_dictionary)

# #Get all the book titles
# def get_book_titles():
#     return list(books_model["title"])

# #get all the book ISBNs
# def get_book_ISBNs():
#     return list(books_model["ISBN"])

#open the model file
#with open(f"{BASE_DIR}/trained_similarity_pipeline-{__version__}.pkl", "rb") as f:
#traceback.print_exc()
#load the model
simularity_model = pickle.load(open(f"{BASE_DIR}/similarity-{__version__}.pkl", "rb"))




#recommend books based on the book title and the number of books to recommend
# def recommend_books_pipeline(title, recommend_num):
#     #get the book id from the title
#     #book_id = model.get_book_id(title)
#     #get the recommended books
#     recommended_books = model.recommend(title, recommend_num)
    
#     #get the book title from the book id
#     recommended_books = [model.get_book_info(title) for title in recommended_books]
#     return recommended_books

def recommend_books_pipeline(title, number_of_books):
   #if the book is not in the dataframe
    if title not in books_model['title'].unique():
        return 'Book not in the dataset.'
    else:
        #get the index of the book in the dataframe
        book_index = books_model[books_model['title'] == title].index[0]
        #get the list of similar books
        distances = simularity_model[book_index]
        #sort the list
        books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:number_of_books+1]
        

        #return all the recommended books titles
        #recommended_books = [books_model.iloc[book[0]].title for book in books_list]
         #return all the recommended books ISBNs
        recommended_books = [books_model.iloc[book[0]].ISBN for book in books_list]
        return recommended_books
        #for book in books_list:
            #print book ISBN and title
            #print(books_model.iloc[book[0]].ISBN+" - "+books_model.iloc[book[0]].title)
            


