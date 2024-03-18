from flask import Flask, render_template, request, send_file, jsonify
from sqlalchemy import create_engine,text
from PAM_analyze import analyze_single_file


app=Flask(__name__)
engine=create_engine("mysql+pymysql://root:password@localhost/test")

connection = engine.connect()
def databaseConnect(engine):
    connection = engine.connect()
    result=connection.execute(text("select * from test2"))
    rows=result.mappings()

    return rows

@app.route('/')
def index():
    rows=databaseConnect(engine)
    
    return render_template('index.html',result_content=rows)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file selected"

    file=request.files['file']

    if file.filename == '':
        return "No selected file"

    file_name=file.filename
    sequence=file.read()
    sequence=str(sequence, 'utf-8')
    sequence=''.join(sequence).replace('\r\n', '')
    
    connection.execute(text(f"insert into test2 (name, sequence) values ('{file_name}', '{sequence}')"))
    connection.commit()
    
    rows=databaseConnect(engine)

    return render_template('index.html', result_content=rows)

# why analysis doesn't work?
@app.route('/analyze', methods=['POST'])
def analyze():
    PAM_option=request.form.get('num').split(',')
    sequence=connection.execute(text("select sequence from test2 where id=1"))
    sequence=sequence.mappings()
    print(sequence)
    PAM_forward,PAM_reverse=analyze_single_file(sequence,PAM_option)
    print(PAM_forward)
    return render_template('index.html', result_content1=PAM_forward, result_content2=PAM_reverse)

@app.route('/data')
def databank():
    rows=databaseConnect(engine)
    return render_template('result.html', result_content=[row for row in rows]) #why I cannot jasonify this result content?

if __name__=='__main__':
    app.run(debug=True)

