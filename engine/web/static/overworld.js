/**
 * overworld.js — Lo-fi Pixel-Art RPG Overworld for Quest Engine
 *
 * A top-down exploration view where players walk a character around a map
 * and enter zone buildings. Built on Phaser 3 (loaded from CDN).
 *
 * Usage:
 *   1. Set window.QUEST_OVERWORLD_CONFIG with zones, theme, etc.
 *   2. Call QuestOverworld.init('container-id')
 *
 * Requires: <script src="https://cdn.jsdelivr.net/npm/phaser@3/dist/phaser.min.js"></script>
 */

// ═══════════════════════════════════════════════════════════════════════════════
//  THEME PALETTES
// ═══════════════════════════════════════════════════════════════════════════════

const OVERWORLD_PALETTES = {
  cyberpunk: {
    bg:          0x08111f,
    bgAlt:       0x0d1a2e,
    grass:       0x0a1628,
    grassAlt:    0x0c1e35,
    dirt:        0x111a2a,
    building:    0x00e5a0,
    buildingAlt: 0x00b4d8,
    path:        0x00b4d8,
    pathEdge:    0x006688,
    roof:        0x009966,
    door:        0x08111f,
    player:      0xff3c78,
    playerAlt:   0xff6699,
    text:        0xc8d8e8,
    textBright:  0xe8f4ff,
    hud:         0x08111f,
    hudBorder:   0x1a3050,
    particle:    0x00e5a0,
    particleAlt: 0x00b4d8,
    locked:      0x333c48,
    complete:    0x00e5a0,
    glow:        0x00e5a0,
    shadow:      0x050a14,
  },
  playful: {
    bg:          0xfff5e6,
    bgAlt:       0xffe8cc,
    grass:       0xb8e6a0,
    grassAlt:    0xa0d890,
    dirt:        0xd4b896,
    building:    0x8b5cf6,
    buildingAlt: 0xa78bfa,
    path:        0xf09040,
    pathEdge:    0xc87030,
    roof:        0x7c3aed,
    door:        0x3b1a80,
    player:      0xff6b6b,
    playerAlt:   0xff8888,
    text:        0x2d1b4e,
    textBright:  0x1a0a30,
    hud:         0xfff5e6,
    hudBorder:   0xd4b896,
    particle:    0xf09040,
    particleAlt: 0x8b5cf6,
    locked:      0xb0a898,
    complete:    0x22c55e,
    glow:        0xf09040,
    shadow:      0x6b5a48,
  },
  neural: {
    bg:          0x150a28,
    bgAlt:       0x1a0e32,
    grass:       0x180c30,
    grassAlt:    0x1e1038,
    dirt:        0x201240,
    building:    0x9333ea,
    buildingAlt: 0xa855f7,
    path:        0x00d4ff,
    pathEdge:    0x0099bb,
    roof:        0x7e22ce,
    door:        0x0a0518,
    player:      0x00d4ff,
    playerAlt:   0x33ddff,
    text:        0xc8b8e8,
    textBright:  0xe8ddff,
    hud:         0x150a28,
    hudBorder:   0x3b1a80,
    particle:    0x9333ea,
    particleAlt: 0x00d4ff,
    locked:      0x3a2850,
    complete:    0x22c55e,
    glow:        0x9333ea,
    shadow:      0x0a0518,
  },
  medieval: {
    bg:          0x2a1f14,
    bgAlt:       0x3a2a1a,
    grass:       0x4a7a30,
    grassAlt:    0x3d6828,
    dirt:        0x8b7355,
    building:    0xd4a040,
    buildingAlt: 0xc89030,
    path:        0xc8b090,
    pathEdge:    0xa89070,
    roof:        0xb8860b,
    door:        0x3a2010,
    player:      0xe44040,
    playerAlt:   0xff5555,
    text:        0xe8d8c0,
    textBright:  0xfff0dd,
    hud:         0x2a1f14,
    hudBorder:   0x5a4a30,
    particle:    0xd4a040,
    particleAlt: 0xc8b090,
    locked:      0x5a4a38,
    complete:    0x22c55e,
    glow:        0xd4a040,
    shadow:      0x1a1008,
  },
  // Extra themes from the CSS system
  unicorn: {
    bg:          0xfff0f5,
    bgAlt:       0xffe4ec,
    grass:       0xc8e8b0,
    grassAlt:    0xb8d8a0,
    dirt:        0xe8c8d0,
    building:    0xd946ef,
    buildingAlt: 0xe879f0,
    path:        0xfbbf24,
    pathEdge:    0xd9a010,
    roof:        0xc026d3,
    door:        0x4a1050,
    player:      0x38bdf8,
    playerAlt:   0x60ccff,
    text:        0x4a1050,
    textBright:  0x2d0a30,
    hud:         0xfff0f5,
    hudBorder:   0xe8a8c0,
    particle:    0xd946ef,
    particleAlt: 0xfbbf24,
    locked:      0xc0b0b8,
    complete:    0x22c55e,
    glow:        0xd946ef,
    shadow:      0x8a6878,
  },
  alien: {
    bg:          0x0a1a0a,
    bgAlt:       0x0e220e,
    grass:       0x0c200c,
    grassAlt:    0x102810,
    dirt:        0x1a2a10,
    building:    0x4ade80,
    buildingAlt: 0x22c55e,
    path:        0x84cc16,
    pathEdge:    0x60a010,
    roof:        0x16a34a,
    door:        0x051005,
    player:      0xfbbf24,
    playerAlt:   0xffcc44,
    text:        0xc0e8c0,
    textBright:  0xe0ffe0,
    hud:         0x0a1a0a,
    hudBorder:   0x1a3a1a,
    particle:    0x4ade80,
    particleAlt: 0x84cc16,
    locked:      0x2a3828,
    complete:    0x4ade80,
    glow:        0x4ade80,
    shadow:      0x050a05,
  },
  ocean: {
    bg:          0x0a1828,
    bgAlt:       0x0e2038,
    grass:       0x1a5060,
    grassAlt:    0x184858,
    dirt:        0x2a4050,
    building:    0x06b6d4,
    buildingAlt: 0x22d3ee,
    path:        0x0ea5e9,
    pathEdge:    0x0880b8,
    roof:        0x0891b2,
    door:        0x051520,
    player:      0xfbbf24,
    playerAlt:   0xffcc44,
    text:        0xc0d8e8,
    textBright:  0xe0f0ff,
    hud:         0x0a1828,
    hudBorder:   0x1a3848,
    particle:    0x06b6d4,
    particleAlt: 0x0ea5e9,
    locked:      0x283840,
    complete:    0x22c55e,
    glow:        0x06b6d4,
    shadow:      0x050c14,
  },
  sunset: {
    bg:          0x1a0c14,
    bgAlt:       0x241018,
    grass:       0x2a1820,
    grassAlt:    0x321c28,
    dirt:        0x3a2028,
    building:    0xf97316,
    buildingAlt: 0xfb923c,
    path:        0xfbbf24,
    pathEdge:    0xd4a010,
    roof:        0xea580c,
    door:        0x1a0808,
    player:      0x38bdf8,
    playerAlt:   0x60ccff,
    text:        0xe8d0c0,
    textBright:  0xfff0e0,
    hud:         0x1a0c14,
    hudBorder:   0x4a2830,
    particle:    0xf97316,
    particleAlt: 0xfbbf24,
    locked:      0x3a2830,
    complete:    0x22c55e,
    glow:        0xf97316,
    shadow:      0x0a0508,
  },
};


// ═══════════════════════════════════════════════════════════════════════════════
//  CONSTANTS
// ═══════════════════════════════════════════════════════════════════════════════

const TILE    = 16;            // Base tile size in pixels
const SCALE   = 3;             // Pixel-art upscale factor
const UNIT    = TILE * SCALE;  // Effective tile size on screen (48px)

const MAP_COLS  = 17;          // Map width in tiles
const MAP_ROWS  = 10;          // Map height in tiles (≈16:9 at 17:10)

const PLAYER_SPEED   = UNIT * 3.5;  // Pixels per second
const BUILDING_W     = UNIT * 2;     // Building width
const BUILDING_H     = UNIT * 2;     // Building height
const PROXIMITY_DIST = UNIT * 1.5;   // Glow/interact distance


// ═══════════════════════════════════════════════════════════════════════════════
//  OVERWORLD SCENE
// ═══════════════════════════════════════════════════════════════════════════════

class OverworldScene extends Phaser.Scene {
  constructor() {
    super({ key: 'OverworldScene' });
  }

  // ── Initialization ──────────────────────────────────────────────────────────

  init() {
    const cfg = window.QUEST_OVERWORLD_CONFIG || {};
    this.zones      = cfg.zones || [];
    this.themeName  = cfg.theme || 'cyberpunk';
    this.packTitle  = cfg.packTitle || 'Quest';
    this.onEnterZone = cfg.onEnterZone || function() {};
    this.pal        = OVERWORLD_PALETTES[this.themeName] || OVERWORLD_PALETTES.cyberpunk;

    this.nearZone     = null;    // Currently highlighted zone
    this.buildingObjs = [];      // Array of building data objects
    this.time_acc     = 0;       // Animation accumulator
  }

  // ── Create ──────────────────────────────────────────────────────────────────

  create() {
    const w = this.scale.width;
    const h = this.scale.height;

    this._drawBackground(w, h);
    this._drawPaths(w, h);
    this._createBuildings();
    this._createPlayer(w, h);
    this._createParticles(w, h);
    this._createHUD(w, h);

    // Input
    this.cursors = this.input.keyboard.createCursorKeys();
    this.wasd    = this.input.keyboard.addKeys({
      up:    Phaser.Input.Keyboard.KeyCodes.W,
      down:  Phaser.Input.Keyboard.KeyCodes.S,
      left:  Phaser.Input.Keyboard.KeyCodes.A,
      right: Phaser.Input.Keyboard.KeyCodes.D,
    });
    this.enterKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.ENTER);
    this.spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

    // Zone enter action
    this.enterKey.on('down', () => this._tryEnterZone());
    this.spaceKey.on('down', () => this._tryEnterZone());

    // Camera bounds
    this.cameras.main.setBounds(0, 0, w, h);
  }

  // ── Update loop ─────────────────────────────────────────────────────────────

  update(time, delta) {
    this._updatePlayerMovement(delta);
    this._updateProximity();
    this._updateAnimations(time, delta);
  }

  // ── Background: tiled grass/dirt pattern ────────────────────────────────────

  _drawBackground(w, h) {
    const gfx = this.add.graphics();
    const pal = this.pal;

    // Fill base
    gfx.fillStyle(pal.bg, 1);
    gfx.fillRect(0, 0, w, h);

    // Tile pattern — alternating grass colors for a subtle checkerboard
    for (let row = 0; row < Math.ceil(h / UNIT); row++) {
      for (let col = 0; col < Math.ceil(w / UNIT); col++) {
        const isAlt = (row + col) % 2 === 0;
        gfx.fillStyle(isAlt ? pal.grass : pal.grassAlt, 1);
        gfx.fillRect(col * UNIT, row * UNIT, UNIT, UNIT);

        // Occasional dirt patch for texture
        if (this._seededRandom(row * 100 + col) > 0.82) {
          gfx.fillStyle(pal.dirt, 0.5);
          const dx = (this._seededRandom(row * 100 + col + 50) * 0.5 + 0.25) * UNIT;
          const dy = (this._seededRandom(row * 100 + col + 99) * 0.5 + 0.25) * UNIT;
          const ds = UNIT * 0.3;
          gfx.fillRect(col * UNIT + dx - ds / 2, row * UNIT + dy - ds / 2, ds, ds);
        }
      }
    }

    // Decorative edge dots (pixel-art grass tufts)
    for (let i = 0; i < 40; i++) {
      const x = this._seededRandom(i * 7 + 3) * w;
      const y = this._seededRandom(i * 7 + 11) * h;
      gfx.fillStyle(pal.grassAlt, 0.6);
      gfx.fillRect(Math.floor(x / 4) * 4, Math.floor(y / 4) * 4, 4, 4);
    }

    gfx.setDepth(0);
  }

  // ── Paths connecting buildings ──────────────────────────────────────────────

  _drawPaths(w, h) {
    if (this.zones.length < 2) return;

    const gfx = this.add.graphics();
    gfx.setDepth(1);
    const pal = this.pal;
    const pathW = UNIT * 0.6;

    // Compute building centers
    const centers = this.zones.map(z => this._zoneToCenterPos(z));

    // Draw path edges (darker outline) then path fill
    for (let i = 0; i < centers.length - 1; i++) {
      const a = centers[i];
      const b = centers[i + 1];
      this._drawPathSegment(gfx, a.x, a.y, b.x, b.y, pathW + 6, pal.pathEdge);
      this._drawPathSegment(gfx, a.x, a.y, b.x, b.y, pathW, pal.path);
    }

    // Pixel-art dashes along paths
    for (let i = 0; i < centers.length - 1; i++) {
      const a = centers[i];
      const b = centers[i + 1];
      const dist = Phaser.Math.Distance.Between(a.x, a.y, b.x, b.y);
      const steps = Math.floor(dist / (UNIT * 0.5));
      for (let s = 0; s <= steps; s++) {
        const t = s / Math.max(steps, 1);
        const px = Phaser.Math.Linear(a.x, b.x, t);
        const py = Phaser.Math.Linear(a.y, b.y, t);
        if (s % 2 === 0) {
          gfx.fillStyle(pal.pathEdge, 0.4);
          gfx.fillRect(Math.floor(px / 4) * 4 - 2, Math.floor(py / 4) * 4 - 2, 4, 4);
        }
      }
    }
  }

  /**
   * Draw a single path segment as a thick line (series of rects for pixel feel).
   */
  _drawPathSegment(gfx, x1, y1, x2, y2, width, color) {
    gfx.fillStyle(color, 0.85);
    const dist = Phaser.Math.Distance.Between(x1, y1, x2, y2);
    const steps = Math.max(Math.ceil(dist / 3), 1);
    const half = width / 2;

    for (let i = 0; i <= steps; i++) {
      const t  = i / steps;
      const px = Phaser.Math.Linear(x1, x2, t);
      const py = Phaser.Math.Linear(y1, y2, t);
      // Snap to 4px grid for pixel-art feel
      const sx = Math.floor(px / 4) * 4;
      const sy = Math.floor(py / 4) * 4;
      gfx.fillRect(sx - half, sy - half, width, width);
    }
  }

  // ── Buildings (zone entries) ────────────────────────────────────────────────

  _createBuildings() {
    this.buildingObjs = [];

    this.zones.forEach((zone, idx) => {
      const pos    = this._zoneToCenterPos(zone);
      const pal    = this.pal;
      const locked = zone.locked;
      const done   = zone.completed;

      const container = this.add.container(pos.x, pos.y);
      container.setDepth(3);

      // ── Glow ring (hidden until near) ──
      const glow = this.add.graphics();
      glow.fillStyle(pal.glow, 0.15);
      glow.fillCircle(0, 0, BUILDING_W * 0.85);
      glow.setAlpha(0);
      container.add(glow);

      // ── Shadow ──
      const shadow = this.add.graphics();
      shadow.fillStyle(pal.shadow, 0.4);
      shadow.fillRect(-BUILDING_W / 2 + 4, -BUILDING_H / 2 + 6, BUILDING_W, BUILDING_H);
      container.add(shadow);

      // ── Main building body ──
      const body = this.add.graphics();
      const bColor = locked ? pal.locked : (idx % 2 === 0 ? pal.building : pal.buildingAlt);
      body.fillStyle(bColor, locked ? 0.5 : 1);
      body.fillRect(-BUILDING_W / 2, -BUILDING_H / 2, BUILDING_W, BUILDING_H);

      // Pixel-art roof (top bar, slightly wider)
      body.fillStyle(locked ? pal.locked : pal.roof, locked ? 0.5 : 1);
      body.fillRect(-BUILDING_W / 2 - 4, -BUILDING_H / 2 - 8, BUILDING_W + 8, 12);

      // Door
      body.fillStyle(pal.door, locked ? 0.3 : 0.9);
      body.fillRect(-8, BUILDING_H / 2 - 20, 16, 20);

      // Window pixels
      if (!locked) {
        body.fillStyle(pal.textBright, 0.5);
        body.fillRect(-BUILDING_W / 2 + 8, -BUILDING_H / 2 + 14, 8, 8);
        body.fillRect( BUILDING_W / 2 - 16, -BUILDING_H / 2 + 14, 8, 8);
        // Window glow
        body.fillStyle(pal.particle, 0.2);
        body.fillRect(-BUILDING_W / 2 + 7, -BUILDING_H / 2 + 13, 10, 10);
        body.fillRect( BUILDING_W / 2 - 17, -BUILDING_H / 2 + 13, 10, 10);
      }

      container.add(body);

      // ── Label ──
      const label = this.add.text(0, BUILDING_H / 2 + 14, zone.name || zone.id, {
        fontFamily: '"Press Start 2P", "JetBrains Mono", monospace',
        fontSize: '8px',
        color: locked ? '#666' : '#' + pal.textBright.toString(16).padStart(6, '0'),
        align: 'center',
        stroke: '#' + pal.shadow.toString(16).padStart(6, '0'),
        strokeThickness: 2,
      });
      label.setOrigin(0.5, 0);
      container.add(label);

      // ── Completed checkmark ──
      let checkmark = null;
      if (done) {
        checkmark = this.add.text(BUILDING_W / 2 - 4, -BUILDING_H / 2 - 4, '\u2713', {
          fontFamily: '"Press Start 2P", monospace',
          fontSize: '14px',
          color: '#' + pal.complete.toString(16).padStart(6, '0'),
          stroke: '#000',
          strokeThickness: 3,
        });
        checkmark.setOrigin(0.5, 0.5);
        container.add(checkmark);
      }

      // ── Lock icon ──
      if (locked) {
        const lock = this.add.text(0, -4, '\u{1F512}', {
          fontSize: '16px',
        });
        lock.setOrigin(0.5, 0.5);
        container.add(lock);
      }

      // ── Interaction prompt (hidden until near) ──
      const prompt = this.add.text(0, -BUILDING_H / 2 - 24, locked ? 'LOCKED' : 'ENTER', {
        fontFamily: '"Press Start 2P", "JetBrains Mono", monospace',
        fontSize: '7px',
        color: locked ? '#666' : '#' + pal.textBright.toString(16).padStart(6, '0'),
        align: 'center',
        backgroundColor: '#' + pal.hud.toString(16).padStart(6, '0'),
        padding: { x: 4, y: 2 },
        stroke: '#' + pal.shadow.toString(16).padStart(6, '0'),
        strokeThickness: 1,
      });
      prompt.setOrigin(0.5, 1);
      prompt.setAlpha(0);
      container.add(prompt);

      this.buildingObjs.push({
        zone,
        container,
        glow,
        prompt,
        checkmark,
        body,
        cx: pos.x,
        cy: pos.y,
        isNear: false,
      });
    });
  }

  // ── Player character ────────────────────────────────────────────────────────

  _createPlayer(w, h) {
    const pal    = this.pal;
    const startX = UNIT * 2;
    const startY = h / 2;

    // Player container
    this.playerContainer = this.add.container(startX, startY);
    this.playerContainer.setDepth(5);

    // Shadow
    const pShadow = this.add.graphics();
    pShadow.fillStyle(pal.shadow, 0.4);
    pShadow.fillEllipse(0, 10, 18, 6);
    this.playerContainer.add(pShadow);

    // Body (16x16 character)
    this.playerGfx = this.add.graphics();
    this._drawPlayerSprite(pal.player, false);
    this.playerContainer.add(this.playerGfx);

    // Movement state
    this.playerVx = 0;
    this.playerVy = 0;
    this.playerFacing = 'right';
    this.playerBobTimer = 0;
    this.isMoving = false;
  }

  /**
   * Draw the player as a simple pixel-art character.
   * This is called each frame to animate the walking bob.
   */
  _drawPlayerSprite(color, bobUp) {
    const g = this.playerGfx;
    const pal = this.pal;
    g.clear();

    const yOff = bobUp ? -2 : 0;

    // Body
    g.fillStyle(color, 1);
    g.fillRect(-8, -8 + yOff, 16, 16);

    // Eyes (two bright pixels)
    g.fillStyle(pal.textBright, 1);
    if (this.playerFacing === 'left') {
      g.fillRect(-6, -4 + yOff, 3, 3);
      g.fillRect(-1, -4 + yOff, 3, 3);
    } else if (this.playerFacing === 'right') {
      g.fillRect(-2, -4 + yOff, 3, 3);
      g.fillRect(3,  -4 + yOff, 3, 3);
    } else {
      g.fillRect(-4, -4 + yOff, 3, 3);
      g.fillRect(2,  -4 + yOff, 3, 3);
    }

    // Highlight pixel (top-left corner shine)
    g.fillStyle(pal.playerAlt, 0.6);
    g.fillRect(-8, -8 + yOff, 4, 4);

    // Feet (two small rects, separated when walking)
    const footSpread = this.isMoving ? (bobUp ? 3 : -1) : 1;
    g.fillStyle(pal.shadow, 1);
    g.fillRect(-6, 8 + yOff, 4, 3);
    g.fillRect(2 + footSpread, 8 + yOff, 4, 3);
  }

  // ── Ambient particles ───────────────────────────────────────────────────────

  _createParticles(w, h) {
    this.ambientParticles = [];

    for (let i = 0; i < 25; i++) {
      const gfx = this.add.graphics();
      const isAlt = i % 3 === 0;
      const size = isAlt ? 3 : 2;
      gfx.fillStyle(isAlt ? this.pal.particleAlt : this.pal.particle, 0.4);
      gfx.fillRect(-size / 2, -size / 2, size, size);
      gfx.setDepth(6);

      const px = Math.random() * w;
      const py = Math.random() * h;
      gfx.setPosition(px, py);

      this.ambientParticles.push({
        gfx,
        baseX: px,
        baseY: py,
        speed: 0.2 + Math.random() * 0.4,
        amplitude: 10 + Math.random() * 20,
        phase: Math.random() * Math.PI * 2,
        drift: (Math.random() - 0.5) * 0.3,
      });
    }
  }

  // ── HUD ─────────────────────────────────────────────────────────────────────

  _createHUD(w, h) {
    const pal = this.pal;
    const completedCount = this.zones.filter(z => z.completed).length;
    const totalCount     = this.zones.length;

    // Background bar
    const hudBg = this.add.graphics();
    hudBg.fillStyle(pal.hud, 0.88);
    hudBg.fillRect(0, 0, w, 32);
    hudBg.lineStyle(1, pal.hudBorder, 0.6);
    hudBg.lineBetween(0, 32, w, 32);
    hudBg.setDepth(10);
    hudBg.setScrollFactor(0);

    // Title (left)
    const title = this.add.text(10, 8, this.packTitle.toUpperCase(), {
      fontFamily: '"Press Start 2P", "JetBrains Mono", monospace',
      fontSize: '9px',
      color: '#' + pal.textBright.toString(16).padStart(6, '0'),
    });
    title.setDepth(10).setScrollFactor(0);

    // Zone counter (center-right)
    const counter = this.add.text(w - 10, 8, `${completedCount}/${totalCount} ZONES`, {
      fontFamily: '"Press Start 2P", "JetBrains Mono", monospace',
      fontSize: '8px',
      color: '#' + pal.complete.toString(16).padStart(6, '0'),
    });
    counter.setOrigin(1, 0).setDepth(10).setScrollFactor(0);

    // Controls hint (bottom bar)
    const hintBg = this.add.graphics();
    hintBg.fillStyle(pal.hud, 0.88);
    hintBg.fillRect(0, h - 22, w, 22);
    hintBg.lineStyle(1, pal.hudBorder, 0.6);
    hintBg.lineBetween(0, h - 22, w, h - 22);
    hintBg.setDepth(10).setScrollFactor(0);

    const hint = this.add.text(w / 2, h - 12, 'WASD to move \u00b7 ENTER to enter zone', {
      fontFamily: '"Press Start 2P", "JetBrains Mono", monospace',
      fontSize: '7px',
      color: '#' + pal.text.toString(16).padStart(6, '0'),
      align: 'center',
    });
    hint.setOrigin(0.5, 0.5).setDepth(10).setScrollFactor(0);
  }

  // ── Movement ────────────────────────────────────────────────────────────────

  _updatePlayerMovement(delta) {
    let vx = 0, vy = 0;

    if (this.cursors.left.isDown  || this.wasd.left.isDown)  vx -= 1;
    if (this.cursors.right.isDown || this.wasd.right.isDown) vx += 1;
    if (this.cursors.up.isDown    || this.wasd.up.isDown)    vy -= 1;
    if (this.cursors.down.isDown  || this.wasd.down.isDown)  vy += 1;

    // Normalize diagonal
    if (vx !== 0 && vy !== 0) {
      vx *= 0.707;
      vy *= 0.707;
    }

    this.isMoving = (vx !== 0 || vy !== 0);

    // Update facing direction
    if (vx < 0) this.playerFacing = 'left';
    else if (vx > 0) this.playerFacing = 'right';
    else if (vy < 0) this.playerFacing = 'up';
    else if (vy > 0) this.playerFacing = 'down';

    const dt = delta / 1000;
    let nx = this.playerContainer.x + vx * PLAYER_SPEED * dt;
    let ny = this.playerContainer.y + vy * PLAYER_SPEED * dt;

    // World bounds
    const w = this.scale.width;
    const h = this.scale.height;
    nx = Phaser.Math.Clamp(nx, 12, w - 12);
    ny = Phaser.Math.Clamp(ny, 36, h - 26);  // Account for HUD

    // Building collision — slide along edges
    for (const b of this.buildingObjs) {
      const halfW = BUILDING_W / 2 + 6;
      const halfH = BUILDING_H / 2 + 6;
      const dx = nx - b.cx;
      const dy = ny - b.cy;

      if (Math.abs(dx) < halfW && Math.abs(dy) < halfH) {
        // Find which axis has least penetration and push out
        const overlapX = halfW - Math.abs(dx);
        const overlapY = halfH - Math.abs(dy);

        if (overlapX < overlapY) {
          nx += (dx > 0 ? overlapX : -overlapX);
        } else {
          ny += (dy > 0 ? overlapY : -overlapY);
        }
      }
    }

    this.playerContainer.x = nx;
    this.playerContainer.y = ny;
  }

  // ── Proximity detection ─────────────────────────────────────────────────────

  _updateProximity() {
    let closestDist = Infinity;
    let closestObj  = null;

    const px = this.playerContainer.x;
    const py = this.playerContainer.y;

    for (const b of this.buildingObjs) {
      const dist = Phaser.Math.Distance.Between(px, py, b.cx, b.cy);
      if (dist < PROXIMITY_DIST && dist < closestDist) {
        closestDist = dist;
        closestObj  = b;
      }
    }

    // Update highlights
    for (const b of this.buildingObjs) {
      const shouldGlow = (b === closestObj);
      if (shouldGlow && !b.isNear) {
        // Entering proximity
        b.isNear = true;
        this.tweens.add({ targets: b.glow,    alpha: 1, duration: 200 });
        this.tweens.add({ targets: b.prompt,   alpha: 1, duration: 200 });
        this.tweens.add({ targets: b.container, scaleX: 1.05, scaleY: 1.05, duration: 150, ease: 'Back.easeOut' });
      } else if (!shouldGlow && b.isNear) {
        // Leaving proximity
        b.isNear = false;
        this.tweens.add({ targets: b.glow,    alpha: 0, duration: 300 });
        this.tweens.add({ targets: b.prompt,   alpha: 0, duration: 300 });
        this.tweens.add({ targets: b.container, scaleX: 1, scaleY: 1, duration: 200 });
      }
    }

    this.nearZone = closestObj;
  }

  // ── Zone entry ──────────────────────────────────────────────────────────────

  _tryEnterZone() {
    if (!this.nearZone) return;
    if (this.nearZone.zone.locked) {
      // Flash the building red briefly
      this.tweens.add({
        targets: this.nearZone.container,
        x: this.nearZone.cx + 4,
        duration: 50,
        yoyo: true,
        repeat: 3,
        onComplete: () => { this.nearZone.container.x = this.nearZone.cx; }
      });
      return;
    }

    const zoneId = this.nearZone.zone.id;

    // Zoom-in transition effect
    this.cameras.main.flash(300, 255, 255, 255, true);
    this.cameras.main.zoomTo(2, 400, 'Power2');

    this.time.delayedCall(450, () => {
      this.onEnterZone(zoneId);
    });
  }

  // ── Animations ──────────────────────────────────────────────────────────────

  _updateAnimations(time, delta) {
    this.time_acc += delta;
    const t = this.time_acc / 1000;

    // Player walking bob
    if (this.isMoving) {
      this.playerBobTimer += delta;
      const bobUp = Math.sin(this.playerBobTimer / 100) > 0;
      this._drawPlayerSprite(this.pal.player, bobUp);
    } else {
      this.playerBobTimer = 0;
      this._drawPlayerSprite(this.pal.player, false);
    }

    // Building idle float
    for (const b of this.buildingObjs) {
      if (!b.isNear) {
        const float = Math.sin(t * 1.5 + b.cx * 0.01) * 2;
        b.container.y = b.cy + float;
      }
    }

    // Glow pulse for nearby building
    if (this.nearZone) {
      const pulse = 0.6 + Math.sin(t * 4) * 0.4;
      this.nearZone.glow.setAlpha(pulse);
    }

    // Ambient particles — gentle drift
    for (const p of this.ambientParticles) {
      const ox = Math.sin(t * p.speed + p.phase) * p.amplitude;
      const oy = Math.cos(t * p.speed * 0.7 + p.phase) * p.amplitude * 0.6;
      p.gfx.setPosition(p.baseX + ox, p.baseY + oy);
      p.gfx.setAlpha(0.2 + Math.sin(t * 2 + p.phase) * 0.2);

      // Wrap around
      if (p.gfx.x < -10) p.baseX += this.scale.width + 20;
      if (p.gfx.x > this.scale.width + 10) p.baseX -= this.scale.width + 20;
    }

    // Checkmark bounce on completed zones
    for (const b of this.buildingObjs) {
      if (b.checkmark) {
        const bounce = Math.sin(t * 3 + b.cx * 0.02) * 1.5;
        b.checkmark.y = -BUILDING_H / 2 - 4 + bounce;
      }
    }
  }

  // ── Helpers ─────────────────────────────────────────────────────────────────

  /**
   * Convert a zone's grid position (x, y) to pixel center coordinates.
   * Grid cells are spaced to fill the map with comfortable padding.
   */
  _zoneToCenterPos(zone) {
    const w = this.scale.width;
    const h = this.scale.height;

    // Determine grid bounds from all zones
    let maxGx = 0, maxGy = 0;
    for (const z of this.zones) {
      if (z.x > maxGx) maxGx = z.x;
      if (z.y > maxGy) maxGy = z.y;
    }

    // Padding: leave space for HUD top/bottom and left margin for player spawn
    const padLeft   = UNIT * 3;
    const padRight  = UNIT * 1.5;
    const padTop    = UNIT * 1.5;
    const padBottom = UNIT * 1;

    const usableW = w - padLeft - padRight;
    const usableH = h - padTop - padBottom;

    const cellW = maxGx > 0 ? usableW / maxGx : usableW;
    const cellH = maxGy > 0 ? usableH / maxGy : usableH;

    return {
      x: padLeft + (zone.x || 0) * cellW,
      y: padTop  + (zone.y || 0) * cellH,
    };
  }

  /**
   * Deterministic pseudo-random for decorative elements (consistent between frames).
   */
  _seededRandom(seed) {
    const x = Math.sin(seed * 127.1 + 311.7) * 43758.5453;
    return x - Math.floor(x);
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  PUBLIC API
// ═══════════════════════════════════════════════════════════════════════════════

window.QuestOverworld = {
  /** Phaser game instance (set after init) */
  game: null,

  /**
   * Initialize the overworld in the given container element.
   *
   * @param {string} containerId - DOM element ID to host the Phaser canvas
   * @returns {Phaser.Game} The Phaser game instance
   */
  init(containerId) {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`[QuestOverworld] Container #${containerId} not found`);
      return null;
    }

    // Responsive sizing: fill container width, max 800px, 16:9 aspect
    const maxWidth  = 800;
    const containerWidth = Math.min(container.clientWidth || maxWidth, maxWidth);
    const width  = containerWidth;
    const height = Math.round(width * (9 / 16));

    const config = {
      type: Phaser.AUTO,
      parent: containerId,
      width,
      height,
      pixelArt: true,                   // Crisp pixel scaling
      antialias: false,
      roundPixels: true,
      backgroundColor: '#000000',
      scale: {
        mode: Phaser.Scale.FIT,          // Scale to fit container
        autoCenter: Phaser.Scale.CENTER_HORIZONTALLY,
        max: { width: maxWidth, height: Math.round(maxWidth * 9 / 16) },
      },
      scene: [OverworldScene],
      // Disable physics — we do our own simple collision
      physics: { default: false },
      // Remove Phaser banner
      banner: false,
    };

    this.game = new Phaser.Game(config);

    // Handle window resize
    const onResize = () => {
      const newWidth = Math.min(container.clientWidth || maxWidth, maxWidth);
      const newHeight = Math.round(newWidth * 9 / 16);
      if (this.game) {
        this.game.scale.resize(newWidth, newHeight);
      }
    };
    window.addEventListener('resize', Phaser.Utils.Function.Debounce(onResize, 250, false));

    return this.game;
  },

  /**
   * Destroy the overworld and clean up.
   */
  destroy() {
    if (this.game) {
      this.game.destroy(true);
      this.game = null;
    }
  },
};
