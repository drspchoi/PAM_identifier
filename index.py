"""
PAM indentifier web application version
"""

import os
from flask import Flask, render_template, request, send_file
import pandas as pd

app = Flask(__name__)
#3/8 how to make it show result in index. Need to save data in dictionary

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
    PAM_option2=request.form.get('num').split(',')
    print(PAM_option)

    temp_result='templates/tmp_result.html'

    PAM_forward=analyze_single_file(file_path,temp_result,PAM_option,PAM_option2)

    '''
    with open(temp_result, 'r') as result_file:
        result_content = result_file.read()
    print(result_content)
    '''
    os.remove(file_path)
    
    return render_template('result.html', result_content=PAM_forward[1], result_content2=PAM_forward[0])

def analyze_single_file(input_file_path, output_file_path, PAM_option, PAM_option2):
    try:
        with open(input_file_path, 'r') as file:
            DNA_sequence = file.read()

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        return  # Skip to the next file if it's not found

    DNA_sequence = ''.join(DNA_sequence).replace('\n', '')

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

    PAM_forward = PAM_forwardstrand(DNA_sequence, PAM_option)
    PAM_reverse = PAM_reversestand(Reverse_strand, PAM_option2)
    forward_df = pd.DataFrame(PAM_forward[0])
    reverse_df = pd.DataFrame(PAM_reverse[0])
    #html_generator(output_file_path, DNA_sequence, Reverse_strand, PAM_forward, PAM_reverse, forward_df, reverse_df)
    return PAM_forward 
'''
def html_generator(output_file_path, DNA_sequence, Reverse_strand, PAM_forward, PAM_reverse, forward_df, reverse_df):
    with open(output_file_path, 'w') as file:
        file.write("<html><head><title>DNA Analysis Report</title></head><body>\n")

        # Write Forward Strand information
        file.write("<h2>Forward Strand Analysis</h2>\n")
        file.write("Forward strand: " + PAM_forward[1] + '<br>\n<br>')
        file.write("Length of sequences: " + str(len(DNA_sequence)) + '<br>\n<br>')
        file.write("PAM location and PAM+Protospacer in Forward strand:<br>\n")

        for i in range(forward_df.shape[0]):
            table = pd.DataFrame(PAM_forward[0][i])
            file.write("<div style='float: left; margin-right: 20px;'>")
            file.write(table.to_html(index=False, classes='table table-bordered table-striped'))
            file.write("</div>")

        file.write("<div style='clear: both;'></div>")

        # Write Reverse Strand information
        file.write("\n<h2>Reverse Strand Analysis</h2>\n")
        file.write("Reverse strand: " + PAM_reverse[1] + '<br>\n<br>')
        file.write("Length of sequences: " + str(len(Reverse_strand)) + '<br>\n<br>')
        file.write("PAM location and PAM+Protospacer in Reverse strand:<br>\n")

        for i in range(reverse_df.shape[0]):
            table = pd.DataFrame(PAM_reverse[0][i])
            file.write("<div style='float: left; margin-right: 20px;'>")
            file.write(table.to_html(index=False, classes='table table-bordered table-striped'))
            file.write("</div>")

        file.write("</body></html>")
'''

def PAM_forwardstrand(DNA_sequence, PAM_option):
    forwardstrand_sequence = list(DNA_sequence)
    result = []
    Final_result = []
    print(PAM_option)
    for PAM in PAM_option:
        forward_position = DNA_sequence.find(PAM)
        while forward_position != -1:
            protospacer = DNA_sequence[forward_position: forward_position + 25]
            GC = (protospacer.count('g') + protospacer.count('c')) / len(protospacer) * 100
            combined_results = {'PAM_position': forward_position + 1, 'PAM+protospacer': protospacer, 'G+C (%)': GC}
            result.append(combined_results)

            forwardstrand_sequence[forward_position: forward_position + 4] = [
                '<strong style="color: red;">' + forwardstrand_sequence[forward_position],
                forwardstrand_sequence[forward_position + 1],
                forwardstrand_sequence[forward_position + 2],
                forwardstrand_sequence[forward_position + 3] + '</strong>'
            ]

            forward_position = DNA_sequence.find(PAM, forward_position + 1)

        Final_result.append(result)
        result = []

    return Final_result, ''.join(forwardstrand_sequence)


def PAM_reversestand(Reverse_strand, PAM_option2):
    Reverse_sequence = list(Reverse_strand)
    result_reverse = []
    final_result = []
    PAM_option2 = [PAM[::-1] for PAM in PAM_option2]

    for PAM in PAM_option2:

        Reverse_position = Reverse_strand.find(PAM)

        if Reverse_position < 21:
            continue

        while Reverse_position != -1:
            Protospacer = Reverse_strand[Reverse_position - 21: Reverse_position + 4]
            GC = (Protospacer.count('g') + Protospacer.count('c')) / len(Protospacer) * 100
            combined_results_reverse = {'PAM_position': Reverse_position + 4, 'PAM+protospacer': Protospacer[::-1],
                                        'G+C (%)': GC}
            result_reverse.append(combined_results_reverse)

            Reverse_sequence[Reverse_position: Reverse_position + 4] = [
                '<strong style="color: red;">' + Reverse_sequence[Reverse_position],
                Reverse_sequence[Reverse_position + 1], Reverse_sequence[Reverse_position + 2],
                Reverse_sequence[Reverse_position + 3] + '</strong>']

            Reverse_position = Reverse_strand.find(PAM, Reverse_position + 1)
        final_result.append(result_reverse)
        result_reverse = []

    return final_result, ''.join(Reverse_sequence)

if __name__=='__main__':
    app.run(debug=True)
