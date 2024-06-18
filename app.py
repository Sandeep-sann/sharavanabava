from flask import Flask, request, render_template, send_file
import pdfplumber
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_text', methods=['POST'])
def extract_text():
    pdf_file = request.files['pdf_file']
    with pdfplumber.open(pdf_file) as pdf:
        extracted_text = ''
        for page in pdf.pages:
            extracted_text += page.extract_text()
    return extracted_text

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    text = request.form['extracted_text']
    tts = gTTS(text, lang='en', slow=True)  # Setting slow=True for slower speed
    audio_file = 'output.mp3'
    tts.save(audio_file)
    return send_file(audio_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
