const writingArea = document.querySelector('#writingArea');
const toast = document.querySelector('#toast');
const sidebar = document.querySelector('#sidebar');
let toastTimer;

function getWritingStats(text) {
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  return { words, minutes: Math.max(1, Math.ceil(words / 200)) };
}

function showMessage(message) {
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
}

function updateStats() {
  const stats = getWritingStats(writingArea.value);
  document.querySelector('#wordCount').textContent = `${stats.words} ${stats.words === 1 ? 'word' : 'words'}`;
  document.querySelector('#readingTime').textContent = `${stats.minutes} min read`;
  writingArea.style.height = 'auto';
  writingArea.style.height = `${Math.max(490, writingArea.scrollHeight)}px`;
}

function updateScore() {
  const remaining = document.querySelectorAll('.suggestion').length;
  const score = 100 - remaining * 4.5;
  document.querySelector('#scoreValue').textContent = Math.round(score);
  document.querySelector('#scoreRing').style.setProperty('--score', score);
  document.querySelector('#suggestionCount').textContent = remaining;
  document.querySelector('#scoreSummary').textContent = remaining ? `${remaining} suggestion${remaining === 1 ? '' : 's'} can make it even stronger.` : 'No more suggestions. Nicely done!';
  document.querySelector('#allClear').classList.toggle('visible', remaining === 0);
}

function removeSuggestion(card, accepted) {
  if (accepted) {
    const find = card.dataset.find;
    const replacement = card.dataset.replace;
    writingArea.value = writingArea.value.replace(find, replacement);
    updateStats();
  }
  card.classList.add('removing');
  setTimeout(() => {
    card.remove();
    updateScore();
  }, 220);
  showMessage(accepted ? 'Suggestion applied' : 'Suggestion dismissed');
}

document.querySelectorAll('.suggestion').forEach((card) => {
  card.querySelector('.accept').addEventListener('click', () => removeSuggestion(card, true));
  card.querySelector('.replacement').addEventListener('click', () => removeSuggestion(card, true));
  card.querySelector('.dismiss').addEventListener('click', () => removeSuggestion(card, false));
});

document.querySelectorAll('[data-tab]').forEach((tab) => tab.addEventListener('click', () => {
  document.querySelector('[data-tab].active').classList.remove('active');
  tab.classList.add('active');
  const showGoals = tab.dataset.tab === 'goals';
  document.querySelector('#suggestionsPanel').hidden = showGoals;
  document.querySelector('#goalsPanel').hidden = !showGoals;
}));

document.querySelector('#newDocument').addEventListener('click', () => {
  document.querySelector('#documentTitle').value = 'Untitled document';
  writingArea.value = '';
  updateStats();
  writingArea.focus();
  sidebar.classList.remove('open');
  showMessage('New document created');
});

document.querySelector('#shareButton').addEventListener('click', async () => {
  if (navigator.clipboard) await navigator.clipboard.writeText(writingArea.value);
  showMessage('Document copied and ready to share');
});

document.querySelector('#menuButton').addEventListener('click', () => {
  const open = sidebar.classList.toggle('open');
  document.querySelector('#menuButton').setAttribute('aria-expanded', String(open));
});
document.querySelector('#closeMenu').addEventListener('click', () => sidebar.classList.remove('open'));
document.querySelector('.upgrade-card button').addEventListener('click', () => showMessage('Pro features are coming soon'));
writingArea.addEventListener('input', updateStats);
updateStats();
