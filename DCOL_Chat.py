#!/usr/bin/env python3

import socket
import argparse
import binascii
from DCOL_Encode import DCOL_Encode

def get_args():

    parser = argparse.ArgumentParser(description="TCP Client for sending hex data.")
    parser.add_argument("ip", help="GNSS IP address")
    parser.add_argument("port", type=int, help="GNSS port number",default=5018)

   args = parser.parse_args()
   return (vars(args))


def main():
    # Argument parser to take IP and port from command line
    args=get_args()
    Encode = DCOL_Encode()

    # Create and connect the socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((args.ip, args.port))
            print(f"Connected to {args.ip}:{args.port}")

            while True:
                # Request packet ID (1 byte in hex)
                packet_id = input("Enter packet ID (1 byte hex, e.g., 03 or 1a) (or 'exit' to quit): ")

                if packet_id.lower() == 'exit':
                    break

                # Validate packet ID (1 byte)
                if len(packet_id) != 2 or not all(c in "0123456789abcdefABCDEF" for c in packet_id):
                    print("Invalid packet ID. Must be 1 byte (2 hex characters).")
                    continue

                # Request data payload in hex
                hex_data = input("Enter hex data to send (or 'exit' to quit): ")

                if hex_data.lower() == 'exit':
                    break

                try:
                    # Convert packet ID and hex data to binary
                    binary_packet_id = binascii.unhexlify(packet_id)
                    binary_data = binascii.unhexlify(hex_data)
                except binascii.Error:
                    print("Invalid hex input. Please try again.")
                    continue

                # Combine packet ID and data
                full_packet = Encode (binary_packet_id,binary_data)

                # Send packet
                s.sendall(full_packet)
                print(f"Sent: {full_packet}")

                # Receive response
                response = s.recv(1024)
                if response:
                    print(f"Received: {binascii.hexlify(response).decode()}")
                else:
                    print("No response from server.")
                    break

        except ConnectionError:
            print(f"Failed to connect to {args.ip}:{args.port}")

if __name__ == "__main__":
    main()
