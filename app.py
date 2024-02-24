import numpy as np
import pickle
import pandas as pd
import streamlit as st 
from PIL import Image

preprocessor = pickle.load(open("artifacts/proprocessor.pkl","rb"))
classifier=pickle.load(open("artifacts/model.pkl","rb"))

def welcome():
    return "Welcome All"

def predict_note_authentication(df):
    x = preprocessor.transform(df)
    prediction=classifier.predict(x)[0]
    print(prediction)
    return prediction

def main():
    st.title("Application")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Student Score Predictor</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    
    # Main Code
    input_text = []
    for i in range(5):
        input_text.append(st.text_input("Enter Text Input {}:".format(i+1)))
    
    input_num = []
    for i in range(2):
        input_num.append(st.number_input("Enter Number Input {}:".format(i+1)))

    d = {
        'gender': input_text[0],
        'race_ethnicity': input_text[1],
        'parental_level_of_education': input_text[2],
        'lunch': input_text[3],
        'test_preparation_course': input_text[4],
        'reading_score': input_num[0],
        'writing_score': input_num[1]
    }

    df = pd.DataFrame(d, index=[0])

    result=""

    if st.button("Predict"):
        try:
            result=predict_note_authentication(df)
            st.success(f'The output is {result:.2f}')
        except Exception as e:
            print(f"maa chud gyi hai error: {e}")

if __name__=='__main__':
    main()