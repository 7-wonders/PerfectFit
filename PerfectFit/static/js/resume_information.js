let sectionCount = 0;

// 내용 길어지면 form 세로 크기 증가
function adjustHeight(element) {
    // 초기 높이를 설정 (240px 또는 50px)
    element.style.height = '50px';

    // 새로운 높이를 계산
    const newHeight = element.scrollHeight;

    // 높이를 조정
    element.style.height = `${newHeight}px`;
}

// 섹션 추가하기 버튼
function addSection() {
    sectionCount++; // 섹션 카운트 증가

    // 아래 요소 제거
    const existingButtons = document.querySelectorAll('.add-content-box button');
    existingButtons.forEach(button => button.remove());

    // 항상 아래에 있어야 하는 요소 제거
    const submitBtnBox = document.querySelector('.submit-btn-box');
    if (submitBtnBox) submitBtnBox.remove();

    // 추가할 항목
    const newSection = document.createElement('div');
    newSection.className = "uk-margin";

    newSection.innerHTML = `
        <label class="uk-form-label" for="resume-information-title-${sectionCount}">항목${sectionCount + 1}(선택 사항)</label>
        <div class="uk-form-controls">
            <input class="uk-input" id="resume-information-title-${sectionCount}" type="text" placeholder="제목을 입력해주세요." name="chapter[]">
        </div>
        <div class="add-content-box">
            <button type="button" class="Regular-16-light" onclick="addSection()">+항목 추가하기</button>
        </div>
    `;

    // 섹션을 폼에 추가
    const form = document.getElementById('resume_write_form');
    form.appendChild(newSection);

    // 항상 아래에 있어야 하는 요소 다시 추가
    if (submitBtnBox) form.appendChild(submitBtnBox);
}

// 직군을 선택하면 그에 해당하는 직업만 나오게 하기
function updateJobList() {
    var selectedOccupation = document.getElementById("resume-information-occupation").value;
    var jobSelect = document.getElementById("resume-information-job");

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

// 주요 키워드 뱃지 추가(뱃지 삭제 시 id값 업데이트 기능 추가)
document.addEventListener('DOMContentLoaded', function() {
    const inputElement = document.getElementById('resume-information-keyword');
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
                    badgeText.name = "keywords[]"

                    const badgeButton = document.createElement('button');
                    badgeButton.className = 'badge-button';
                    badgeButton.id = `badge-btn-${badgeCounter}`;
                    badgeButton.textContent = 'X';

                    const badgeInput = document.createElement('input');
                    badgeInput.id = `badge-input-${badgeCounter}`;
                    badgeInput.type = 'hidden';
                    badgeInput.name = 'keywords[]';
                    badgeInput.value = text;

                    badgeButton.addEventListener('click', function() {
                        badgeContainer.removeChild(badge);
                        badgeContainer.removeChild(badgeInput);
                        updateBadgeIDs(); // ID 재정렬 함수 호출
                    });

                    badge.appendChild(badgeText);
                    badge.appendChild(badgeButton);
                    badgeContainer.appendChild(badge);
                    badgeContainer.appendChild(badgeInput);
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
                const badgeInput = badge.querySelector('.badge-input');

                if (badgeText && badgeButton && badgeInput) {
                    badgeText.id = `badge-text-${badgeCounter}`;
                    badgeButton.id = `badge-btn-${badgeCounter}`;
                    badgeInput.id = `badge-input-${badgeCounter}`;
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



// 주요 키워드 포커스 이벤트
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


// 입력 필드가 모두 채워졌는지 검사하는 함수
function checkFormCompletion() {
    const button = document.getElementById("resume-information-submit");
    const inputs = [
        document.getElementById("resume-information-occupation"),
        document.getElementById("resume-information-job"),
        document.getElementById("resume-information-merit"),
        document.getElementById("resume-information-disadvantage")
    ];

    // 모든 입력 필드가 채워졌는지 확인
    let allFilled = inputs.every(input => {
        return input && (input.tagName === "SELECT" ? input.value && input.value !== "직군을 선택해주세요" : input.value.trim() !== "");
    });

    // badge 클래스가 있는 div가 존재하는지 확인
    const hasBadges = document.querySelectorAll("div.badge").length > 0;

    // 경력 선택 여부 확인
    const experience = document.getElementById("resume-information-experience").value;
    let selectExperience;
    if(experience === "신입" || experience === "경력") selectExperience = true


    if (allFilled && hasBadges && selectExperience) {
        button.style.backgroundColor = "#2B7FFF";
        button.style.color = "#fff";
    } else {
        button.style.backgroundColor = ""; // 기본 색상으로 복귀
        button.style.color = ""; // 기본 색상으로 복귀
    }
}

// submit 버튼 클릭 시 동작
function submitInformation() {
    const experience = document.getElementById("resume-information-experience").value;
    let selectExperience;
    const inputs = [
        {
            element: document.getElementById("resume-information-occupation"),
            name: "직군"
        },
        {
            element: document.getElementById("resume-information-job"),
            name: "직업"
        },
        {
            element: document.getElementById("resume-information-merit"),
            name: "장점"
        },
        {
            element: document.getElementById("resume-information-disadvantage"),
            name: "단점"
        }
    ];

    // badge 클래스가 있는 div가 존재하는지 확인
    const hasBadges = document.querySelectorAll("div.badge").length > 0;

    // 입력 필드 확인
    for (const input of inputs) {
        const value = input.element.tagName === "SELECT" ? input.element.value : input.element.value.trim();
        if (!value || (input.element.tagName === "SELECT" && value === "직군을 선택해주세요")) {
            alert(`${input.name}을(를) 채워주세요.`);
            input.element.focus(); // 해당 입력 필드로 포커스 이동
            event.preventDefault();
            return; // 함수 종료
        }
    }
    // 경력 선택 여부 확인 후 경고
    if(experience === "신입" || experience === "경력") selectExperience = true
    if(!selectExperience) {
        alert("경력을 선택해주세요.");
        event.preventDefault();
        return;
    }
    // Badge가 없는 경우 경고
    if (!hasBadges) {
        alert("키워드를 추가해주세요.");
        event.preventDefault();
        return; // 함수 종료
    }

    // 모든 조건이 충족되면 폼 제출 (추가적인 동작이 필요하면 여기에 작성)
    alert("자기소개서를 작성하기 위한 제출되었습니다.");
}

// 모든 필드에 이벤트 리스너 추가
function setupEventListeners() {
    const inputs = [
        document.getElementById("resume-information-occupation"),
        document.getElementById("resume-information-job"),
        document.getElementById("resume-information-experience"),
        document.getElementById("resume-information-merit"),
        document.getElementById("resume-information-disadvantage")
    ];

    inputs.forEach(input => {
        // select 요소는 change 이벤트, input과 textarea는 input 이벤트 리스너를 추가
        if (input.tagName === "SELECT") {
            input.addEventListener("change", checkFormCompletion);
        } else {
            input.addEventListener("input", checkFormCompletion);
        }
    });

    // badge div에 대한 변경을 감지하기 위해 MutationObserver를 사용
    const badgeContainer = document.querySelector('.badge-container');
    const observer = new MutationObserver(checkFormCompletion);
    observer.observe(badgeContainer, { childList: true, subtree: true });

    // 버튼 클릭 이벤트 리스너 추가
    handleButtonClick();
}

// 페이지 로드 시 초기 버튼 상태 설정 및 이벤트 리스너 추가
window.onload = () => {
    checkFormCompletion();
    setupEventListeners();
};












