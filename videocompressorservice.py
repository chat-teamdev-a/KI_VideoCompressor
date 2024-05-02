import socket
import json

def mmp(command_number, file_name, output_file):
    json_data = {
        "command_number": command_number,
        "file_name": file_name,
        "output_file": output_file
    }
    json_str = json.dumps(json_data)  # 辞書からJSONに変更
    json_size = len(json_str).to_bytes(16, byteorder='big')
    media_type = b'mp4'  # 実際のメディアタイプを設定
    media_type_size = len(media_type).to_bytes(1, byteorder='big')
    payload = b'Your media data here'  # 実際のメディアデータを設定
    payload_size = len(payload).to_bytes(47, byteorder='big')

    return json_size + media_type_size + json_str.encode() + media_type + payload_size + payload


def send_request(command_number, file_name, output_file, address, port):
    request = mmp(command_number, file_name, output_file)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((address, port))
        header = len(request).to_bytes(64, byteorder='big')
        s.sendall(header + request)
        data = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            data += chunk
        with open(output_file, "wb") as f:
            f.write(data)
        print(f"Video processed and downloaded successfully as {output_file}.")

if __name__ == "__main__":
    command_number = input("Enter the command number (1: Compress, 2: Change resolution, 3: Change the video aspect ratio, 4: Convert video to audio, 5: Create GIFs): ")
    file_name = input("Enter the file name to process: ")
    output_file = input("Enter the output file name: ")
    send_request(command_number, file_name, output_file, "localhost", 9050)
