import numpy as np
import pickle
import pandas as pd
#from flasgger import Swagger
import streamlit as st 

from PIL import Image

#app=Flask(__name__)
#Swagger(app)

pickle_in = open("artifacts\model.pkl","rb")
classifier=pickle.load(pickle_in)

pickle_in2 = open("artifacts\proprocessor.pkl","rb")
preprocessor = pickle.load(pickle_in2)





#@app.route('/')
def welcome():
    return "Welcome All"

#@app.route('/predict',methods=["Get"])
def predict_note_authentication(gender,race,parent,lunch,test,read,write):
    d = {
        'gender': gender,
        'race_ethnicity': race,
        'parental_level_of_education': parent,
        'lunch': lunch,
        'test_preparation_course': test,
        'reading_score': read,
        'writing_score': write
    }
    l = pd.DataFrame(d,index=[0])
    x = preprocessor.fit_transform(l)
    prediction=classifier.predict(x)
    print(prediction)
    return prediction



def main():
    st.title("Bank Authenticator")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Streamlit Bank Authenticator ML App </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    gender = st.text_input("gender","Type Here")
    race = st.text_input("race","Type Here")
    parent = st.text_input("parent","Type Here")
    lunch = st.text_input("lunch","Type Here")
    test= st.text_input("test","Type Here")
    read = st.text_input("read","Type Here")
    write = st.text_input("write","Type Here")

    result=""
    if st.button("Predict"):
        result=predict_note_authentication(gender,race,parent,lunch,test,read,write)
    st.success('The output is {}'.format(result))
    if st.button("About"):
        st.text("Lets LEarn")
        st.text("Built with Streamlit")

if __name__=='__main__':
    main()
    