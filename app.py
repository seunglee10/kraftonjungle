from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017")
db = client.dbjungle
memos = db.memos

# 메모 조회
@app.route("/")
def home():
    memo_list = list(memos.find().sort("likes", -1))
    for memo in memo_list:
        memo["_id"] = str(memo["_id"])
    return render_template("index.html", memos=memo_list)


# 메모 저장
@app.route("/memo", methods=["POST"])
def save_memo():
    title = request.form.get("title")
    content = request.form.get("content")

    memo = {
        "title": title,
        "content": content,
        "likes": 0
    }
    memos.insert_one(memo)
    return redirect(url_for("home"))


# 메모 수정
@app.route("/update/<memo_id>", methods=["PATCH"])
def update_memo(memo_id):
    title = request.form.get("title")
    content = request.form.get("content")

    memos.update_one(
        {"_id": ObjectId(memo_id)},
        {"$set": {
            "title": title,
            "content": content
        }}
    )
    return redirect(url_for("home"))


# 메모 삭제
@app.route("/delete/<memo_id>")
def delete_memo(memo_id):
    memos.delete_one(
        {"_id": ObjectId(memo_id)}
    )
    return redirect(url_for("home"))


# 좋아요 수 증가
@app.route("/like/<memo_id>")
def like_memo(memo_id):
    memos.update_one(
        {"_id": ObjectId(memo_id)},
        {"$inc": {"likes": 1}}
    )
    return redirect(url_for("home")) 


# 좋아요 순으로 조회
@app.route("/edit/<memo_id>")
def edit_memo(memo_id):
    memo_list = list(memos.find().sort("likes", -1))
    for memo in memo_list:
        memo["_id"] = str(memo["_id"])
        
    return render_template(
        "index.html",
        memos=memo_list,
        edit_id=memo_id
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

