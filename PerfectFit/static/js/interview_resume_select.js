document.addEventListener("DOMContentLoaded", async () => {
    // 테이블의 tbody를 선택
    const dataBody = document.getElementById("data-body");

    try {
        // 이력서 데이터를 가져오는 API 호출
        const resumes = await fetchResumes();

        // 데이터를 렌더링
        renderResumes(resumes, dataBody);

        // 폼 제출 이벤트 처리
        const form = document.querySelector("#resumeForm");
        form.addEventListener("submit", (event) => {
            const selectedResume = document.querySelector("input[name='resumeId']:checked");
            if (!selectedResume) {
                event.preventDefault();
                alert("이력서를 선택해주세요.");
            }
        });
    } catch (error) {
        console.error("이력서 데이터를 가져오는 중 오류가 발생했습니다:", error);
    }
});

// API 호출로 이력서 데이터를 가져오는 함수
async function fetchResumes() {
    const response = await fetch("/user/mypage/resume?page=1&count=10", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: "ACCESS TOKEN", // 실제 토큰으로 대체
        },
    });

    if (!response.ok) {
        throw new Error("이력서 데이터를 가져오지 못했습니다.");
    }

    const data = await response.json();
    return data.resumes; // 이력서 리스트 반환
}

// 이력서를 테이블에 렌더링하는 함수
function renderResumes(resumes, dataBody) {
    // 기존 데이터 초기화
    dataBody.innerHTML = "";

    resumes.forEach((resume) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>
                <input type="radio" name="resumeId" value="${resume.resumeId}" required />
            </td>
            <td>${resume.title}</td>
            <td>${resume.job}</td>
            <td>${resume.level}</td>
            <td>${new Date(resume.createdTime).toLocaleDateString()}</td>
        `;

        dataBody.appendChild(row);
    });
}
