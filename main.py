from flask import Flask, render_template, request, redirect, url_for, send_file, send_from_directory
import os
import yt_dlp
from moviepy.editor import VideoFileClip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')

def download_video(url, output_path='video.mp4.webm'):
    try:

        # Supprimer le fichier s'il existe déjà
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], output_path)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], output_path))

        # Utilisez le chemin complet pour sauvegarder la vidéo
        video_path = os.path.join(app.config['UPLOAD_FOLDER'], output_path)

        ydl_opts = {'outtmpl': video_path, 'format': 'bestvideo+bestaudio/best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            return video_path
    except Exception as e:
        print(f"Erreur lors du téléchargement de la vidéo : {e}")
        return None

def convert_to_mp3(video_path, output_path='audio.mp3'):
    try:
        # Supprimer le fichier s'il existe déjà
        if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], output_path)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], output_path))
        
        # Utilisez le chemin complet pour sauvegarder le fichier audio
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], output_path)

        # Extraire l'audio au format MP3
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_path, codec='mp3')
        print("Conversion vers MP3 terminée.")
        return audio_path
    except Exception as e:
        print(f"Erreur lors de la conversion vers MP3 : {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def convert():
    video_url = request.form['video_url']

    # Télécharger la vidéo depuis YouTube
    downloaded_video_path = download_video(video_url)

    if downloaded_video_path:
        # Convertir la vidéo en MP3
        converted_audio_path = convert_to_mp3(downloaded_video_path)
        if converted_audio_path:
            download_link = url_for('download_file', filename='audio.mp3')
            return render_template('index.html', download_link=download_link, show_loader=False)
        else:
            return render_template('index.html', error_message='Erreur lors de la conversion en MP3.', show_loader=False)
    else:
        return render_template('index.html', error_message='Erreur lors du téléchargement de la vidéo.', show_loader=False)
@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
