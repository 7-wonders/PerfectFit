document.addEventListener('DOMContentLoaded', function() {
    const nextButton = document.getElementById('nextButton');
    const formInputs = document.querySelectorAll('#informationForm input');

    // 입력 필드에서 변화가 있을 때마다 실행되는 함수
    function checkInputs() {
        let allFilled = true;

        // 각 입력 필드에서 값이 비어있는지 확인
        formInputs.forEach(input => {
            if (input.value.trim() === '') {
                allFilled = false;
            }
        });

        // 모든 입력이 채워지면 "다음" 버튼 활성화
        if (allFilled) {
            nextButton.disabled = false;
        } else {
            nextButton.disabled = true;
        }
    }

    // 각 입력 필드에 이벤트 리스너 추가 (입력값 변화 시마다 checkInputs 함수 실행)
    formInputs.forEach(input => {
        input.addEventListener('input', checkInputs);
    });

    // 이메일 인증 버튼
    const emailButton = document.getElementById('emailButton');

    // 이메일 인증 버튼 클릭 시 처리
    // emailButton.addEventListener('click', async function(event) {
    //     const emailInput = document.getElementById('email');
    //     const emailDomainSelect = document.getElementById('emailDomain');
    //
    //     const email = emailInput.value + emailDomainSelect.value;
    //     const verifyCode = generateVerificationCode();
    //
    //     // 이메일과 인증 코드를 서버로 전송하는 함수 호출
    //     await send_verification_code(email, verifyCode);
    // });
});

// function generateVerificationCode() {
//     return Math.floor(1000 + Math.random() * 9000); // 1000에서 9999 사이의 숫자
// }

async function send_verification_code() {
    const emailTmp = document.getElementById(`email`).value;
    const emailDomain = document.getElementById(`emailDomain`).value;
    const email = emailTmp + emailDomain;

    try {
        const response = await instance.post('/user/verify/send', JSON.stringify({
            email: email
        }));
        // 응답 성공 시 알림
        if(response.status === 204) {
            alert('이메일 인증 코드를 발송했습니다.');
        }
    } catch (error) {
        console.error('Error sending verification code:', error);
        alert('이메일 전송 중 오류가 발생했습니다.');
    }
}

async function compare_verification_code(email) {
    const verifyCode = document.getElementById(`verificationCode`).value;

    try {
        const response = await instance.post('/user/verify/compare', JSON.stringify({
            email: email,
            verifyCode: verifyCode
        }));
        // 응답 성공 시 알림
        if(response.status === 204) {
            alert('이메일 인증 성공하였습니다');
        }
    } catch (error) {
        console.error('Error sending verification code:', error);
        alert('이메일 인증 코드 확인 실패');
    }
}

function backButton() {
    history.back();
}

