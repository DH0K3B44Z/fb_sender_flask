from flask import Flask, render_template, request, redirect, url_for
import threading
import sender

app = Flask(__name__)
sending_thread = None
is_running = False

@app.route("/", methods=["GET", "POST"])
def index():
    global is_running

    if request.method == "POST":
        tokens = request.form.get("tokens")
        thread_id = request.form.get("thread_id")
        delay = int(request.form.get("delay"))
        message_file = request.files["message_file"]

        with open("tokens.txt", "w") as f:
            f.write(tokens.strip())

        message_file.save("messages.txt")

        if not is_running:
            is_running = True
            threading.Thread(
                target=sender.start_sending,
                args=("tokens.txt", "messages.txt", thread_id, delay),
                daemon=True
            ).start()

        return redirect(url_for("index"))

    return render_template("index.html", is_running=is_running)

@app.route("/stop")
def stop():
    global is_running
    is_running = False
    sender.stop_sending()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
