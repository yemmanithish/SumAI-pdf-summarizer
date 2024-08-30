from flask import Flask, request, render_template_string,render_template
import pdfplumber
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

app = Flask(__name__)

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def summarize_text(text, sentence_count=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=sentence_count)
    return '\n'.join([f'• {sentence}' for sentence in summary])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['pdf_file']
        sentence_count = int(request.form['sentence_count'])
        if file and file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)
            summary = summarize_text(text, sentence_count)
            return render_template('summary.html', summary=summary)
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
