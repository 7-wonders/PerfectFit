document.addEventListener("DOMContentLoaded", async () => {
    try {
        // 질문 및 답변 가져오기
        const questionsData = await fetchQuestions();
        renderQuestions(questionsData);
    } catch (error) {
        console.error("질문 또는 답변을 가져오는 중 오류가 발생했습니다:", error);
    }
});

// 질문 및 답변 가져오기 API 호출
async function fetchQuestions() {
    const response = await fetch("/api/questions", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: "ACCESS TOKEN", // 실제 토큰 값으로 대체
        },
    });

    if (!response.ok) {
        throw new Error("질문 데이터를 가져오지 못했습니다.");
    }

    const data = await response.json();
    return data.questions; // 질문 리스트 반환
}

// 질문 및 답변 렌더링
function renderQuestions(questions) {
    const form = document.getElementById("questions-form");

    // 기존 질문 초기화
    form.innerHTML = "";

    questions.forEach((question) => {
        // 각 질문 및 답변 렌더링
        const questionBlock = document.createElement("div");
        questionBlock.classList.add("question");

        // Form 요소 추가
        questionBlock.innerHTML = `
            <label for="answer-${question.questionId}" class="question-title">
                ${question.question}
            </label>
            <textarea
                id="answer-${question.questionId}"
                name="answer-${question.questionId}"
                rows="3"
                class="answer"
                readonly
            >${question.answer ? question.answer : "아직 답변이 작성되지 않았습니다."}</textarea>
            <button
                type="button"
                class="check-button"
                onclick="fetchImprovement(${question.questionId})"
            >
                개선 사항 확인
            </button>
            <hr class="divider">
        `;

        form.appendChild(questionBlock);
    });
}

// 개선사항 가져오기 및 표시
async function fetchImprovement(questionId) {
    try {
        const formData = new FormData();
        formData.append("questionId", questionId);

        const response = await fetch(`/api/improvements/${questionId}`, {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("개선 사항 데이터를 가져오지 못했습니다.");
        }

        const data = await response.json();
        renderImprovement(data.improvement); // 개선 사항 표시
    } catch (error) {
        console.error("개선 사항 가져오기 중 오류 발생:", error);
    }
}

// 개선 사항 렌더링
function renderImprovement(improvement) {
    const rightPanel = document.querySelector(".right-panel .result-content");
    rightPanel.textContent = improvement || "개선 사항이 없습니다.";
}
