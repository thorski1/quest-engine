/**
 * illustrations.js — Dynamic SVG illustrations for quest-engine.
 * Generates themed visual elements: progress rings, achievement badges,
 * star ratings, XP bars, zone maps, and decorative backgrounds.
 * No external images needed — all generated via JavaScript + SVG.
 */

const QuestIllustrations = (() => {

  /**
   * Create an animated circular progress ring.
   * Usage: QuestIllustrations.progressRing(container, percent, { size, color, label })
   */
  function progressRing(container, percent, opts = {}) {
    const size = opts.size || 120;
    const stroke = opts.stroke || 8;
    const color = opts.color || getComputedStyle(document.documentElement).getPropertyValue('--primary').trim() || '#00e5a0';
    const bg = opts.bg || getComputedStyle(document.documentElement).getPropertyValue('--border').trim() || '#1e3a5f';
    const label = opts.label || '';
    const r = (size - stroke) / 2;
    const circ = 2 * Math.PI * r;
    const offset = circ * (1 - percent / 100);

    const svg = `
      <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" style="transform:rotate(-90deg)">
        <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="${bg}" stroke-width="${stroke}"/>
        <circle cx="${size/2}" cy="${size/2}" r="${r}" fill="none" stroke="${color}" stroke-width="${stroke}"
          stroke-dasharray="${circ}" stroke-dashoffset="${circ}" stroke-linecap="round"
          style="transition:stroke-dashoffset 1s ease;">
          <animate attributeName="stroke-dashoffset" from="${circ}" to="${offset}" dur="1s" fill="freeze"/>
        </circle>
      </svg>
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%) rotate(0deg);text-align:center;">
        <div style="font-size:${size/4}px;font-weight:800;color:var(--text-bright);">${Math.round(percent)}%</div>
        ${label ? `<div style="font-size:${size/8}px;color:var(--text-dim);">${label}</div>` : ''}
      </div>`;

    container.style.position = 'relative';
    container.style.display = 'inline-block';
    container.innerHTML = svg;
  }

  /**
   * Create an animated XP bar with glow effect.
   */
  function xpBar(container, current, max, opts = {}) {
    const width = opts.width || '100%';
    const height = opts.height || 12;
    const pct = Math.min(current / max * 100, 100);
    const color = getComputedStyle(document.documentElement).getPropertyValue('--primary').trim();

    container.innerHTML = `
      <div style="width:${width};height:${height}px;background:var(--xp-bar-bg);border-radius:${height/2}px;overflow:hidden;position:relative;">
        <div style="width:0%;height:100%;border-radius:${height/2}px;background:linear-gradient(90deg,${color},var(--secondary));transition:width 1s ease;box-shadow:0 0 8px ${color}40;">
        </div>
      </div>
      <div style="display:flex;justify-content:space-between;font-size:0.7rem;color:var(--text-dim);margin-top:2px;">
        <span>${current} XP</span>
        <span>${max} XP</span>
      </div>`;

    // Animate after render
    requestAnimationFrame(() => {
      const fill = container.querySelector('div > div');
      if (fill) fill.style.width = pct + '%';
    });
  }

  /**
   * Generate animated star rating SVG.
   */
  function starRating(container, stars, maxStars = 3) {
    const size = 32;
    let html = '<div style="display:flex;gap:4px;">';
    for (let i = 0; i < maxStars; i++) {
      const filled = i < stars;
      const delay = i * 0.15;
      html += `
        <svg width="${size}" height="${size}" viewBox="0 0 24 24" style="animation:star-pop 0.3s ease ${delay}s both;">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
            fill="${filled ? 'var(--warn)' : 'var(--border)'}" stroke="${filled ? 'var(--warn)' : 'none'}" stroke-width="1"/>
        </svg>`;
    }
    html += '</div>';
    container.innerHTML = html;
  }

  /**
   * Create a zone progress map — connected nodes showing completion.
   */
  function zoneMap(container, zones) {
    const nodeR = 16;
    const gap = 60;
    const w = zones.length * gap + 40;
    const h = 60;
    let svg = `<svg width="100%" height="${h}" viewBox="0 0 ${w} ${h}" style="max-width:${w}px;">`;

    zones.forEach((z, i) => {
      const x = 20 + i * gap;
      const y = h / 2;
      const color = z.completed ? 'var(--primary)' : z.active ? 'var(--warn)' : 'var(--border)';
      const fill = z.completed ? color : 'var(--bg-surface)';

      // Connection line to next
      if (i < zones.length - 1) {
        const nextColor = zones[i+1].completed ? 'var(--primary)' : 'var(--border)';
        svg += `<line x1="${x + nodeR}" y1="${y}" x2="${x + gap - nodeR}" y2="${y}" stroke="${nextColor}" stroke-width="2" stroke-dasharray="${z.completed ? '' : '4,4'}"/>`;
      }

      // Node circle
      svg += `<circle cx="${x}" cy="${y}" r="${nodeR}" fill="${fill}" stroke="${color}" stroke-width="2"/>`;

      // Icon
      if (z.completed) {
        svg += `<text x="${x}" y="${y + 4}" text-anchor="middle" fill="var(--bg)" font-size="12" font-weight="bold">✓</text>`;
      } else if (z.active) {
        svg += `<circle cx="${x}" cy="${y}" r="4" fill="${color}"><animate attributeName="r" values="3;5;3" dur="1.5s" repeatCount="indefinite"/></circle>`;
      }

      // Label
      svg += `<text x="${x}" y="${y + nodeR + 14}" text-anchor="middle" fill="var(--text-dim)" font-size="9">${z.name.substring(0, 8)}</text>`;
    });

    svg += '</svg>';
    container.innerHTML = svg;
  }

  return { progressRing, xpBar, starRating, zoneMap };
})();

// Auto-initialize illustrations on page load
document.addEventListener('DOMContentLoaded', () => {
  // Progress rings
  document.querySelectorAll('[data-progress-ring]').forEach(el => {
    const pct = parseFloat(el.dataset.progressRing) || 0;
    const label = el.dataset.label || '';
    const size = parseInt(el.dataset.size) || 100;
    QuestIllustrations.progressRing(el, pct, { size, label });
  });

  // XP bars
  document.querySelectorAll('[data-xp-bar]').forEach(el => {
    const parts = el.dataset.xpBar.split('/');
    QuestIllustrations.xpBar(el, parseInt(parts[0]) || 0, parseInt(parts[1]) || 100);
  });

  // Star ratings
  document.querySelectorAll('[data-stars]').forEach(el => {
    QuestIllustrations.starRating(el, parseInt(el.dataset.stars) || 0);
  });
});

// CSS for star animation
const style = document.createElement('style');
style.textContent = '@keyframes star-pop{0%{transform:scale(0);opacity:0}60%{transform:scale(1.2)}100%{transform:scale(1);opacity:1}}';
document.head.appendChild(style);
