from flask import Flask, render_template, request, jsonify
from rag import ask_rag

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({
                "answer": "من فضلك اكتبي سؤالك الأول."
            }), 400

        answer = ask_rag(question)

        return jsonify({
            "answer": answer
        })

    except Exception as e:
        print("Error:", e)

        return jsonify({
            "answer": "حصل خطأ أثناء معالجة السؤال."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)