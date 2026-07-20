import os
import yt_dlp

class VideoDownloader:
    """
    Downloads source long-form videos from YouTube, Vimeo, Twitch, or direct MP4 URLs.
    """
    def __init__(self, output_dir="/tmp/auto_clipper/downloads"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def download(self, url: str) -> dict:
        out_tmpl = os.path.join(self.output_dir, '%(id)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': out_tmpl,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith('.mp4'):
                filename = os.path.splitext(filename)[0] + '.mp4'

            return {
                "id": info.get("id"),
                "title": info.get("title"),
                "duration": info.get("duration"),
                "filepath": filename
            }
