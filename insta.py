import streamlit as st
from instagrapi import Client

st.title("Post Generator")

username = st.text_input("Instagram_Username")
password = st.text_input("Instagram_Password", type="password")
image_path = st.text_input("Image_Path")
caption = st.text_area("Caption")

if st.button("Post"):
    try:
        cl = Client()
        cl.login(username, password)
        media = cl.photo_upload(image_path, caption)
        st.success("Posted successfully!")
    except Exception as e:
        st.error(f"Error: {e}")