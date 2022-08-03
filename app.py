#!/usr/bin/python
# -*- coding: utf-8 -*-
import streamlit as st
import re

from pathlib import Path
from PIL import Image
from zipfile import ZipFile

st.title('Image to WebP Converter')

uploaded_files = st.file_uploader('Choose a Image File',
                                  accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()

quality_value = st.slider('Choose Quality Score', 0, 100, 80)

if st.button('Convert to WebP'):
    if len(uploaded_files) > 0:
        zipObj = ZipFile('images.zip', 'w')  # Create and open archive
        zipObj.write('webp_images/readme.txt')  # Add readme file to archive

        for file in reversed(uploaded_files):
            new_file_name = re.sub(
                '\..*', '.webp', str(file.name))  # Set new filename
            new_file_path = 'webp_images/' + new_file_name  # Set new file path
            image = Image.open(file)  # Open image
            image.save(fp=new_file_path, format='webp',
                       quality=quality_value)  # Convert image to webp
            new_file_size = round(Path(new_file_path).stat(
            ).st_size / 1000, 2)  # Calculate new file size
            # Print success message and file size
            st.write(new_file_name, new_file_size, 'KB ✅')
            zipObj.write(new_file_path)  # Add file to archive
            Path(new_file_path).unlink()  # Delete file

        zipObj.close()  # Close archive

        with open('images.zip', 'rb') as f:
            # Defaults to 'application/octet-stream'
            st.download_button('Download Zip', f, file_name='images.zip')

    else:
        st.error('No Files uploaded')  # Error message if no file was uploaded
