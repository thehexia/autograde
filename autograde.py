import os
import sys
from subprocess import call

folder = os.path.abspath(sys.argv[1]);
res_folder = "RESULT_" + os.path.basename(sys.argv[1]);

# for every file in the folder
for filename in os.listdir(folder):
    # result text is stored in the folder
    res_path = res_folder + '/' + filename + ".txt"
    res_path = os.path.abspath(res_path)

    if not res_path:
        print("ERROR: SAVED FAIL")
        break

    # only compile the .cpp files.
    if filename.endswith('.cpp'):
        call(["g++", "-std=c++11", filename])
        call(["a.out"])
