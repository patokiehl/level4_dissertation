import time
import os
class Logger:
    def __init__(self, user_ID):
        
        self.user_id = user_ID
        self.user_dir = os.path.join('data', f'participant{user_ID}') 
        os.makedirs(self.user_dir, exist_ok=True)

    def write_raw(self, message, calibration_counter):
        timestamp = time.time()
        self.calibration_filepath = os.path.join(self.user_dir, 'raw.csv')
        parsed_message = message.split('|')
        parsed_message = [value.split(':', 1)[1] for value in parsed_message]
        with open(self.calibration_filepath, "a") as f:
            f.write(f"{timestamp},{','.join(parsed_message)},{calibration_counter}\n")



    def write_meta(self, ID, age_range, gender, temperature, manual):
        self.meta_filepath = os.path.join(self.user_dir, 'meta.csv')
        timestamp = time.time()
        with open(self.meta_filepath, "a") as f:
            f.write(f"{timestamp},{ID},{age_range},{gender},{temperature},{manual}\n")
    
    def write_calibration(self, message, calibration_counter):
        timestamp = time.time()
        self.calibration_filepath = os.path.join(self.user_dir, f'calibration{calibration_counter}.csv')
        parsed_message = message.split('|')
        parsed_message = [value.split(':', 1)[1] for value in parsed_message]
        with open(self.calibration_filepath, "a") as f:
            f.write(f"{timestamp},{','.join(parsed_message)}\n")

    def close(self):
        self.file.close()


