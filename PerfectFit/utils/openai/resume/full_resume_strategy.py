import json

from openai.types.chat import ChatCompletion

from utils.openai.resume.resume_strategy import ResumeStrategy, CreateResume, Resume


class FullResumeStrategy(ResumeStrategy):
    """전체 자기소개서를 작성하는 전략 클래스입니다."""

    def __init__(self, resume: CreateResume):
        super().__init__()
        self.resume = resume

    @property
    def system_content(self) -> str:
        return f"""
        너는 자기소개서를 작성에 뛰어난 인공지능이야.\n
        자기소개서 각 단락의 모든 글자는 최소 500자 이상이어야 하고, 최대 1000자까지 작성할 수 있어.\n
        
        각 단락의 제목이 제공되면 무조건 단락의 제목에 맞게 자기소개서를 제공해야 하고, 단락 제목이 제공되지 않는다면 무작위로 4개의 단락을 지정 후 작성하면 돼.\n
        단락의 제목의 예시는 다음과 같아.\n
        e.g) 성장 과정, 입사 후 포부, 지원 동기, 경력 및 경험 등\n
        
        사용자는 다음과 같은 형식으로 너에게 정보를 제공할 것이고, 너는 임의로 정보를 절대 무시하면 안 돼.\n
        [] 안에 있는 내용은 사용자가 제공하는 정보에 대한 설명이며, 사용자가 정보를 제공할 때 []로 묶어서 정보를 제공할 거야. \n
        단, [] 안에 어떠한 글자도 없다면 해당 정보는 제공하지 않는 것으로 간주해.\n
        
        - 각 단락의 제목 : [제목1, 제목2, 제목3, ...]\n
        - 키워드 : [강조할 키워드로 이루어진 문자열]\n
        - 직무 : [지원하고자 하는 직무 또는 직업]\n
        - 경력 : [지원자의 경력 상태]\n
        - 장점 : [지원자가 강조하고자 하는 장점]\n
        - 단점 : [지원자가 가지고 있는 단점]\n
        - 작성 방향성 : [지원자가 작성하고자 하는 자기소개서의 방향성]\n
        - 각 자기 소개서 단락 : [각 자기소개서의 단락]\n
        """

    @property
    def question(self) -> str:
        return f"""
        다음과 같은 정보를 사용하여 자기소개서를 만들어, json 형태로 반환해줘.
        
        - 각 단락의 제목 : [{self.resume.chapter}]\n
        - 키워드 : [{self.resume.keywords}]\n
        - 직무 : [{self.resume.job_name}]\n
        - 경력 : [{self.resume.level}]\n
        - 장점 : [{self.resume.pros}]\n
        - 단점 : [{self.resume.cons}]\n
        - 작성 방향성 : [{self.resume.directional}]\n
        """

    def parse_answer(self, completion: ChatCompletion) -> Resume:
        results = json.loads(completion.choices[0].message.function_call.arguments)
        sections = [Resume.Section(title=section['title'], content=section['content'])
                    for section in results['sections']]

        return Resume(sections=sections)
