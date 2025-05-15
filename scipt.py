import requests
from flask import Flask, render_template, url_for, request as req

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer Token"}

        data = req.form.get("data", "")
        maxL = int(req.form.get("maxL", 100))  # Default max length to avoid errors
        minL = maxL // 4

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            try:
                response_data = response.json()
                print("API Response:", response_data)
                return response_data
            except Exception as e:
                print("Error parsing response:", e)
                return []

        output = query({
            "inputs": data,
            "parameters": {"min_length": minL, "max_length": maxL},
        })

        if isinstance(output, list) and output:
            result_text = output[0].get("summary_text", "Summarization failed.")
        else:
            result_text = "Unexpected response format or empty output."

        return render_template("index.html", result=result_text)

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
