// 백엔드에게 검색 필터에 대한 값을 보낼 조건을 검사하기 위한 변수
let occupationCount = 0;
let jobCount = 0;
let levelCount = 0;
let selectedOccupationId;
let selectedJobId;
let selectedOccupation;
let selectedJob;

window.onload = function() {
    const savedOccupation = localStorage.getItem('selectedOccupation');
    const savedJob = localStorage.getItem('selectedJob');

    const urlParams = new URLSearchParams(window.location.search);
    const urlOccupationId = urlParams.get('occupation_id');
    const urlJobId = urlParams.get('job_id');

    // 저장된 값이 있다면 해당 값을 표시
    if (savedOccupation && urlOccupationId) {
        const occupationSpan = document.getElementById("occupation");
        occupationSpan.textContent = savedOccupation;
    }

    if (savedJob && urlJobId) {
        const jobSpan = document.getElementById("job");
        jobSpan.textContent = savedJob;
    }
};


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

// 직군 선택시 직업 보여주기
async function showJobList(button) {
    selectedOccupation = button.textContent.trim();  // 직군 이름
    selectedOccupationId = button.value;  // 직군 ID (value에서 가져옴)
    localStorage.setItem('selectedOccupationId', selectedOccupationId);
    const jobListBox = document.getElementById("job-list-box");
    const occupationSpan = document.getElementById("occupation");
    const occupationListBox = document.getElementById("occupation-list-box");
    const jobSpan = document.getElementById("job");
    const urlParams = new URLSearchParams(window.location.search);
    const currentJob = urlParams.get('job');

    // occupation의 텍스트 업데이트
    occupationSpan.textContent = selectedOccupation;
    localStorage.setItem('selectedOccupation', selectedOccupation);

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

    try {
        // 백엔드 API 호출: 선택한 직군 ID를 경로에 동적으로 전달
        const response = await instance.get(`/job/${selectedOccupationId}`);

        // 백엔드로부터 받은 직업 데이터
        const jobList = response.data.jobs;

        // 새로운 테이블 생성 및 클래스 추가
        const table = document.createElement("table");
        table.classList.add("uk-table");  // 테이블에 기존과 동일한 클래스 적용

        const tbody = document.createElement("tbody");

        // 25개의 직업을 5x5 테이블로 나누기
        let jobIndex = 0;
        for (let i = 0; i < 5; i++) {  // 행 생성
            const tr = document.createElement("tr");
            for (let j = 1; j <= 5; j++) {  // 열 생성
                const td = document.createElement("td");
                td.classList.add("list-array");  // td에 기존과 동일한 클래스 추가

                if (jobIndex < jobList.length) {
                    const job = jobList[jobIndex];
                    const jobName = job.jobName;  // 직업 이름 가져오기
                    const jobId = job.jobId;
                    const button = document.createElement("button");

                    // 버튼에 텍스트 및 클래스 설정
                    button.type = "button";
                    button.className = "none-style-btn Regular-16-light";  // 기본 스타일
                    button.textContent = jobName;
                    button.value = jobId;
                    button.onclick = () => setJob(jobName); // 직업 선택 시 처리할 함수

                    // URL의 job과 현재 직업 이름이 같으면 색상 변경
                    if (jobName === currentJob) {
                        button.style.color = "#2B7FFF";
                        button.style.setProperty("color", "#2B7FFF", "important"); // !important를 추가하려면 setProperty 사용
                    }
                    td.appendChild(button);  // td에 버튼 추가
                }
                tr.appendChild(td);  // tr에 td 추가
                jobIndex++;  // 직업 인덱스 증가
            }
            tbody.appendChild(tr);
        }

        table.appendChild(tbody);
        jobListBox.appendChild(table);  // job-list-box에 테이블 추가

    } catch (error) {
        console.error("직업 목록 불러오기 실패:", error);
        alert("직업 목록을 불러오는 데 실패했습니다. 다시 시도해주세요.");
    }
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
        selectedJobId = selectedButton.value;
        localStorage.setItem('selectedJobId', selectedJobId);
    }

    // 직업 리스트 숨기기
    jobListBox.style.display = "none";

    // 선택된 직업의 이름을 job span에 설정
    jobSpan.textContent = jobName;
    selectedJob = jobName;
    localStorage.setItem('selectedJob', selectedJob);
    jobCount++;
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

// 최신순, 인기순 버튼을 눌렀을 때 이벤트
function setArray(arrayType) {
    const arrayButtons = document.querySelectorAll(".select-array"); // 최신순/인기순 버튼들
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

    const job = document.getElementById("job").textContent.trim();
    const occupation = document.getElementById("occupation").textContent.trim();
    const level = document.getElementById("level").textContent.trim();
    const sort = selectedButton ? selectedButton.textContent.trim() : "";
    const currentParams = new URLSearchParams(window.location.search); // 현재 URL의 쿼리 파라미터
    const params = new URLSearchParams();
    const savedOccupationId = localStorage.getItem('selectedOccupationId');
    const savedJobId = localStorage.getItem('selectedJobId');


    if (job !== "직업 선택") params.append("job_id", savedJobId);
    if (occupation !== "직군 선택") params.append("occupation_id", savedOccupationId);
    if (level !== "경력 선택") params.append("level", level);

    // 현재 URL에서 page 값이 존재하면 추가
    if (currentParams.has("page")) {
        params.append("page", currentParams.get("page"));
    }
    if (currentParams.has("search")) {
        params.append("search", currentParams.get("search"));
    }
    if (sort === "인기순") params.append("sort", 'f');
    else if (sort === "최신순") params.append("sort", 'r');
    window.location.href = `/resume?${params.toString()}`;

}

// 검색어를 입력한 input 검색 이벤트(구현 되었을 때 적용)
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("search-input").addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            const searchText = event.target.value.trim();
            const job = document.getElementById("job").textContent.trim();
            const occupation = document.getElementById("occupation").textContent.trim();
            const level = document.getElementById("level").textContent.trim();
            const selectedButton = document.querySelector(".recent-or-popular .select-array.selected");
            const sort = selectedButton ? selectedButton.textContent.trim() : "";
            const savedOccupationId = localStorage.getItem('selectedOccupationId');
            const savedJobId = localStorage.getItem('selectedJobId');
            localStorage.setItem('search', searchText);

            const currentParams = new URLSearchParams(window.location.search);
            const params = new URLSearchParams();


            if (sort) params.append("sort", sort);
            if (job !== "직업 선택") params.append("job_id", savedJobId);
            if (occupation !== "직군 선택") params.append("occupation_id", savedOccupationId);
            if (level !== "경력 선택") params.append("level", level);

            // 현재 URL에서 page 값이 존재하면 추가
            if (currentParams.has("page")) {
                params.append("page", currentParams.get("page"));
            }
            if (currentParams.has("search")) {
                params.delete("search", currentParams.get("search"));
            }
            params.append("search", searchText);
            window.location.href = `/resume?${params.toString()}`;
        }
    });
});

function searchBtn(button) {
    const job = document.getElementById("job").textContent.trim();
    const occupation = document.getElementById("occupation").textContent.trim();
    const level = document.getElementById("level").textContent.trim();
    const selectedButton = document.querySelector(".recent-or-popular .select-array.selected");

    const sort = selectedButton ? selectedButton.textContent.trim() : "";

    const currentParams = new URLSearchParams(window.location.search); // 현재 URL의 쿼리 파라미터
    const params = new URLSearchParams();
    const savedOccupationId = localStorage.getItem('selectedOccupationId');
    const savedJobId = localStorage.getItem('selectedJobId');

    if (sort) params.append("sort", sort);
    if (job !== "직업 선택") params.append("job_id", savedJobId);
    if (occupation !== "직군 선택") params.append("occupation_id", savedOccupationId);
    if (level !== "경력 선택") params.append("level", level);

    // 현재 URL에서 page 값이 존재하면 추가
    if (currentParams.has("page")) {
        params.append("page", currentParams.get("page"));
    }
    if (currentParams.has("search")) {
        params.append("search", currentParams.get("search"));
    }

    window.location.href = `/resume?${params.toString()}`;
}



async function reLoadJob(selectedOccupationId) {
    localStorage.setItem('selectedOccupationId', selectedOccupationId);
    const jobListBox = document.getElementById("job-list-box");
    const urlParams = new URLSearchParams(window.location.search);
    const currentJob = Number(urlParams.get('job_id'));

    try {
        // 백엔드 API 호출: 선택한 직군 ID를 경로에 동적으로 전달
        const response = await instance.get(`/job/${selectedOccupationId}`);

        // 백엔드로부터 받은 직업 데이터
        const jobList = response.data.jobs;
        
        // "직군을 선택해주세요" 지우기
        jobListBox.innerHTML = "";

        // 새로운 테이블 생성 및 클래스 추가
        const table = document.createElement("table");
        table.classList.add("uk-table");  // 테이블에 기존과 동일한 클래스 적용

        const tbody = document.createElement("tbody");

        // 25개의 직업을 5x5 테이블로 나누기
        let jobIndex = 0;
        for (let i = 0; i < 5; i++) {  // 행 생성
            const tr = document.createElement("tr");
            for (let j = 1; j <= 5; j++) {  // 열 생성
                const td = document.createElement("td");
                td.classList.add("list-array");  // td에 기존과 동일한 클래스 추가

                if (jobIndex < jobList.length) {
                    const job = jobList[jobIndex];
                    const jobName = job.jobName;  // 직업 이름 가져오기
                    const jobId = job.jobId;
                    const button = document.createElement("button");

                    // 버튼에 텍스트 및 클래스 설정
                    button.type = "button";
                    button.className = "none-style-btn Regular-16-light";  // 기본 스타일
                    button.textContent = jobName;
                    button.value = jobId;
                    button.onclick = () => setJob(jobName); // 직업 선택 시 처리할 함수

                    // URL의 job과 현재 직업 이름이 같으면 색상 변경
                    if (jobId === currentJob) {
                        button.style.color = "#2B7FFF";
                        button.style.setProperty("color", "#2B7FFF", "important"); // !important를 추가하려면 setProperty 사용
                    }
                    td.appendChild(button);  // td에 버튼 추가
                }
                tr.appendChild(td);  // tr에 td 추가
                jobIndex++;  // 직업 인덱스 증가
            }
            tbody.appendChild(tr);
        }

        table.appendChild(tbody);
        jobListBox.appendChild(table);  // job-list-box에 테이블 추가

    } catch (error) {
        console.error("직업 목록 불러오기 실패:", error);
        alert("직업 목록을 불러오는 데 실패했습니다. 다시 시도해주세요.");
    }
}

// 새로고침 될 때마다 직군이 선택되어 있으면 직업 목록을 가져옵니다.
document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    if(urlParams.get('occupation_id'))
        reLoadJob(Number(urlParams.get('occupation_id')));
});




