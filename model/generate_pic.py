import requests
from PIL import Image
from io import BytesIO
import streamlit as st

@st.cache()
def generate_pic(text_to_search, ax):
    """
    we define a function here to use the api frpm arasaac, and return the image based on the text that we search
    ref: https://arasaac.org/developers/api

    Args:
        text_to_search (_type_): _description_
        ax (_type_): _description_
    """
    search_url = f"https://api.arasaac.org/api/pictograms/en/bestsearch/{text_to_search}"
    search_response = requests.get(search_url)
    search_json = search_response.json()
    if search_json:
        pic_url = f"https://api.arasaac.org/api/pictograms/{search_json[0]['_id']}?download=false"
        pic_response = requests.get(pic_url)
        img = Image.open(BytesIO(pic_response.content))
        ax.imshow(img)
        ax.set_title(text_to_search)
    else:
        ax.set_title(text_to_search)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
