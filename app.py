
from flask import Flask, render_template, request

app = Flask(__name__)

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
            print("我選擇的主題:", topic)
            if topic == "輸入輸出":
                question_text = "Python 使用哪個函數顯示文字？"
            else:
                question_text = f"目前選擇的主題是：{topic} (請練習相關題目)"
                
        # 2. 點擊「提交答案」按鈕
        elif action == "check":
            student_answer = request.form.get("student_answer", "")
            print("學生提交的答案:", student_answer)
            
            # 保持原本的主題與題目，讓畫面上的選項維持住
            if topic == "輸入輸出":
                question_text = "Python 使用哪個函數顯示文字？"
            
            # 判斷答案（正確答案是 B. print()）
            if student_answer == "B":
                feedback = "答對了！"
            else:
                feedback = "答錯了！"

    return render_template("index.html", topic=topic, question_text=question_text, feedback=feedback)

if __name__ == "__main__":
    app.run(debug=True, port=5001)