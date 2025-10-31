from flask import Blueprint
from flask import request

from agents import self_introduction, interview_outline, generate_questions, qa_diagnose
from entity.state import State, SelfIntroduction, InterviewOutline, Questions, AnswerAnalysis
from tools.sse_response import SSEResponse

interview_stream_bp = Blueprint('interview_stream', __name__, url_prefix='/interview')


@interview_stream_bp.route('/generate_self_introduction_stream', methods=['POST'])
def generate_self_introduction_stream():
    """
    流式生成自我介绍
    请求参数:
    - pdf_text: 简历文本内容
    - job_description: 岗位描述
    """
    pdf_text = request.json.get("pdf_text", "")
    job_description = request.json.get("job_description", "")

    def generate():
        sse = SSEResponse()
        try:
            state = State(pdf_text=pdf_text, job_description=job_description)
            full_response = ""
            for chunk in self_introduction.run_stream(state):
                if isinstance(chunk, str):
                    full_response += chunk
                    yield sse.send({"delta": full_response})
                elif isinstance(chunk, State):
                    yield sse.final(
                        SelfIntroduction(self_introduction=chunk.self_introduction.self_introduction).__str__())
                else:
                    yield sse.error(str(chunk))
        except Exception as e:
            yield sse.error(str(e))
        finally:
            yield sse.end("end")

    return SSEResponse.stream(generate)


@interview_stream_bp.route('/generate_interview_outline_stream', methods=['POST'])
def generate_interview_outline_stream():
    """
    流式生成面试大纲
    请求参数:
    - pdf_text: 简历文本内容
    - job_description: 岗位描述
    """
    pdf_text = request.json.get("pdf_text", "")
    job_description = request.json.get("job_description", "")

    def generate():
        sse = SSEResponse()
        try:
            state = State(pdf_text=pdf_text, job_description=job_description)
            full_response = ""
            for chunk in interview_outline.run_stream(state):
                if isinstance(chunk, str):
                    full_response += chunk
                    yield sse.send({"delta": full_response})
                elif isinstance(chunk, State):
                    yield sse.final(
                        InterviewOutline(outline=chunk.interview_outline.outline).__str__()
                    )
                else:
                    yield sse.error(str(chunk))
        except Exception as e:
            yield sse.error(str(e))
        finally:
            yield sse.end("end")

    return SSEResponse.stream(generate)


@interview_stream_bp.route('/generate_questions_stream', methods=['POST'])
def generate_questions_stream():
    """
    流式生成问题列表
    请求参数:
    - interview_outline_item: 面试大纲条目
    """
    interview_outline_item = request.json.get('interview_outline_item')

    def generate():
        sse = SSEResponse()
        try:
            if not interview_outline_item:
                yield sse.error("面试大纲条目不能为空")
                return

            state = State(current_outline=interview_outline_item)
            full_response = ""
            for chunk in generate_questions.run_stream(state):
                if isinstance(chunk, str):
                    full_response += chunk
                    yield sse.send({"delta": full_response})
                elif isinstance(chunk, State):
                    yield sse.final(
                        Questions(questions=chunk.questions.questions).__str__()
                    )
                else:
                    yield sse.error(str(chunk))
        except Exception as e:
            yield sse.error(str(e))
        finally:
            yield sse.end("end")

    return SSEResponse.stream(generate)


@interview_stream_bp.route('/analyze_answer_stream', methods=['POST'])
def analyze_answer_stream():
    """
    流式分析用户答案
    请求参数:
    - question: 问题
    - user_answer: 用户答案
    """
    question = request.json.get('question')
    user_answer = request.json.get('user_answer')

    def generate():
        sse = SSEResponse()
        try:
            if not question or not user_answer:
                yield sse.error("问题和用户答案都不能为空")
                return

            state = State(current_question=question, current_user_answer=user_answer)
            full_response = ""
            for chunk in qa_diagnose.run_stream(state):
                if isinstance(chunk, str):
                    full_response += chunk
                    yield sse.send({"delta": full_response})
                elif isinstance(chunk, State):
                    yield sse.final(
                        AnswerAnalysis(answer_evaluation=chunk.current_analysis.answer_evaluation,
                                       standard_answer=chunk.current_analysis.standard_answer).__str__()
                    )
                else:
                    yield sse.error(str(chunk))
        except Exception as e:
            yield sse.error(str(e))
        finally:
            yield sse.end("end")

    return SSEResponse.stream(generate)
