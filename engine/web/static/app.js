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
  initPageTransition();
  initKeyboardShortcuts();
  initScrollToResult();
  initTypewriter();
  initAnswerAnimations();
  initConfetti();
  initSoundTriggers();
  initTimer();
  initOptionHoverEffects();
  focusAnswerInput();
  initCardParallax();
  initHeaderPulse();
  initFloatingHelp();
});

// ── Page transition ─────────────────────────────────────────────────────────

function initPageTransition() {
  // Fade in on load
  document.body.style.opacity = '0';
  document.body.style.transition = 'opacity 0.25s ease';
  requestAnimationFrame(() => { document.body.style.opacity = '1'; });

  // Fade out on navigation
  document.querySelectorAll('a[href]:not([target="_blank"]):not([href^="#"]):not([href^="javascript"])').forEach(link => {
    link.addEventListener('click', function(e) {
      if (e.ctrlKey || e.metaKey || e.shiftKey) return; // Allow new tab
      e.preventDefault();
      document.body.style.opacity = '0';
      setTimeout(() => { window.location.href = this.href; }, 200);
    });
  });
}

// ── Option hover micro-interactions ─────────────────────────────────────────

function initOptionHoverEffects() {
  document.querySelectorAll('.option-btn').forEach(btn => {
    btn.addEventListener('mouseenter', () => {
      if (window.QuestSounds) QuestSounds.click();
    });
  });

  // Hub card hover sound
  document.querySelectorAll('.hub-card').forEach(card => {
    card.addEventListener('mouseenter', () => {
      if (window.QuestSounds) QuestSounds.click();
    });
  });
}

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

// ── Card hover parallax (subtle 3D tilt) ──────────────────────────────────

function initCardParallax() {
  var targets = document.querySelectorAll('.class-card, .rec-card, .cat-card, .realm, .path-head, .hub-card');
  if (!targets.length) return;
  // Respect reduced motion
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  targets.forEach(function(el) {
    el.style.transformStyle = 'preserve-3d';
    el.addEventListener('mousemove', function(e) {
      var rect = el.getBoundingClientRect();
      var x = (e.clientX - rect.left) / rect.width;
      var y = (e.clientY - rect.top) / rect.height;
      var rx = (0.5 - y) * 6;
      var ry = (x - 0.5) * 6;
      el.style.transform = 'perspective(800px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) translateY(-2px)';
    });
    el.addEventListener('mouseleave', function() {
      el.style.transform = '';
    });
  });
}

// ── Header pulse for streak and level ─────────────────────────────────────

function initFloatingHelp() {
  // Only render on pages that actually have keyboard shortcuts (challenge)
  if (!document.querySelector('.challenge-card')) return;
  if (document.getElementById('floating-help-btn')) return;

  var btn = document.createElement('button');
  btn.id = 'floating-help-btn';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Keyboard shortcuts');
  btn.title = 'Keyboard shortcuts (press ?)';
  btn.textContent = '?';
  btn.style.cssText = [
    'position: fixed', 'bottom: 1rem', 'right: 1rem',
    'width: 40px', 'height: 40px', 'border-radius: 50%',
    'background: rgba(255,255,255,0.05)',
    'border: 1.5px solid rgba(255,255,255,0.12)',
    'color: #c8d8e8', 'font-weight: 800', 'font-size: 1.1rem',
    'cursor: pointer', 'z-index: 900',
    'backdrop-filter: blur(10px)',
    'transition: all 0.15s',
  ].join(';');
  btn.onmouseover = function() {
    btn.style.background = 'rgba(0,229,160,0.15)';
    btn.style.borderColor = '#00e5a0';
    btn.style.color = '#00e5a0';
  };
  btn.onmouseout = function() {
    btn.style.background = 'rgba(255,255,255,0.05)';
    btn.style.borderColor = 'rgba(255,255,255,0.12)';
    btn.style.color = '#c8d8e8';
  };

  var panel = document.createElement('div');
  panel.id = 'floating-help-panel';
  panel.style.cssText = [
    'position: fixed', 'bottom: 4rem', 'right: 1rem',
    'padding: 1rem 1.25rem', 'border-radius: 12px',
    'background: rgba(18, 24, 36, 0.96)',
    'border: 1px solid rgba(255,255,255,0.1)',
    'color: #e8f4ff', 'font-size: 0.82rem',
    'min-width: 220px', 'z-index: 900',
    'box-shadow: 0 12px 36px rgba(0,0,0,0.5)',
    'backdrop-filter: blur(12px)',
    'opacity: 0', 'visibility: hidden',
    'transform: translateY(6px)',
    'transition: opacity 0.15s, transform 0.15s, visibility 0.15s',
  ].join(';');
  panel.innerHTML = [
    '<div style="font-size:0.68rem;font-weight:800;color:#00e5a0;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.6rem;">Keyboard Shortcuts</div>',
    '<div style="display:grid;grid-template-columns:auto 1fr;gap:0.35rem 0.7rem;">',
    '<kbd class="fh-k">A B C D</kbd><span>Choose answer</span>',
    '<kbd class="fh-k">1–4</kbd><span>Choose answer</span>',
    '<kbd class="fh-k">H</kbd><span>Hint</span>',
    '<kbd class="fh-k">S</kbd><span>Skip</span>',
    '<kbd class="fh-k">Enter</kbd><span>Next / Submit</span>',
    '<kbd class="fh-k">?</kbd><span>Toggle this panel</span>',
    '<kbd class="fh-k">Esc</kbd><span>Close</span>',
    '</div>',
  ].join('');
  // Add kbd style
  var kbdStyle = document.createElement('style');
  kbdStyle.textContent = '.fh-k { display:inline-block;padding:0.15rem 0.5rem;background:rgba(0,229,160,0.12);border:1px solid rgba(0,229,160,0.3);border-radius:6px;color:#00e5a0;font-weight:700;font-family:var(--font-mono,monospace);font-size:0.72rem;text-align:center;min-width:28px; }';
  document.head.appendChild(kbdStyle);

  document.body.appendChild(btn);
  document.body.appendChild(panel);

  function togglePanel() {
    var open = panel.style.visibility !== 'visible';
    panel.style.visibility = open ? 'visible' : 'hidden';
    panel.style.opacity = open ? '1' : '0';
    panel.style.transform = open ? 'translateY(0)' : 'translateY(6px)';
  }
  btn.addEventListener('click', togglePanel);
  document.addEventListener('keydown', function(e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === '?') { e.preventDefault(); togglePanel(); }
    if (e.key === 'Escape' && panel.style.visibility === 'visible') togglePanel();
  });
  document.addEventListener('click', function(e) {
    if (e.target !== btn && !panel.contains(e.target) && panel.style.visibility === 'visible') {
      togglePanel();
    }
  });
}

function initHeaderPulse() {
  if (!document.getElementById('header-pulse-style')) {
    var s = document.createElement('style');
    s.id = 'header-pulse-style';
    s.textContent = [
      '@keyframes streak-pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.08); } }',
      '@keyframes glow-pulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(0,229,160,0.3); } 50% { box-shadow: 0 0 0 6px rgba(0,229,160,0); } }',
      '.stat-streak { animation: streak-pulse 1.6s ease-in-out infinite; display: inline-block; }',
      '.xp-bar-fill { position: relative; }',
      '.xp-bar-fill::after { content: ""; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.35), transparent); background-size: 50% 100%; background-repeat: no-repeat; animation: xp-shimmer 2.5s linear infinite; }',
      '@keyframes xp-shimmer { 0% { background-position: -50% 0; } 100% { background-position: 150% 0; } }',
    ].join('\n');
    document.head.appendChild(s);
  }
}

// ── Answer feedback animations (+XP pop-up, shake, pulse) ─────────────────

function initAnswerAnimations() {
  // Inject animation keyframes once
  if (!document.getElementById('answer-fx-style')) {
    var style = document.createElement('style');
    style.id = 'answer-fx-style';
    style.textContent = [
      '@keyframes xp-float { 0% { opacity: 0; transform: translate(-50%, 0) scale(0.8); }',
      '  15% { opacity: 1; transform: translate(-50%, -8px) scale(1.1); }',
      '  100% { opacity: 0; transform: translate(-50%, -70px) scale(1); } }',
      '@keyframes shake-fx { 0%, 100% { transform: translateX(0); }',
      '  20% { transform: translateX(-10px); } 40% { transform: translateX(10px); }',
      '  60% { transform: translateX(-6px); } 80% { transform: translateX(6px); } }',
      '@keyframes correct-pulse { 0% { box-shadow: 0 0 0 0 rgba(0,229,160,0.6); }',
      '  70% { box-shadow: 0 0 0 20px rgba(0,229,160,0); }',
      '  100% { box-shadow: 0 0 0 0 rgba(0,229,160,0); } }',
      '@keyframes levelup-burst { 0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0; }',
      '  50% { transform: translate(-50%, -50%) scale(1.15); opacity: 1; }',
      '  100% { transform: translate(-50%, -50%) scale(1); opacity: 1; } }',
      '.xp-popup { position: fixed; top: 35%; left: 50%;',
      '  font-size: 2.2rem; font-weight: 900; color: #00e5a0;',
      '  text-shadow: 0 2px 20px rgba(0,229,160,0.6), 0 0 40px rgba(0,229,160,0.4);',
      '  z-index: 9999; pointer-events: none; animation: xp-float 1.8s ease-out both; font-family: var(--font); }',
      '.challenge-card.shake-fx { animation: shake-fx 0.4s; border-color: #ff6b6b !important; }',
      '.challenge-card.correct-fx { animation: correct-pulse 0.8s ease-out; border-color: #00e5a0 !important; }',
      '.level-up-modal { position: fixed; top: 50%; left: 50%;',
      '  padding: 2rem 2.5rem; border-radius: 24px; z-index: 9999;',
      '  background: linear-gradient(135deg, #00e5a0, #00b4d8); color: #0a0e1a;',
      '  font-weight: 900; text-align: center; box-shadow: 0 0 80px rgba(0,229,160,0.6);',
      '  animation: levelup-burst 0.5s ease-out both; pointer-events: none; }',
      '.level-up-modal .lu-title { font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.15em; }',
      '.level-up-modal .lu-num { font-size: 3rem; line-height: 1; margin: 0.35rem 0; }',
      '.level-up-modal .lu-sub { font-size: 0.95rem; opacity: 0.85; }',
    ].join('\n');
    document.head.appendChild(style);
  }

  var card = document.querySelector('.challenge-card');
  if (!card) return;

  // Correct answer: +XP pop-up, pulse, possibly level-up modal
  var correct = document.querySelector('.result-correct');
  if (correct) {
    card.classList.add('correct-fx');
    var xp = document.querySelector('.xp-gained');
    if (xp) {
      var pop = document.createElement('div');
      pop.className = 'xp-popup';
      pop.textContent = xp.textContent.trim();
      document.body.appendChild(pop);
      setTimeout(function() { pop.remove(); }, 2000);
    }
    var lu = document.querySelector('.level-up-badge');
    if (lu) {
      // Parse "🎉 Level Up! 5 — Title"
      var match = lu.textContent.match(/Level Up!\s*(\d+)\s*[—-]\s*(.+)/);
      if (match) {
        var modal = document.createElement('div');
        modal.className = 'level-up-modal';
        modal.innerHTML =
          '<div class="lu-title">Level Up!</div>' +
          '<div class="lu-num">' + match[1] + '</div>' +
          '<div class="lu-sub">' + match[2] + '</div>';
        document.body.appendChild(modal);
        setTimeout(function() {
          modal.style.transition = 'opacity 0.4s';
          modal.style.opacity = '0';
          setTimeout(function() { modal.remove(); }, 400);
        }, 2200);
      }
    }
  }

  // Wrong answer: shake
  var wrong = document.querySelector('.result-wrong');
  if (wrong) {
    card.classList.add('shake-fx');
    setTimeout(function() { card.classList.remove('shake-fx'); }, 500);
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

// ── TTS playback ────────────────────────────────────────────────────────────
//
// Tries backend TTS (ElevenLabs / Google) first for high-quality audio. If the
// backend returns no audio or errors, falls back to the browser's built-in
// Web Speech API, which works offline in every modern browser.

var _ttsAudio = null;
var _ttsSpeech = null;

function _stopTTS() {
  if (_ttsAudio) {
    try { _ttsAudio.pause(); } catch (e) {}
    _ttsAudio = null;
  }
  if (_ttsSpeech && window.speechSynthesis) {
    try { window.speechSynthesis.cancel(); } catch (e) {}
    _ttsSpeech = null;
  }
  document.querySelectorAll('.tts-play-btn .tts-icon, .tts-btn .tts-icon').forEach(function(ic) {
    ic.textContent = '🔊';
  });
}

function _resetIcon(iconEl) {
  iconEl.textContent = '🔊';
}

function _speakWithBrowser(text, iconEl) {
  if (!('speechSynthesis' in window) || !('SpeechSynthesisUtterance' in window)) {
    iconEl.textContent = '🔇';
    setTimeout(function() { _resetIcon(iconEl); }, 1500);
    return;
  }
  var utter = new SpeechSynthesisUtterance(text.substring(0, 500));
  // Try to pick a good English voice
  var voices = window.speechSynthesis.getVoices();
  var preferred = voices.find(function(v) { return /en-(US|GB)/i.test(v.lang) && /google|samantha|natural|daniel/i.test(v.name); })
    || voices.find(function(v) { return /en-(US|GB)/i.test(v.lang); })
    || voices[0];
  if (preferred) utter.voice = preferred;
  utter.rate = 1.0;
  utter.pitch = 1.0;
  utter.onend = function() { _resetIcon(iconEl); _ttsSpeech = null; };
  utter.onerror = function() { _resetIcon(iconEl); _ttsSpeech = null; };
  _ttsSpeech = utter;
  window.speechSynthesis.speak(utter);
}

function playTTS(btn) {
  var text = btn.dataset.text;
  if (!text) return;
  var iconEl = btn.querySelector('.tts-icon') || btn;

  // Toggle: clicking while playing stops playback.
  if (_ttsAudio || _ttsSpeech) {
    _stopTTS();
    return;
  }

  // Strip Rich markup
  text = text.replace(/\[\/?\w+[^\]]*\]/g, '');
  var theme = document.documentElement.dataset.theme || '';
  iconEl.textContent = '⏳';

  // Try server TTS first via fetch so we can cleanly fall back on failure.
  var url = '/api/tts?text=' + encodeURIComponent(text.substring(0, 500)) + '&theme=' + theme;
  fetch(url)
    .then(function(r) {
      if (!r.ok || r.status === 204) throw new Error('no-audio');
      var ct = r.headers.get('content-type') || '';
      if (ct.indexOf('audio') === -1) throw new Error('not-audio');
      return r.blob();
    })
    .then(function(blob) {
      if (!blob || blob.size < 100) throw new Error('empty');
      var objUrl = URL.createObjectURL(blob);
      _ttsAudio = new Audio(objUrl);
      _ttsAudio.onended = function() { _resetIcon(iconEl); _ttsAudio = null; URL.revokeObjectURL(objUrl); };
      _ttsAudio.onerror = function() { _resetIcon(iconEl); _ttsAudio = null; URL.revokeObjectURL(objUrl); };
      return _ttsAudio.play();
    })
    .catch(function() {
      // Backend TTS unavailable — use Web Speech API
      _ttsAudio = null;
      _speakWithBrowser(text, iconEl);
    });
}

// ── AI Tutor explain ─────────────────────────────────────────────────────────

function aiExplain(btn) {
  var question = btn.dataset.question || '';
  var answer = btn.dataset.answer || '';
  var el = document.getElementById('ai-explanation');
  if (!el) return;
  btn.textContent = '🤖 Thinking...';
  btn.disabled = true;

  fetch('/api/explain?question=' + encodeURIComponent(question) + '&answer=' + encodeURIComponent(answer))
    .then(function(r) { return r.json(); })
    .then(function(data) {
      el.style.display = 'block';
      el.innerHTML = '<strong>🤖 AI Tutor:</strong> ' + (data.explanation || 'No explanation available.');
      btn.style.display = 'none';
    })
    .catch(function() {
      el.style.display = 'block';
      el.textContent = 'Could not load explanation.';
      btn.textContent = '🤖 Explain why';
      btn.disabled = false;
    });
}

// ── Challenge timer ──────────────────────────────────────────────────────────

function initTimer() {
  var display = document.getElementById('timer-display');
  if (!display) return;
  var start = Date.now();
  window._challengeStartTime = start;
  var interval = setInterval(function() {
    var elapsed = ((Date.now() - start) / 1000).toFixed(1);
    display.textContent = elapsed + 's';
    // Color coding: green < 5s, yellow < 15s, red > 15s
    if (elapsed < 5) display.style.color = 'var(--primary)';
    else if (elapsed < 15) display.style.color = 'var(--warn)';
    else display.style.color = 'var(--accent)';
  }, 100);
  document.querySelectorAll('.option-form, .text-answer-form').forEach(function(form) {
    form.addEventListener('submit', function() {
      clearInterval(interval);
      var elapsed = ((Date.now() - start) / 1000).toFixed(1);
      display.textContent = elapsed + 's ✓';
      // Set elapsed time in hidden field for speed bonus XP
      var elField = form.querySelector('.elapsed-field');
      if (elField) elField.value = elapsed;
    });
  });
}

// ── Utility ─────────────────────────────────────────────────────────────────

function focusAnswerInput() {
  const input = document.querySelector('.text-answer-input');
  if (input) {
    setTimeout(() => input.focus(), 50);
  }
}
