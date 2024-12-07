import smtplib
import os
from email.mime.text import MIMEText
import random
import redis  # Redis 쓰신다고 하셨던 것이 기억나서, Redis 사용하는 방향으로 한번 작성해보았습니다!
from dotenv import load_dotenv
load_dotenv()

# Redis 클라이언트 초기화

class VerificationService:
    @staticmethod
    def generate_verification_code():
        """6자리 숫자로 구성된 인증 코드를 생성합니다."""
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_verification_code(email: str):
        verification_code = VerificationService.generate_verification_code()
        # 이메일 전송 설정
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        # 이메일 내용 구성
        subject = "PerfectFit에 오신것을 환영합니다."
        body = f"인증 번호 : {verification_code}"
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = smtp_username
        message["To"] = email

        # SMTP 서버에 연결하여 이메일 전송
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, email, message.as_string())

        from config.config_redis import Redis
        redis_instance = Redis()
        redis_key = f"email:{email}:requirements"
        redis_value = verification_code

        redis_instance.save_verify(redis_key, redis_value)
        # 인증 코드를 Redis에 저장하고 유효 기간을 5분(300초)으로 설정
        # redis_client.setex(f"verification_code:{email}", 300, verification_code)

    @staticmethod
    def verify_code(email: str, code: str) -> bool:
        """입력한 인증 코드가 유효한지 검증합니다."""
        # Redis에서 인증 코드 가져오기
        from config.config_redis import Redis
        redis_instance = Redis()
        saved_code = redis_instance.get(f"email:{email}:requirements")

        # 코드가 존재하지 않거나 일치하지 않으면 False 반환
        if saved_code is None:
            return False

        if saved_code == code:
            # 인증 성공 후 Redis에서 해당 인증 코드 삭제
            redis_instance.delete(f"email:{email}:requirements")
            return True
        else:
            return False