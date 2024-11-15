const questions = [
    { text: "2024년 동안 프로젝트를 총 3개를 진행하였는데, 2024년 이전에는 프로젝트를 따로 안 하신 이유가 있는지 궁금합니다." },
    { text: "API 호출 시 발생할 수 있는 오류에 대해 설명해주세요." },
    { text: "보안 측면에서 개발할 때 중요한 점은 무엇인가요?" },
    { text: "보안 측면에서 개발할 때 중요한 점은 무엇인가요?" }
];

let currentQuestionIndex = 0;
let timerInterval;
let userAnswers = [];

function loadQuestion() {
    document.getElementById("question-text").textContent = questions[currentQuestionIndex].text;
    document.getElementById("question-number").textContent = `${currentQuestionIndex + 1}/${questions.length}`;
    document.getElementById("answer-input").value = "";
    startTimer(60);
}

function startTimer(seconds) {
    clearInterval(timerInterval);
    let timeRemaining = seconds;

    timerInterval = setInterval(() => {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        document.getElementById("timer").textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

        if (timeRemaining > 0) {
            timeRemaining--;
        } else {
            clearInterval(timerInterval);
            alert("시간이 종료되었습니다. 다음 질문으로 이동해 주세요.");
        }
    }, 1000);
}

document.getElementById("next-button").addEventListener("click", () => {
    const answer = document.getElementById("answer-input").value;
    userAnswers[currentQuestionIndex] = answer;

    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        loadQuestion();
    } else {
        clearInterval(timerInterval);
        showConfirmationModal();
    }
});

function showConfirmationModal() {
    UIkit.modal("#confirmation-modal").show();
    const questionList = document.getElementById("question-list");
    questionList.innerHTML = "";

    questions.forEach((question, index) => {
        const questionItem = document.createElement("div");
        questionItem.classList.add("question-item");
        questionItem.innerHTML = `
            <div style="display: flex; align-items: center;">
                <input type="checkbox" class="question-checkbox">
                <label class="question-item-content">
                    ${index + 1}. ${question.text}
                </label>
                <span class="toggle-arrow" onclick="toggleAnswer(this)">▼</span>
            </div>
            <div class="answer-text">${userAnswers[index] || "답변이 없습니다."}</div>
        `;
        questionList.appendChild(questionItem);
    });
}

function toggleAnswer(element) {
    const questionItem = element.closest(".question-item");
    const answerText = questionItem.querySelector(".answer-text");

    questionItem.classList.toggle("open"); // open 클래스 토글

    if (answerText.style.display === "none" || !answerText.style.display) {
        answerText.style.display = "block";
    } else {
        answerText.style.display = "none";
    }
}


document.getElementById("confirm-button").addEventListener("click", () => {
    alert("질문이 공개되었습니다.");
});

document.getElementById("cancel-button").addEventListener("click", () => {
    alert("질문 공개가 취소되었습니다.");
});

loadQuestion();
