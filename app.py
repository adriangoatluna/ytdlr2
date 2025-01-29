from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            download_path = stream.download()
            return send_file(download_path, as_attachment=True)
        except Exception as e:
            return f"Error: {e}"
    
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
