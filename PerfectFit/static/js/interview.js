let currentQuestionIndex = 0;
let timerInterval;
let questions = [];

// DOMContentLoaded 이벤트로 초기화
document.addEventListener("DOMContentLoaded", async () => {
    const questionsData = await fetchQuestions(); // 질문 목록 가져오기
    questions = questionsData.questions; // 질문 리스트 저장
    loadQuestion(); // 첫 질문 로드

    // 폼 제출 이벤트 처리
    const form = document.getElementById("question-form");
    form.addEventListener("submit", (event) => {
        event.preventDefault(); // 기본 폼 제출 동작 방지

        const answerInput = document.getElementById("answer-input").value.trim();

        if (!answerInput) {
            alert("답변을 입력해주세요.");
            return;
        }

        // 답변 저장 (추후 서버로 저장 가능)
        console.log(`Question ID: ${questions[currentQuestionIndex].questionId}, Answer: ${answerInput}`);

        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
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
async function fetchQuestions() {
    const response = await fetch("/api/questions", {
        headers: {
            "Content-Type": "application/json",
            Authorization: "ACCESS TOKEN", // 실제 토큰 값으로 대체
        },
    });

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
    const modal = document.getElementById("confirmation-modal");
    UIkit.modal(modal).show(); // 공개 여부 모달 표시
}

// 모달창 닫기
document.getElementById("cancel-button").addEventListener("click", () => {
    const modal = document.getElementById("confirmation-modal");
    UIkit.modal(modal).hide(); // 공개 여부 모달 숨기기
});
