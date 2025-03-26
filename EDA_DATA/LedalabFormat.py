import os

# Credit to Shaun Macdonald - edited to be able to work with multiple files
current_dir = os.getcwd()
input_folder = os.path.join(current_dir, "RAW_files")
output_folder = os.path.join(current_dir, "formatted_files")

def parse_file(in_file):
    out_file = os.path.join(output_folder, "parsed" + in_file)
    input_file = os.path.join(input_folder, in_file)
    w = open(out_file, "w")
    f = open(input_file, 'r')
    lines = f.readlines()[3:]
    for row in lines:
        row = row.rstrip()
        csvrow = row.split()
        signal = csvrow[5:]
        for i in signal:
            uS = ( ((float(i)/1024)*3.3)/0.12   )
            w.write(str(uS) + "\n")  
    w.close() 



for file_name in os.listdir(input_folder):
    file_path = os.path.join(input_folder, file_name)
    parse_file(file_name)