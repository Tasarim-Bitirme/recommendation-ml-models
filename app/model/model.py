import pickle
import re
from pathlib import Path
#import traceback
# import streamlit as st
import pandas as pd
import numpy as np






__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve(strict=True).parent


#THIS IS THE CONTENT BASED RECOMMENDATION MODEL PART:
#Load the books model:

books_dictionary = pickle.load(open(f"{BASE_DIR}/final_books.pkl", "rb"))

books_model = pd.DataFrame(books_dictionary)

#load the model
simularity_model = pickle.load(open(f"{BASE_DIR}/similarity-{__version__}.pkl", "rb"))

#Recommendation function
def content_based_filtering(title, number_of_books):
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
        


#THIS IS THE COLLABORATIVE FILTERING MODEL PART:
#Load the books model:
books_user_rating = pickle.load(open(f"{BASE_DIR}/user_book_rating_model.pkl", "rb"))

books_user_rating_model = pd.DataFrame(books_user_rating)



#Load the books, ratings and users model:
books_user_isbn_rating= pickle.load(open(f"{BASE_DIR}/book_isbn_title_user_rating_model.pkl", "rb"))

books_isbn_title_user_rating_model = pd.DataFrame(books_user_isbn_rating)
#print("Books Model: ",books_isbn_title_user_rating_model.head())

#load the recommendation model
simularity_model = pickle.load(open(f"{BASE_DIR}/simularity.pkl", "rb"))

#Test the model
#print("Books Model: ",books_model.head())

#print("Simularity Model: ",simularity_model)




def collaborative_filtering(title, number_of_books):
    #if the book is not in the dataframe
    if title not in books_user_rating_model.index:
        print('Book not in the dataset!!')
        return
    else:
        #get the index of the book in the dataframe
        book_index = books_user_rating_model.index.get_loc(title)
        #get the list of similar books
        similar_books = list(enumerate(simularity_model[book_index]))
        similar_books = sorted(similar_books, key=lambda x:x[1], reverse=True)
        similar_books = similar_books[1:number_of_books+1]
        #return all the recommended books isbns
        #recommended_books_isbn = [books_model.index[book[0]] for book in similar_books]
        recommended_books_isbn = [books_isbn_title_user_rating_model.index[i][0] for i in range(len(books_isbn_title_user_rating_model.index))]
        ##return recommended_books_isbn

        recommended_books = [recommended_books_isbn[isbn[0]] for isbn in similar_books]

        # for isbn in recommended_books_isbn:
        #     recommended_books.append(recommended_books_isbn[isbn[0]])
        return recommended_books



    


#BAYESIAN APPROACH

def hybrid_based_recommendation_bayesian_arpoach(title, num_of_rec):
  # Get recommendations from collaborative filtering model
  collab_recs = collaborative_filtering(title, num_of_rec)
  
  # Get recommendations from content-based filtering model
  content_recs = content_based_filtering(title, num_of_rec)
  
  # Combine the recommendations using a Bayesian network
  recommendations = []
  for collab_rec in collab_recs:
    for content_rec in content_recs:
      if collab_rec == content_rec:
        # Recommendations from both models agree, so we can be more confident in this recommendation
        recommendations.append(collab_rec)
  if len(recommendations) < num_of_rec:
    # If we don't have enough recommendations yet, add the remaining items from either model
    recommendations.extend(collab_recs[len(recommendations):])
    recommendations.extend(content_recs[len(recommendations):])
  
  # Return the top 'num_of_rec' recommendations
  return recommendations[:num_of_rec]


#WARP APPROACH

def hybrid_based_recommendation_warp_aproach(title, num_of_rec):
  # Get recommendations from collaborative filtering model
  collab_recs = collaborative_filtering(title, num_of_rec)
  
  # Get recommendations from content-based filtering model
  content_recs = content_based_filtering(title, num_of_rec)
  
  # Combine the recommendations using WARP loss
  recommendations = []
  for i, collab_rec in enumerate(collab_recs):
    for j, content_rec in enumerate(content_recs):
      if collab_rec == content_rec:
        # Recommendations from both models agree, so we can assign a higher weight to this recommendation
        recommendations.append((collab_rec, i + j))
  recommendations.sort(key=lambda x: x[1])
  
  # Return the top 'num_of_rec' recommendations
  return [rec[0] for rec in recommendations][:num_of_rec]
