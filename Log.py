import datetime
class Logger:
    def __init__(self):
        self.file = open('data/raw/log.csv', 'a')

    def write(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.file.write(f"{timestamp},{message}\n")
        self.file.flush()


    def close(self):
        self.file.close()

