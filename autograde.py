import os
import sys
from subprocess import call, check_output, STDOUT, CalledProcessError, Popen, PIPE

"""
USAGE:

python autograde.py folder-name

To grade with keyboard input.

python autograde.py folder-name input-file-name.txt

Outputs text files for each student containing compiler output,
program output, and source code in one text file into a folder
called RESULT_folder-name

Terminates all programs running longer than 5 seconds to avoid
infinite loops.

Must have python 3.3+.

Will only grade individual cpp files.
TODO: Support zipped folders.
TODO: Support input prompts.

"""

folder = os.path.abspath(sys.argv[1]);
res_folder = os.path.abspath("RESULT_" + os.path.normpath(sys.argv[1]));

has_input = False
input_file = 0
input_text = ""

if len(sys.argv) > 2:
    input_file = os.path.abspath(sys.argv[2])
    has_input = True
    input_text = open(input_file, "r").read()

if has_input:
    print(input_text)

if not os.path.exists(res_folder):
    os.makedirs(res_folder)

# for every file in the folder
for filename in os.listdir(folder):
    # only compile the .cpp files.
    if filename.endswith('.cpp'):
        # result text is stored in the folder
        res_path = os.path.abspath(res_folder + '/' + filename + ".txt")
        file_path = os.path.abspath(folder + "/" + filename)
        compile_path = os.path.abspath(res_folder + '/' + filename + ".out");

        # output file or create if it doesn't exist.
        f = open(res_path, "w+")
        f.truncate() # delete any existing content

        f.write("\n============= Compiler Output ===============\n")
        f.flush();
        ok = True
        try:
            check_output(["g++-4.9", file_path, "-o", compile_path], stderr=f)
        except CalledProcessError:
            ok = False

        # run
        if ok:
            f.write("\n============= Program Output ===============\n")
            f.flush();

        cmd = compile_path
        # timeout in 5 seconds
        try:
            p = Popen([cmd], stdout=f, stderr=f, stdin=PIPE)
            if has_input:
                p.stdin.write(bytes(input_text, 'utf-8'))
                p.stdin.close()
                p.wait(timeout=5)
        except Exception as ex:
            print(ex)

        #clean up the compiled file
        try:
            os.remove(compile_path)
        except:
            pass

        # write the contents of the cpp to output
        src_path = os.path.abspath(folder + '/' + filename)
        f.write("\n========= Source Code ===========\n")
        try:
            f.writelines([l for l in open(src_path).readlines()])
        except:
            continue

        f.close()
