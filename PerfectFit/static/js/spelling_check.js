function spell_check(){
    const inputText = document.getElementById('input-text').value;
    const outputText = document.getElementById('output-text');

    fetch('/interview/spellcheck', {
        method: 'POST' ,
        headers: {'Content-Type' : 'application/json',},
        body: JSON.stringify({ content: inputText}),
    }).then(response=> {
        if(!response.ok){
            throw new Error('Server Error ! ');
        }
        return response.json();
    }).then(data =>{
        outputText.value = data;
    }).catch(error => {
       console.error('API 에러'+ error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text'); // textarea 요소
    const charCount = document.getElementById('char-count'); // 글자 수 표시 요소
    const maxLength = 1000; // 최대 글자 수

    // 'input' 이벤트 리스너를 추가하여 실시간으로 글자 수를 갱신
    inputText.addEventListener('input', function() {
        // 현재 글자 수를 가져와서 업데이트
        const currentLength = inputText.value.length;
        charCount.textContent = currentLength; // 글자 수 표시

        // 최대 글자 수에 도달하면 글자 수를 빨간색으로 표시하는 예시
        if (currentLength >= maxLength) {
            charCount.style.color = 'red';  // 최대 글자 수에 도달하면 빨간색으로 표시

        } else {
            charCount.style.color = '';  // 기본 색상으로 돌아감
        }
    });
});

function copy() {
    // output-text textarea 요소 가져오기
    var outputText = document.getElementById('output-text');

    // textarea 선택
    outputText.select();
    outputText.setSelectionRange(0, 99999); // 모바일 브라우저를 위한 추가 코드

    try {
        // 클립보드에 복사
        var successful = document.execCommand('copy');
        if (successful) {
            // 복사 성공 시 알림
            alert('교정된 텍스트가 클립보드에 복사되었습니다!');
        } else {
            // 복사 실패 시 알림
            alert('복사에 실패했습니다. 다시 시도해주세요.');
        }
    } catch (err) {
        console.error('복사 중 오류가 발생했습니다:', err);
    }
}

document.getElementById('copy-logo').addEventListener('click', function() {
    // output-text textarea 요소 가져오기
    var outputText = document.getElementById('output-text');

    // textarea 선택
    outputText.select();
    outputText.setSelectionRange(0, 99999); // 모바일 브라우저를 위한 추가 코드

    try {
        // 클립보드에 복사
        var successful = document.execCommand('copy');
        if (successful) {
            // 복사 성공 시 알림
            alert('교정된 텍스트가 클립보드에 복사되었습니다!');
        } else {
            // 복사 실패 시 알림
            alert('복사에 실패했습니다. 다시 시도해주세요.');
        }
    } catch (err) {
        console.error('복사 중 오류가 발생했습니다:', err);
    }
});