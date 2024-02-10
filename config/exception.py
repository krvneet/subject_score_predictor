import sys
from config.logging_config import logging

# function that return only relevant error message details
def error_message_detail(error, error_detail:sys):
    _, _, exc_tb = error_detail.exc_info() # exc_tb is a exception trace back variable/object
    filename = exc_tb.tb_frame.f_code.co_filename
    error_message = f"Error occured in file [{filename}] at line number [{exc_tb.tb_lineno}], Error Message: [{str(error)}]"
    return error_message


class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        logging.info(f"Error: {error_message}")
    
    def __str__(self):  
        return self.error_message


# Testing Code
# if __name__ == "__main__":
#     try:
#         a = 1/0
#     except Exception as e:
#         logging.info("DIVIDE BY ZERO EXCEPTION")
#         raise CustomException(e, sys)