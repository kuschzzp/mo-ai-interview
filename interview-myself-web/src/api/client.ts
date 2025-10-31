// 通过 Vite 代理转发到后端，避免 CORS
const BASE_URL = '/api';

export type ApiResponse<T> = {
    code: number;
    data: T;
    message: string;
};

async function handleJson<T>(res: Response): Promise<ApiResponse<T>> {
    const json = await res.json();
    if (!res.ok || json.code !== 200) {
        throw new Error(json.message || `请求失败(${res.status})`);
    }
    return json as ApiResponse<T>;
}

export async function processResume(file: File): Promise<{ pdf_text: string }> {
    const form = new FormData();
    form.append('file', file);
    const res = await fetch(`${BASE_URL}/interview/process_resume`, {
        method: 'POST',
        body: form,
    });
    const json = await handleJson<{ pdf_text: string }>(res);
    return json.data;
}

export async function generateSelfIntroduction(payload: { job_description: string; pdf_text: string }): Promise<{
    self_introduction: string
}> {
    const res = await fetch(`${BASE_URL}/interview/generate_self_introduction`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
    });
    const json = await handleJson<{ self_introduction: string }>(res);
    return json.data;
}

export async function generateInterviewOutline(payload: { job_description: string; pdf_text: string }): Promise<{
    outline: string[]
}> {
    const res = await fetch(`${BASE_URL}/interview/generate_interview_outline`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
    });
    const json = await handleJson<{ outline: string[] }>(res);
    return json.data;
}

export async function generateQuestions(payload: { interview_outline_item: string }): Promise<{ questions: string[] }> {
    const res = await fetch(`${BASE_URL}/interview/generate_questions`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
    });
    const json = await handleJson<{ questions: string[] }>(res);
    return json.data;
}

export async function analyzeAnswer(payload: { question: string; user_answer: string }): Promise<{
    answer_evaluation: string;
    standard_answer?: string
}> {
    const res = await fetch(`${BASE_URL}/interview/analyze_answer`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload),
    });
    const json = await handleJson<{ answer_evaluation: string; standard_answer?: string }>(res);
    return json.data;
}

// ---- 流式SSE工具（兼容path风格） ----
type SSEHandler = {
  onDelta?: (text: string) => void;
  onFinal?: (payload: any) => void;
  onError?: (err: string) => void;
  onEnd?: () => void;
};

async function fetchWithSSEStream(
  path: string,
  body: any,
  handler: SSEHandler
) {
  const resp = await fetch(`${BASE_URL}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!resp.body) {
    handler.onError?.('未获取到流式响应体');
    handler.onEnd?.();
    return;
  }
  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';
  let done = false;
  while (!done) {
    const { value, done: rDone } = await reader.read();
    if (value) {
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split(/\r?\n/);
      buffer = lines.pop() ?? '';
      for (const line of lines) {
        const prefix = 'data: ';
        if (line.startsWith(prefix)) {
          try {
            const { type, content } = JSON.parse(line.substring(prefix.length));
            if (type === 'delta') {
              handler.onDelta?.(content.delta ?? '');
            } else if (type === 'final') {
              let payload;
              try {
                payload = JSON.parse(content);
              } catch (e) { payload = content; }
              handler.onFinal?.(payload);
            } else if (type === 'end') {
              handler.onEnd?.();
            } else if (type === 'error') {
              handler.onError?.(content);
              handler.onEnd?.();
            }
          } catch (e) {
            handler.onError?.('解析流事件失败: ' + (e instanceof Error ? e.message : '未知错误'));
          }
        }
      }
    }
    done = rDone;
  }
  handler.onEnd?.();
}

// ---- 流接口实现，直接复用原有path，仅增加_stream ----
export function generateSelfIntroductionStream(
  payload: { job_description: string; pdf_text: string },
  handler: SSEHandler
) {
  return fetchWithSSEStream('/interview/generate_self_introduction_stream', payload, handler);
}

export function generateInterviewOutlineStream(
  payload: { job_description: string; pdf_text: string },
  handler: SSEHandler
) {
  return fetchWithSSEStream('/interview/generate_interview_outline_stream', payload, handler);
}

export function generateQuestionsStream(
  payload: { interview_outline_item: string },
  handler: SSEHandler
) {
  return fetchWithSSEStream('/interview/generate_questions_stream', payload, handler);
}

export function analyzeAnswerStream(
  payload: { question: string; user_answer: string },
  handler: SSEHandler
) {
  return fetchWithSSEStream('/interview/analyze_answer_stream', payload, handler);
}


