import socket
import ffmpeg
import json


class VideoProcessor: #動画を変更するクラス
    def __init__(self):
        pass

    def compress_video(self, input_file, output_file, bitrate='500k'):# 圧縮する関数
        (
            ffmpeg
            .input(input_file)
            .output(output_file, b=bitrate)
            .run()
        )

    def change_resolution(self, input_file, output_file, resolution='720x480'): # 解像度を変更する関数
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vf=f"scale={resolution}")
            .run()
        )

    def change_aspect_ratio(self, input_file, output_file, aspect_ratio='1:1'): # アスペクト比を変更する関数
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vf=f"scale=640:640,setsar={aspect_ratio}")
            .run()
        )

    def convert_to_audio(self, input_file, output_file): # 音声ファイルへ変換する関数
        (
            ffmpeg
            .input(input_file)
            .output(output_file, acodec='mp3')
            .run()
        )

    def convert_to_gif(self, input_file, output_file, start_time, duration, fps=10): #gifへ変更する関数
        (
            ffmpeg
            .input(input_file, ss=start_time, t=duration)
            .output(output_file, vf=f"fps={fps}", pix_fmt='rgb24')
            .run()
        )

class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.processor = VideoProcessor()

    @staticmethod
    def parse_header(header: bytes) -> dict:
        json_size = int.from_bytes(header[:16], byteorder='big') # 最初の16バイト
        media_type_size = int(header[16]) # 次の1バイト
        payload_size = int.from_bytes(header[17:64], byteorder='big') # 残り47バイト
        return {
            "json_size": json_size,
            "media_type_size": media_type_size,
            "payload_size": payload_size
        }

    def handle_client(self, conn):
        try:
            header_size = 64
            header = conn.recv(header_size)
            if not header:
                return

            header_info = self.parse_header(header)
            json_size = header_info["json_size"]
            payload_size = header_info["payload_size"]

            # 必要なデータサイズだけを受信し、バッファに保存する
            data = b""
            while len(data) < json_size + payload_size:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk

            # 受信したデータが期待通りのサイズであるかどうかを確認する
            if len(data) != json_size + payload_size:
                raise ValueError("Received incomplete data")

            # 以降の処理は変更なし
            json_data = data[:json_size].decode()
            print("Received JSON data:", json_data)

            media_data = data[json_size:]

            json_obj = json.loads(json_data)
            command_number = json_obj["command_number"]
            file_name = json_obj["file_name"]
            output_file = json_obj["output_file"]

            if command_number == '1':
                self.process_video('compress', file_name, output_file)
            elif command_number == '2':
                self.process_video('change_resolution', file_name, output_file)
            elif command_number == '3':
                self.process_video('change_aspect_ratio', file_name, output_file)
            elif command_number == '4':
                self.process_video('convert_to_audio', file_name, output_file)
            elif command_number == '5':
                self.process_video('convert_to_gif', file_name, output_file)

            with open(output_file, "rb") as f:
                data = f.read()
                conn.sendall(data)

        except FileNotFoundError as e:
            error_data = {
                "error_code": 404,
                "description": "File not found error.",
                "solution": "Please check the file path and try again."
            }
            self.send_error(conn, error_data)
            print(f"File not found error: {e}")

        except Exception as e:
            error_data = {
                "error_code": 500,
                "description": "An unexpected error occurred.",
                "solution": "Please try again later."
            }
            print(f"Unexpected error occurred: {e}")  # ここで e を定義
            self.send_error(conn, error_data)

    def send_error(self, conn, error_data):
        error_json = json.dumps(error_data)
        conn.sendall(error_json.encode())


    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.processor = VideoProcessor()

    @staticmethod
    def parse_header(header: bytes) -> dict:
        json_size = int.from_bytes(header[:16], byteorder='big') # 最初の16バイト
        media_type_size = int(header[16]) # 次の1バイト
        payload_size = int.from_bytes(header[17:64], byteorder='big') # 残り47バイト
        return {
            "json_size": json_size,
            "media_type_size": media_type_size,
            "payload_size": payload_size
        }

    def handle_client(self, conn):
        try:
            header_size = 64
            header = conn.recv(header_size)
            if not header:
                return

            header_info = self.parse_header(header)
            json_size = header_info["json_size"]
            payload_size = header_info["payload_size"]

            # 必要なデータサイズだけを受信し、バッファに保存する
            data = b""
            while len(data) < json_size + payload_size:
                chunk = conn.recv(1024)
                if not chunk:
                    break
                data += chunk

            # 受信したデータが期待通りのサイズであるかどうかを確認する
            if len(data) != json_size + payload_size:
                raise ValueError("Received incomplete data")

            # 以降の処理は変更なし
            json_data = data[:json_size].decode()
            media_data = data[json_size:]

            print("Received JSON data:", json_data) 

            json_obj = json.loads(json_data)
            command_number = json_obj["command_number"]
            file_name = json_obj["file_name"]
            output_file = json_obj["output_file"]

            if command_number == '1':
                self.process_video('compress', file_name, output_file)
            elif command_number == '2':
                self.process_video('change_resolution', file_name, output_file)
            elif command_number == '3':
                self.process_video('change_aspect_ratio', file_name, output_file)
            elif command_number == '4':
                self.process_video('convert_to_audio', file_name, output_file)
            elif command_number == '5':
                self.process_video('convert_to_gif', file_name, output_file)

            with open(output_file, "rb") as f:
                data = f.read()
                conn.sendall(data)

        except FileNotFoundError as e:
            error_data = {
                "error_code": 404,
                "description": "File not found error.",
                "solution": "Please check the file path and try again."
            }
            self.send_error(conn, error_data)
            print(f"File not found error: {e}")

        except Exception as e:
            error_data = {
                "error_code": 500,
                "description": "An unexpected error occurred.",
                "solution": "Please try again later."
            }
            self.send_error(conn, error_data)
            print(f"Unexpected error occurred: {e}")
    def send_error(self, conn, error_data):
        error_json = json.dumps(error_data)
        conn.sendall(error_json.encode())

    def process_video(self, method, input_file, output_file):
        if method == 'compress':
            self.processor.compress_video(input_file, output_file)
        elif method == 'change_resolution':
            self.processor.change_resolution(input_file, output_file)
        elif method == 'change_aspect_ratio':
            self.processor.change_aspect_ratio(input_file, output_file)
        elif method == 'convert_to_audio':
            self.processor.convert_to_audio(input_file, output_file)
        elif method == 'convert_to_gif':
            self.processor.convert_to_gif(input_file, output_file, start_time=10, duration=5)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(1)
            print("Server is listening...")
            while True:
                conn, addr = s.accept() #conn:socketのオブジェクト addr:アドレス
                with conn:
                    print(f"Connected by {addr}")
                    self.handle_client(conn)

if __name__ == "__main__":
    server = Server("localhost", 9001)
    server.start()
