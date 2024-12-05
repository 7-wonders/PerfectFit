document.addEventListener('DOMContentLoaded', function() {
    // 버튼과 부모 요소를 선택
    const addProjectButton = document.getElementById('addProjectButton');

    const addCareerButton = document.getElementById('addCareerButton');
    const careerExpContainer = document.getElementById('careerExp');

    // 프로젝트 추가 함수


    // 경력 추가 함수
    function addCareer(event) {
        event.preventDefault(); // 기본 동작 방지 (폼 전송 방지)

        // 새로운 경력 경험 폼을 생성
        const newCareer = document.createElement('div');
        newCareer.classList.add('uk-margin');
        newCareer.innerHTML = `
            <div class="uk-flex uk-flex-between">
                <label class="uk-form-label" for="form-stacked-email">회사 이름</label>
            </div>
            <div class="uk-form-controls">
                <input class="uk-input" type="text" placeholder="회사 이름">
            </div>

            <div class="uk-margin">
                <label class="uk-form-label" for="form-stacked-text">경력 기간</label>
                <div class="uk-flex">
                    <div class="uk-width-1-4@s uk-flex-first">
                        <input class="uk-input" type="text" aria-label="25">
                    </div>
                    <div class="uk-card uk-margin-left"> ~ </div>
                    <div class="uk-width-1-4@s uk-flex-last uk-margin-left">
                        <input class="uk-input" type="text" aria-label="25">
                    </div>
                </div>
            </div>

            <div class="uk-margin">
                <div class="uk-form-controls">
                    <input class="uk-input" type="text" placeholder="직책">
                </div>
            </div>

            <div class="uk-margin">
                <div class="uk-form-controls">
                    <input class="uk-input" type="text" placeholder="맡은 일">
                </div>
            </div>

            <div class="uk-margin">
                <div class="uk-form-controls">
                    <input class="uk-input" type="text" placeholder="퇴사 사유">
                </div>
            </div>
        `;

        // 새로운 경력 경험 폼을 'careerExp' 컨테이너에 추가
        careerExpContainer.appendChild(newCareer);
    }

    // 버튼 클릭 시 각 함수 실행

});

function addProject() {

    const projectExpContainer = document.getElementById('projectExp');

    // 새로운 프로젝트 경험 폼을 생성
    const newProject = document.createElement('div');
    newProject.classList.add('uk-margin');
    newProject.innerHTML = `
        <div class="uk-flex uk-flex-between">
            <label class="uk-form-label" for="form-stacked-text">프로젝트 이름</label>
        </div>
        <div class="uk-form-controls">
            <input class="uk-input" type="text" placeholder="프로젝트 이름">
        </div>
        <div class="uk-margin">
            <label class="uk-form-label" for="form-stacked-text">프로젝트 기간</label>
            <div class="uk-flex">
                <div class="uk-width-1-4@s uk-flex-first">
                    <input class="uk-input" type="text" aria-label="25">
                </div>
                <div class="uk-card uk-margin-left"> ~ </div>
                <div class="uk-width-1-4@s uk-flex-last uk-margin-left">
                    <input class="uk-input" type="text" aria-label="25">
                </div>
            </div>
        </div>
        <div class="uk-margin">
            <label class="uk-form-label" for="form-stacked-text">프로젝트 내용</label>
            <textarea class="uk-textarea" rows="5" placeholder="프로젝트 내용" aria-label="Textarea"></textarea>
        </div>
    `;

    // 새로운 프로젝트 경험 폼을 'projectExp' 컨테이너에 추가
    projectExpContainer.appendChild(newProject);
}