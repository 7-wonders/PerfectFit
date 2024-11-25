// 백엔드에게 검색 필터에 대한 값을 보낼 조건을 검사하기 위한 변수
let occupationCount = 0;
let jobCount = 0;
let levelCount = 0;

// 검색 필터 버튼 클릭하면 테이블 닫기
document.addEventListener("DOMContentLoaded", function () {
    let activeIndex = -1;  // 현재 활성화된 탭을 추적하기 위한 변수

    // 처음에는 모든 콘텐츠를 숨기기
    document.querySelectorAll(".search-content, .search-content-level").forEach(content => content.style.display = "none");

    // 각 탭에 클릭 이벤트 추가
    document.querySelectorAll(".search-filter-wrapper li").forEach((tab, index) => {
        tab.addEventListener("click", function (event) {
            event.preventDefault();

            // 클릭된 탭에 따른 콘텐츠 요소 찾기
            const content = document.querySelectorAll(".search-content, .search-content-level")[index];

            // 동일한 탭을 다시 누른 경우, 콘텐츠를 숨기고 activeIndex를 초기화
            if (activeIndex === index) {
                content.style.display = "none";
                activeIndex = -1;
            } else {
                // 모든 콘텐츠 숨기기
                document.querySelectorAll(".search-content, .search-content-level").forEach(content => content.style.display = "none");

                // 클릭된 탭의 콘텐츠만 표시하고 activeIndex 업데이트
                content.style.display = "block";
                activeIndex = index;
            }
        });
    });
});

// 직군을 선택 했을 때 직업 내용 세팅
function showJobList(button) {
    const occupationName = button.textContent.trim();  // 선택한 직군 이름
    const jobListBox = document.getElementById("job-list-box");
    const occupationSpan = document.getElementById("occupation");
    const occupationListBox = document.getElementById("occupation-list-box");
    const jobSpan = document.getElementById("job");

    // occupation의 텍스트 업데이트 및 카운트 증가
    occupationSpan.textContent = occupationName;
    occupationCount++;

    // occupation-list-box 숨기기
    occupationListBox.style.display = "none";

    // job의 텍스트가 "직업 선택"이 아닐 경우 초기화
    if (jobSpan.textContent.trim() !== "직업 선택") {
        jobSpan.textContent = "직업 선택";
    }

    // 기존 job-list-box의 내용 비우기
    jobListBox.innerHTML = "";

    // 직군 버튼에 색상 적용
    const occupationButtons = document.querySelectorAll("#occupation-list-box button");
    occupationButtons.forEach((btn) => {
        // 기존 선택된 버튼의 색상 초기화
        btn.classList.remove("selected");
        btn.classList.add("Regular-16-light");
        btn.style.color = "rgba(0, 0, 0, 0.50)";
    });

    // 클릭한 직군 버튼에 선택된 스타일 추가
    button.classList.add("selected");
    button.classList.remove("Regular-16-light");
    button.style.color = "#2B7FFF"; // 직군 선택 버튼 색상

    // 새로운 테이블 생성 및 클래스 추가
    const table = document.createElement("table");
    table.classList.add("uk-table");  // 테이블에 기존과 동일한 클래스 적용

    const tbody = document.createElement("tbody");

    // 25개의 직업을 5x5 테이블로 나누기
    for (let i = 0; i < 5; i++) {  // 행 생성
        const tr = document.createElement("tr");
        for (let j = 1; j <= 5; j++) {  // 열 생성
            const td = document.createElement("td");
            td.classList.add("list-array");  // td에 기존과 동일한 클래스 추가

            const jobIndex = i * 5 + j;  // 직업 번호 계산
            const jobName = `${occupationName}-${jobIndex}`;  // 직업 이름 생성
            const button = document.createElement("button");

            // 버튼에 텍스트 및 클래스 설정
            button.type = "button";
            button.className = "none-style-btn Regular-16-light";  // 기본 스타일
            button.textContent = jobName;
            button.onclick = () => setJob(jobName);

            td.appendChild(button);  // td에 버튼 추가
            tr.appendChild(td);      // tr에 td 추가
        }
        tbody.appendChild(tr);
    }

    table.appendChild(tbody);
    jobListBox.appendChild(table);  // job-list-box에 테이블 추가

    // 백엔드로 데이터 보내기 (구현 되었을 때 테스트 예정)
    // sendDataToBackend();
}

// 직업을 선택할 때 실행되는 함수
function setJob(jobName) {
    const jobSpan = document.getElementById("job");
    const jobListBox = document.getElementById("job-list-box");

    // 직업 리스트의 모든 버튼을 가져옴
    const jobButtons = document.querySelectorAll("#job-list-box button");

    // 모든 직업 버튼의 색상 초기화
    jobButtons.forEach((btn) => {
        btn.classList.remove("selected");
        btn.classList.add("Regular-16-light");
        btn.style.color = "rgba(0, 0, 0, 0.50)";
    });

    // 선택된 직업 버튼에 색상 및 스타일 적용
    const selectedButton = Array.from(jobButtons).find((btn) => btn.textContent === jobName);
    if (selectedButton) {
        selectedButton.classList.add("selected");
        selectedButton.classList.remove("Regular-16-light");
        selectedButton.style.color = "#2B7FFF"; // 직업 버튼의 색상 변경
    }

    // 직업 리스트 숨기기
    jobListBox.style.display = "none";

    // 선택된 직업의 이름을 job span에 설정
    jobSpan.textContent = jobName;
    jobCount++;

    // 백엔드로 데이터 보내기 (구현 되었을 때 테스트 예정)
    // sendDataToBackend();
}


// 경력 선택할 때 실행되는 함수
function setLevel(level) {
    const levelSpan = document.getElementById("level");
    const levelListBox = document.getElementById("level-list-box");

    // 경력 리스트의 모든 버튼을 가져옴
    const levelButtons = document.querySelectorAll("#level-list-box button");

    // 모든 경력 버튼의 색상 초기화
    levelButtons.forEach((btn) => {
        btn.classList.remove("selected");
        btn.classList.add("Regular-16-light");
        btn.style.color = "rgba(0, 0, 0, 0.50)";
    });

    // 선택된 경력 버튼에 색상 및 스타일 적용
    const selectedButton = Array.from(levelButtons).find((btn) => btn.textContent === level);
    if (selectedButton) {
        selectedButton.classList.add("selected");
        selectedButton.classList.remove("Regular-16-light");
        selectedButton.style.color = "#2B7FFF"; // 경력 버튼의 색상 변경
    }

    // 경력 리스트 숨기기
    levelListBox.style.display = "none";

    // 선택된 경력의 이름을 level span에 설정
    levelSpan.textContent = level;
    levelCount++;

    // 백엔드로 데이터 보내기 (구현 되었을 때 테스트 예정)
    // sendDataToBackend();
}

// 백엔드로 검색 필터에 대한 값을 보내기 위한 예시 함수(직군, 직업, 경력, 정렬 방식)
// function sendDataToBackend() {
//     const occupation = document.getElementById("occupation").textContent;
//     const job = document.getElementById("job").textContent;
//     const level = document.getElementById("level").textContent;
//
//     // 선택된 정렬 버튼의 텍스트 가져오기
//     const selectedArrayType = document.querySelector(".select-array.selected").textContent;
//
//     // 카운트가 0이 아닐 경우에만 전송
//     if (occupationCount > 0 && jobCount > 0 && levelCount > 0) {
//         fetch("/your-backend-endpoint", {
//             method: "POST",
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ occupation, job, level, arrayType: selectedArrayType })
//         })
//         .then(response => response.json())
//         .then(data => {
//             console.log("Data sent to backend:", data);
//         })
//         .catch(error => {
//             console.error("Error:", error);
//         });
//     }
// }


// 최신순, 인기순 버튼을 눌렀을 때 이벤트
function setArray(arrayType) {
    const arrayButtons = document.querySelectorAll(".select-array"); // 최신순/인기순 버튼들
    const occupationSpan = document.getElementById("occupation");    // 직군 Span
    const jobSpan = document.getElementById("job");                  // 직업 Span
    const levelSpan = document.getElementById("level");              // 경력 Span

    // 모든 버튼의 색상 초기화
    arrayButtons.forEach((btn) => {
        btn.classList.remove("selected");
        btn.classList.add("Regular-16");
        btn.style.color = "rgba(0, 0, 0, 0.50)"; // 기본 색상
    });

    // 선택된 버튼에 색상 및 스타일 적용
    const selectedButton = Array.from(arrayButtons).find((btn) => btn.textContent.trim() === arrayType);
    if (selectedButton) {
        selectedButton.classList.add("selected");
        selectedButton.classList.remove("Regular-16");
        selectedButton.style.color = "#2B7FFF"; // 선택된 버튼 색상
    }

    // occupation, job, level의 텍스트 가져와서 변환(API 구현 되었을 때 실행)
    // const occupationText = occupationSpan.textContent.trim() === "직군 선택" ? null : occupationSpan.textContent.trim();
    // const jobText = jobSpan.textContent.trim() === "직업 선택" ? null : jobSpan.textContent.trim();
    // const levelText = levelSpan.textContent.trim() === "경력 선택" ? null : levelSpan.textContent.trim();

    // 백엔드로 보낼 데이터 객체(구현 되었을 때 실행)
    // const requestData = {
    //     occupation: occupationText,
    //     job: jobText,
    //     level: levelText,
    //     arrayType: arrayType // 선택된 정렬 방식 (최신순/인기순)
    // };

    // 백엔드로 데이터 전송(구현 되었을 때 실행)
    // fetch("/api/endpoint", {  // 백엔드 URL로 교체
    //     method: "POST",
    //     headers: {
    //         "Content-Type": "application/json"
    //     },
    //     body: JSON.stringify(requestData)
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log("백엔드 응답:", data);
    //     // 추가 작업 수행 가능
    // })
    // .catch(error => console.error("데이터 전송 오류:", error));
}

// 검색어를 입력한 input 검색 이벤트(구현 되었을 때 적용)
// document.getElementById("search-input").addEventListener("keydown", function(event) {
//     // Enter 키 감지
//     if (event.key === "Enter") {
//         event.preventDefault(); // 기본 동작 방지 (폼 제출 등)
//
//         const searchText = event.target.value.trim(); // 검색 텍스트
//
//         // 입력된 검색어가 비어있지 않을 때만 전송
//         if (searchText) {
//             fetch("/your-backend-endpoint", {
//                 method: "POST",
//                 headers: {
//                     "Content-Type": "application/json"
//                 },
//                 body: JSON.stringify({ searchText })
//             })
//             .then(response => response.json())
//             .then(data => {
//                 console.log("Search text sent to backend:", data);
//                 // 필요에 따라 검색어 결과 표시 등의 작업 수행 가능
//             })
//             .catch(error => {
//                 console.error("Error:", error);
//             });
//         }
//     }
// });


