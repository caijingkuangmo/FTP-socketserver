import os

has_file_size=os.stat('1.zip').st_size
print(type(has_file_size))