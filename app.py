from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.dbjungle
memos = db.memos


# 메인 페이지 (좋아요 내림차순)
@app.route("/")
def home():
    memo_list = list(memos.find().sort("likes", -1))
    for memo in memo_list:
        memo["_id"] = str(memo["_id"])
    return render_template("index.html", memos=memo_list)


# 메모 저장
@app.route("/memo", methods=["POST"])
def save_memo():
    memos.insert_one({
        "title": request.form["title"],
        "content": request.form["content"],
        "likes": 0
    })
    return jsonify({"result": "success"})


# 메모 수정
@app.route("/update/<memo_id>", methods=["PATCH"])
def update_memo(memo_id):
    memos.update_one(
        {"_id": ObjectId(memo_id)},
        {"$set": {
            "title": request.form["title"],
            "content": request.form["content"]
        }}
    )
    return jsonify({"result": "success"})


# 메모 삭제
@app.route("/delete/<memo_id>", methods=["DELETE"])
def delete_memo(memo_id):
    memos.delete_one({"_id": ObjectId(memo_id)})
    return jsonify({"result": "success"})


# 좋아요 증가
@app.route("/like/<memo_id>", methods=["POST"])
def like_memo(memo_id):
    memos.update_one(
        {"_id": ObjectId(memo_id)},
        {"$inc": {"likes": 1}}
    )
    return jsonify({"result": "success"})


if __name__ == "__main__":
    app.run(debug=True)
