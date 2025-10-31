import os

from langchain_core.messages import AIMessageChunk
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from constants.prompts import SELF_INTRODUCTION_PROMPT
from entity.state import State, SelfIntroduction
from llm.llm_provider import get_tongyi_langchain_llm
from log.log_config import init_logger

logger = init_logger(__name__)


def build_prompt(parser):
    template = ChatPromptTemplate(
        messages=[
            ("system", SELF_INTRODUCTION_PROMPT),
            # 这里的第二个system 是为了让大模型输出的内容按照 pydantic 模型格式输出结果方便后续处理
            ("system", "请按照以下格式输出结果:\n{format_instructions}"),
            ("human",
             """
             # 个人简历信息
             {user_detail}
             #岗位需求描述: 
             {job_requirements}
             """)
        ],
        # 必须用户填充的消息
        input_variables=["user_detail", "job_requirements"],
        # 预先填充好的字段
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    return template


def run(state: State) -> State:
    logger.info("开始执行【自我介绍】生成任务")
    if not state.pdf_text:
        raise Exception("简历文本没有内容！")

    parser = PydanticOutputParser(pydantic_object=SelfIntroduction)
    chain = build_prompt(parser) | get_tongyi_langchain_llm(os.getenv("SELF_INTRODUCTION_MODEL_NAME"))
    full_response = ""
    for chunk in chain.stream({"user_detail": state.pdf_text, "job_requirements": state.job_description}):
        if isinstance(chunk, AIMessageChunk):
            content = chunk.content
            full_response += content
            print(content, end="", flush=True)
    state.self_introduction = parser.parse(full_response)
    logger.info(state.self_introduction)
    return state


def run_stream(state: State):
    logger.info("开始执行【自我介绍】生成任务")
    if not state.pdf_text:
        raise Exception("简历文本没有内容！")

    parser = PydanticOutputParser(pydantic_object=SelfIntroduction)
    chain = build_prompt(parser) | get_tongyi_langchain_llm(os.getenv("SELF_INTRODUCTION_MODEL_NAME"))
    full_response = ""
    for chunk in chain.stream({"user_detail": state.pdf_text, "job_requirements": state.job_description}):
        if isinstance(chunk, AIMessageChunk):
            content = chunk.content
            full_response += content
            yield content
    state.self_introduction = parser.parse(full_response)
    logger.info(state.self_introduction)
    yield state


if __name__ == '__main__':
    from tools.pdf_utils import read_pdf_text
    from dotenv import load_dotenv

    load_dotenv()
    pdf_text = read_pdf_text(pdf_path="/Users/kusch/Desktop/sundries/简历/0702.pdf")
    job_des = """
**【岗位职责】** 1. 负责基于 Dify、Coze、Spring AI 等平台/框架的智能体应用设计与开发； 2. 参与公司智能体相关产品的架构设计、核心功能开发与性能优化； 3. 结合业务需求，设计和实现智能体的多模态交互、任务编排、知识库调用等能力； 4. 构建并优化智能体与后端系统的集成，包括数据库、缓存、消息队列等中间件； 5. 跟踪前沿AI Agent技术，探索创新应用场景，推动智能体技术在公司产品中的落地。 **【任职要求】** 1. 计算机、软件工程、人工智能相关专业本科及以上学历，具备扎实的编程基础，两年以上工作经验； 2. 精通 Java，熟悉 Spring、Spring Boot 框架，具备良好的面向对象设计与编码能力； 3. 熟悉 MySQL、Redis、Kafka 等主流数据库和中间件，具备高并发、高可用系统设计经验者优先； 4. 熟悉 Dify、Coze、Spring AI 等智能体开发框架/平台，有实际项目经验者优先； 5. 具备良好的系统分析与问题解决能力，能够独立完成模块设计与实现； 6. 热衷于前沿AI技术，具备快速学习能力与良好的团队协作精神。 **【加分项】** 1. 有 RAG、LangChain、LLM 应用开发经验； 2. 熟悉微服务架构、容器化部署（Docker、K8s）； 3. 参与过智能客服、AI助手、企业级智能体系统研发项目。  
    """
    # run(State(pdf_text=None))
    # run(State(pdf_text=pdf_text))
    # run(State(pdf_text=pdf_text, job_description=job_des))

    for chunk in run_stream(State(pdf_text=pdf_text, job_description=job_des)):
        if isinstance(chunk, str):
            print(chunk, end="", flush=True)
            # print(1)
        elif isinstance(chunk, State):
            print(2)
            print(chunk.pdf_text)
        else:
            print("啥也不是")
