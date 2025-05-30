from flask import Flask, request, render_template, send_file, jsonify
import yt_dlp
import os
import shutil
import logging
import webbrowser
import threading

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# region Funktion zum Herunterladen der YouTube-Playlist oder Videos als MP3
def download_youtube_as_mp3(url, output_path):
    ydl_opts = {
        'cookiesfrombrowser': ('firefox',),
        'age_limit': 99,
        'extractor_args': {
            'youtubetab': ['skip=authcheck']
        },
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        # Prüfe, ob es sich um eine Playlist handelt, und nummeriere entsprechend
        'outtmpl': os.path.join(output_path, '%(playlist_index)s - %(title)s.%(ext)s') if is_playlist(url) else os.path.join(output_path, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def is_playlist(url):
    # Prüft, ob es sich um eine YouTube-Playlist handelt anhand der Parameter in der URL
    is_playlist = 'playlist' in url or 'list=' in url
    logging.debug(f"URL: {url} | Is Playlist: {is_playlist}")
    return is_playlist

# endregion

# region Route für die Startseite
@app.route('/')
def index():
    return render_template('index.html')
# endregion

# region Route für den Download-Prozess
@app.route('/download', methods=['POST'])
def download():
    playlist_url = request.form.get('playlist_url')
    output_path = './downloads'

    # region Eingabevalidierung
    if not playlist_url or 'youtube.com' not in playlist_url:
        logging.error("Invalid URL provided.")
        return jsonify({'error': 'Please add a valid YouTube link.'}), 400
    # endregion

    # region Verzeichnis leeren, falls es existiert
    if os.path.exists(output_path):
        logging.info("Clearing existing download directory.")
        for filename in os.listdir(output_path):
            file_path = os.path.join(output_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Datei oder symbolischen Link löschen
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Unterordner löschen
            except Exception as e:
                logging.error(f"Fehler beim Löschen von {file_path}: {e}")
    else:
        os.makedirs(output_path)
    # endregion

    try:
        if is_playlist(playlist_url):
            # Wenn es sich um eine Playlist handelt, heruntergeladen und ZIP erstellen
            logging.info("Detected as playlist. Downloading playlist and creating ZIP.")
            download_youtube_as_mp3(playlist_url, output_path)
            shutil.make_archive('mp3_playlist', 'zip', output_path)
            zip_path = 'mp3_playlist.zip'
            logging.debug(f"Returning ZIP file: {zip_path}")
            return send_file(
                zip_path,
                as_attachment=True,
                download_name='mp3_playlist.zip',
                mimetype='application/zip'
            )
        else:
            # Wenn es sich um ein einzelnes Video handelt, herunterladen und als MP3 zurückgeben
            logging.info("Detected as single video. Downloading video as MP3.")
            download_youtube_as_mp3(playlist_url, output_path)
            mp3_files = [f for f in os.listdir(output_path) if f.endswith('.mp3')]
            logging.debug(f"MP3 files found: {mp3_files}")
            if mp3_files:
                mp3_file_path = os.path.join(output_path, mp3_files[0])
                logging.debug(f"Returning MP3 file: {mp3_file_path}")
                return send_file(
                    mp3_file_path,
                    as_attachment=True,
                    download_name=mp3_files[0],
                    mimetype='audio/mpeg'
                )
            else:
                logging.error("No MP3 file found after download.")
                return jsonify({'error': 'Failed to find the MP3 file.'}), 500
    except Exception as e:
        logging.error(f"Error during download process: {e}")
        return jsonify({'error': f'Failed to process the link: {str(e)}'}), 500
# endregion

# Starten der Flask-App
def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1, open_browser).start()
    app.run(debug=False)
