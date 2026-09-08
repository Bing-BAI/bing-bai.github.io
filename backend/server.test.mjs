import test from 'node:test';
import assert from 'node:assert/strict';
import {createApp, normalizeAnswer} from './server.mjs';
const origin = 'https://bing-bai.github.io';
const env = {DASHSCOPE_API_KEY:'test-secret',BAILIAN_APP_ID:'test-app-123',AGENT_ENABLED:'true',KNOWLEDGE_APPROVED:'true'};
async function fixture(t, options = {}) {
  const server = createApp({env, ...options});
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  t.after(() => new Promise(resolve => {server.closeAllConnections(); server.close(resolve);}));
  const base = `http://127.0.0.1:${server.address().port}`;
  return (body, extra = {}) => fetch(base + '/api/chat', {method:'POST',headers:{Origin:origin,'Content-Type':'application/json',...extra.headers},body:JSON.stringify(body)});
}
test('normalizes approved citations without exposing document chunks, internal URLs, or thoughts', () => {
  const answer = normalizeAnswer({output:{text:'参与过部署<ref>[1]</ref>。',thoughts:['private'],doc_references:[{index_id:'1',doc_name:'04-customer-delivery.md',text:'private chunk',doc_url:'https://private.example'}]}});
  assert.equal(answer.answer,'参与过部署[1]。');
  assert.equal(answer.sources[0].url,origin+'/projects/customer-delivery.html');
  assert.ok(!JSON.stringify(answer).includes('private'));
});
test('rejects unsupported or missing evidence', () => {
  for (const refs of [[],[{index_id:'1',doc_name:'private-resume.md'}]]) {
    const answer=normalizeAnswer({output:{text:'Unsupported fact',doc_references:refs}});
    assert.ok(!answer.answer.includes('Unsupported')); assert.deepEqual(answer.sources,[]);
  }
});
test('sends only question to Beijing app with server-owned key and app ID', async t => {
  let received;
  const call = await fixture(t,{fetchImpl:async (url,options) => {
    received={url,options};
    return {ok:true,json:async () => ({output:{text:'视觉工程[1]',doc_references:[{index_id:'1',doc_name:'01-profile'}]}})};
  }});
  const response = await call({question:'  擅长什么？  '});
  assert.equal(response.status,200);
  assert.equal(received.url,'https://dashscope.aliyuncs.com/api/v1/apps/test-app-123/completion');
  assert.equal(received.options.headers.Authorization,'Bearer test-secret');
  assert.deepEqual(JSON.parse(received.options.body).input,{prompt:'擅长什么？'});
  assert.equal(response.headers.get('access-control-allow-origin'),origin);
  assert.ok(!(await response.text()).includes('test-secret'));
});
test('blocks caller overrides, invalid inputs, and foreign origins before provider call', async t => {
  let calls=0;
  const call=await fixture(t,{fetchImpl:async()=>{calls++;throw new Error('must not call');}});
  for (const body of [{question:''},{question:'a'.repeat(1001)},{question:'hello',app_id:'private'},{question:'hello',session_id:'other-user'},null]) {
    assert.equal((await call(body)).status,400);
  }
  assert.equal((await call({question:'hello'},{headers:{Origin:'https://other.example'}})).status,403);
  assert.equal(calls,0);
});
test('fails closed without knowledge approval and hides upstream failures', async t => {
  const off=await fixture(t,{env:{...env,KNOWLEDGE_APPROVED:'false'}});
  assert.equal((await off({question:'hello'})).status,503);
  const broken=await fixture(t,{fetchImpl:async()=>{throw new Error('test-secret provider trace');}});
  const response=await broken({question:'hello'});
  assert.equal(response.status,502); assert.ok(!(await response.text()).includes('test-secret'));
});
test('global rate cap prevents further billable calls', async t => {
  let count=0;
  const call=await fixture(t,{now:()=>100000,fetchImpl:async()=>{count++; return {ok:true,json:async()=>({output:{text:'no refs'}})};}});
  for (let i=0;i<20;i++) assert.equal((await call({question:'hello'})).status,200);
  assert.equal((await call({question:'hello'})).status,429);
  assert.equal(count,20);
});
