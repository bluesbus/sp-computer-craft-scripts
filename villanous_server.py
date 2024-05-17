from flask import Flask, request, send_file, jsonify
import os
import youtube_dl
import ffmpeg

app = Flask(__name__)

# directory for the music files
DOWNLOAD_DIR = "music_downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_and_convert(youtube_url):
    # download the youtube video
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, 'temp.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        audio_file_path = ydl.prepare_filename(info_dict).replace('.webm', '.wav').replace('.m4a', '.wav')

    # conver the youtube to the right format
    output_path = os.path.join(DOWNLOAD_DIR, f"{info_dict['id']}.wav")
    ffmpeg.input(audio_file_path).output(output_path, format='wav', acodec='pcm_u8', ac=1, ar='48k').run(overwrite_output=True)
    os.remove(audio_file_path)
    return output_path

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    youtube_url = data.get('url')
    if not youtube_url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        file_path = download_and_convert(youtube_url)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
