import logging
import os

class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)
        self.directory = os.getcwd() + "/logs/output/"

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        if not self.hasHandlers():
            self.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Stream handler
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.addHandler(stream_handler)

            # File handler
            file_handler = logging.FileHandler(f'{self.directory}/{name}.log')
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)
