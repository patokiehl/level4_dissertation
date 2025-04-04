import os
import datetime
import json

current_dir = os.getcwd()
input_folder = os.path.join(current_dir, "RAW_EDA_data")
output_folder = os.path.join(current_dir, "formatted_EDA_data")

def parse_file(in_file):
    input_file = os.path.join(input_folder, in_file)
    with open(input_file, 'r') as f:
        lines = f.readlines()
    # needed to be able to map date and time to a unix timestamp
    header_data = None 
    for line in lines: 
        if line.startswith('# {'): # take the header data from opensignals
            header_data = line[1:].strip()
            break

    header = json.loads(header_data)
    #print(header)
    device_info = list(header.values())[0]

    date_str = device_info["date"]
    time_str = device_info["time"]

    dt_str = f"{date_str} {time_str}"
    dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S.%f")
    dt = dt.replace(tzinfo=datetime.timezone.utc)

    base_timestamp = dt.timestamp() # convert to unix timestamp
    #print(base_timestamp)

    sampling_rate = device_info.get("sampling rate", 10)
    out_file = os.path.join(output_folder, in_file)

    try:
        header_end_index = lines.index("# EndOfHeader\n")
    except ValueError:
        print("Could not find header end in", in_file)
        return
    data_lines = lines[header_end_index+1:]
    
    # Sampling of EDA data, adapted from work by Shaun Macdonald - adapted by adding a timestamp from the raw file
    with open(out_file, "w") as w:
        sample_index = 0
        for row in data_lines:
            row = row.rstrip()
            csvrow = row.split()
            signal_values = csvrow[5:]
            for value in signal_values:
                uS = (((float(value) / 1024) * 3.3) / 0.12)
                sample_timestamp = base_timestamp + (sample_index / sampling_rate) # update the timestamp by 1/10 seconds for each sample
                w.write(f"{sample_timestamp},{uS}\n")
                sample_index += 1

for file_name in os.listdir(input_folder):
    parse_file(file_name)
