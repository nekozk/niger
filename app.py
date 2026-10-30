
from flask import Flask, render_template, request
import os
import json
from dotenv import load_dotenv
from google import genai
from flask import Flask, render_template, request,session

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
def generate_question(topic):
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=f"""請根據「{topic}」產生一道 Python 初學者的四選一選擇題。
        只能有一個正確答案。
        請回覆 JSON 格式，包含 question、A、B、C、D、answer、explanation 七個欄位。
        answer 只能填入 A、B、C 或 D。
        explanation 請用繁體中文解釋正確答案，50字以內。""",
        config={"response_mime_type": "application/json"}
    )
    return json.loads(response.text)
app = Flask(__name__)
app.secret_key = os.urandom(32)
@app.route("/", methods=["POST", "GET"])
@app.route("/", methods=["POST", "GET"])
def home():
    topic = ""
    question_text = ""
    feedback = ""
    
    if request.method == "POST":
        action = request.form.get("action", "")
        topic = request.form.get("topic", "")
        
        # 1. 點擊「幫我出題」按鈕
        if action == "generate":
            if not topic:
                question_text = "請先選擇學習主題"
            else:
                question_data = generate_question(topic)
                session["question_data"] = question_data
                session["topic"] = topic
                question_text = question_data["question"]
                
        # 2. 點擊「提交答案」按鈕
        elif action == "check":
            question_data = session.get("question_data", {})
            topic = session.get("topic", "")  # 確保抓回原本的主題
            student_answer = request.form.get("student_answer", "")
            
            if not question_data:
                feedback = "目前尚未產生題目，請先點擊幫我出題。"
            else:
                question_text = question_data["question"]
                if student_answer == "":
                    feedback = "請先選擇答案。"
                elif student_answer == question_data["answer"]:
                    feedback = "答對了！" + question_data["explanation"]
                else:
                    feedback = "答錯了！正確答案是 " + question_data["answer"] + "。" + question_data["explanation"]

    # 關鍵：這裡必須包含 question_data 與 topic，網頁才能顯示四個選項與維持狀態！
    return render_template(
        "index.html", 
        topic=topic, 
        question_text=question_text, 
        feedback=feedback,
        question_data=session.get("question_data", {})
    )
if __name__ == "__main__":
    app.run(debug=True, port=5001)