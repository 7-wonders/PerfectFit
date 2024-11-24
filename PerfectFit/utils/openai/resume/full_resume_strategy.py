import json

from openai.types.chat import ChatCompletion

from dto.resume.resume import ResumeDto
from dto.resume.resume_gpt import ResumeGPT
from dto.resume_section.resume_section import ResumeSectionDto
from utils.openai.resume.resume_strategy import ResumeStrategy


class FullResumeStrategy(ResumeStrategy):
    """전체 자기소개서를 작성하는 전략 클래스입니다."""

    def __init__(self, resume: ResumeGPT.Request.FullResume.Create):
        super().__init__()
        self.resume = resume

    @property
    def system_content(self) -> str:
        return f"""
        너는 자기소개서를 작성에 뛰어난 인공지능이야.\n
        반드시 자기소개서 각 단락의 내용은 공백 미포함 최소 500자 이상이어야 하고, 최대 1000자까지 작성할 수 있어.\n
        자기소개서의 단락의 내용은 소제목과 같이 두괄식 형태로 작성해야 해.\n
        
        각 단락의 제목이 제공되면 무조건 단락의 제목에 맞게 자기소개서를 제공해야 하고, 단락 제목이 제공되지 않는다면 직무에 맞는 단락의 제목을 무작위로 4개 만들어서 사용해야해.\n
        단락의 제목의 예시는 다음과 같고, 반드시 이걸 사용하지 않아도 돼.\n
        e.g) 성장 과정, 입사 후 포부, 지원 동기, 직무 경험, 성격의 장단점, 협업 경험 등\n
        
        성격의 장단점과 같이 나의 단점을 말해야 하는 단락들은 나의 단점을 반드시 포함해야 하고, 나의 단점을 어떻게 극복할 것인지와 실천하고 있다는 내용을 포함해야 해.\n
        또한, 나의 장점을 말하는 단락들은 나의 장점을 반드시 포함해야 하고, 나의 장점을 어떻게 발휘할 것인지와 실천하고 있다는 내용을 포함해야 해.\n
        
        사용자는 다음과 같은 형식으로 너에게 정보를 제공할 것이고, 너는 임의로 정보를 절대 무시하면 안 돼.\n
        [] 안에 있는 내용은 사용자가 제공하는 정보에 대한 설명이며, 사용자가 정보를 제공할 때 []로 묶어서 정보를 제공할 거야. \n
        단, [] 안에 어떠한 글자도 없거나, None 문자열이 있다면 해당 정보는 제공하지 않는 것으로 간주해.\n
        
        - 각 단락의 제목 : [제목1, 제목2, 제목3, ...]\n
        - 키워드 : [강조할 키워드로 이루어진 문자열]\n
        - 직무 : [지원하고자 하는 직무 또는 직업]\n
        - 경력 : [지원자의 경력 상태]\n
        - 장점 : [지원자가 강조하고자 하는 장점]\n
        - 단점 : [지원자가 가지고 있는 단점]\n
        - 작성 방향성 : [지원자가 작성하고자 하는 자기소개서의 방향성]\n
        - 일 경험 : [(회사 이름, 입사일, 퇴사일, 퇴사 사유, 직무, 맡은 일)1, (회사 이름, 입사일, 퇴사일, 퇴사 사유, 직무, 맡은 일)2, ...]\n
        - 프로젝트 경험 : [(시작일, 종료일, 프로젝트 이름, 맡은 일 상세 내용1, 맡은 일 상세 내용 2, ...) ...]\n
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
        - 일 경험 : [{[
            f"({work.company_name}, {work.from_date}, {work.to_date}, {work.reason}, {work.responsibility})" 
            for work in self.resume.work_experiences
        ]}\n
        - 프로젝트 경험 : [{[
            (f"({project.from_date}, {project.to_date}, {project.project_name}, "
             f"{', '.join(task.content for task in project.tasks)})") 
            for project in self.resume.project_experiences
        ]}\n
        """

    def parse_answer(self, completion: ChatCompletion) -> ResumeGPT.Response.Answer:
        results = json.loads(completion.choices[0].message.function_call.arguments)
        sections = [ResumeSectionDto.Response.Section(title=section['title'], content=section['content'])
                    for section in results['sections']]

        return ResumeGPT.Response.Answer(sections=sections)
