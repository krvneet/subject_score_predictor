import logging
import time 
import os
from datetime import datetime


LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
LOGS_PATH = os.path.join(os.getcwd(),"logs")
os.makedirs(LOGS_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE_NAME)

# Basic logging object/info
logging.basicConfig(
    filename = LOG_FILE_PATH, # In which file we have to write logs? Hence, requires whole file path.
    format = '[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO    
)


# Testing Code
if __name__ == "__main__":
    for i in range(1, 4):
        logging.info(f"Test {i}: Logging is working fine :)")
        time.sleep(3)