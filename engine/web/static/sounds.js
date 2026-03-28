/**
 * sounds.js — Synthesized sound effects for Quest Engine
 * Uses Web Audio API — no audio files required.
 * Respects user preference: localStorage.getItem('quest-sound') !== 'off'
 */

const QuestSounds = (() => {
  let ctx = null;

  function getCtx() {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    return ctx;
  }

  function isEnabled() {
    return localStorage.getItem('quest-sound') !== 'off';
  }

  function playTone(freq, duration, type = 'sine', volume = 0.15) {
    if (!isEnabled()) return;
    try {
      const c = getCtx();
      const osc = c.createOscillator();
      const gain = c.createGain();
      osc.type = type;
      osc.frequency.value = freq;
      gain.gain.setValueAtTime(volume, c.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, c.currentTime + duration);
      osc.connect(gain);
      gain.connect(c.destination);
      osc.start(c.currentTime);
      osc.stop(c.currentTime + duration);
    } catch (e) { /* Audio not supported */ }
  }

  function playSequence(notes) {
    if (!isEnabled()) return;
    try {
      const c = getCtx();
      let t = c.currentTime;
      notes.forEach(([freq, dur, type]) => {
        const osc = c.createOscillator();
        const gain = c.createGain();
        osc.type = type || 'sine';
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0.12, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + dur);
        osc.connect(gain);
        gain.connect(c.destination);
        osc.start(t);
        osc.stop(t + dur);
        t += dur * 0.7;
      });
    } catch (e) { /* Audio not supported */ }
  }

  return {
    /** Cheerful ascending chime — correct answer */
    correct() {
      playSequence([
        [523, 0.12, 'sine'],   // C5
        [659, 0.12, 'sine'],   // E5
        [784, 0.2, 'sine'],    // G5
      ]);
    },

    /** Soft descending tone — wrong answer */
    wrong() {
      playSequence([
        [350, 0.15, 'triangle'],
        [280, 0.25, 'triangle'],
      ]);
    },

    /** Triumphant fanfare — level up */
    levelUp() {
      playSequence([
        [523, 0.1, 'sine'],    // C5
        [659, 0.1, 'sine'],    // E5
        [784, 0.1, 'sine'],    // G5
        [1047, 0.35, 'sine'],  // C6
      ]);
    },

    /** Achievement unlock — sparkly */
    achievement() {
      playSequence([
        [880, 0.08, 'sine'],   // A5
        [1109, 0.08, 'sine'],  // C#6
        [1319, 0.08, 'sine'],  // E6
        [1760, 0.3, 'sine'],   // A6
      ]);
    },

    /** Zone complete — triumphant chord */
    zoneComplete() {
      playSequence([
        [392, 0.15, 'sine'],   // G4
        [494, 0.15, 'sine'],   // B4
        [587, 0.15, 'sine'],   // D5
        [784, 0.4, 'sine'],    // G5
      ]);
    },

    /** Soft click — button/option press */
    click() {
      playTone(600, 0.06, 'sine', 0.08);
    },

    /** Hint reveal — gentle */
    hint() {
      playTone(440, 0.15, 'triangle', 0.1);
    },

    /** Toggle sound on/off */
    toggle() {
      const current = localStorage.getItem('quest-sound');
      if (current === 'off') {
        localStorage.removeItem('quest-sound');
        this.click();
        return true;
      } else {
        localStorage.setItem('quest-sound', 'off');
        return false;
      }
    },

    isEnabled,
  };
})();

// Export for use in app.js
if (typeof window !== 'undefined') window.QuestSounds = QuestSounds;
