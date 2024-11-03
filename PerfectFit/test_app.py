import json
from flask import Flask
from app import user_bp  # 앱이 실행되는 파일 이름을 사용해야 합니다.

app = Flask(__name__)
app.register_blueprint(user_bp)

def test_get_users():
    with app.test_client() as client:
        response = client.get('/users')
        assert response.status_code == 200
        data = json.loads(response.data)
        print("Get Users Test:", data)

def test_get_user():
    with app.test_client() as client:
        response = client.get('/user/1')  # ID가 1인 사용자로 테스트
        assert response.status_code == 200
        data = json.loads(response.data)
        print("Get User Test:", data)

def test_get_info():
    with app.test_client() as client:
        response = client.get('/user/mypage/info')
        assert response.status_code == 200
        data = json.loads(response.data)
        print("Get Info Test:", data)

if __name__ == "__main__":
    test_get_users()
    test_get_user()
    test_get_info()
