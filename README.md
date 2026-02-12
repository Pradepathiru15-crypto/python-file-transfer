# File Transfer System

A simple file transfer system using Python socket programming with TCP.

## Files

- **server.py** - The server that receives files from clients
- **client.py** - The client that sends files to the server

## Requirements

- Python 3.x (no external libraries needed)

## How to Run

### Step 1: Start the Server

Open a terminal/command prompt and run:

```bash
cd C:\Users\Pradepathiru\.gemini\antigravity\scratch\file_transfer_system
python server.py
```

You should see:
```
==================================================
       FILE TRANSFER SERVER
==================================================

[*] Server started successfully!
[*] Listening on 127.0.0.1:5001
[*] Waiting for incoming connections...
```

### Step 2: Run the Client (in a new terminal)

Open another terminal/command prompt and run:

```bash
cd C:\Users\Pradepathiru\.gemini\antigravity\scratch\file_transfer_system
python client.py
```

### Step 3: Send a File

1. When prompted, enter the full path to the file you want to send
2. You can also drag and drop a file into the terminal
3. The client will show progress as the file transfers
4. The server will save the file in its current directory

## Example Usage

**Client Terminal:**
```
[?] Enter the file path to send (or 'quit' to exit): C:\Users\example\photo.jpg

[*] Connecting to 127.0.0.1:5001...
[+] Connected to server!
[*] Preparing to send: photo.jpg
[*] File size: 102400 bytes
[*] Server ready. Starting file transfer...
[*] Progress: 100.0% (102400/102400 bytes)
[+] File 'photo.jpg' sent successfully!
[*] Connection closed.

[+] Transfer complete!
```

**Server Terminal:**
```
[+] Connection established from 127.0.0.1:54321
[*] Receiving file: photo.jpg
[*] File size: 102400 bytes
[*] Progress: 100.0% (102400/102400 bytes)
[+] File 'photo.jpg' received successfully!
[+] Saved to: C:\...\file_transfer_system\photo.jpg
[*] Connection closed.

[*] Waiting for next connection...
```

## Features

- ✅ TCP socket communication (reliable transfer)
- ✅ Transfers any file type (text, images, videos, etc.)
- ✅ Progress display during transfer
- ✅ Error handling for common issues
- ✅ Clear console messages
- ✅ Beginner-friendly code with comments

## Configuration

You can modify these settings at the top of each file:

| Setting | Default | Description |
|---------|---------|-------------|
| HOST | 127.0.0.1 | Server IP address |
| PORT | 5001 | Server port number |
| BUFFER_SIZE | 1024 | Chunk size in bytes |

## Troubleshooting

1. **"Could not bind to address"** - The port is already in use. Either close the other program using it or change PORT to a different number.

2. **"Connection refused"** - Make sure the server is running before starting the client.

3. **"File not found"** - Check that the file path is correct. Use full absolute paths.
