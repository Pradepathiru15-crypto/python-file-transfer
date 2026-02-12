"""
File Transfer Server
=====================
A simple TCP server that receives files from clients.

This server:
- Listens on localhost (127.0.0.1) port 5001
- Accepts client connections
- Receives file name and file data
- Saves the file with its original name
- Displays progress messages

Author: File Transfer System
"""

import socket
import os

# =====================
# SERVER CONFIGURATION
# =====================
HOST = '127.0.0.1'  # Server IP address (localhost)
PORT = 5001         # Port to listen on
BUFFER_SIZE = 1024  # Size of data chunks to receive (1 KB)
SEPARATOR = "<SEPARATOR>"  # Separator between filename and filesize

def start_server():
    """
    Main function to start the file transfer server.
    Creates a TCP socket, binds to the specified address, and waits for connections.
    """
    
    # Create a TCP socket
    # AF_INET = IPv4 addressing
    # SOCK_STREAM = TCP (reliable, connection-oriented)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow socket address reuse (helps when restarting the server quickly)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind the socket to our address and port
        server_socket.bind((HOST, PORT))
        print(f"[*] Server started successfully!")
        print(f"[*] Listening on {HOST}:{PORT}")
        print(f"[*] Waiting for incoming connections...\n")
        
        # Listen for incoming connections (1 = max queued connections)
        server_socket.listen(1)
        
        while True:
            # Accept a client connection
            # This blocks until a client connects
            client_socket, client_address = server_socket.accept()
            print(f"[+] Connection established from {client_address[0]}:{client_address[1]}")
            
            try:
                # Receive file information (filename and filesize)
                # First, we receive the metadata about the file
                received_data = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                
                # Check if we received valid data
                if not received_data:
                    print("[-] No data received from client.")
                    client_socket.close()
                    continue
                
                # Split the received data to get filename and filesize
                # Format: filename<SEPARATOR>filesize
                filename, filesize = received_data.split(SEPARATOR)
                
                # Extract just the filename (remove any path information)
                filename = os.path.basename(filename)
                filesize = int(filesize)
                
                print(f"[*] Receiving file: {filename}")
                print(f"[*] File size: {filesize} bytes")
                
                # Send acknowledgment to client to start sending file data
                client_socket.send("READY".encode('utf-8'))
                
                # Open file for writing in binary mode
                # Binary mode is important for all file types (images, PDFs, etc.)
                bytes_received = 0
                
                with open(filename, 'wb') as file:
                    # Keep receiving data until we have the complete file
                    while bytes_received < filesize:
                        # Calculate how many bytes are left to receive
                        bytes_remaining = filesize - bytes_received
                        
                        # Receive data (either BUFFER_SIZE or remaining bytes, whichever is smaller)
                        chunk = client_socket.recv(min(BUFFER_SIZE, bytes_remaining))
                        
                        # If no data received, connection might be broken
                        if not chunk:
                            print("[-] Connection lost during transfer!")
                            break
                        
                        # Write received chunk to file
                        file.write(chunk)
                        bytes_received += len(chunk)
                        
                        # Calculate and display progress
                        progress = (bytes_received / filesize) * 100
                        print(f"\r[*] Progress: {progress:.1f}% ({bytes_received}/{filesize} bytes)", end='')
                
                # Print newline after progress bar
                print()
                
                # Check if file was completely received
                if bytes_received == filesize:
                    print(f"[+] File '{filename}' received successfully!")
                    print(f"[+] Saved to: {os.path.abspath(filename)}")
                    
                    # Send success confirmation to client
                    client_socket.send("SUCCESS".encode('utf-8'))
                else:
                    print(f"[-] File transfer incomplete. Received {bytes_received}/{filesize} bytes.")
                    client_socket.send("FAILED".encode('utf-8'))
                    
            except ValueError as e:
                print(f"[-] Error parsing file information: {e}")
            except Exception as e:
                print(f"[-] Error during file transfer: {e}")
            finally:
                # Close the client connection
                client_socket.close()
                print(f"[*] Connection closed.\n")
                print("[*] Waiting for next connection...")
                
    except OSError as e:
        print(f"[-] Error: Could not bind to {HOST}:{PORT}")
        print(f"[-] Details: {e}")
        print("[*] Make sure the port is not already in use.")
    except KeyboardInterrupt:
        print("\n[*] Server shutting down...")
    finally:
        # Close the server socket
        server_socket.close()
        print("[*] Server stopped.")


# =====================
# MAIN ENTRY POINT
# =====================
if __name__ == "__main__":
    print("=" * 50)
    print("       FILE TRANSFER SERVER")
    print("=" * 50)
    print()
    start_server()
