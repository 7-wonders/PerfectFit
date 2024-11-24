document.addEventListener("DOMContentLoaded", () => {
    const jobCategories = [
        {
            name: "경영 · 행정 · 사무직",
            jobs: ["사무직", "행정관리", "회계담당자", "기획 전문가"]
        },
        {
            name: "개발/데이터",
            jobs: [
                "웹 개발자",
                "시스템 개발자",
                "데이터 분석가",
                "AI 엔지니어",
                "데이터 엔지니어",
                "프론트엔드 개발자",
                "백엔드 개발자"
            ]
        },
        {
            name: "마케팅/광고",
            jobs: ["마케팅 전략가", "광고 기획자", "SNS 매니저", "브랜드 매니저"]
        }
    ];

    const jobCategorySection = document.querySelector(".job-category-section");

    jobCategories.forEach((category) => {
        const categoryElement = document.createElement("div");
        categoryElement.classList.add("job-category");

        const categoryHeader = document.createElement("div");
        categoryHeader.classList.add("job-category-header");
        categoryHeader.innerHTML = `${category.name} <span>(${category.jobs.length}개)</span>`;

        const categoryBody = document.createElement("div");
        categoryBody.classList.add("job-category-body");
        category.jobs.forEach((job) => {
            const jobButton = document.createElement("button");
            jobButton.classList.add("job-role");
            jobButton.textContent = job;
            categoryBody.appendChild(jobButton);
        });

        categoryBody.style.display = "none";

        categoryHeader.addEventListener("click", () => {
            categoryBody.style.display = categoryBody.style.display === "block" ? "none" : "block";
        });

        categoryElement.appendChild(categoryHeader);
        categoryElement.appendChild(categoryBody);
        jobCategorySection.appendChild(categoryElement);
    });
});

