let currentQuestionIndex = 0;
let timerInterval;
let questions = [];

// DOMContentLoaded 이벤트로 초기화
document.addEventListener("DOMContentLoaded", async () => {

    const questionsData = await fetchQuestions(interviewId); // 질문 목록 가져오기

    questions = questionsData.questions; // 질문 리스트 저장
    console.log(questions);
    loadQuestion(); // 첫 질문 로드

    // 폼 제출 이벤트 처리
    const form = document.getElementById("question-form");
    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // 기본 폼 제출 동작 방지

        const answerInput = document.getElementById("answer-input").value.trim();

        if (!answerInput) {
            alert("답변을 입력해주세요.");
            return;
        }

        // 답변 저장 (추후 서버로 저장 가능)
        console.log(`Question ID: ${questions[currentQuestionIndex]["question_id"]}, Answer: ${answerInput}`);

        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            const formData = new FormData(form); // 폼 데이터 생성
            formData.append("questionId", questions[currentQuestionIndex]["question_id"]);
            formData.append("answer", answerInput);

            fetch(form.action, {
                method: "POST",
                body: formData,
            })
                .then((response) => {
                    if (response.ok) {

                    } else {
                        alert("답변 제출 중 문제가 발생했습니다.");
                    }
                })
                .catch((error) => {
                    console.error("Error submitting form:", error);
                    alert("네트워크 오류가 발생했습니다. 다시 시도해주세요.");
                });

            loadQuestion(); // 다음 질문 로드
        } else {
            clearInterval(timerInterval);
            showCompletionModal(); // 모든 질문 완료 시 모달창 표시
        }
    });


    // 공개 여부 버튼 이벤트 리스너
    document.getElementById("confirm-button").addEventListener("click", () => {
        alert("질문과 답변을 공개합니다.");
    });

    document.getElementById("cancel-button").addEventListener("click", () => {
        alert("공개 설정이 취소되었습니다.");
    });
});

// 질문 데이터 가져오기
async function fetchQuestions(interviewId) {
    console.log("id : "+ interviewId);
    const response = await fetch(`/interview/${interviewId}`, {
        headers: {
            "Content-Type": "application/json",
            Authorization: "ACCESS TOKEN", // 실제 토큰 값으로 대체
        },
    });
    console.log(response)
    if (!response.ok) {
        throw new Error("질문 데이터를 가져올 수 없습니다.");
    }

    return await response.json(); // 질문 데이터 반환
}

// 질문 로드 함수
function loadQuestion() {
    if (!questions || questions.length === 0) return;

    const currentQuestion = questions[currentQuestionIndex];

    // 질문 내용 업데이트
    document.getElementById("question-text").textContent = currentQuestion.question;
    document.getElementById("question-id").value = currentQuestion.questionId; // hidden input에 설정
    document.getElementById("question-number-hidden").value = currentQuestionIndex + 1; // hidden input에 설정

    // UI 업데이트
    document.getElementById("answer-input").value = ""; // 입력 필드 초기화
    document.getElementById("question-number").textContent = `${currentQuestionIndex + 1}/${questions.length}`;

    // 타이머 시작
    startTimer(60);
}

// 타이머 시작 함수
function startTimer(seconds) {
    clearInterval(timerInterval); // 이전 타이머 정리
    let timeRemaining = seconds;

    timerInterval = setInterval(() => {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        document.getElementById("timer").textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;

        if (timeRemaining > 0) {
            timeRemaining--;
        } else {
            clearInterval(timerInterval);
            alert("시간이 종료되었습니다. 다음 질문으로 이동합니다.");

            if (currentQuestionIndex < questions.length - 1) {
                currentQuestionIndex++;
                loadQuestion();
            } else {
                showCompletionModal(); // 모든 질문 완료 시 모달창 표시
            }
        }
    }, 1000);
}

// 완료 모달 표시 함수
function showCompletionModal() {
    loadModalQuestions(); // 질문과 답변 로드
    const modal = document.getElementById("confirmation-modal");
    UIkit.modal(modal).show(); // 공개 여부 모달 표시
}

// 모달창 닫기
document.getElementById("cancel-button").addEventListener("click", () => {
    const modal = document.getElementById("confirmation-modal");
    UIkit.modal(modal).hide(); // 공개 여부 모달 숨기기
});

// 체크박스 선택 및 처리
document.getElementById("confirm-button").addEventListener("click", () => {
    const selectedQuestions = [];
    const unSelectedQuestions = [];
    document.querySelectorAll("#questions-container input[type='checkbox']:checked").forEach((checkbox) => {
        selectedQuestions.push(checkbox.value); // 선택된 질문 ID 저장
    });
    document.querySelectorAll("#questions-container input[type='checkbox']:not(:checked)").forEach((checkbox) => {
        unSelectedQuestions.push(checkbox.value); // 선택된 질문 ID 저장
    });

    if (selectedQuestions.length === 0) {
        alert("선택된 항목이 없습니다.");
        return;
    }
    const form = document.getElementById("public-selection-form");

    const formData = new FormData(form); // 폼 데이터 생성
    formData.append("isShareIds", selectedQuestions);
    formData.append("isCloseIds", unSelectedQuestions);

    fetch(form.action, {
    method: "PATCH",
    body: formData,
    })
        .then((response) => {
            if (response.ok) {

            } else {
                alert("공개 설정 중 에러 발생.");
            }
        })
        .catch((error) => {
            console.error("Error submitting form:", error);
            alert("네트워크 오류가 발생했습니다. 다시 시도해주세요.");
        });

});

// 질문과 답변 데이터를 가져와서 모달에 표시
async function loadModalQuestions() {
    const questionListElement = document.getElementById("question-list");
    questionListElement.innerHTML = ""; // 기존 내용 초기화

    const response = await fetch(`/interview/ispublic/${interviewId}`, {
        headers: {
            "Content-Type": "application/json",
            Authorization: "ACCESS TOKEN", // 실제 토큰 값으로 대체
        },
    });

    if (!response.ok) {
        alert("질문과 답변 데이터를 가져올 수 없습니다.");
        return;
    }

    const data = await response.json(); // 질문과 답변 데이터

    // 일반 for 루프 사용
    for (let index = 0; index < data.length; index++) {
        const item = data[index];

        // 각 질문과 답변에 대한 HTML 요소 생성
        const questionAnswerItem = document.createElement("div");
        questionAnswerItem.classList.add("uk-margin");

        const questionText = document.createElement("p");
        questionText.classList.add("uk-text-bold");
        questionText.textContent = `Q${index + 1}. ${item.title}`;

        const answerText = document.createElement("p");
        answerText.classList.add("uk-text-muted");
        answerText.textContent = `A: ${item.answer || "답변 없음"}`;

        // 체크박스 생성
        const checkboxWrapper = document.createElement("label");
        checkboxWrapper.classList.add("uk-checkbox-wrapper");
        checkboxWrapper.style.display = "flex";
        checkboxWrapper.style.alignItems = "center";

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "publish_question";
        checkbox.value = item.questionId;
        checkbox.classList.add("uk-checkbox");
        checkboxWrapper.appendChild(checkbox);

        const checkboxLabel = document.createElement("span");
        checkboxLabel.style.marginLeft = "8px";
        checkboxLabel.textContent = "공개 여부";
        checkboxWrapper.appendChild(checkboxLabel);

        // 모달에 추가
        questionAnswerItem.appendChild(questionText);
        questionAnswerItem.appendChild(answerText);
        questionAnswerItem.appendChild(checkboxWrapper);
        questionListElement.appendChild(questionAnswerItem);
    }
}
