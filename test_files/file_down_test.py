import os
import sys
import time
import signal

# len(sys.argv) : 파라미터 개수(파라미터없이 실행만 시킬 경우, 개수는 1.)
def exit_handler(signum, frame):
    # print("Handler is exiting due to signal:", signum)
    print("Finished !")
    filepath = os.getcwd()
    print(filepath)
    filename = os.path.join("test_files", "result_files", str(time.strftime("%Y-%m-%d__%A__%H:%M:%S")) + ".txt")
    print(filename)
    file = open(filename, "w")
    file.write("X_coord = " + str(sys.argv[1]) + "\n")
    file.write("Y_coord = " + str(sys.argv[2]) + "\n")
    file.close()
    sys.exit()

signal.signal(signal.SIGTERM, exit_handler)

while True:
    print("Hello World")
    time.sleep(1)