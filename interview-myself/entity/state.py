from typing import List, Optional

from pydantic import BaseModel, Field


# ========== 自定义基类：让 str(obj) 返回 JSON ==========
class JsonSerializableModel(BaseModel):
    def __str__(self):
        return self.model_dump_json()

    class Config:
        pass


# ================== 协助大模型输出对象 ========================
class SelfIntroduction(JsonSerializableModel):
    self_introduction: str = Field(description="自我介绍文本")


class InterviewOutline(JsonSerializableModel):
    outline: List[str] = Field(description="面试大纲")


class Questions(JsonSerializableModel):
    questions: List[str] = Field(description="问题")


class AnswerAnalysis(JsonSerializableModel):
    answer_evaluation: str = Field(description="答案评价")
    standard_answer: str = Field(description="标准答案")


# ================== 全局上下文对象 ========================
class State(JsonSerializableModel):
    # PDF 简历文本
    pdf_text: Optional[str] = None
    # 岗位说明
    job_description: Optional[str] = None
    # 自我介绍文本
    self_introduction: Optional[SelfIntroduction] = None
    # 面试大纲
    interview_outline: Optional[InterviewOutline] = None
    # 当前大纲数据
    current_outline: Optional[str] = None
    # 问题列表
    questions: Optional[Questions] = None

    current_question: Optional[str] = None
    current_user_answer: Optional[str] = None
    current_analysis: Optional[AnswerAnalysis] = None
