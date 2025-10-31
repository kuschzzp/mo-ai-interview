import os

from langchain_core.messages import AIMessageChunk
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate

from constants.prompts import DIAGNOSE_PROMPT
from entity.state import State, AnswerAnalysis
from llm.llm_provider import get_tongyi_langchain_llm
from log.log_config import init_logger

logger = init_logger(__name__)


def build_prompt(parser):
    template = ChatPromptTemplate(
        messages=[
            ("system", DIAGNOSE_PROMPT),
            # 这里的第二个system 是为了让大模型输出的内容按照 pydantic 模型格式输出结果方便后续处理
            ("system", "请按照以下格式输出结果:\n{format_instructions}"),
            ("human",
             """
             原始问题：
             {question}
             用户答案： 
             {user_answer}
             """)
        ],
        # 必须用户填充的消息
        input_variables=["question", "user_answer"],
        # 预先填充好的字段
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    return template


def run(state: State) -> State:
    if not state.current_question or not state.current_user_answer:
        raise Exception("不存在问题、或者用户没有提供回答")

    logger.info("开始执行【问答分析诊断】")

    parser = PydanticOutputParser(pydantic_object=AnswerAnalysis)
    chain = build_prompt(parser) | get_tongyi_langchain_llm(os.getenv("QA_DIAGNOSE_MODEL_NAME"))

    full_response = ""
    for chunk in chain.stream({"question": state.current_question, "user_answer": state.current_user_answer}):
        if isinstance(chunk, AIMessageChunk):
            content = chunk.content
            full_response += content
            print(content, end="", flush=True)
    state.current_analysis = parser.parse(full_response)
    logger.info(state.current_analysis)
    return state


def run_stream(state: State):
    if not state.current_question or not state.current_user_answer:
        raise Exception("不存在问题、或者用户没有提供回答")

    logger.info("开始执行【问答分析诊断】")

    parser = PydanticOutputParser(pydantic_object=AnswerAnalysis)
    chain = build_prompt(parser) | get_tongyi_langchain_llm(os.getenv("QA_DIAGNOSE_MODEL_NAME"))

    full_response = ""
    for chunk in chain.stream({"question": state.current_question, "user_answer": state.current_user_answer}):
        if isinstance(chunk, AIMessageChunk):
            content = chunk.content
            full_response += content
            yield content
    state.current_analysis = parser.parse(full_response)
    logger.info(state.current_analysis)
    yield state


if __name__ == '__main__':
    # run(State(
    #     current_question="在 Java 中，synchronized 关键字底层是如何实现的？它在 JDK 1.6 之后做了哪些优化？",
    #     current_user_answer="这个我忘记了，我记得是锁"
    # ))
    from dotenv import load_dotenv

    load_dotenv()

    for chunk in run_stream(State(
            current_question="在 Java 中，synchronized 关键字底层是如何实现的？它在 JDK 1.6 之后做了哪些优化？",
            current_user_answer="这个我忘记了，我记得是锁"
    )):
        if isinstance(chunk, str):
            # print(chunk, end="", flush=True)
            print(1)
        elif isinstance(chunk, State):
            print(2)
            print(chunk.current_question)
        else:
            print("啥也不是")
