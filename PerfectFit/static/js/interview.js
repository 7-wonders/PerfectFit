let currentQuestionIndex = 0;
let timerInterval;
let questions = [];

// 페이지 로드 후 초기화
document.addEventListener("DOMContentLoaded", async () => {
    try {
        const questionsData = await fetchQuestions(interviewId); // 질문 목록 가져오기
        questions = questionsData.questions;
        loadQuestion(); // 첫 질문 로드
    } catch (error) {
        console.error("질문 데이터 로드 실패:", error);
        alert("질문 데이터를 가져오는 중 문제가 발생했습니다.");
    }

    // 폼 제출 이벤트
    const form = document.getElementById("question-form");
    form.addEventListener("submit", handleFormSubmit);

    // 모달 버튼 이벤트
    document.getElementById("confirm-button").addEventListener("click", handleConfirmPublic);
    document.getElementById("cancel-button").addEventListener("click", handleCancelPublic);
});

// 질문 데이터 가져오기
async function fetchQuestions(interviewId) {
    const response = await fetch(`/interview/${interviewId}`, {
        headers: {
            "Content-Type": "application/json",
            Authorization: "ACCESS TOKEN",
        },
    });

    if (!response.ok) {
        throw new Error("질문 데이터를 가져올 수 없습니다.");
    }
    return await response.json();
}

// 폼 제출 처리
async function handleFormSubmit(event) {
    event.preventDefault();

    const answerInput = document.getElementById("answer-input").value.trim();
    if (!answerInput) {
        alert("답변을 입력해주세요.");
        return;
    }

    try {
        // 서버에 답변 저장
        const formData = new FormData(event.target);
        formData.append("questionId", questions[currentQuestionIndex]["question_id"]);
        formData.append("answer", answerInput);

        const response = await fetch(event.target.action, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("답변 저장 실패");
        }

        // 다음 질문 로드
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            loadQuestion();
        } else {
            clearInterval(timerInterval);
            showCompletionModal(); // 모든 질문 완료 시 모달 표시
        }
    } catch (error) {
        console.error("답변 제출 중 오류:", error);
        alert("답변 제출 중 문제가 발생했습니다.");
    }
}

// 질문 로드
function loadQuestion() {
    if (!questions || questions.length === 0) return;

    const currentQuestion = questions[currentQuestionIndex];

    // 질문 UI 업데이트
    document.getElementById("question-text").textContent = currentQuestion.question;
    document.getElementById("question-id").value = currentQuestion.questionId;
    document.getElementById("question-number-hidden").value = currentQuestionIndex + 1;

    // UI 초기화
    document.getElementById("answer-input").value = "";
    document.getElementById("question-number").textContent = `${currentQuestionIndex + 1}/${questions.length}`;

    // 타이머 시작
    startTimer(60);
}

// 타이머
function startTimer(seconds) {
    clearInterval(timerInterval); // 기존 타이머 초기화
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
                showCompletionModal();
            }
        }
    }, 1000);
}

// 완료 모달 표시
async function showCompletionModal() {
    try {
        await loadModalQuestions(); // 모달 데이터 로드
        const modal = document.getElementById("confirmation-modal");
        UIkit.modal(modal).show();
    } catch (error) {
        console.error("모달 데이터 로드 실패:", error);
        alert("모달 데이터를 가져오는 중 문제가 발생했습니다.");
    }
}

// 모달 데이터 로드
async function loadModalQuestions() {
    const questionListElement = document.getElementById("question-list");
    questionListElement.innerHTML = ""; // 초기화

    const response = await fetch(`/interview/ispublic/${interviewId}`, {
        headers: {
            "Content-Type": "application/json",
            Authorization: "ACCESS TOKEN",
        },
    });

    if (!response.ok) {
        throw new Error("질문과 답변 데이터를 가져올 수 없습니다.");
    }

    const data = await response.json();
    data.forEach((item, index) => {
        const questionAnswerItem = document.createElement("div");
        questionAnswerItem.classList.add("uk-margin");

        questionAnswerItem.innerHTML = `
            <p class="uk-text-bold">Q${index + 1}. ${item.title}</p>
            <p class="uk-text-muted">A: ${item.answer || "답변 없음"}</p>
            <label class="uk-checkbox-wrapper" style="display: flex; align-items: center;">
                <input type="checkbox" name="publish_question" value="${item.questionId}" class="uk-checkbox">
                <span style="margin-left: 8px;">공개 여부</span>
            </label>
        `;

        questionListElement.appendChild(questionAnswerItem);
    });
}

// 공개 여부 확인 버튼
async function handleConfirmPublic() {
    const selectedQuestions = Array.from(
        document.querySelectorAll("#questions-container input[type='checkbox']:checked")
    ).map((checkbox) => checkbox.value);

    const unSelectedQuestions = Array.from(
        document.querySelectorAll("#questions-container input[type='checkbox']:not(:checked)")
    ).map((checkbox) => checkbox.value);

    if (selectedQuestions.length === 0) {
        alert("선택된 항목이 없습니다.");
        return;
    }

    try {
        const response = await fetch("/interview/ispublic", {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                Authorization: "ACCESS TOKEN",
            },
            body: JSON.stringify({
                isShareIds: selectedQuestions,
                isCloseIds: unSelectedQuestions,
            }),
        });

        if (!response.ok) {
            throw new Error("공개 설정 실패");
        }

        alert("공개 설정이 완료되었습니다.");
    } catch (error) {
        console.error("공개 설정 중 오류:", error);
        alert("공개 설정 중 문제가 발생했습니다.");
    }
}

// 모달 닫기 버튼
function handleCancelPublic() {
    const modal = document.getElementById("confirmation-modal");
    UIkit.modal(modal).hide();
}
