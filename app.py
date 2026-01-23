from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.dbjungle
memos = db.memos

# 문자열 id를 ObjectId로 변환, 실패 시 None 반환
def parse_object_id(id_str):
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        return None
        
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
    _id = parse_object_id(memo_id)
    if _id is None:
        return jsonify({"result": "invalid id"}), 400

    result = memos.update_one(
        {"_id": _id},
        {"$set": {
            "title": request.form["title"],
            "content": request.form["content"]
        }}
    )

    if result.matched_count == 0:
        return jsonify({"result": "not found"}), 404

    return jsonify({"result": "success"})


# 메모 삭제
@app.route("/delete/<memo_id>", methods=["DELETE"])
def delete_memo(memo_id):
    _id = parse_object_id(memo_id)
    if _id is None:
        return jsonify({"result": "invalid id"}), 400

    result = memos.delete_one({"_id": _id})
    if result.deleted_count == 0:
        return jsonify({"result": "not found"}), 404

    return jsonify({"result": "success"})


# 좋아요 증가
@app.route("/like/<memo_id>", methods=["POST"])
def like_memo(memo_id):
    _id = parse_object_id(memo_id)
    if _id is None:
        return jsonify({"result": "invalid id"}), 400

    result = memos.update_one(
        {"_id": _id},
        {"$inc": {"likes": 1}}
    )

    if result.matched_count == 0:
        return jsonify({"result": "not found"}), 404

    return jsonify({"result": "success"})


if __name__ == "__main__":
    app.run(debug=True)
