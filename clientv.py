import socket
import json

def mmp(command_number, file_name, output_file):
    # JSONデータを構築
    json_data = {
        "command_number": str(command_number),
        "file_name": file_name,
        "output_file": output_file
    }
    json_str = json.dumps(json_data)  # 辞書からJSONに変換

    # メディアデータを読み込み
    with open(file_name, "rb") as f:
        media_data = f.read()

    # 各データのサイズを計算
    json_size = len(json_str).to_bytes(16, byteorder='big')
    json_size_padded = json_size.ljust(16, b'\x00')  # JSONサイズを16バイトにパディング
    media_type = b'mp4'  # 実際のメディアタイプを設定
    media_type_size = len(media_type).to_bytes(1, byteorder='big')
    payload_size = len(media_data).to_bytes(47, byteorder='big')

    # データを結合して返す
    return json_size_padded + media_type_size + json_str.encode() + media_type + payload_size + media_data

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
        if data.startswith(b'{"error_code":'):
            error_data = json.loads(data)
            print(f"Error code: {error_data['error_code']}")
            print(f"An error occurred: {error_data['description']}")
            print(f"Solution: {error_data['solution']}")
        else:
            with open(output_file, "wb") as f:
                f.write(data)
            print(f"Video processed and downloaded successfully as {output_file}.")

if __name__ == "__main__":
    command_number = input("Enter the command number (1: Compress, 2: Change resolution, 3: Change the video aspect ratio, 4: Convert video to audio, 5: Create GIFs): ")
    file_name = input("Enter the file name to process: ")
    output_file = input("Enter the output file name: ")
    send_request(command_number, file_name, output_file, "localhost", 9001)
