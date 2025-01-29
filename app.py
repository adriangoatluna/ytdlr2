from flask import Flask, render_template, request, send_file
from pytube import YouTube, request as pytube_request
import os

# Fix for "Too Many Requests" (429) error
pytube_request.default_range_func = lambda _: (0, None)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]

        try:
            # Get YouTube video
            yt = YouTube(url)

            # Get the best available video (instead of .get_highest_resolution())
            stream = yt.streams.filter(progressive=True, file_extension="mp4").first()

            # Download the video
            download_path = stream.download()

            # Send the file to the user
            return send_file(download_path, as_attachment=True)

        except Exception as e:
            return f"Error: {e}"  # Display the error if something goes wrong

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
