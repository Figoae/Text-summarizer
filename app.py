from flask import Flask, render_template, request
from transformers import pipeline, BartForConditionalGeneration, BartTokenizer
import tempfile
import os
from PyPDF2 import PdfReader
import docx

# Load models
whisper_model = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-small",
    device="cpu"  # change to "cuda:0" if you have GPU
)
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

app = Flask(__name__)
feedback_list = []


def extract_text_from_file(file_path):
    """Extract text from PDF, DOCX, or TXT file."""
    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif ext == ".docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        return ""


def trim_to_word_limit(summary_text, word_limit):
    """Trim summary to approximately the desired word limit."""
    words = summary_text.split()
    if len(words) > word_limit:
        return " ".join(words[:word_limit])
    return summary_text


def summarize_text(text, word_limit):
    """Summarize text using BART and enforce word-based length."""
    if not text.strip():
        return "No text found to summarize."

    # Convert word limit to token limit (roughly 1.3x)
    max_len = int(word_limit * 1.3)
    min_len = max(20, int(word_limit * 0.8))

    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs["input_ids"],
        num_beams=4,
        min_length=min_len,
        max_length=max_len,
        early_stopping=True,
        no_repeat_ngram_size=3,
    )

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    summary = trim_to_word_limit(summary, word_limit)
    return summary


@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    if request.method == "POST" and "data" in request.form:
        text = request.form["data"]
        word_limit = int(request.form["maxL"])
        summary = summarize_text(text, word_limit)

    return render_template("index.html", result=summary, feedbacks=feedback_list)


@app.route("/voice", methods=["POST"])
def voice():
    if "voicefile" not in request.files:
        return render_template("index.html", result="No file uploaded.", feedbacks=feedback_list)

    voice_file = request.files["voicefile"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        voice_file.save(temp_audio.name)

    try:
        result = whisper_model(temp_audio.name)
        transcription = result.get("text", "Could not transcribe audio.")
    except Exception as e:
        transcription = f"Error transcribing audio: {e}"

    return render_template("index.html", result=transcription, feedbacks=feedback_list)


@app.route("/document", methods=["POST"])
def document():
    """Handle document upload and summarization."""
    if "docfile" not in request.files:
        return render_template("index.html", result="No file uploaded.", feedbacks=feedback_list)

    file = request.files["docfile"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[-1]) as temp_doc:
        file.save(temp_doc.name)

    text = extract_text_from_file(temp_doc.name)

    if not text.strip():
        return render_template("index.html", result="No readable text found in file.", feedbacks=feedback_list)

    word_limit = int(request.form.get("maxL", 150))
    summary = summarize_text(text, word_limit)

    return render_template("index.html", result=summary, feedbacks=feedback_list)


@app.route("/feedback", methods=["POST"])
def feedback():
    name = request.form.get("name", "Anonymous")
    comment = request.form.get("comment", "")
    rating = request.form.get("rating", "5")

    feedback_list.append({"name": name, "comment": comment, "rating": rating})

    return render_template("index.html", result=None, feedbacks=feedback_list)


if __name__ == "__main__":
    app.run(debug=True)
