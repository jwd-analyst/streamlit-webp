#!/usr/bin/python
# -*- coding: utf-8 -*-
import streamlit as st
from pathlib import Path
from PIL import Image
from zipfile import ZipFile
import re

st.title('Image to WebP Converter')

uploaded_files = st.file_uploader('Choose a Image File',
                                  accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()

     # st.write("filename:", uploaded_file.name)

quality_value = st.slider('Choose Quality Score', 0, 100, 80)

if st.button('Convert to WebP'):
    if len(uploaded_files) > 0:
     zipObj = ZipFile('images.zip', 'w')
     zipObj.write('webp_images/readme.txt')

     for file in reversed(uploaded_files):
          new_file_name = re.sub('\..*', '.webp', str(file.name))
          new_file_path = 'webp_images/' + new_file_name
          image = Image.open(file)  # Open image
          image.save(fp= new_file_path, format='webp',
                    quality=quality_value)  # Convert image to webp
          new_file_size = round(Path(new_file_path).stat().st_size / 1000, 2)
          st.write(new_file_name, new_file_size, 'KB ✅')
          zipObj.write(new_file_path)
          Path(new_file_path).unlink()

     zipObj.close()
     
     with open('images.zip', 'rb') as f:
          st.download_button('Download Zip', f, file_name='images.zip')  # Defaults to 'application/octet-stream'

    else:
     st.error('No Files uploaded')