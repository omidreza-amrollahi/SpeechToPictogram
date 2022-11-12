import os
import whisper
import streamlit as st
from pydub import AudioSegment
from model.clean_text import clean_text
from model.POS_tagging import POS_tagging
from model.save_pictogram import save_pictogram
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="Whisper based ASR",
    page_icon="musical_note",
    layout="wide",
    initial_sidebar_state="auto",
)

audio_tags = {'comments': 'Converted using pydub!'}

upload_path = "uploads/"
download_path = "downloads/"
transcript_path = "transcripts/"

# @st.cache(persist=True,allow_output_mutation=False,show_spinner=True,suppress_st_warning=True)
@st.cache()
def to_mp3(audio_file, output_audio_file, upload_path, download_path):
    ## Converting Different Audio Formats To MP3 ##
    if audio_file.name.split('.')[-1].lower()=="wav":
        audio_data = AudioSegment.from_wav(os.path.join(upload_path,audio_file.name))
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="mp3":
        audio_data = AudioSegment.from_mp3(os.path.join(upload_path,audio_file.name))
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="ogg":
        audio_data = AudioSegment.from_ogg(os.path.join(upload_path,audio_file.name))
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="wma":
        audio_data = AudioSegment.from_file(os.path.join(upload_path,audio_file.name),"wma")
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="aac":
        audio_data = AudioSegment.from_file(os.path.join(upload_path,audio_file.name),"aac")
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="flac":
        audio_data = AudioSegment.from_file(os.path.join(upload_path,audio_file.name),"flac")
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="flv":
        audio_data = AudioSegment.from_flv(os.path.join(upload_path,audio_file.name))
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower()=="mp4":
        audio_data = AudioSegment.from_file(os.path.join(upload_path,audio_file.name),"mp4")
        audio_data.export(os.path.join(download_path,output_audio_file), format="mp3", tags=audio_tags)
    return output_audio_file

@st.cache()
def process_audio(filename, model_type):
    model = whisper.load_model(model_type)
    result = model.transcribe(filename, fp16=False)
    return result["text"]

@st.cache()
def save_transcript(transcript_data, txt_file):
    with open(os.path.join(transcript_path, txt_file),"w") as f:
        f.write(transcript_data)

def generate_pictogram(text_list):
    """
    we define a function here to use the api frpm arasaac, and return the image based on the text that we search
    ref: https://arasaac.org/developers/api

    Args:
        text_to_search (_type_): _description_
        ax (_type_): _description_
    """
    text_length = len(text_list)
    for i, col in enumerate(st.columns(text_length)):
        with col:
            search_url = f"https://api.arasaac.org/api/pictograms/en/bestsearch/{text_list[i]}"
            search_response = requests.get(search_url)
            search_json = search_response.json()
            if search_json:
                pic_url = f"https://api.arasaac.org/api/pictograms/{search_json[0]['_id']}?download=false"
                pic_response = requests.get(pic_url)
                img = Image.open(BytesIO(pic_response.content))
                st.image(img, use_column_width='auto', caption=text_list[i])
            else:
                st.write(f"no image found for /{text_list[i]}/")

st.title("Speech to Pictogram")
st.info('Supports all popular audio formats - WAV, MP3, MP4, OGG, WMA, AAC, FLAC, FLV')
uploaded_file = st.file_uploader("Upload audio file", type=["wav","mp3","ogg","wma","aac","flac","mp4","flv"])

audio_file = None

if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    with open(os.path.join(upload_path,uploaded_file.name),"wb") as f:
        f.write((uploaded_file).getbuffer())
    with st.spinner(f"Processing Audio ..."):
        output_audio_file = uploaded_file.name.split('.')[0] + '.mp3'
        output_audio_file = to_mp3(uploaded_file, output_audio_file, upload_path, download_path)
        audio_file = open(os.path.join(download_path,output_audio_file), 'rb')
        audio_bytes = audio_file.read()
    print("Opening ",audio_file)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Feel free to play your uploaded audio file")
        st.audio(audio_bytes)
    with col2:
        whisper_model_type = st.radio("Please choose your model type", ('Tiny', 'Base', 'Small', 'Medium', 'Large'))

    if st.button("Generate Transcript"):
        with st.spinner(f"Generating Transcript..."):
            transcript = process_audio(str(os.path.abspath(os.path.join(download_path,output_audio_file))), whisper_model_type.lower())

            output_txt_file = str(output_audio_file.split('.')[0]+".txt")

            save_transcript(transcript, output_txt_file)
            output_file = open(os.path.join(transcript_path,output_txt_file),"r")
            output_file_data = output_file.read()

        st.write(f"Transcript: {output_file_data}")

        if st.download_button(
                             label="Download Transcript",
                             data=output_file_data,
                             file_name=output_txt_file,
                             mime='text/plain'
                         ):
            st.balloons()
            st.success('Download Successful !!')

    if st.button("Generate Pictogram"):
        with st.spinner(f"Generating Pictogram..."):
            transcript = process_audio(str(os.path.abspath(os.path.join(download_path,output_audio_file))), whisper_model_type.lower())
            cleaned_text, concatString = clean_text(transcript)
            prediction = POS_tagging(concatString).make_predictions()
            generate_pictogram(prediction)

else:
    st.warning('Please upload your audio file')

st.markdown("<br><hr><center>Made by <a href='mailto:omidreza.ir@gmail.com?subject=Speech to pictogram WebApp!&body=Please specify the issue you are facing with the app.'><strong>Omidreza</strong></a> </center><hr>", unsafe_allow_html=True)


