from flask import Flask, render_template, request, send_file
from sqlalchemy import create_engine,text


app=Flask(__name__)
engine=create_engine("mysql+pymysql://root:password@localhost/test")

connection = engine.connect()


@app.route('/')
def index():
    result=connection.execute(text("select * from test"))

    rows=result.mappings()
    
    return render_template('index.html',result_content=[row['sequence'] for row in rows])

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file selected"

    file=request.files['file']

    if file.filename == '':
        return "No selected file"
    
    file_name=file.filename
    content=file.read()
    content=str(content, 'utf-8')
    print(content)
    connection.execute(text(f"insert into test (id, name, sequence) values (3, '{file_name}', '{content}')"))
    connection.commit()

    return render_template('index.html')
    
if __name__=='__main__':
    app.run(debug=True)

