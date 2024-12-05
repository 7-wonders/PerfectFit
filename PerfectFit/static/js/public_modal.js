const publicModalClickHandler = () => {
    const questionContainersEle = document.querySelectorAll('.question-container');

    questionContainersEle.forEach(questionContainerEle => {
        questionContainerEle.addEventListener('click', (event) => {
            const isExpand = event.target.dataset.expand === 'true';

            let parentNode = event.target;
            while (!parentNode.classList.contains('item')) {
                parentNode = parentNode.parentElement;
            }

            console.log(parentNode);

            const arrowNode = parentNode.querySelector('.down-arrow');
            const contentNode = parentNode.querySelector('.content');

            if (!isExpand) {
                contentNode.classList.add('animation');
                arrowNode.classList.add('rotate');
                event.target.dataset.expand = 'true';
            } else {
                contentNode.classList.remove('animation');
                arrowNode.classList.remove('rotate');
                event.target.dataset.expand = 'false';
            }
        });
    });
};

const btnClickHandler = () => {
    const publicBtnEle = document.querySelector('#modal-public-btn');
    const unPublicBtnEle = document.querySelector('#modal-un-public-btn');

    publicBtnEle.addEventListener('click', async () => {
        const publicBtnEle = Array.from(document.querySelectorAll('input[name="is-public"]'));
        const [publicIds, unPublicIds] = publicBtnEle.reduce(
            ([publicList, unPublicList], btn) => {
                const questionId = btn.dataset.questionId;

                if (btn.checked) {
                    publicList.push(questionId);
                } else {
                    unPublicList.push(questionId);
                }

                return [publicList, unPublicList];
            },
            [[], []]
        );

        try {
            const response = await instance.patch('/interview/ispublic', JSON.stringify({
                isShareIds: publicIds,
                isCloseIds: unPublicIds
            }));

            if (response.status === 204) {
                alert('공개 여부 변경에 성공했습니다.');
                window.location.reload();
            } else {
                alert('공개 여부 변경에 실패했습니다.');
            }
        } catch (error) {
            alert('공개 여부 변경에 실패했습니다.');
        }
    });

    unPublicBtnEle.addEventListener('click', async () => {
        const publicBtnEle = Array.from(document.querySelectorAll('input[name="is-public"]'));
        const unPublicIds = publicBtnEle.map(btn => btn.dataset.questionId);

        try {
            const response = await instance.patch('/interview/ispublic', JSON.stringify({
                isShareIds: [],
                isCloseIds: unPublicIds
            }));

            if (response.status === 204) {
                alert('공개 여부 변경에 성공했습니다.');
                window.location.reload();
            } else {
                alert('공개 여부 변경에 실패했습니다.');
            }
        } catch (error) {
            alert('공개 여부 변경에 실패했습니다.');
        }
    });
};

window.addEventListener('load', () => {
    publicModalClickHandler();
    btnClickHandler();
});