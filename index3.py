from flask import Flask, render_template, request, send_file, jsonify
#from sqlalchemy import create_engine,text
from PAM_analyze import analyze_single_file
from db import start, upload_to_db, selection

app=Flask(__name__)

@app.route('/')
def index():
    rows=start()
    return render_template('index.html',result_content=rows)

#8/29 How to render it...beutifully..8/30 I think I need to change the way to save the data. 
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file selected"

    file=request.files['file']

    if file.filename == '':
        return "No selected file"

    sequence=file.read()
    sequence=str(sequence, 'utf-8')
    sequence=''.join(sequence).replace('\r\n', '')
    print(sequence)

    result=upload_to_db(sequence)
    message=file.filename+" uploaded successfully"
    return render_template('index.html', result_content=result, message=message)

@app.route('/analyze', methods=['POST'])
def analyze():

    PAM_option=request.form.get('num').split(',')
    if PAM_option==['']:
        return "No sequences entered"
    gene_number=request.form.get('sequences')
    sequence=selection(gene_number)
    PAM_forward,PAM_reverse=analyze_single_file(sequence[0],PAM_option)
    return render_template('index.html', result_content=start(), gene_number=gene_number, PAM_option=PAM_option, PAM_forward=PAM_forward, PAM_reverse=PAM_reverse)

@app.route('/data')
def databank():
    rows=start()
    return render_template('data.html', result_content=[row for row in rows]) #why I cannot jasonify this result content?

if __name__=='__main__':
    app.run(debug=True)

