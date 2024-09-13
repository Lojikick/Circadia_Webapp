from flask import Flask, render_template, send_file
import csv
import os

app = Flask(__name__)

@app.route('/')
def baseFunc():
    html_content = """
    <h1>Welcome to MedTech EdTech FinTech BCI B2B SaaS</h1>
    <p>This is a subtitle.</p>
    <ul>
        <li>/sendRawEEG/  -  get raw CSV</li>
        <li>/displayRawEEG/  -  see raw CSV in browser</li>
        <li>/modelOutput/  -  get the model output</li>
    </ul>
    """
    
    # Return the HTML content
    return html_content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)