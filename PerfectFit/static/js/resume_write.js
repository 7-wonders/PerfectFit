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

    // 기존의 "섹션 추가하기" 버튼을 제거
    const existingButtons = document.querySelectorAll('.right-box');
    existingButtons.forEach(box => box.remove());

    // 항상 아래에 있어야 하는 요소 제거
    const publicCheckbox = document.querySelector('.public-check-box');
    const resumeSubmitBox = document.querySelector('.resume-submit-box');

    if (publicCheckbox) publicCheckbox.remove();
    if (resumeSubmitBox) resumeSubmitBox.remove();

    // 새로운 섹션 추가
    const newSection = document.createElement('div');
    newSection.className = "resume-container";
    newSection.id = `resume-write-container${sectionCount}`;

    newSection.innerHTML = `
        <div class="resume-write-header">
            <label class="uk-form-label" for="resume-write-title-${sectionCount}">항목${sectionCount + 1}</label>
            <div class = "resume-write-header-right">
                <button type="button" uk-tooltip="AI 작성하기" class="Regular-16-light custom-button" id="ai-resume-write-${sectionCount}" onclick="aiResumeWrite(${sectionCount})"><img src="${iconAiPath}"/></button>
                <button type="button" uk-tooltip="삭제" class="Regular-16-light custom-button delete-section-btn" onclick="deleteSection(${sectionCount})"><img src="${iconRemovePath}"/></button>
            </div>
        </div>
        <div class="uk-form-controls">
            <input class="uk-input" id="resume-write-title-${sectionCount}" type="text" placeholder="제목을 입력해주세요." name="sections[][title]">
        </div>
        <div class="uk-margin">
            <div class="uk-form-controls">
                <textarea class="uk-textarea resume-content" id="resume-write-content-${sectionCount}" placeholder="내용을 입력해주세요." name="sections[][content]" style="resize: none; overflow-y: hidden;" oninput="adjustHeight(this)"></textarea>
            </div>
        </div>
        <div class="right-box">
            <button type="button" class="Regular-16-light custom-button add-section-btn" onclick="addSection()">+섹션 추가하기</button>
        </div>
    `;

    // 폼에 섹션 추가
    const form = document.getElementById('resume_write_form');
    form.appendChild(newSection);

    // 항상 아래에 있어야 하는 요소 다시 추가
    if (publicCheckbox) form.appendChild(publicCheckbox);
    if (resumeSubmitBox) form.appendChild(resumeSubmitBox);

    // 입력 필드 체크 업데이트
    checkFormCompletion();
}

// 섹션 삭제하기 버튼
function deleteSection(sectionId) {
    // 삭제할 섹션을 선택하고 삭제
    const sectionToDelete = document.getElementById(`resume-write-container${sectionId}`);
    if (sectionToDelete) sectionToDelete.remove();

    // 섹션 번호와 ID, 라벨 업데이트
    sectionCount--;
    const sections = document.querySelectorAll('.resume-container');
    sections.forEach((section, index) => {
        section.id = `resume-write-container${index}`;

        // 라벨 업데이트
        const label = section.querySelector('.uk-form-label');
        label.setAttribute('for', `resume-write-title-${index}`);
        label.textContent = `항목${index + 1}`;

        // 제목 입력 필드 업데이트
        const titleInput = section.querySelector('.uk-input');
        titleInput.id = `resume-write-title-${index}`;

        // 내용 입력 필드 업데이트
        const contentTextarea = section.querySelector('.resume-content');
        contentTextarea.id = `resume-write-content-${index}`;

        // AI 작성하기 버튼 업데이트
        const aiButton = section.querySelector('.custom-button');
        aiButton.id = `ai-resume-write-${index}`;
        aiButton.setAttribute('onclick', `aiResumeWrite(${index})`);

        // 삭제 버튼 업데이트
        const deleteButton = section.querySelector('.delete-section-btn');
        if (deleteButton) {
            deleteButton.id = `delete-section-${index}`;
            deleteButton.setAttribute('onclick', `deleteSection(${index})`);
        }
    });

    // 모든 기존 .right-box 요소 제거
    document.querySelectorAll('.right-box').forEach(box => box.remove());

    // 마지막 섹션에 새로운 .right-box와 "섹션 추가하기" 버튼 추가
    if (sections.length > 0) {
        const lastSection = sections[sections.length - 1];

        const newRightBox = document.createElement('div');
        newRightBox.className = "right-box";

        const addButton = document.createElement('button');
        addButton.type = "button";
        addButton.className = "Regular-16-light custom-button add-section-btn";
        addButton.onclick = addSection;
        addButton.textContent = "+섹션 추가하기";

        newRightBox.appendChild(addButton);
        lastSection.appendChild(newRightBox);
    }

    // 입력 필드 체크 업데이트
    checkFormCompletion();
}

// 페이지가 실행 된 후 직업 목록을 한번 호출
document.addEventListener("DOMContentLoaded", function() {
    // 직군 선택값 가져오기
    const selectedOccupation = document.getElementById("resume-write-occupation").value;

    // 직군이 이미 선택된 상태라면, 직업 목록을 한번 호출
    if (selectedOccupation) {
        updateJobList();
    }
});

//주요 키워드 뱃지 관련 코드
document.addEventListener('DOMContentLoaded', function() {
    const inputElement = document.getElementById('resume-write-keyword');
    const badgeContainer = document.querySelector('.badge-container');

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

        // 템플릿으로 생성된 초기 배지에 삭제 기능 추가
        function initializeExistingBadges() {
            const existingBadges = badgeContainer.querySelectorAll('.badge');
            existingBadges.forEach((badge, index) => {
                const badgeButton = badge.querySelector('.badge-button');
                if (badgeButton) {
                    badgeButton.addEventListener('click', function() {
                        badgeContainer.removeChild(badge);
                        updateBadgeIDs();
                    });
                }
            });
        }

        initializeExistingBadges();

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
                        updateBadgeIDs();
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
            badgeCounter = 0;

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

            badgeCounter = badges.length;
        }
    } else {
        console.error('Element with ID "resume-write-keyword" or "badge-container" not found.');
    }
});

// 주요 키워드 div 포커스 이벤트 추가
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
    const button = document.getElementById("resume-write-submit");
    const inputs = [
        document.getElementById("resume-write-main-title"),
        document.getElementById("resume-write-occupation"),
        document.getElementById("resume-write-job"),
        document.getElementById("resume-write-experience"),
        document.getElementById("resume-write-merit"),
        document.getElementById("resume-write-disadvantage")
    ];

    // 섹션 추가하기로 인해 늘어날 자기소개서 제목 및 내용 처리
    const contentInputs = document.querySelectorAll('[id^="resume-write-content-"]');
    const titleInputs = document.querySelectorAll('[id^="resume-write-title-"]');

    // 배열에 자기소개서 내용 및 제목 추가
    inputs.push(...contentInputs, ...titleInputs);

    // 모든 입력 필드가 채워졌는지 확인
    let allFilled = Array.from(inputs).every(input => {
        return input && (input.tagName === "SELECT" ? input.value : input.value.trim() !== "");
    });

    // 경력 선택 여부 확인
    const experience = document.getElementById("resume-write-experience").value;
    let selectExperience;
    if(experience === "신입" || experience === "경력") selectExperience = true

    // badge 클래스가 있는 div가 존재하는지 확인
    const hasBadges = document.querySelectorAll("div.badge").length > 0;

    // 입력 필드에 따른 버튼 스타일 변경
    if (allFilled && hasBadges && selectExperience) {
        button.style.color = "#175FE6";
        button.style.border = "1px solid #175FE6";
    } else {
        button.style.color = ""; // 기본 색상으로 복귀
        button.style.border = "1px solid rgba(0,0,0, 0.50)";
    }
}

// 입력 필드에 이벤트 리스너 추가 (입력 필드에 따른 저장 버튼 style 변경을 위해 필요)
function setupEventListeners() {
    const form = document.getElementById('resume_write_form');

    // form 내에서 input과 textarea에 대한 이벤트 리스너를 동적으로 추가
    form.addEventListener('input', function(event) {
       if (event.target && (event.target.id.startsWith("resume-write-content-") || event.target.id.startsWith("resume-write-title-")
           || event.target.id === "resume-write-main-title" ||  event.target.id === "resume-write-merit" ||  event.target.id === "resume-write-disadvantage")) {
            checkFormCompletion();
        }
    });

    // select 요소에 대한 이벤트 리스너
    const selectElements = document.querySelectorAll('select');
    selectElements.forEach(select => {
        select.addEventListener("change", checkFormCompletion);
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


// 필요한 섹션 수에 맞춰 섹션 추가(임시 저장 목록 불러오기에 필요한 함수)
function addSectionIfNeeded(requiredCount) {
    while (sectionCount < requiredCount) {
        addSection();
    }
}

// 임시 저장 목록 불러오기
function loadResumeData(resumeId) {
    const sampleData = {
        title: "수정된 제목 예시",
        occupation: "직군5",
        job: "직업5-2",
        experience: "경력",
        merit: "수정된 장점 예시",
        disadvantage: "수정된 단점 예시",
        directionality: "수정된 방향성 예시",
        sections: [
            { title: "수정된 섹션 제목 1", content: "수정된 섹션 내용 1" },
            { title: "수정된 섹션 제목 2", content: "수정된 섹션 내용 2" },
            { title: "수정된 섹션 제목 3", content: "수정된 섹션 내용 3" }
        ],
        keywords: ["성실", "착함", "리더쉽", "팀워크"]
    };

    badgeCounter = sampleData.keywords.length;

    // 기존 배지 삭제
    const badgeContainer = document.querySelector('.badge-container');
    badgeContainer.innerHTML = ''; // 기존 배지들을 모두 삭제

    // 기존 필드 업데이트
    document.getElementById("resume-write-main-title").value = sampleData.title;
    document.getElementById("resume-write-merit").value = sampleData.merit;
    document.getElementById("resume-write-disadvantage").value = sampleData.disadvantage;
    document.getElementById("resume-write-directionality").value = sampleData.directionality;

    addSectionIfNeeded(sampleData.sections.length - 1);

    // 직군 및 직업 선택
    const occupationSelect = document.getElementById("resume-write-occupation");
    const jobSelect = document.getElementById("resume-write-job");
    const experienceSelect = document.getElementById("resume-write-experience");

    if (occupationSelect) {
        Array.from(occupationSelect.options).forEach(option => {
            option.selected = (option.value === sampleData.occupation);
        });
        updateJobList();
    }

    if (jobSelect) {
        Array.from(jobSelect.options).forEach(option => {
            option.selected = (option.text === sampleData.job);
        });
    }

    if (experienceSelect) {
        Array.from(experienceSelect.options).forEach(option => {
            option.selected = (option.value === sampleData.experience);
        });
    }

    // 각 섹션 필드 데이터 업데이트
    const titleInputs = document.querySelectorAll('[id^="resume-write-title-"]');
    const contentInputs = document.querySelectorAll('[id^="resume-write-content-"]');

    sampleData.sections.forEach((section, index) => {
        if (titleInputs[index]) titleInputs[index].value = section.title;
        if (contentInputs[index]) contentInputs[index].value = section.content;
    });

    // keywords 배열을 순회하여 배지 생성
    sampleData.keywords.forEach((keyword, index) => {
        const badge = document.createElement('div');
        badge.className = 'badge';

        const badgeText = document.createElement('span');
        badgeText.className = 'badge-text';
        badgeText.id = `badge-text-${index}`;
        badgeText.textContent = keyword;

        const badgeButton = document.createElement('button');
        badgeButton.className = 'badge-button';
        badgeButton.id = `badge-btn-${index}`;
        badgeButton.textContent = 'X';

        const badgeInput = document.createElement('input');
        badgeInput.id = `badge-input-${index}`;
        badgeInput.type = 'hidden';
        badgeInput.name = 'keywords[]';
        badgeInput.value = keyword;

        badge.appendChild(badgeText);
        badge.appendChild(badgeButton);
        badgeContainer.appendChild(badge);
        badgeContainer.appendChild(badgeInput);

        // 버튼 클릭 시 배지 삭제
        badgeButton.addEventListener('click', function() {
            badgeContainer.removeChild(badge);
            updateBadgeIDs();
        });
    });

    // 입력 필드 추가 (배지들 뒤에 추가)
    const inputElement = document.createElement('input');
    inputElement.className = 'keyword-input Regular-16';
    inputElement.id = 'resume-write-keyword';
    inputElement.type = 'text';
    badgeContainer.appendChild(inputElement);

    // 입력 필드 너비 조정 함수
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

    // 입력 필드 이벤트 처리
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
                    updateBadgeIDs();
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

    function updateBadgeIDs() {
            const badges = badgeContainer.querySelectorAll('.badge');
            badgeCounter = 0;

            badges.forEach(badge => {
                const badgeText = badge.querySelector('.badge-text');
                const badgeButton = badge.querySelector('.badge-button');
                const badgeInput = badge.querySelector('.badge-input');

                if (badgeText && badgeButton) {
                    badgeText.id = `badge-text-${badgeCounter}`;
                    badgeButton.id = `badge-btn-${badgeCounter}`;
                    badgeInput.id = `badge-input-${badgeCounter}`;
                    badgeCounter++;
                }
            });

            badgeCounter = badges.length;
    }

    checkFormCompletion(); // 폼 완료 여부 체크
}

// 임시 저장 목록 삭제
function removeResumeData(resumeId) {
    // 콘솔에 resumeId를 출력해서 확인 (테스트 용도)
    console.log(`Removing resume with ID: ${resumeId}`);

    // 해당 resumeId를 가진 <tr> 요소를 찾아서 제거
    const resumeRow = document.getElementById(`resume-${resumeId}`);
    if (resumeRow) {
        resumeRow.remove();
    }

    // 여기서 API 호출을 추가하면 서버에서 해당 resumeId를 삭제할 수 있습니다.
    // 예: fetch(`/api/remove-resume/${resumeId}`, { method: 'DELETE' });

    // 여기에 AJAX 요청을 추가하여 서버와 통신을 할 수 있습니다.
}

// 자기소개서 "저장" 버튼 클릭 시 동작
function submitResume() {
    // 자기소개서 항목 및 내용
    const contentInputs = document.querySelectorAll('[id^="resume-write-content-"]');
    const titleInputs = document.querySelectorAll('[id^="resume-write-title-"]');

    // 경력 필드
    const experience = document.getElementById("resume-write-experience").value;
    let selectExperience = false;

    // 고정 입력 필드 목록
    const inputs = [
        {
            element: document.getElementById("resume-write-main-title"),
            name: "제목"
        },
        {
            element: document.getElementById("resume-write-occupation"),
            name: "직군"
        },
        {
            element: document.getElementById("resume-write-job"),
            name: "직업"
        },
        {
            element: document.getElementById("resume-write-merit"),
            name: "장점"
        },
        {
            element: document.getElementById("resume-write-disadvantage"),
            name: "단점"
        }
    ];

    // 주요 키워드 배지 확인
    const hasBadges = document.querySelectorAll("div.badge").length > 0;

    // 고정 필드 입력 확인
    for (const input of inputs) {
        const value = input.element.tagName === "SELECT" ? input.element.value : input.element.value.trim();
        if (!value || (input.element.tagName === "SELECT" && value === "직군을 선택해주세요")) {
            alert(`${input.name}을(를) 채워주세요.`);
            input.element.focus(); // 해당 입력 필드로 포커스 이동
            event.preventDefault();
            return; // 함수 종료
        }
    }

    // 경력 필드 확인
    if (experience === "신입" || experience === "경력") {
        selectExperience = true;
    }
    if (!selectExperience) {
        alert("경력을 선택해주세요.");
        document.getElementById("resume-write-experience").focus();
        event.preventDefault();
        return;
    }

    // 자기소개서 항목 및 내용 확인
    for (let i = 0; i < titleInputs.length; i++) {
        const title = titleInputs[i].value.trim();
        const content = contentInputs[i]?.value.trim();

        if (!title) {
            alert(`자기소개서 항목${i + 1}을(를) 채워주세요.`);
            titleInputs[i].focus();
            event.preventDefault();
            return;
        }

        if (!content) {
            alert(`자기소개서 내용${i + 1}을(를) 채워주세요.`);
            contentInputs[i]?.focus();
            event.preventDefault();
            return;
        }
    }

    // 키워드 배지 확인
    if (!hasBadges) {
        alert("주요 키워드를 추가해주세요.");
        event.preventDefault();
        return;
    }

    // 모든 조건이 충족되면 제출
    alert("자기소개서가 제출되었습니다.");
}

