from flask import Flask, render_template, request, send_file, jsonify
#from sqlalchemy import create_engine,text
from PAM_analyze import analyze_single_file
import sqlite3

app=Flask(__name__)
#engine=create_engine("mysql+pymysql://root:password@localhost/test")
#connection = engine.connect()



'''
def databaseConnect(engine):
    connection = engine.connect()
    result=connection.execute(text("select * from test2"))
    rows=result.mappings()

    return rows
'''
#8/26 sqlalchemy to sqlite3. Server is little bit complicated"
@app.route('/')
def index():
    conn=sqlite3.connect("gene_data.db")
    cursor=conn.cursor()
    cursor.execute("select * from DNA_list")
    #rows=databaseConnect(engine)
    
    return render_template('index.html',result_content=cursor.fetchall())

#8/26 Upload is working. But code is too complicated, 8/27 Upload and analysis worked. request.form didn't work for a while but it worked now. How to render it...beutifully..
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
    
    conn=sqlite3.connect("gene_data.db")
    cursor=conn.cursor()
    cursor.execute("insert into DNA_list (dna) values(?)", [sequence])
    print("added ", sequence)
    cursor.execute("select * from DNA_list")
    #conn.commit()
    
    return render_template('index.html', result_content=cursor.fetchall())

@app.route('/analyze', methods=['POST'])
def analyze():
    PAM_option=request.form.get('num').split(',')
    gene_number=request.form.get('sequences')
    conn=sqlite3.connect("gene_data.db")
    cursor=conn.cursor()
    cursor.execute("select dna from DNA_list where id= ?", (gene_number))
    sequence=cursor.fetchone()
    PAM_forward,PAM_reverse=analyze_single_file(sequence[0],PAM_option)
    return render_template('result.html', PAM_option=PAM_option, result_content=PAM_forward, result_content2=PAM_reverse)

@app.route('/data')
def databank():
    rows=databaseConnect(engine)
    return render_template('result.html', result_content=[row for row in rows]) #why I cannot jasonify this result content?

if __name__=='__main__':
    app.run(debug=True)

