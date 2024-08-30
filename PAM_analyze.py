def analyze_single_file(DNA_sequence, PAM_option):
    
    NA_sequence = ''.join(DNA_sequence).replace('\n', '')
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
            GC = "{:.2f}".format(GC)
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