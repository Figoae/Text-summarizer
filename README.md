# Text Summarizer

A **web-based text summarization application** built with **Flask** and **Hugging Face Transformers**. It supports summarizing **text input**, **uploaded documents** (PDF, DOCX, TXT), and **voice recordings** using automatic speech recognition. Users can also leave feedback and rate the tool.

---

## Features

- Summarize plain text input with customizable summary length.
- Upload documents (PDF, DOCX, TXT) and generate summaries.
- Upload voice recordings (mp3, wav, m4a) and transcribe them using **Whisper** model.
- Adjustable summary length via slider.
- Collect user feedback with name, comment, and rating.
- Clean and responsive web interface.

---

## Technologies Used

- **Flask** – Web framework.
- **Transformers (Hugging Face)** – BART model for text summarization.
- **Whisper (OpenAI)** – Automatic speech recognition for voice input.
- **PyPDF2** – Extract text from PDF files.
- **python-docx** – Extract text from DOCX files.
- **HTML, CSS, JavaScript** – Frontend interface.

---

## Installation

1. **Clone the repository:**

git clone https://github.com/Figoae/Text-summarizer.git
cd Text-summarizer

2.**Create a virtual environment**

python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

3. **Install dependencies:**
   pip install -r requirements.txt

4. **File Structure**
Text-summarizer/
├── app.py                # Flask backend
├── templates/
│   └── index.html        # Web interface
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── ...

5.**Usage**

Run the Flask app:

python app.py
create a global server - https://dashboard.ngrok.com/get-started/setup/windows
After using token command execute - ngrok http 5000


Open your browser and navigate to:

http://127.0.0.1:5000/ (local)


Features:

Text Summarizer: Paste your text and adjust summary length.

Document Summarizer: Upload PDF, DOCX, or TXT files and set word limit.

Voice Transcription: Upload an audio file to transcribe and summarize.

Feedback: Leave comments and ratings for the tool.
