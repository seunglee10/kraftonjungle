from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId


# ============================================
# 설정
# ============================================
app = Flask(__name__)

client = MongoClient("mongodb://jungle:junglememo@localhost:27017/admin")
db = client.dbjungle
memos = db.memos


# ============================================
# 메시지 상수
# ============================================
class Msg:
    # 에러
    INVALID_ID = "유효하지 않은 ID입니다"
    NOT_FOUND = "메모를 찾을 수 없습니다"
    EMPTY_TITLE = "제목을 입력해주세요"
    EMPTY_CONTENT = "내용을 입력해주세요"
    # 성공
    CREATED = "저장되었습니다"
    UPDATED = "수정되었습니다"
    DELETED = "삭제되었습니다"


# ============================================
# 커스텀 예외
# ============================================
class ApiError(Exception):
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code


# ============================================
# 에러 핸들러
# ============================================
@app.errorhandler(ApiError)
def handle_api_error(e):
    return jsonify({"result": "error", "message": e.message}), e.status_code


@app.errorhandler(Exception)
def handle_exception(_):
    return jsonify({"result": "error", "message": "서버 오류가 발생했습니다"}), 500


# ============================================
# 헬퍼 함수
# ============================================
def parse_object_id(id_str):
    """문자열을 ObjectId로 변환"""
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        raise ApiError(Msg.INVALID_ID, 400)


def get_form_data(*fields):
    """폼 데이터를 가져오고 유효성 검증"""
    data = {}
    for field in fields:
        value = request.form.get(field, "").strip()
        if not value:
            if field == "title":
                raise ApiError(Msg.EMPTY_TITLE, 400)
            elif field == "content":
                raise ApiError(Msg.EMPTY_CONTENT, 400)
        data[field] = value
    return data


def success(message=None, status_code=200):
    """성공 응답"""
    return jsonify({"result": "success", "message": message}), status_code


def check_update_result(result):
    """업데이트 결과 검증"""
    if result.matched_count == 0:
        raise ApiError(Msg.NOT_FOUND, 404)


# ============================================
# 라우트
# ============================================
@app.route("/")
def home():
    """메인 페이지 (좋아요 내림차순)"""
    memo_list = list(memos.find().sort("likes", -1))
    for memo in memo_list:
        memo["_id"] = str(memo["_id"])
    return render_template("index.html", memos=memo_list)


@app.route("/memo", methods=["POST"])
def save_memo():
    """메모 저장"""
    data = get_form_data("title", "content")
    memos.insert_one({
        "title": data["title"],
        "content": data["content"],
        "likes": 0
    })
    return success(Msg.CREATED, 201)


@app.route("/update/<memo_id>", methods=["PATCH"])
def update_memo(memo_id):
    """메모 수정"""
    _id = parse_object_id(memo_id)
    data = get_form_data("title", "content")

    result = memos.update_one(
        {"_id": _id},
        {"$set": {"title": data["title"], "content": data["content"]}}
    )
    check_update_result(result)
    return success(Msg.UPDATED)


@app.route("/delete/<memo_id>", methods=["DELETE"])
def delete_memo(memo_id):
    """메모 삭제"""
    _id = parse_object_id(memo_id)

    result = memos.delete_one({"_id": _id})
    if result.deleted_count == 0:
        raise ApiError(Msg.NOT_FOUND, 404)

    return success(Msg.DELETED)


@app.route("/like/<memo_id>", methods=["POST"])
def like_memo(memo_id):
    """좋아요 증가"""
    _id = parse_object_id(memo_id)

    result = memos.update_one({"_id": _id}, {"$inc": {"likes": 1}})
    check_update_result(result)
    return success()


# ============================================
# 실행
# ============================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)