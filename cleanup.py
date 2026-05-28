from app import create_app, db
import os

app = create_app()

with app.app_context():
    print("기존 데이터베이스 정보를 삭제합니다...")
    db.drop_all()
    db.create_all()
    print("데이터베이스 초기화 완료. 이제 새로운 계정을 생성할 수 있습니다.")
