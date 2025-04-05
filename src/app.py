# app.py
from flask import Flask, render_template, request
from agents.Agent import Agent
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    image_url = None

    if request.method == "POST":
        if "image" in request.files:
            image = request.files["image"]
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image_url = "/" + filepath

            natureAgent = Agent(
                name="natureAgent",
                instruction="You need to give a concise plan to make the location from the image better for nature to reinvest in the biodiversity. Be direct and be clear so don't give universal advice but give advice that is good for the given image. Answer in bulletpoints. Never use anything like **.",
                model="gpt-4o",
                openAI=True,
                images=[filepath],
            )

            response = natureAgent.run("Make a plan for the image", debug=False)

    return render_template("index.html", response=response, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
