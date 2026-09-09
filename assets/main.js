const isEnglish = document.documentElement.lang === 'en';
const textFor = (zh, en) => isEnglish ? en : zh;
// Real links also work without JS; preserve the current section when switching.
function syncLanguageLinks() {
  document.querySelectorAll('[data-language]').forEach(link => {
    const url = new URL(link.href);
    url.hash = location.hash;
    link.href = url.href;
  });
}
syncLanguageLinks();
window.addEventListener('hashchange', syncLanguageLinks);

document.querySelectorAll('.filters').forEach(group => {
  group.hidden = false;
  group.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    group.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    document.querySelectorAll('.post-row').forEach(row => {
      row.hidden = button.dataset.filter !== '*' && row.dataset.category !== button.dataset.filter;
      if (!row.hidden) count++;
    });
    document.querySelector('.filter-status').textContent = textFor(`显示 ${count} 篇文章`, `Showing ${count} articles`);
  });
});

const form = document.querySelector('#ask-form');
if (form && form.dataset.api) {
  const endpoint = form.dataset.api;
  const status = document.querySelector('#agent-status');
  const question = document.querySelector('#question');
  const submit = form.querySelector('button');
  const chips = [...document.querySelectorAll('[data-question]')];
  const conversation = document.querySelector('#conversation');
  let ready = false;
  let busy = false;
  function setControls() {
    question.disabled = !ready || busy;
    submit.disabled = !ready || busy;
    chips.forEach(b => b.disabled = !ready || busy);
  }
  function message(who, text, sources = []) {
    const box = document.createElement('div'); box.className = `message ${who}`;
    const label = document.createElement('strong'); label.textContent = who === 'user' ? textFor("你", "You") : textFor("白冰的 Agent", "Bing’s Agent");
    const paragraph = document.createElement('p'); paragraph.textContent = text;
    box.append(label, paragraph);
    const list = document.createElement('ul');
    for (const source of sources) {
      // Render links only to known public pages, never model-supplied HTML or download URLs.
      try {
        const url = new URL(source.url);
        if (url.origin !== 'https://bing-bai.github.io' || !/^\/(about\.html|projects\/[a-z-]+\.html)$/.test(url.pathname)) continue;
        const li = document.createElement('li'); const link = document.createElement('a');
        if (isEnglish) url.pathname = '/en' + url.pathname;
        link.href = url.href; link.textContent = `[${source.id}] ${source.title}`;
        li.append(link); list.append(li);
      } catch { /* Invalid citations are omitted. */ }
    }
    if (list.childElementCount) box.append(list);
    conversation.append(box);
  }
  async function connect() {
    try {
      const health = new URL(endpoint); health.pathname = '/health'; health.search = ''; health.hash = '';
      const response = await fetch(health, {signal:AbortSignal.timeout(10000), credentials:'omit'});
      ready = response.ok && (await response.json()).ready === true;
      status.textContent = ready ? textFor("已连接 · 根据公开资料回答，每次提问独立处理。", "Connected · Answers use public information. Each question is independent.") : textFor("知识助手尚未启用，请稍后再试。", "The assistant is not enabled yet. Please try again later.");
    } catch { status.textContent = textFor("暂时无法连接知识助手。请稍后刷新，或先浏览项目介绍。", "Unable to connect. Try refreshing later, or explore the projects."); }
    setControls();
  }
  chips.forEach(button => button.addEventListener('click', () => {
    question.value = button.dataset.question; question.focus();
  }));
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (!ready || busy || !question.value.trim()) return;
    const text = question.value.trim();
    busy = true; setControls(); message('user', text);
    status.textContent = textFor("正在检索资料并生成回答…", "Retrieving sources and preparing an answer…");
    try {
      const response = await fetch(endpoint, {method:'POST',credentials:'omit',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({question:text}),signal:AbortSignal.timeout(55000)});
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || textFor("回答暂时不可用，请稍后重试。", "The answer is temporarily unavailable. Please try again later."));
      if (typeof data.answer !== 'string') throw new Error(textFor("回答格式异常，请稍后重试。", "Unexpected answer format. Please try again later."));
      message('assistant',data.answer,Array.isArray(data.sources) ? data.sources : []);
      question.value = '';
      status.textContent = textFor("回答完成。你可以继续提出一个独立问题。", "Answer complete. You can ask another independent question.");
    } catch (error) {
      status.textContent = error.name === 'TimeoutError' ? textFor("回答超时，请稍后重试。", "The request timed out. Please try again.") : (error.message || textFor("连接失败，请稍后重试。", "Connection failed. Please try again."));
    } finally { busy = false; setControls(); question.focus(); }
  });
  void connect();
}

// Native scrolling remains available without JavaScript; buttons add mouse navigation.
document.querySelectorAll('.projects-section').forEach(section => {
  const track = section.querySelector('.projects-grid');
  const controls = section.querySelector('.carousel-controls');
  if (!track || !controls) return;
  const previous = controls.querySelector('[data-scroll="-1"]');
  const next = controls.querySelector('[data-scroll="1"]');
  function update() {
    const max = Math.max(0, track.scrollWidth - track.clientWidth);
    controls.hidden = max <= 2;
    previous.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft >= max - 2;
  }
  controls.addEventListener('click', event => {
    const button = event.target.closest('button[data-scroll]');
    if (!button || button.disabled) return;
    const card = track.querySelector('.project-card');
    const step = (card?.getBoundingClientRect().width || track.clientWidth * .8) + (parseFloat(getComputedStyle(track).columnGap) || 0);
    track.scrollBy({left: Number(button.dataset.scroll) * step,
      behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'});
  });
  track.addEventListener('scroll', update, {passive:true});
  if ('ResizeObserver' in window) new ResizeObserver(update).observe(track);
  else window.addEventListener('resize', update);
  update();
});
