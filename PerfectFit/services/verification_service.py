import smtplib
from email.mime.text import MIMEText
import random
import redis  # Redis 쓰신다고 하셨던 것이 기억나서, Redis 사용하는 방향으로 한번 작성해보았습니다!

# Redis 클라이언트 초기화
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

class VerificationService:
    @staticmethod
    def generate_verification_code():
        """6자리 숫자로 구성된 인증 코드를 생성합니다."""
        return str(random.randint(100000, 999999))

    @staticmethod
    def send_verification_code(email: str):
        verification_code = VerificationService.generate_verification_code()

        # 이메일 전송 설정
        smtp_server = "smtp.example.com"  # 실제 SMTP 서버 주소로 변경
        smtp_port = 587
        smtp_username = "your_email@example.com"  # 실제 이메일로 변경
        smtp_password = "your_password"  # 실제 비밀번호로 변경

        # 이메일 내용 구성
        subject = "Your Verification Code"
        body = f"Your verification code is: {verification_code}"
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = smtp_username
        message["To"] = email

        # SMTP 서버에 연결하여 이메일 전송
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, email, message.as_string())

        # 인증 코드를 Redis에 저장하고 유효 기간을 5분(300초)으로 설정
        redis_client.setex(f"verification_code:{email}", 300, verification_code)

    @staticmethod
    def verify_code(email: str, code: str) -> bool:
        """입력한 인증 코드가 유효한지 검증합니다."""
        # Redis에서 인증 코드 가져오기
        saved_code = redis_client.get(f"verification_code:{email}")

        # 코드가 존재하지 않거나 일치하지 않으면 False 반환
        if saved_code is None:
            return False

        if saved_code == code:
            # 인증 성공 후 Redis에서 해당 인증 코드 삭제
            redis_client.delete(f"verification_code:{email}")
            return True
        else:
            return False