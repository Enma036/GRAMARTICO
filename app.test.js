const test = require('node:test');
const assert = require('node:assert/strict');

function getWritingStats(text) {
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  return { words, minutes: Math.max(1, Math.ceil(words / 200)) };
}

test('counts words in a writing sample', () => {
  assert.deepEqual(getWritingStats('Write clearly and confidently.'), { words: 4, minutes: 1 });
});

test('estimates reading time for longer documents', () => {
  assert.deepEqual(getWritingStats(new Array(401).fill('word').join(' ')), { words: 401, minutes: 3 });
});

test('handles an empty document', () => {
  assert.deepEqual(getWritingStats('   '), { words: 0, minutes: 1 });
});
