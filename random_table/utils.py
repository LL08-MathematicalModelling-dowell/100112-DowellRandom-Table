

def extract_digits(number):
    str_number = str(number)
    return int(str_number[0] + str_number[-1])

def check_value_integer_string(value):
    if isinstance(value ,str):
        if not value.isdigit():
            return False
    elif isinstance(value , int):
        return True