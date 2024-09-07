import cv2
from paddleocr import PaddleOCR
from gtts import gTTS
import numpy as np
from io import BytesIO  # For creating in-memory files

class ImageToText:
    def __init__(self, img_path='drug1.jpg'):
        self.ocr = PaddleOCR(lang='en')
        self.img_path = img_path

    def extract_text_from_image(self):
        '''
        Uses the PaddleOCR object to perform OCR on the image specified by self.img_path. 
        This returns a result object that contains details about the detected text and its position in the image.
        '''
        result = self.ocr.ocr(self.img_path)
        texts = [res[1][0] for res in result[0]]
        txt = ' '.join(texts)
        return txt, result

    def visualize_ocr_result(self, result):

        img = cv2.imread(self.img_path)

        #Converts the image from BGR (OpenCV's default color format) to RGB (standard color format) 
        #to ensure correct color representation.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        for box, text in zip(result[0], result[0]):
            #Extracts the coordinates of the bounding box around the text.
            box_coords = box[0]

            #Draws the bounding box around the detected text on the image
            cv2.polylines(img, [np.array(box_coords, np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
            
            #Adds the detected text on top of the image, near the bounding box
            cv2.putText(img, text[1][0], tuple(map(int, box_coords[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Encodes the image as a JPEG format and stores it in a buffer.
        _, buffer = cv2.imencode('.jpg', img)

        #Converts the buffer into an in-memory file-like object (BytesIO) for easier handling and downloading
        img_bytes = BytesIO(buffer.tobytes())
        
        # Return in-memory file for download
        return img_bytes

    def save_text_to_file(self, text):
        # Converts the text into bytes using UTF-8 encoding and wraps it in a BytesIO object.
        text_bytes = BytesIO(text.encode('utf-8'))
        text_bytes.seek(0)  # Move cursor to the start of the file
        return text_bytes

class TextToSpeech:
    def __init__(self, lang='en', slow=False):
        self.lang = lang
        self.slow = slow

    def convert_text_to_speech(self, text):
        tts = gTTS(text=text, lang=self.lang, slow=self.slow)
        #Returns the gTTS object, which contains the text-to-speech conversion ready to be saved or played.
        return tts

    def save_speech_to_file(self, text):
        tts = self.convert_text_to_speech(text)
        
        # allows us to store the audio data without writing it to disk.
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)  # Move cursor to the start of the file
        # Returns the in-memory file-like object containing the audio data
        return audio_file

