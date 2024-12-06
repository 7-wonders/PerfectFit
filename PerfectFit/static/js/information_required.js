let emailSuccess = false;

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
        if (allFilled && emailSuccess) {
            nextButton.disabled = false;
        } else {
            nextButton.disabled = true;
        }
    }

    // 각 입력 필드에 이벤트 리스너 추가 (입력값 변화 시마다 checkInputs 함수 실행)
    formInputs.forEach(input => {
        input.addEventListener('input', checkInputs);
    });
});

async function send_verification_code() {
    const emailTmp = document.getElementById(`email`).value;
    const emailDomain = document.getElementById(`emailDomain`).value;
    const email = emailTmp + emailDomain;
    console.log(email);

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

function disabledDomain() {
    console.log("disabled 실행");
    const emailInput = document.getElementById('email');
    const emailDomainSelect = document.getElementById('emailDomain');

    // 이메일 입력 필드의 값이 변경될 때 이벤트 처리
    emailInput.addEventListener('input', () => {
        if (emailInput.value.includes('@')) {
            emailDomainSelect.disabled = true; // 비활성화
            emailDomainSelect.value = "";
            document.getElementById(`none-domain`).textContent = "- - -"
        } else {
            emailDomainSelect.disabled = false; // 활성화
            document.getElementById(`none-domain`).textContent = "이메일 주소 선택"
        }
    });
}

async function compare_verification_code() {
    const verifyCode = document.getElementById(`verificationCode`).value;
    const emailTmp = document.getElementById(`email`).value;
    const emailDomain = document.getElementById(`emailDomain`).value;
    const email = emailTmp + emailDomain;
    try {
        const response = await instance.post('/user/verify/compare', JSON.stringify({
            email: email,
            verifyCode: verifyCode
        }));
        // 응답 성공 시 알림
        if(response.status === 204) {
            alert('이메일 인증 성공하였습니다');
            emailSuccess = true;
        }
    } catch (error) {
        console.error('Error sending verification code:', error);
        alert('이메일 인증 코드 확인 실패');
    }
}

function backButton() {
    history.back();
}

