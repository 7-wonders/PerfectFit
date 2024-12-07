document.addEventListener("DOMContentLoaded", () => {


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

