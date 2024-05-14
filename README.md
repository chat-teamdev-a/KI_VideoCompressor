# Video Compressor Service
## 概要

このプログラムは、動画処理を行うサービスです。クライアントが指定した動画ファイルに対して、圧縮、解像度変更、アスペクト比変更、音声への変換、GIFへの変換のいずれかの操作をリクエストできます。

## インストール

1. Python 3.x をインストールします。
2. `ffmpeg-python` パッケージをインストールします。

   ```bash
   pip install ffmpeg-python
   ```

## 使い方

### サーバーの起動

1. `videocompressorservice_server.py` を実行してサーバーを起動します。

   ```bash
   python videocompressorservice_server.py
   ```

### クライアントからのリクエスト

1. `videocompressorservice.py` を実行してクライアントとして動作させます。

   ```bash
   python videocompressorservice.py
   ```

2. プログラムは、コマンド番号、ファイル名、出力ファイル名の入力を求めます。
3. コマンド番号を次のように入力します。
   - 1: 動画の圧縮
   - 2: 解像度の変更
   - 3: アスペクト比の変更
   - 4: 動画を音声に変換
   - 5: GIF への変換
4. ファイル名と出力ファイル名を入力します。
5. リクエストがサーバーに送信され、処理された動画ファイルがダウンロードされます。

## 注意事項

- サーバーはローカルホスト（localhost）上でのみ動作します。
- 処理された動画ファイルは、クライアントと同じディレクトリに保存されます。
