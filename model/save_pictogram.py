import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('AGG')
from model.generate_pic import generate_pic
import io
import streamlit as st

# we generate an initial pictogram
# here we see the am, eating, an having a problem
@st.cache()
def save_pictogram(text_list):
    """_summary_

    Args:
        text_list (_type_): _description_
    """
    fig, ax = plt.subplots(1,len(text_list), figsize=(10,1.75))
    for i, text in enumerate(text_list):
        generate_pic(text, ax[i])
    return fig