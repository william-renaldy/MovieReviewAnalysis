import streamlit as st
from predictor import Processor,Model
import getmovie

processor = Processor()
model = Model()

st.set_page_config(page_title="Movie Review Analyser", page_icon=r"static/images/bg.jpg")
st.title("Movie Review Analysis")

movie = st.text_input("Enter the movie name: ").strip()


if movie:
    review,movie_name = getmovie.GetMovie(movie)

    if isinstance(review,list):
        X = processor.pre_process(review)

        result = model.predict(X)

        result = sum(result)/len(result)



        print(result)
        if result > 0.7:
            message = f"The movie is Good"
        elif result > 0.4:
            message = f"The movie is Neutral"
        else:
            message = f"The movie is Bad" 

    else:
        message = review  


    st.markdown(f"Movie Title: {movie_name}")
    # st.markdown(f"Year: {year}")

    st.subheader(message)
