import os
from pyment import PyComment

filename = 'copy_important_files.py'

c = PyComment(filename)
c.proceed()
c.diff_to_file(os.path.basename(filename) + ".patch")
for s in c.get_output_docs():
    print(s)