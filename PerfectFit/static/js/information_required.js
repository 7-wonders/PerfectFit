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
});