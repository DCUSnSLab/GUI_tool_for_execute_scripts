import os

def parent_process():
    print("This is the parent process.")
    print("Parent PID:", os.getpid())

def child_process():
    print("This is the child process.")
    print("Child PID:", os.getpid())

child_pid = os.fork()

if child_pid == 0:
    child_process()
else:
    parent_process()