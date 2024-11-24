document.addEventListener("DOMContentLoaded", () => {
    const data = [
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        },
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
        ,
        {
            company: "한국자산관리공사",
            type: "신입",
            testTitle: "~~의 모의 면접",
            position: "일반사무",
            feedback: ["인재상1", "인재상2", "이러면 안돼요!"],
        }
    ];

    const cardContainer = document.getElementById("card-container");
    const paginationContainer = document.getElementById("pagination");
    const totalCountElement = document.querySelector(".total-count strong");
    const tabs = document.querySelectorAll(".tab");
    const tabContents = {
        category: document.getElementById("category-tab"),
        position: document.getElementById("position-tab"),
        search: document.getElementById("search-tab"),
    };

    const CARDS_PER_PAGE = 8; // 페이지당 카드 수
    let currentPage = 1;

    // 총 저장건수 업데이트 함수
    function updateTotalCount() {
        totalCountElement.textContent = `${data.length}개`;
    }

    // 카드 렌더링 함수
    function renderCards(page) {
        cardContainer.innerHTML = "";

        // 현재 페이지 데이터 계산
        const startIndex = (page - 1) * CARDS_PER_PAGE;
        const endIndex = startIndex + CARDS_PER_PAGE;
        const pageData = data.slice(startIndex, endIndex);

        // 카드 생성
        pageData.forEach((item) => {
            const card = document.createElement("div");
            card.classList.add("card");

            card.innerHTML = `
                <div class="card-content">
                    <div class="card-header">
                        <span class="company">${item.company}</span>
                        <span class="status">${item.type}</span>
                    </div>
                    <h3 class="test-title">${item.testTitle}</h3>
                    <div class="card-body">
                        <p class="position">지원 분야: ${item.position}</p>
                        <ul class="feedback-list">
                            <li class="feedback positive"><i class="icon">👍</i> ${item.feedback[0]}</li>
                            <li class="feedback positive"><i class="icon">👍</i> ${item.feedback[1]}</li>
                            <li class="feedback negative"><i class="icon">👎</i> ${item.feedback[2]}</li>
                        </ul>
                    </div>
                </div>
            `;
            cardContainer.appendChild(card);
        });

        // 빈 카드 채우기 (플레이스홀더)
        const placeholders = CARDS_PER_PAGE - pageData.length;
        for (let i = 0; i < placeholders; i++) {
            const placeholder = document.createElement("div");
            placeholder.classList.add("card", "placeholder");
            cardContainer.appendChild(placeholder);
        }
    }

    // 페이지네이션 렌더링 함수
    function renderPagination() {
        paginationContainer.innerHTML = "";

        const totalPages = Math.ceil(data.length / CARDS_PER_PAGE);

        for (let i = 1; i <= totalPages; i++) {
            const li = document.createElement("li");
            const button = document.createElement("button");
            button.textContent = i;
            button.className = i === currentPage ? "active" : "";
            button.addEventListener("click", () => {
                currentPage = i;
                renderCards(currentPage);
                renderPagination();
            });
            li.appendChild(button);
            paginationContainer.appendChild(li);
        }
    }

    // 탭 활성화 처리 함수
    function activateTab(tabId) {
        // 모든 탭 비활성화
        tabs.forEach((tab) => tab.classList.remove("active"));

        // 모든 탭 콘텐츠 숨기기
        Object.values(tabContents).forEach((content) => {
            content.style.display = "none";
        });

        // 클릭된 탭 활성화 및 콘텐츠 표시
        const clickedTab = document.querySelector(`[data-tab="${tabId}"]`);
        if (clickedTab) clickedTab.classList.add("active");

        // 관련 콘텐츠 활성화
        if (tabContents[tabId]) {
            tabContents[tabId].style.display = "block";
        }

        // 카드와 페이지네이션 기본 렌더링 (내용 검색에서도 카드 표시)
        if (tabId === "search" || tabId === "category") {
            renderCards(currentPage);
            renderPagination();
        }
    }

    // 데이터 추가 함수
    function addData(newItem) {
        data.push(newItem);
        updateTotalCount();
        renderCards(currentPage);
        renderPagination();
    }

    // 탭 클릭 이벤트 등록
    tabs.forEach((tab) => {
        tab.addEventListener("click", () => {
            const tabId = tab.getAttribute("data-tab");
            activateTab(tabId);
        });
    });

    // 초기 렌더링
    function init() {
        updateTotalCount();
        renderCards(currentPage);
        renderPagination();
        activateTab("category"); // 기본 활성화 탭
    }

    init();
});
