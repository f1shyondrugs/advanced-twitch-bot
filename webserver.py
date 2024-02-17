from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/customtext', methods=['GET', 'POST'])
def home():
    with open("templates/latesttext", "r") as f:
        lines = f.readlines()
        user = str(lines[0]).strip()
        text = str(lines[1])
    return render_template("index.html", text=text, user=user)


@app.route('/activepoll')
def homeaaa():
    return "poll"





if __name__ == '__main__':
    app.run(debug=True)

