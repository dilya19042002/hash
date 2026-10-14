from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS 설정: 모든 도메인에서의 요청을 허용 (실무에서는 특정 도메인만 지정 권장)
CORS(app, resources={r"/*": {"origins": "*"}})

# 해시 테이블 클래스 정의 (체이닝 방식 충돌 해결)
class HashTable:
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.table = [[] for _ in range(capacity)]

    # 2. 해시 값 계산 함수 (키의 내장 해시값을 버킷 크기로 나머지 연산)
    def hash_value(self, key):
        return hash(str(key)) % self.capacity

    # 4. 데이터 추가 함수 (O(1) 평균 시간 복잡도)
    def add(self, key, value):
        idx = self.hash_value(key)
        # 이미 존재하는 키라면 값 업데이트
        for item in self.table[idx]:
            if item[0] == key:
                item[1] = value
                return f"키 '{key}'의 값이 '{value}'(으)로 갱신되었습니다. (버킷: {idx})"
        # 존재하지 않으면 새 항목 추가
        self.table[idx].append([key, value])
        return f"키 '{key}', 값 '{value}'가 버킷 {idx}에 추가되었습니다."

    # 3. 해시 검색 함수 (O(1) 평균, 최악의 경우 O(N))
    def search(self, key):
        idx = self.hash_value(key)
        for item in self.table[idx]:
            if item[0] == key:
                return {"found": True, "bucket": idx, "value": item[1], "message": f"탐색 성공! 버킷 {idx}에서 키 '{key}'를 찾았습니다."}
        return {"found": False, "bucket": idx, "value": None, "message": f"탐색 실패: 키 '{key}'를 찾을 수 없습니다."}

    # 5. 데이터 삭제 함수
    def remove(self, key):
        idx = self.hash_value(key)
        for i, item in enumerate(self.table[idx]):
            if item[0] == key:
                del self.table[idx][i]
                return f"버킷 {idx}에서 키 '{key}'가 삭제되었습니다."
        return f"삭제 실패: 키 '{key}'가 존재하지 않습니다."

    # 6. 전체 구조 덤프 함수
    def dump(self):
        return {
            "capacity": self.capacity,
            "buckets": self.table
        }

# 전역 해시 테이블 인스턴스 생성
ht = HashTable(capacity=5)

@app.route('/init', methods=['POST'])
def api_init():
    """1. 초기화 API"""
    global ht
    data = request.get_json() or {}
    capacity = int(data.get('capacity', 5))
    ht = HashTable(capacity=capacity)
    return jsonify({"status": "success", "message": f"해시 테이블이 용량 {capacity}로 초기화되었습니다.", "dump": ht.dump()})

@app.route('/hash_value', methods=['POST'])
def api_hash_value():
    """2. 해시 값 계산 API"""
    data = request.get_json() or {}
    key = data.get('key')
    if key is None:
        return jsonify({"status": "error", "message": "키 값이 없습니다."}), 400
    idx = ht.hash_value(key)
    return jsonify({"status": "success", "key": key, "bucket": idx})

@app.route('/search', methods=['POST'])
def api_search():
    """3. 검색 API"""
    data = request.get_json() or {}
    key = data.get('key')
    result = ht.search(key)
    return jsonify({"status": "success", "result": result, "dump": ht.dump()})

@app.route('/add', methods=['POST'])
def api_add():
    """4. 추가 API"""
    data = request.get_json() or {}
    key = data.get('key')
    value = data.get('value')
    if key is None or value is None:
        return jsonify({"status": "error", "message": "키와 값을 모두 입력하세요."}), 400
    msg = ht.add(key, value)
    return jsonify({"status": "success", "message": msg, "dump": ht.dump()})

@app.route('/remove', methods=['POST'])
def api_remove():
    """5. 삭제 API"""
    data = request.get_json() or {}
    key = data.get('key')
    msg = ht.remove(key)
    return jsonify({"status": "success", "message": msg, "dump": ht.dump()})

@app.route('/dump', methods=['GET'])
def api_dump():
    """6. 덤프 API"""
    return jsonify({"status": "success", "dump": ht.dump()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
