from flask import Flask, request, render_template
import spacy
from spacy import displacy

# Load the small English NLP model
nlp = spacy.load('en_core_web_sm')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/entity', methods=['POST'])
def entity():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                # Read and decode file contents
                readable_file = file.read().decode('utf-8', errors='ignore')
                print("Uploaded Text:", readable_file)  # Debugging output

                # Process the text using spaCy NLP
                document = nlp(readable_file)
                print("Processed Document:", document)  # Debugging output

                # Print entities and their types
                for ent in document.ents:
                    print(ent.text, ent.label_)  # Debugging entity types

                # Render the entities using spaCy's displacy
                file_html = displacy.render(document, style='ent')
                print("Rendered HTML:", file_html)  # Debugging output

                # Return the original text and the NER result
                return render_template('index.html', html=file_html, text=readable_file)
            except Exception as e:
                print(f"Error processing file: {e}")
                return render_template('index.html', error="An error occurred while processing the file.")
        else:
            return render_template('index.html', error="No file selected.")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
p