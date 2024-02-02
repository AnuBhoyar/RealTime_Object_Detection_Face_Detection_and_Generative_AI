from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_resonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(upload_file):
    if upload_file:
        bytes_data=upload_file.getvalue()
        image_parts=[
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="Gemini calories prediction App")
st.header("Gemini calories prediction App")
input=st.text_input("Input Prompt:",key="input")
upload_file=st.file_uploader("Choose image ",type=['jpg','jpeg','png'])
image=""
if upload_file:
    image=Image.open(upload_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button('Tell me total calories')

input_prompt="""
You are an expert nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake.
               is below format

               1. Item 1 - no of calories
               2. Item 2 - no of calories
               ----
               ----
               Finally you also mention whether food is healthy or not and also mention percentage split of the ratio of carbohydrate,
               fats,protein,sugar and other important things reuired in our diet.
"""

if submit:
    image_data=input_image_setup(upload_file)
    response=get_gemini_resonse(input_prompt,image_data,input)
    st.subheader("The response is")
    st.write(response)


