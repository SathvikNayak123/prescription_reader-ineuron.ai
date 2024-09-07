import streamlit as st
from image_reader import ImageToText, TextToSpeech
import tempfile
import os

# Title of the app
st.title('Prescription OCR and Text-to-Speech Converter')

# Image upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    #This creates a temporary file with a .jpg extension where the uploaded image is saved.
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name
    
    # Initialize ImageToText class with uploaded image
    ocr = ImageToText(img_path=temp_file_path)
    
    # Extract text from the image
    extracted_text, ocr_result = ocr.extract_text_from_image()
    
    # Display the extracted text
    st.subheader("Extracted Text:")
    st.write(extracted_text)
    
    # Option to download the extracted text
    text_file = ocr.save_text_to_file(extracted_text)
    st.download_button("Download Extracted Text", data=text_file, file_name='extracted_text.txt', mime='text/plain')
    
    # Visualize OCR result on image
    img_bytes = ocr.visualize_ocr_result(ocr_result)
    st.image(img_bytes, caption="OCR Result")

    # Convert text to speech
    tts = TextToSpeech()
    
    if st.button("Play Audio"):
        audio_file = tts.save_speech_to_file(extracted_text)
        st.audio(audio_file, format="audio/mp3")
        st.success("Playing the audio...")

    # Option to download the audio
    # Option to download the audio
    audio_file = tts.save_speech_to_file(extracted_text)
    st.download_button("Download Audio", data=audio_file, file_name='prescription_audio.mp3', mime='audio/mp3')

    # Cleanup after app runs
    os.remove(temp_file_path)
