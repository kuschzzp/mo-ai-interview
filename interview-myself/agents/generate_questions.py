import os

from langchain_core.messages import AIMessageChunk
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from constants.prompts import GENERATE_QUESTIONS_FROM_OUTLINE_PROMPT
from entity.state import State, Questions
from llm.llm_provider import get_tongyi_langchain_llm
from log.log_config import init_logger

logger = init_logger(__name__)


def build_prompt(parser):
    template = ChatPromptTemplate(
        messages=[
            ("system", GENERATE_QUESTIONS_FROM_OUTLINE_PROMPT),
            # 这里的第二个system 是为了让大模型输出的内容按照 pydantic 模型格式输出结果方便后续处理
            ("system", "请按照以下格式输出结果:\n{format_instructions}"),
            ("human", "本次需要生成问题的大纲信息：{interview_outline_item}")
        ],
        # 必须用户填充的消息
        input_variables=["interview_outline_item"],
        # 预先填充好的字段
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    return template


def run(state: State) -> State:
    if not state.current_outline:
        if not state.interview_outline:
            raise Exception("大纲List没有数据！！")
        state.current_outline = state.interview_outline[0]

    logger.info(f"开始执行【问题列表】生成任务 ==> 本次的大纲是：【{state.current_outline}】")

    parser = PydanticOutputParser(pydantic_object=Questions)
    chain = build_prompt(parser) | get_tongyi_langchain_llm(os.getenv("GENERATE_QUESTIONS_MODEL_NAME"))

    full_response = ""
    for chunk in chain.stream({"interview_outline_item": state.current_outline}):
        if isinstance(chunk, AIMessageChunk):
            content = chunk.content
            full_response += content
            print(content, end="", flush=True)
    state.questions = parser.parse(full_response)
    logger.info(state.questions)
    return state


def run_stream(state: State):
    if not state.current_outline:
        if not state.interview_outline:
            raise Exception("大纲List没有数据！！")
        state.current_outline = state.interview_outline[0]

    logger.info(f"开始执行【问题列表】生成任务 ==> 本次的大纲是：【{state.current_outline}】")

    parser = PydanticOutputParser(pydantic_object=Questions)
    chain = build_prompt(parser) | get_tongyi_langchain_llm(os.getenv("GENERATE_QUESTIONS_MODEL_NAME"))

    full_response = ""
    for chunk in chain.stream({"interview_outline_item": state.current_outline}):
        if isinstance(chunk, AIMessageChunk):
            content = chunk.content
            full_response += content
            yield content
    state.questions = parser.parse(full_response)
    logger.info(state.questions)
    yield state


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()

    # run(State(
    #     current_outline="Java 核心与并发编程能力考察：结合简历中提到的 Java 并发、线程池、Synchronized、CAS、ThreadLocal 等技术点，准备相关原理理解与实战案例，例如在 CRM 系统中使用 CompletableFuture 优化响应时间的具体实现。"))

    for chunk in run_stream(State(
            current_outline="Java 核心与并发编程能力考察：结合简历中提到的 Java 并发、线程池、Synchronized、CAS、ThreadLocal 等技术点，准备相关原理理解与实战案例，例如在 CRM 系统中使用 CompletableFuture 优化响应时间的具体实现。")):
        if isinstance(chunk, str):
            # print(chunk, end="", flush=True)
            print(1)
        elif isinstance(chunk, State):
            print(2)
            print(chunk.current_outline)
        else:
            print("啥也不是")
