

class RandomTableError(Exception):
    pass

class DatabaseFetchError(RandomTableError):
    pass 

class RandomTableTypeError(RandomTableError):
    pass