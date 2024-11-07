
// 내용 길어지면 form 세로 크기 증가
function adjustHeight(element) {
    // 초기 높이를 설정 (240px 또는 50px)
    if (element.classList.contains('resume-content')) {
        element.style.height = '240px';
    } else {
        element.style.height = '50px';
    }

    // 새로운 높이를 계산
    const newHeight = element.scrollHeight;

    // 높이를 조정
    element.style.height = `${newHeight}px`;
}

// 섹션 추가하기 버튼
function addSection() {
    sectionCount++; // 섹션 카운트 증가

    // 아래 요소 제거
    const existingButtons = document.querySelectorAll('.add-section-btn');
    existingButtons.forEach(button => button.remove());

    // 항상 아래에 있어야 하는 요소 제거
    const publicCheckbox = document.querySelector('.public-check-box');
    const resumeSubmitBox = document.querySelector('.resume-submit-box');

    if (publicCheckbox) publicCheckbox.remove();
    if (resumeSubmitBox) resumeSubmitBox.remove();

    // 추가할 항목
    const newSection = document.createElement('div');
    newSection.className = "resume-container";
    newSection.id = `resume-write-container${sectionCount}`;

    newSection.innerHTML = `
        <div class="resume-write-header">
            <label class="uk-form-label" for="resume-write-title-${sectionCount}">항목${sectionCount + 1}</label>
            <button type="button" class="Regular-16-light custom-button" id="ai-resume-write-${sectionCount}" onclick="aiResumeWrite(${sectionCount})"><img src="${iconAiPath}"/>AI 작성하기</button>
        </div>
        <div class="uk-form-controls">
            <input class="uk-input" id="resume-write-title-${sectionCount}" type="text" placeholder="제목을 입력해주세요." name="sections[][title]">
        </div>
        <div class="uk-margin">
            <div class="uk-form-controls">
                <textarea class="uk-textarea resume-content" id="resume-write-content-${sectionCount}" placeholder="내용을 입력해주세요." name="sections[][content]" style="resize: none; overflow-y: hidden;" oninput="adjustHeight(this)" name="content_${sectionCount}"></textarea>
            </div>
        </div>
        <div class="right-box">
            <button type="button" class="Regular-16-light custom-button add-section-btn" onclick="addSection()">+섹션 추가하기</button>
        </div>
    `;

    // 섹션을 폼에 추가
    const form = document.getElementById('resume_write_form');
    form.appendChild(newSection);

    // 항상 아래에 있어야 하는 요소 다시 추가
    if (publicCheckbox) form.appendChild(publicCheckbox);
    if (resumeSubmitBox) form.appendChild(resumeSubmitBox);
}

// 직군을 선택하면 그에 해당하는 직업만 나오게 하기
function updateJobList() {
    var selectedOccupation = document.getElementById("resume-write-occupation").value;
    var jobSelect = document.getElementById("resume-write-job");

    // 직업 목록 초기화
    jobSelect.innerHTML = '';

    if (selectedOccupation in jobList) {
        jobList[selectedOccupation].forEach(function(job) {
            var option = document.createElement("option");
            option.text = job;
            jobSelect.add(option);
        });
    }
}

// ai 작성하기 애니메이션
function aiResumeWrite(idNumber) {
    const text = "안녕하세요 반갑습니다 안녕하세요 반갑습니다 안녕하세요 반갑습니다";
    const titleInput = document.getElementById(`resume-write-title-${idNumber}`);
    const textarea = document.getElementById(`resume-write-content-${idNumber}`);
    const button = document.getElementById(`ai-resume-write-${idNumber}`);

    // 제목 입력란이 비어 있는지 확인
    if (!titleInput.value.trim()) {
        alert("제목을 입력해주세요");
        return; // 제목이 없으면 함수 실행 중단
    }

    if (textarea && button) {
        let index = 0;

        // 버튼 비활성화
        button.disabled = true;
        textarea.value = ''; // 기존 내용을 지웁니다.

        function typeWriter() {
            if (index < text.length) {
                textarea.value += text.charAt(index);
                index++;
                setTimeout(typeWriter, 100); // 타이핑 속도를 조절합니다 (100ms 간격)
            } else {
                // 타이핑 완료 후 버튼 활성화
                button.disabled = false;
            }
        }

        typeWriter();
    }
}

// 주요 키워드 뱃지 추가(뱃지 삭제 시 id값 업데이트 기능 추가)
document.addEventListener('DOMContentLoaded', function() {
    const inputElement = document.getElementById('resume-write-keyword');
    const badgeContainer = document.querySelector('.badge-container');
    let badgeCounter = 1; // 배지 ID를 위한 카운터 초기화

    if (inputElement && badgeContainer) {
        function adjustInputWidth() {
            const tempSpan = document.createElement('span');
            tempSpan.style.visibility = 'hidden';
            tempSpan.style.whiteSpace = 'pre';
            tempSpan.style.fontSize = window.getComputedStyle(inputElement).fontSize;
            tempSpan.textContent = inputElement.value || inputElement.placeholder;
            document.body.appendChild(tempSpan);
            const width = tempSpan.offsetWidth + 10;
            document.body.removeChild(tempSpan);

            inputElement.style.width = `${width}px`;
        }

        adjustInputWidth();

        inputElement.addEventListener('input', adjustInputWidth);

        inputElement.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                const text = inputElement.value.trim();

                if (text) {
                    badgeContainer.removeChild(inputElement);

                    const badge = document.createElement('div');
                    badge.className = 'badge';

                    const badgeText = document.createElement('span');
                    badgeText.className = 'badge-text';
                    badgeText.id = `badge-text-${badgeCounter}`;
                    badgeText.textContent = text;
                    badgeText.name = "keywords[]";

                    const badgeButton = document.createElement('button');
                    badgeButton.className = 'badge-button';
                    badgeButton.id = `badge-btn-${badgeCounter}`;
                    badgeButton.textContent = 'X';

                    badgeButton.addEventListener('click', function() {
                        badgeContainer.removeChild(badge);
                        updateBadgeIDs(); // ID 재정렬 함수 호출
                    });

                    badge.appendChild(badgeText);
                    badge.appendChild(badgeButton);
                    badgeContainer.appendChild(badge);

                    badgeContainer.appendChild(inputElement);

                    badgeCounter++;
                    inputElement.value = '';
                    adjustInputWidth();
                    inputElement.focus();
                }
            }
        });

        // 삭제 후 ID 재정렬 및 최신 badgeCounter 업데이트 함수
        function updateBadgeIDs() {
            const badges = badgeContainer.querySelectorAll('.badge');
            badgeCounter = 1;

            badges.forEach(badge => {
                const badgeText = badge.querySelector('.badge-text');
                const badgeButton = badge.querySelector('.badge-button');

                if (badgeText && badgeButton) {
                    badgeText.id = `badge-text-${badgeCounter}`;
                    badgeButton.id = `badge-btn-${badgeCounter}`;
                    badgeCounter++;
                }
            });

            // badgeCounter가 마지막 배지 ID + 1로 설정되도록 조정
            badgeCounter = badges.length + 1;
        }
    } else {
        console.error('Element with ID "resume-write-keyword" or "badge-container" not found.');
    }
});




document.addEventListener('DOMContentLoaded', function() {
    const inputElement = document.querySelector('.keyword-input');
    const inputBox = document.querySelector('.keyword-input-box');

    if (inputElement && inputBox) {
        inputElement.addEventListener('focus', function() {
            inputBox.style.borderColor = '#39f'; // 포커스 시 테두리 색상 변경
            inputBox.style.color = '#fff'; // 포커스 시 텍스트 색상 변경
            inputBox.style.textShadow = 'none'; // 포커스 시 텍스트 그림자 제거
            inputElement.placeholder ='';
        });

        inputElement.addEventListener('blur', function() {
            // 포커스를 잃었을 때 원래 스타일로 되돌리기
            inputBox.style.borderColor = ''; // 기본값으로 되돌리기
            inputBox.style.color = ''; // 기본값으로 되돌리기
            inputBox.style.textShadow = ''; // 기본값으로 되돌리기
        });
    } else {
        console.error('Element with class "keyword-input" or "keyword-input-box" not found.');
    }
});
