/**
 * app.js — Minimal JS for Quest Engine Web
 *
 * Handles:
 * - Keyboard shortcuts (A/B/C/D for quiz options, Enter to submit)
 * - Auto-scroll to result after answer submission
 * - Typewriter effect for narrative text (zone intros)
 * - Confetti burst on zone completion (playful theme)
 */

document.addEventListener('DOMContentLoaded', () => {
  initKeyboardShortcuts();
  initScrollToResult();
  initTypewriter();
  initConfetti();
  initSoundTriggers();
  initTimer();
  focusAnswerInput();
});

// ── Keyboard shortcuts ──────────────────────────────────────────────────────

function initKeyboardShortcuts() {
  document.addEventListener('keydown', (e) => {
    // Don't fire shortcuts when typing in an input
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    // Don't fire when modifier keys are held
    if (e.ctrlKey || e.metaKey || e.altKey) return;

    const key = e.key.toLowerCase();

    // Quiz option keys: a/b/c/d or 1/2/3/4 → click corresponding option button
    const letterMap = { a: 0, b: 1, c: 2, d: 3 };
    const numMap = { '1': 0, '2': 1, '3': 2, '4': 3 };
    let idx = letterMap[key] ?? numMap[key] ?? -1;
    if (idx >= 0) {
      const optionForms = document.querySelectorAll('.option-form');
      if (optionForms[idx]) {
        const btn = optionForms[idx].querySelector('.option-btn');
        if (btn) { btn.click(); e.preventDefault(); }
      }
    }

    // Enter / Space → click "Next" button or focus text input
    if (e.key === 'Enter' || e.key === ' ') {
      // If there's a next-challenge link visible, click it
      const nextBtn = document.querySelector('.next-challenge-action .btn, .zone-complete-banner .btn-primary');
      if (nextBtn) { nextBtn.click(); e.preventDefault(); return; }
      // Otherwise focus text input
      const textInput = document.querySelector('.text-answer-input');
      if (textInput && document.activeElement !== textInput) {
        textInput.focus();
        e.preventDefault();
      }
    }

    // H → hint button (works with any action path)
    if (key === 'h' && !e.shiftKey) {
      const hintBtn = document.querySelector('form[action$="/hint"] button');
      if (hintBtn) { hintBtn.click(); e.preventDefault(); }
    }

    // S → skip button
    if (key === 's' && !e.shiftKey) {
      const skipBtn = document.querySelector('form[action$="/skip"] button');
      if (skipBtn) { skipBtn.click(); e.preventDefault(); }
    }
  });
}

// ── Auto-scroll to result ───────────────────────────────────────────────────

function initScrollToResult() {
  const resultBanner = document.querySelector('.result-banner, .zone-complete-banner');
  if (resultBanner) {
    setTimeout(() => {
      resultBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 80);
  }
}

// ── Typewriter effect for narrative text ────────────────────────────────────

function initTypewriter() {
  const narrativeEl = document.querySelector('.intro-narrative');
  if (!narrativeEl) return;

  // Only animate if we haven't seen this zone before (check sessionStorage)
  const key = 'tw-' + window.location.pathname;
  if (sessionStorage.getItem(key)) return;
  sessionStorage.setItem(key, '1');

  const html = narrativeEl.innerHTML;
  narrativeEl.innerHTML = '';
  narrativeEl.style.opacity = '1';

  // Type out the HTML by revealing characters progressively
  // We parse the HTML as text nodes + element nodes and reveal them
  const temp = document.createElement('div');
  temp.innerHTML = html;

  let charDelay = 12; // ms per character
  let totalDelay = 0;

  function revealNode(node, parent) {
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent;
      const span = document.createElement('span');
      parent.appendChild(span);
      for (let i = 0; i < text.length; i++) {
        const char = text[i];
        setTimeout(() => { span.textContent += char; }, totalDelay);
        totalDelay += charDelay;
        // Pause slightly at punctuation
        if (['.', '!', '?'].includes(char)) totalDelay += 80;
        if ([',', ';'].includes(char)) totalDelay += 30;
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      if (node.tagName === 'BR') {
        setTimeout(() => { parent.appendChild(document.createElement('br')); totalDelay += 20; }, totalDelay);
        totalDelay += 20;
        return;
      }
      const el = document.createElement(node.tagName);
      el.className = node.className;
      parent.appendChild(el);
      for (const child of node.childNodes) {
        revealNode(child, el);
      }
    }
  }

  for (const child of temp.childNodes) {
    revealNode(child, narrativeEl);
  }
}

// ── Confetti on zone/pack completion (playful theme) ───────────────────────

function initConfetti() {
  const theme = document.documentElement.dataset.theme;
  if (theme !== 'playful') return;

  const isComplete = document.querySelector('.zone-complete-banner, .complete-page');
  if (!isComplete) return;

  // Simple CSS confetti burst — create colored particles
  const colors = ['#6c5ce7', '#00b4d8', '#ff7043', '#ffd600', '#66bb6a', '#f48fb1'];
  const container = document.body;

  for (let i = 0; i < 60; i++) {
    const particle = document.createElement('div');
    particle.style.cssText = `
      position: fixed;
      width: ${4 + Math.random() * 6}px;
      height: ${4 + Math.random() * 6}px;
      background: ${colors[Math.floor(Math.random() * colors.length)]};
      border-radius: ${Math.random() > 0.5 ? '50%' : '2px'};
      left: ${20 + Math.random() * 60}vw;
      top: -10px;
      opacity: 1;
      z-index: 9998;
      pointer-events: none;
      animation: confetti-fall ${1.5 + Math.random() * 1.5}s ease-in ${Math.random() * 0.5}s forwards;
    `;
    container.appendChild(particle);
    setTimeout(() => particle.remove(), 3500);
  }

  // Inject keyframes if not already present
  if (!document.getElementById('confetti-style')) {
    const style = document.createElement('style');
    style.id = 'confetti-style';
    style.textContent = `
      @keyframes confetti-fall {
        0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
        80%  { opacity: 1; }
        100% { transform: translateY(100vh) rotate(${Math.random() > 0.5 ? '' : '-'}${360 + Math.random() * 360}deg); opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }
}

// ── Sound effect triggers ───────────────────────────────────────────────────

function initSoundTriggers() {
  if (!window.QuestSounds) return;

  // Correct answer sound
  const correctBanner = document.querySelector('.result-correct');
  if (correctBanner) {
    // Check for zone/pack complete
    const zoneComplete = document.querySelector('.zone-complete-banner');
    if (zoneComplete) {
      QuestSounds.zoneComplete();
    } else {
      QuestSounds.correct();
    }
    // Check for level up
    const levelUp = document.querySelector('.level-up-badge');
    if (levelUp) setTimeout(() => QuestSounds.levelUp(), 400);
    // Check for achievement
    const achievement = document.querySelector('.achievement-badge');
    if (achievement) setTimeout(() => QuestSounds.achievement(), 600);
  }

  // Wrong answer sound + streak break
  const wrongBanner = document.querySelector('.result-wrong');
  if (wrongBanner) {
    QuestSounds.wrong();
    // If there was a streak, flash the streak display
    const streakEl = document.querySelector('.streak-display');
    if (streakEl) {
      streakEl.style.animation = 'shake 0.3s ease';
      streakEl.style.opacity = '0.3';
    }
  }

  // Option click sounds
  document.querySelectorAll('.option-btn').forEach(btn => {
    btn.addEventListener('mousedown', () => QuestSounds.click());
  });
}

// ── Challenge timer ──────────────────────────────────────────────────────────

function initTimer() {
  var display = document.getElementById('timer-display');
  if (!display) return;
  var start = Date.now();
  var interval = setInterval(function() {
    var elapsed = ((Date.now() - start) / 1000).toFixed(1);
    display.textContent = elapsed + 's';
  }, 100);
  // Stop when an answer form is submitted
  document.querySelectorAll('.option-form, .text-answer-form').forEach(function(form) {
    form.addEventListener('submit', function() { clearInterval(interval); });
  });
}

// ── Utility ─────────────────────────────────────────────────────────────────

function focusAnswerInput() {
  const input = document.querySelector('.text-answer-input');
  if (input) {
    setTimeout(() => input.focus(), 50);
  }
}
