import os
import tempfile

from flask import Blueprint
from flask import request

from agents import self_introduction, interview_outline, generate_questions, qa_diagnose
from entity.state import State
from tools.api_response import api_response
from tools.pdf_utils import read_pdf_text

interview_bp = Blueprint('interview', __name__, url_prefix='/interview')


@interview_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查接口"""
    return api_response(200, "服务正常", {"status": "healthy"})


@interview_bp.route('/generate_self_introduction', methods=['POST'])
def generate_self_introduction():
    """
    生成自我介绍
    请求参数:
    - pdf_text: 简历文本内容
    - job_description: 岗位描述
    """
    try:
        data = request.get_json()
        pdf_text = data.get('pdf_text')
        job_description = data.get('job_description', '')

        if not pdf_text:
            return api_response(400, "简历文本不能为空", None)

        state = State(pdf_text=pdf_text, job_description=job_description)
        state = self_introduction.run(state)

        return api_response(200, "成功生成自我介绍", {
            "self_introduction": state.self_introduction.self_introduction
        })
    except Exception as e:
        return api_response(500, f"生成自我介绍失败: {str(e)}", None)


@interview_bp.route('/generate_interview_outline', methods=['POST'])
def generate_interview_outline():
    """
    生成面试大纲
    请求参数:
    - pdf_text: 简历文本内容
    - job_description: 岗位描述
    """
    try:
        data = request.get_json()
        pdf_text = data.get('pdf_text')
        job_description = data.get('job_description', '')

        if not pdf_text:
            return api_response(400, "简历文本不能为空", None)

        state = State(pdf_text=pdf_text, job_description=job_description)
        state = interview_outline.run(state)

        return api_response(200, "成功生成面试大纲", {
            "outline": state.interview_outline.outline
        })
    except Exception as e:
        return api_response(500, f"生成面试大纲失败: {str(e)}", None)


@interview_bp.route('/generate_questions', methods=['POST'])
def generate_questions_api():
    """
    根据面试大纲生成问题列表
    请求参数:
    - interview_outline_item: 面试大纲条目
    """
    try:
        data = request.get_json()
        interview_outline_item = data.get('interview_outline_item')

        if not interview_outline_item:
            return api_response(400, "面试大纲条目不能为空", None)

        state = State(current_outline=interview_outline_item)
        state = generate_questions.run(state)

        return api_response(200, "成功生成问题列表", {
            "questions": state.questions.questions
        })
    except Exception as e:
        return api_response(500, f"生成问题列表失败: {str(e)}", None)


@interview_bp.route('/analyze_answer', methods=['POST'])
def analyze_answer():
    """
    分析用户答案
    请求参数:
    - question: 问题
    - user_answer: 用户答案
    """
    try:
        data = request.get_json()
        question = data.get('question')
        user_answer = data.get('user_answer')

        if not question or not user_answer:
            return api_response(400, "问题和用户答案都不能为空", None)

        state = State(current_question=question, current_user_answer=user_answer)
        state = qa_diagnose.run(state)

        return api_response(200, "成功分析答案", {
            "answer_evaluation": state.current_analysis.answer_evaluation,
            "standard_answer": state.current_analysis.standard_answer
        })
    except Exception as e:
        return api_response(500, f"分析答案失败: {str(e)}", None)


@interview_bp.route('/process_resume', methods=['POST'])
def process_resume():
    """
    处理上传的PDF简历文件，提取文本内容
    """
    try:
        if 'file' not in request.files:
            return api_response(400, "没有上传文件", None)

        file = request.files['file']
        if file.filename == '':
            return api_response(400, "文件名不能为空", None)

        # 保存临时文件
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            file.save(tmp_file.name)
            tmp_file_path = tmp_file.name

        try:
            # 提取PDF文本
            text = read_pdf_text(tmp_file_path)
            return api_response(200, "成功解析PDF文件", {"pdf_text": text})
        finally:
            # 删除临时文件
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    except Exception as e:
        return api_response(500, f"处理简历失败: {str(e)}", None)
