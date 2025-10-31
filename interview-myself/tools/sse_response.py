import json
from flask import Response

class SSEResponse:
    """
    简化版 SSE 响应类：所有信息统一放在 data: 里
    每条消息统一 JSON 格式：
    {
        "type": "delta" | "error" | "end" | "final",
        "content": "消息内容",
        "id": 可选消息ID
    }
    用法：
        yield sse.send("这是内容")
        yield sse.error("出错了")
        yield sse.end("任务完成")
    """

    def __init__(self):
        self._closed = False

    def send(self, content, msg_type="delta", id=None):
        """发送普通消息"""
        if self._closed:
            return ""
        data = {"type": msg_type, "content": content}
        if id is not None:
            data["id"] = id
        return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    def error(self, content, id=None):
        """发送错误消息"""
        data = {"type": "error", "content": content}
        if id is not None:
            data["id"] = id
        return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    def end(self, content="结束", id=None):
        """发送结束消息"""
        self._closed = True
        data = {"type": "end", "content": content}
        if id is not None:
            data["id"] = id
        return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    def final(self, content, id=None):
        """发送最终完整结果"""
        data = {"type": "final", "content": content}
        if id is not None:
            data["id"] = id
        return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    @staticmethod
    def stream(generator_func):
        """快速生成 Flask Response"""
        return Response(generator_func(), mimetype="text/event-stream")
