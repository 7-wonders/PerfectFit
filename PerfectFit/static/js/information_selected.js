// 프로젝트 추가
function addProject() {
    const projectExpContainer = document.getElementById(`projectExp`)

    if(document.getElementById(`add-project-btn`)) document.getElementById(`add-project-btn`).remove();

    // 새로운 프로젝트 경험 폼을 생성
    const newProject = document.createElement('div');
    newProject.classList.add('uk-margin');
    newProject.id = `project-wrapper-${projectCount}`
    newProject.innerHTML = `
        <div class="uk-margin">
            <div class="uk-flex uk-flex-between">
                <label class="uk-form-label" for="form-stacked-email">프로젝트 경험${projectCount + 1}</label>
                <button type="button" class="add-btn" id = "add-project-btn" onclick="addProject()">+ 프로젝트 추가하기</button>
            </div>

            <div class="uk-form-controls">
                <input class="uk-input" name="projectExperiences[${projectCount}][projectName]" id="form-stacked-text" type="text" placeholder="프로젝트 이름">
            </div>
        </div>

        <div class="uk-margin">
            <label class="uk-form-label" for="form-stacked-text">프로젝트 기간</label>
            <div class="uk-flex">
                <div class="uk-width-1-3@s uk-flex-first">
                    <input class="uk-input" name="projectExperiences[${projectCount}][fromDate]" type="date" aria-label="25">
                </div>
                <div class="uk-card uk-margin-left">
                    ~
                </div>
                <div class="uk-width-1-3@s uk-flex-last uk-margin-left">
                    <input class="uk-input" name="projectExperiences[${projectCount}][toDate]" type="date" aria-label="25">
                </div>
            </div>
        </div>
        <div class = "uk-margin">
            <input class="uk-input" name="projectExperiences[${projectCount}][contents]" type="text" placeholder="프로젝트 내용1">
        </div>
        <div class = "add-right-btn-box">
            <button type="button" class = "add-btn" id = "add-project-content-btn-${projectCount}" onclick="addProjectContent(${projectCount})">+ 내용 추가하기</button>
        </div>
    `;

    // 새로운 프로젝트 경험 폼을 'projectExp' 컨테이너에 추가
    projectExpContainer.appendChild(newProject);
    projectCount++;
}

function addProjectContent(num) {

    if(document.getElementById(`add-project-content-btn-${num}`)) {
        document.getElementById(`add-project-content-btn-${num}`).remove();
    }
    // 프로젝트 내용 입력 필드를 추가할 부모 요소 (projectWrapper)
    const projectWrapper = document.getElementById(`project-wrapper-${num}`);

    // 새로운 input 요소 생성
    const newContentDiv = document.createElement('div');
    newContentDiv.classList.add('uk-margin');

    const newInput = document.createElement('input');
    newInput.classList.add('uk-input');
    newInput.setAttribute('name', `projectExperiences[${num}][contents]`);
    newInput.setAttribute('type', 'text');
    newInput.setAttribute('placeholder', `프로젝트 내용${projectWrapper.querySelectorAll('.uk-margin').length - 1}`);

    // 새로운 버튼 요소 생성
    const addBtnBox = document.createElement('div');
    addBtnBox.classList.add('add-right-btn-box');

    const addButton = document.createElement('button');
    addButton.setAttribute('type', 'button');
    addButton.classList.add('add-btn');
    addButton.id = `add-project-content-btn-${num}`
    addButton.setAttribute('onclick', `addProjectContent(${num})`);
    addButton.innerText = '+ 내용 추가하기';

    // 새로운 요소를 parent 요소에 추가
    newContentDiv.appendChild(newInput);
    addBtnBox.appendChild(addButton);
    projectWrapper.appendChild(newContentDiv);
    projectWrapper.appendChild(addBtnBox);

}


function addCareer() {
    const careerExpContainer = document.getElementById('careerExp');

    if(document.getElementById(`add-career-btn`)) {
        document.getElementById(`add-career-btn`).remove();
    }

    // 새로운 경력 경험 폼을 생성
    const newCareer = document.createElement('div');
    newCareer.classList.add('uk-margin');
    newCareer.innerHTML = `
        <div class="uk-margin">
            <div class="uk-flex uk-flex-between">
                <label class="uk-form-label" for="form-stacked-email">경력${careerCount + 1}</label>
                <button class="add-btn" id="add-career-btn" onclick="addCareer()">+ 경력 추가하기</button>
            </div>

            <div class="uk-form-controls">
                <input class="uk-input" id="form-stacked-text" name="workExperiences[${careerCount}][company_name]" type="text" placeholder="회사 이름">
            </div>

            <div class="uk-margin">
                <label class="uk-form-label" for="form-stacked-text">경력 기간</label>
                <div class="uk-flex">
                    <div class="uk-width-1-3@s uk-flex-first">
                        <input class="uk-input" name="workExperiences[${careerCount}][fromDate]" type="date" aria-label="25">
                    </div>
                    <div class="uk-card uk-margin-left">
                        ~
                    </div>
                    <div class="uk-width-1-3@s uk-flex-last uk-margin-left">
                        <input class="uk-input" name="workExperiences[${careerCount}][toDate]" type="date" aria-label="25">
                    </div>
                </div>
            </div>

            <div class="uk-margin">
                <div class="uk-form-controls">
                    <input class="uk-input" name="workExperiences[${careerCount}][position]" id="form-stacked-text" type="text" placeholder="직책">
                </div>
            </div>
            <div class="uk-margin">
                <div class="uk-form-controls">
                    <input class="uk-input" name="workExperiences[${careerCount}][responsibility]" id="form-stacked-text" type="text" placeholder="담당 업무">
                </div>
            </div>
            <div class="uk-margin">
                <div class="uk-form-controls">
                    <input class="uk-input" name="workExperiences[${careerCount}][reason]" id="form-stacked-text" type="text" placeholder="퇴사 사유">
                </div>
            </div>
        </div>
    `;

    // 새로운 경력 경험 폼을 'careerExp' 컨테이너에 추가
    careerExpContainer.appendChild(newCareer);
    careerCount++;
}

function backButton() {
    history.back();
}