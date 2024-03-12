"""
PAM indentifier web application version
"""

import os
from flask import Flask, render_template, request, send_file
import pandas as pd

app = Flask(__name__)
#3/8 how to make it show result in index. Need to save data in dictionary
#3/10 reverse stand generator function, PAM_forward and reverse functon combined, data structure changed to dictionary. for loop needs to be simplified using if  

@app.route('/')
def index():
    return render_template('index5.html')

@app.route('/upload',methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file=request.files['file']
    print(file.filename)

    if file.filename == '':
        return "No selected file"

    file_path=os.path.join('templates', file.filename)
    file.save(file_path)

    PAM_option=request.form.get('num').split(',')
    print(PAM_option)

    temp_result='templates/tmp_result.html'

    PAM_forward,PAM_reverse=analyze_single_file(file_path,temp_result,PAM_option)

    os.remove(file_path)
    
    return render_template('result.html', result_content=PAM_forward, result_content2=PAM_reverse)

def analyze_single_file(input_file_path, output_file_path, PAM_option):
    try:
        with open(input_file_path, 'r') as file:
            DNA_sequence = file.read()

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        return  # Skip to the next file if it's not found

    DNA_sequence = ''.join(DNA_sequence).replace('\n', '')
    Reverse_strand = ReverseStrandGenerator(DNA_sequence)

    PAM_forward = PAM_identifier(DNA_sequence, PAM_option,"forward")
    PAM_reverse = PAM_identifier(DNA_sequence, PAM_option,"backward")

    return PAM_forward, PAM_reverse 

def ReverseStrandGenerator(DNA_sequence):
    Reverse_strand = ""
    for x in DNA_sequence:
        if x == 'a':
            Reverse_strand += 't'
        elif x == 't':
            Reverse_strand += 'a'
        elif x == 'g':
            Reverse_strand += 'c'
        elif x == 'c':
            Reverse_strand += 'g'
        else:
            Reverse_strand += x
    return Reverse_strand

def PAM_identifier(DNA_sequence, PAM_option, direction):
    combined_results={'PAM_position':[], 'PAM+protospacer':[], 'G+C (%)':[]}
    final_result={}

    if direction=="forward":
        input_sequence = list(DNA_sequence)

    elif direction=="backward":
        DNA_sequence=ReverseStrandGenerator(DNA_sequence)
        input_sequence = list(DNA_sequence)
        PAM_option=[PAM[::-1] for PAM in PAM_option]
        
    for PAM in PAM_option:
        PAM_position = DNA_sequence.find(PAM)

        if direction=="backward" and PAM_position < 21:
            continue   

        while PAM_position != -1:
            protospacer = DNA_sequence[PAM_position: PAM_position + 25] if direction =="forward" else DNA_sequence[PAM_position-21:PAM_position+4]
            GC = (protospacer.count('g') + protospacer.count('c')) / len(protospacer) * 100
            combined_results['PAM_position'].append(PAM_position + 1 if direction=="forward" else PAM_position +4)
            combined_results['PAM+protospacer'].append(protospacer if direction=="forward" else protospacer[::-1])
            combined_results['G+C (%)'].append(GC)

            input_sequence[PAM_position: PAM_position + 4] = [
                    '<strong style="color: red;">' + input_sequence[PAM_position],
                    input_sequence[PAM_position + 1],
                    input_sequence[PAM_position + 2],
                    input_sequence[PAM_position + 3] + '</strong>']

            PAM_position = DNA_sequence.find(PAM, PAM_position + 1)

        final_result[PAM]=combined_results
        combined_results={'PAM_position':[],'PAM+protospacer':[],'G+C (%)':[]}
    
    return final_result, ''.join(input_sequence)


if __name__=='__main__':
    app.run(debug=True)
