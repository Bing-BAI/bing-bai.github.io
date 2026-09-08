document.querySelectorAll('.filters').forEach(group => {
  group.hidden = false;
  group.addEventListener('click', event => {
    const button = event.target.closest('button[data-filter]');
    if (!button) return;
    group.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    let count = 0;
    document.querySelectorAll('.post-row').forEach(row => {
      row.hidden = button.dataset.filter !== '全部文章' && row.dataset.category !== button.dataset.filter;
      if (!row.hidden) count++;
    });
    document.querySelector('.filter-status').textContent = `显示 ${count} 篇文章`;
  });
});
