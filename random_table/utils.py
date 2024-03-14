

def extract_digits(number):
    str_number = str(number)
    return int(str_number[0] + str_number[-1])

def check_value_integer_string(value):
    if isinstance(value ,str):
        if not value.isdigit():
            return False
    elif isinstance(value , int):
        return True
    
def calculate_columns(size):
    # Define the maximum number of columns
    max_columns = 10


    rows = size // max_columns
    if size % max_columns != 0:
        rows += 1

    # Calculate the number of columns
    columns = size // rows

    return columns