// // 직군을 선택하면 그에 해당하는 직업만 나오게 하기
// function updateJobList() {
//     var selectedOccupation = document.getElementById("resume-write-occupation").value;
//     var jobSelect = document.getElementById("resume-write-job");
//     // 직업 목록 초기화
//     jobSelect.innerHTML = '';
//
//     if (selectedOccupation in jobList) {
//         jobList[selectedOccupation].forEach(function(job) {
//             var option = document.createElement("option");
//             option.text = job;
//             jobSelect.add(option);
//         });
//     }
// }

// 자기소개서 작성하기 - 직군 선택시 해당하는 직업 호출
async function updateJobList() {
    const selectedOccupation = document.getElementById("resume-write-occupation").value;
    const jobSelect = document.getElementById("resume-write-job");

    // 직업 목록 초기화
    jobSelect.innerHTML = '';

    // 직군 선택이 비어 있는 경우 종료
    if (!selectedOccupation) {
        return;
    }

    try {
        // 백엔드 API 호출: 선택한 직군 ID를 경로에 동적으로 전달
        const response = await instance.get(`/job/${selectedOccupation}`);
        // 백엔드로부터 받은 직업 데이터
        const jobList = response.data.jobs;

        // 직업 데이터를 기반으로 <option> 추가
        jobList.forEach(function (job) {
            const option = document.createElement("option");
            option.value = job.jobId; // jobId를 value로 설정
            option.text = job.jobName; // jobName을 표시
            jobSelect.add(option);
        });

    } catch (error) {
        console.error("직업 목록 불러오기 실패:", error);
        console.log(selectedOccupation);
        alert("직업 목록을 불러오는 데 실패했습니다. 다시 시도해주세요.");
    }
}

// 자기소개서 작성하기 - 넘어온 직업이 없을시 한 번 직업 호출
document.addEventListener("DOMContentLoaded", function() {
    if(getJob)
        updateJobList();
});


// 자기소개서 작성하기 - ai 작성하기 API 통신 예시
async function aiResumeWrite(idNumber) {
    // 입력 필드 및 필요한 요소들 가져오기
    const titleInput = document.getElementById(`resume-write-title-${idNumber}`);
    const textarea = document.getElementById(`resume-write-content-${idNumber}`);
    const button = document.getElementById(`ai-resume-write-${idNumber}`);
    const keywords = Array.from(document.querySelectorAll('[id^="badge-input-"]')).map(input => input.value.trim());
    const directional = document.getElementById("resume-write-directionality").value.trim() || null;
    const jobId = document.getElementById("resume-write-job").value;
    const level = document.getElementById("resume-write-experience").value;
    const pros = document.getElementById("resume-write-merit").value.trim();
    const cons = document.getElementById("resume-write-disadvantage").value.trim();
     // 로딩 애니메이션 추가
    let loadingDots = 0;
    // 버튼 비활성화
    button.disabled = true;
    textarea.disabled = true;
    const loadingMessageBase = "AI가 자기소개서를 작성중입니다";
    textarea.value = loadingMessageBase;
    const loadingInterval = setInterval(() => {
        loadingDots = (loadingDots + 1) % 4; // 점이 0~3개까지 순환
        const dots = ".".repeat(loadingDots);
        textarea.value = `${loadingMessageBase}${dots}`;
    }, 500); // 500ms 간격으로 업데이트

    try {
        // 백엔드로 데이터 전송
        console.log(keywords);
        const response = await instance.post('/resume/write/part', JSON.stringify({
                keywords: keywords,
                jobId: Number(jobId),
                level: level,
                pros: pros,
                cons: cons,
                directional: directional,
                chapterTitle: titleInput.value.trim()
            }));

        // 백엔드로부터 받은 데이터
        const text = response.data.content;

        // 로딩 애니메이션 제거
        clearInterval(loadingInterval);

        // 애니메이션을 통한 텍스트 출력
        let index = 0;
        textarea.value = ""; // 기존 내용을 지움

        function typeWriter() {
            if (index < text.length) {
                textarea.value += text.charAt(index);
                index++;
                setTimeout(typeWriter, 15); // 타이핑 속도 조절
            } else {
                // 버튼 활성화
                button.disabled = false;
                textarea.disabled = false;
            }
        }

        typeWriter();
    } catch (error) {
        console.error("AI 생성 요청 실패:", error);
        if(error.status === 400)
            aiResumeWriteValidation();
        else
            alert("AI 생성 중 오류가 발생했습니다. 다시 시도해주세요.");

        // 로딩 애니메이션 제거
        clearInterval(loadingInterval);
        textarea.value = ""; // 오류 시 텍스트 영역 초기화

        // 버튼 활성화
        button.disabled = false;
        textarea.disabled = false;
    }
    checkFormCompletion();
}
