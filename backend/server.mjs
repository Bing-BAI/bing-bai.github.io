import http from 'node:http';
import { pathToFileURL } from 'node:url';

const ORIGIN = 'https://bing-bai.github.io';
const SOURCE_MAP = {
  '01-profile': {title: '个人背景与能力', path: '/about.html'},
  '02-visual-product-search': {title: '工业零件识别与检索', path: '/projects/visual-product-search.html'},
  '03-visual-inspection': {title: '铁路设备异常检测', path: '/projects/visual-inspection.html'},
  '04-customer-delivery': {title: '制造业系统交付', path: '/projects/customer-delivery.html'},
  '05-boiler-extraction': {title: '设备铭牌信息抽取', path: '/projects/boiler-extraction.html'},
  '06-driving-diagnosis': {title: '双摄驾驶诊断', path: '/projects/driving-diagnosis.html'},
  '07-edge-localization': {title: '视觉定位模型量化', path: '/projects/edge-localization.html'},
  '08-shovel-edge-ai': {title: '工程机械活动识别', path: '/projects/shovel-edge-ai.html'},
  '09-sensor-model-compression': {title: '传感器选择与模型压缩', path: '/projects/sensor-model-compression.html'},
};
const NO_EVIDENCE = '目前公开资料中没有足够的可引用依据来回答这个问题。你可以查看项目和个人介绍，或换一个关于技术经历的问题。';

export function normalizeAnswer(payload) {
  const output = payload?.output;
  if (!output || typeof output.text !== 'string' || !output.text.trim() || output.text.length > 20000) {
    throw new Error('Invalid upstream response');
  }
  const refs = Array.isArray(output.doc_references) ? output.doc_references : [];
  const sources = [];
  let unknownSource = false;
  for (const ref of refs) {
    const name = typeof ref?.doc_name === 'string' ? ref.doc_name.replace(/\.(md|txt)$/i, '') : '';
    const entry = SOURCE_MAP[name];
    if (!entry) { unknownSource = true; continue; }
    const id = String(ref.index_id ?? '');
    if (!/^\d{1,3}$/.test(id)) { unknownSource = true; continue; }
    if (!sources.some(s => s.id === id && s.url === ORIGIN + entry.path)) {
      sources.push({id, title: entry.title, url: ORIGIN + entry.path});
    }
  }
  // No raw document links, chunks, file IDs, or internal thoughts reach the browser.
  if (unknownSource || sources.length === 0) return {answer: NO_EVIDENCE, sources: []};
  return {answer: output.text.replace(/<ref>\s*(\[\d+\])\s*<\/ref>/g, '$1'), sources};
}

export function createApp({env = process.env, fetchImpl = fetch, now = Date.now} = {}) {
  const appId = env.BAILIAN_APP_ID || '';
  const apiKey = env.DASHSCOPE_API_KEY || '';
  const origin = env.ALLOWED_ORIGIN || ORIGIN;
  if (origin !== ORIGIN && !/^http:\/\/(localhost|127\.0\.0\.1):\d+$/.test(origin)) {
    throw new Error('ALLOWED_ORIGIN must be the blog or a loopback preview origin');
  }
  const ready = env.AGENT_ENABLED === 'true' && env.KNOWLEDGE_APPROVED === 'true'
    && /^[a-zA-Z0-9_-]{8,128}$/.test(appId) && Boolean(apiKey);
  let active = 0, windowStart = 0, requests = 0;
  const send = (res, status, data, cors = false) => {
    res.writeHead(status, {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff',
      'Vary': 'Origin',
      ...(cors ? {'Access-Control-Allow-Origin': origin} : {}),
    });
    res.end(JSON.stringify(data));
  };
  const handler = async (req, res) => {
    const cors = req.headers.origin === origin;
    if (req.url === '/health' && req.method === 'GET') {
      return send(res, 200, {ready}, cors);
    }
    if (req.url !== '/api/chat') return send(res, 404, {error:'接口不存在。'}, cors);
    if (!cors) return send(res, 403, {error:'请求来源不受支持。'});
    if (req.method === 'OPTIONS') {
      res.writeHead(204, {'Access-Control-Allow-Origin':origin,'Access-Control-Allow-Methods':'POST, OPTIONS',
        'Access-Control-Allow-Headers':'Content-Type','Vary':'Origin','Access-Control-Max-Age':'600'});
      return res.end();
    }
    if (req.method !== 'POST') return send(res,405,{error:'请使用 POST 请求。'},true);
    if (!ready) return send(res,503,{error:'知识助手尚未启用，请稍后再试。'},true);
    if ((req.headers['content-type'] || '').split(';')[0].trim().toLowerCase() !== 'application/json') {
      return send(res,415,{error:'请发送 JSON 格式的问题。'},true);
    }
    // Conservative per-process global cap. FC/edge quotas must enforce limits across instances.
    if (now() - windowStart >= 60000) { windowStart = now(); requests = 0; }
    if (requests >= 20 || active >= 2) return send(res,429,{error:'提问较多，请稍后再试。'},true);
    requests++; active++;
    try {
      const chunks = [];
      let size = 0;
      for await (const chunk of req) {
        size += chunk.length;
        if (size > 8192) return send(res,413,{error:'问题内容过长。'},true);
        chunks.push(chunk);
      }
      const body = Buffer.concat(chunks).toString('utf8');
      let data;
      try { data = JSON.parse(body); } catch { return send(res,400,{error:'请求格式不正确。'},true); }
      if (!data || Array.isArray(data) || typeof data !== 'object' ||
          Object.keys(data).some(key => key !== 'question') || typeof data.question !== 'string' ||
          !data.question.trim() || data.question.length > 1000) {
        return send(res,400,{error:'请提交 1–1000 字的问题。'},true);
      }
      const result = await fetchImpl(`https://dashscope.aliyuncs.com/api/v1/apps/${appId}/completion`, {
        method:'POST', redirect:'error',
        headers:{'Authorization':`Bearer ${apiKey}`,'Content-Type':'application/json'},
        body:JSON.stringify({input:{prompt:data.question.trim()},parameters:{has_thoughts:false},debug:{}}),
        signal:AbortSignal.timeout(45000),
      });
      if (!result.ok) return send(res,result.status === 429 ? 429 : 502,{error:'知识服务暂时不可用，请稍后重试。'},true);
      const answer = normalizeAnswer(await result.json());
      return send(res,200,answer,true);
    } catch {
      // Never return upstream error details or log the user's question / API key.
      return send(res,502,{error:'回答暂时未能完成，请稍后重试。'},true);
    } finally { active--; }
  };
  const server = http.createServer((req,res) => { void handler(req,res); });
  server.requestTimeout = 60000;
  server.headersTimeout = 15000;
  server.keepAliveTimeout = 65000;
  return server;
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const port = Number(process.env.PORT || 9000);
  const server = createApp();
  server.listen(port, '0.0.0.0', () => console.log(`Agent API listening on port ${port}`));
}
