"""
File Transfer Client
=====================
A simple TCP client that sends files to the server.

This client:
- Connects to the server at localhost:5001
- Asks user for the file path to send
- Sends the file name and file data in chunks
- Displays progress and status messages

Author: File Transfer System
"""

import socket
import os

# =====================
# CLIENT CONFIGURATION
# =====================
HOST = '127.0.0.1'  # Server IP address (localhost)
PORT = 5001         # Server port
BUFFER_SIZE = 1024  # Size of data chunks to send (1 KB)
SEPARATOR = "<SEPARATOR>"  # Separator between filename and filesize


def send_file(filepath):
    """
    Send a file to the server.
    
    Args:
        filepath: Path to the file to send
        
    Returns:
        True if file was sent successfully, False otherwise
    """
    
    # Create a TCP socket
    # AF_INET = IPv4 addressing
    # SOCK_STREAM = TCP (reliable, connection-oriented)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        print(f"[*] Connecting to {HOST}:{PORT}...")
        client_socket.connect((HOST, PORT))
        print(f"[+] Connected to server!")
        
        # Get the filename and file size
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        
        print(f"[*] Preparing to send: {filename}")
        print(f"[*] File size: {filesize} bytes")
        
        # Send file information to server
        # Format: filename<SEPARATOR>filesize
        file_info = f"{filename}{SEPARATOR}{filesize}"
        client_socket.send(file_info.encode('utf-8'))
        
        # Wait for server acknowledgment
        response = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        
        if response != "READY":
            print(f"[-] Server not ready. Response: {response}")
            return False
        
        print("[*] Server ready. Starting file transfer...")
        
        # Open and send the file in chunks
        bytes_sent = 0
        
        with open(filepath, 'rb') as file:
            while True:
                # Read a chunk of data from the file
                chunk = file.read(BUFFER_SIZE)
                
                # If no more data to read, we're done
                if not chunk:
                    break
                
                # Send the chunk to the server
                client_socket.send(chunk)
                bytes_sent += len(chunk)
                
                # Calculate and display progress
                progress = (bytes_sent / filesize) * 100
                print(f"\r[*] Progress: {progress:.1f}% ({bytes_sent}/{filesize} bytes)", end='')
        
        # Print newline after progress bar
        print()
        
        # Wait for server confirmation
        confirmation = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        
        if confirmation == "SUCCESS":
            print(f"[+] File '{filename}' sent successfully!")
            return True
        else:
            print(f"[-] Server reported transfer failed: {confirmation}")
            return False
            
    except ConnectionRefusedError:
        print(f"[-] Error: Could not connect to {HOST}:{PORT}")
        print("[*] Make sure the server is running.")
        return False
    except FileNotFoundError:
        print(f"[-] Error: File not found: {filepath}")
        return False
    except PermissionError:
        print(f"[-] Error: Permission denied to read file: {filepath}")
        return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False
    finally:
        # Close the socket connection
        client_socket.close()
        print("[*] Connection closed.")


def main():
    """
    Main function to run the file transfer client.
    Prompts user for file path and sends the file to the server.
    """
    
    print("=" * 50)
    print("       FILE TRANSFER CLIENT")
    print("=" * 50)
    print()
    print(f"[*] Server address: {HOST}:{PORT}")
    print()
    
    while True:
        # Ask user for the file path
        print("-" * 50)
        filepath = input("[?] Enter the file path to send (or 'quit' to exit): ").strip()
        
        # Check if user wants to quit
        if filepath.lower() in ['quit', 'exit', 'q']:
            print("[*] Goodbye!")
            break
        
        # Check if path is empty
        if not filepath:
            print("[-] Please enter a valid file path.")
            continue
        
        # Remove quotes if user added them (common on Windows when dragging files)
        filepath = filepath.strip('"').strip("'")
        
        # Check if file exists
        if not os.path.isfile(filepath):
            print(f"[-] Error: File not found: {filepath}")
            print("[*] Please check the path and try again.")
            continue
        
        # Check if file is readable
        if not os.access(filepath, os.R_OK):
            print(f"[-] Error: Cannot read file: {filepath}")
            print("[*] Please check file permissions.")
            continue
        
        print()
        
        # Send the file
        success = send_file(filepath)
        
        if success:
            print("\n[+] Transfer complete!")
        else:
            print("\n[-] Transfer failed. Please try again.")
        
        print()


# =====================
# MAIN ENTRY POINT
# =====================
if __name__ == "__main__":
    main()
