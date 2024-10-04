from database.config import db
 ## DB에서 테이블 생성시 도메인폴더 안 py파일에서 작업 해 줘야함. 이건 우편봉투임

class User(db.Model):
    __tablename__ = 'user'  # 테이블 이름
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self): ## 이걸 해줘야 유저이름이 찍힘.
        return f'<User {self.name}>'
