def extract_digits(number):
    str_number = str(number)
    return int(str_number[0] + str_number[-1])