from flask import Flask, request, send_file, jsonify
import os
import yt_dlp as youtube_dl
import ffmpeg
import logging

app = Flask(__name__)

# Directory for the music files
DOWNLOAD_DIR = "music_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

logging.basicConfig(level=logging.DEBUG)

def download_and_convert(youtube_url):
    try:
        # Download the YouTube video
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, 'temp.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'verbose': True  # Enable verbose output for debugging
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_url, download=True)
            audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')
            logging.info(f"Downloaded audio to {audio_file_path}")

        # Convert to 8-bit unsigned WAV, 48 kHz, mono
        output_path = os.path.join(DOWNLOAD_DIR, f"{info_dict['id']}.wav")
        ffmpeg.input(audio_file_path).output(output_path, format='wav', acodec='pcm_u8', ac=1, ar='48k').run(overwrite_output=True)
        logging.info(f"Converted audio to {output_path}")
        os.remove(audio_file_path)
        logging.info(f"Deleted original file {audio_file_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error during download and conversion: {e}")
        raise

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    youtube_url = data.get('url')
    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        file_path = download_and_convert(youtube_url)
        if not os.path.exists(file_path):
            return jsonify({"error": "File not found after conversion"}), 500
        # Construct the file URL to return
        file_url = f"http://{request.host}/audio/{os.path.basename(file_path)}"
        logging.info(f"File URL to return: {file_url}")
        return jsonify({"file_url": file_url}), 200
    except Exception as e:
        logging.error(f"Error during file processing: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    file_path = os.path.join(DOWNLOAD_DIR, filename)
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
