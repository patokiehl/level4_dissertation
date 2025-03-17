import datetime
import os
class Logger:
    def __init__(self, user_ID):
        self.user_id = user_ID
        self.user_dir = os.path.join('data', user_ID) 
        os.makedirs(self.user_dir, exist_ok=True)

    def write_raw(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.calibration_filepath = os.path.join(self.user_dir, 'raw.csv')
        parsed_message = message.split('|')
        parsed_message = [value.split(':', 1)[1] for value in parsed_message]
        with open(self.calibration_filepath, "a") as f:
            f.write(f"{timestamp},{','.join(parsed_message)}\n")



    def write_meta(self, ID, age_range, gender, temperature, manual):
        self.meta_filepath = os.path.join(self.user_dir, 'meta.csv')
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        with open(self.meta_filepath, "a") as f:
            f.write(f"{timestamp},{ID},{age_range},{gender},{temperature},{manual}\n")
    
    def write_calibration(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.calibration_filepath = os.path.join(self.user_dir, 'calibration.csv')
        parsed_message = message.split('|')
        parsed_message = [value.split(':', 1)[1] for value in parsed_message]
        with open(self.calibration_filepath, "a") as f:
            f.write(f"{timestamp},{','.join(parsed_message)}\n")

    def close(self):
        self.file.close()


