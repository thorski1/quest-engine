/**
 * platformer.js — Mario-style side-scrolling quiz platformer.
 * Built on Phaser 3 using ONLY generated graphics (no sprites/images).
 *
 * Based on verified Phaser patterns from official docs + examples.
 * Key: this.add.rectangle() + this.physics.add.existing() + explicit colliders.
 */

const QuestPlatformer = (() => {

  const PALETTES = {
    cyberpunk:  { sky: '#08111f', ground: '#0f2240', platform: '#1a3a5f', player: '#00e5a0', coin: '#ffd700', qblock: '#ffa500', text: '#e8f4ff', hurt: '#ff3c78' },
    playful:    { sky: '#c8e0ff', ground: '#8b6914', platform: '#6c5ce7', player: '#6c5ce7', coin: '#ffd700', qblock: '#ffa500', text: '#2d1b4e', hurt: '#ff7043' },
    neural:     { sky: '#0c0c1e', ground: '#1a1a40', platform: '#7c6cf0', player: '#22d3ee', coin: '#ffd700', qblock: '#ffa500', text: '#ededff', hurt: '#f472b6' },
    medieval:   { sky: '#1a1209', ground: '#2a1f10', platform: '#6b4f30', player: '#d4a843', coin: '#ffd700', qblock: '#ffa500', text: '#f0e6d0', hurt: '#cc3333' },
    unicorn:    { sky: '#1a0825', ground: '#251038', platform: '#6a3090', player: '#e040fb', coin: '#ffd700', qblock: '#ffa500', text: '#f8f0ff', hurt: '#ff6090' },
    alien:      { sky: '#050510', ground: '#0a0a20', platform: '#1a1a50', player: '#39ff14', coin: '#ffd700', qblock: '#ffa500', text: '#e0e0ff', hurt: '#ff1493' },
    ocean:      { sky: '#041825', ground: '#0c2a3d', platform: '#15405a', player: '#00c9db', coin: '#ffd700', qblock: '#ffa500', text: '#e0f4ff', hurt: '#ff7043' },
    sunset:     { sky: '#1a0a1e', ground: '#351838', platform: '#502850', player: '#ff6b35', coin: '#ffd700', qblock: '#ffa500', text: '#fff0f8', hurt: '#ff3366' },
  };

  function hexToNum(hex) { return parseInt(hex.replace('#', ''), 16); }

  let game = null;

  class GameScene extends Phaser.Scene {
    constructor() { super('GameScene'); }

    init() {
      const cfg = window.QUEST_PLATFORMER_CONFIG || {};
      this.challenges = cfg.challenges || [];
      this.pal = PALETTES[cfg.theme] || PALETTES.cyberpunk;
      this.onComplete = cfg.onComplete || function(){};
      this.onFail = cfg.onFail || function(){};
      this.zoneName = cfg.zoneName || 'Level';
      this.solved = 0;
      this.hearts = 3;
      this.xpCollected = 0;
      this.isQuizOpen = false;
      this.facingRight = true;
    }

    create() {
      const W = this.scale.width;
      const H = this.scale.height;
      const WORLD_W = Math.max(W * 3, (this.challenges.length + 2) * 300);

      // World + camera bounds
      this.physics.world.setBounds(0, 0, WORLD_W, H);
      this.cameras.main.setBounds(0, 0, WORLD_W, H);
      this.cameras.main.setBackgroundColor(this.pal.sky);

      // ═══ GROUND ═══
      const groundY = H - 20;
      this.groundParts = [];
      for (let x = 0; x < WORLD_W; x += 64) {
        const g = this.add.rectangle(x + 32, groundY, 64, 40, hexToNum(this.pal.ground));
        this.physics.add.existing(g, true);
        this.groundParts.push(g);
      }

      // ═══ PLATFORMS + QUESTION BLOCKS ═══
      this.platformParts = [];
      this.qBlocks = [];
      const spacing = (WORLD_W - 200) / (this.challenges.length + 1);

      this.challenges.forEach((ch, i) => {
        const px = 200 + spacing * (i + 1);
        const py = groundY - 100 - Math.sin(i * 0.8) * 40 - (i % 3) * 30;

        // Platform rectangle
        const plat = this.add.rectangle(px, py, 120, 16, hexToNum(this.pal.platform));
        this.physics.add.existing(plat, true);
        this.platformParts.push(plat);

        // Question block on top of platform
        const qb = this.add.rectangle(px, py - 24, 28, 28, hexToNum(this.pal.qblock));
        qb.setStrokeStyle(2, 0xcc8800);
        const qt = this.add.text(px, py - 24, '?', {
          fontSize: '16px', fontFamily: 'monospace', color: '#000', fontStyle: 'bold',
        }).setOrigin(0.5);

        // Float animation
        this.tweens.add({
          targets: [qb, qt], y: py - 28,
          duration: 700 + i * 80, yoyo: true, repeat: -1, ease: 'Sine.easeInOut',
        });

        this.qBlocks.push({ block: qb, text: qt, challenge: ch, x: px, y: py, answered: false });
      });

      // ═══ COINS ═══
      this.coinObjects = [];
      for (let i = 0; i < this.challenges.length * 3; i++) {
        const cx = 150 + Math.random() * (WORLD_W - 300);
        const cy = groundY - 60 - Math.random() * 80;
        const coin = this.add.circle(cx, cy, 5, hexToNum(this.pal.coin));
        this.physics.add.existing(coin, true);
        this.coinObjects.push(coin);
        this.tweens.add({
          targets: coin, y: cy - 4, duration: 500 + Math.random() * 300,
          yoyo: true, repeat: -1, ease: 'Sine.easeInOut',
        });
      }

      // ═══ PLAYER ═══
      this.player = this.add.rectangle(80, groundY - 60, 24, 32, hexToNum(this.pal.player));
      this.physics.add.existing(this.player);
      this.player.body.setBounce(0.1);
      this.player.body.setCollideWorldBounds(true);

      // Player eyes
      this.eyeL = this.add.circle(0, 0, 3, 0xffffff);
      this.eyeR = this.add.circle(0, 0, 3, 0xffffff);
      this.pupilL = this.add.circle(0, 0, 1.5, 0x000000);
      this.pupilR = this.add.circle(0, 0, 1.5, 0x000000);

      // ═══ COLLIDERS (explicit — required for physics to work) ═══
      this.groundParts.forEach(g => this.physics.add.collider(this.player, g));
      this.platformParts.forEach(p => this.physics.add.collider(this.player, p));
      this.coinObjects.forEach(c => {
        this.physics.add.overlap(this.player, c, () => {
          c.destroy();
          this.xpCollected += 5;
          this.updateHUD();
        });
      });

      // ═══ CAMERA ═══
      this.cameras.main.startFollow(this.player, true, 0.08, 0.08);

      // ═══ INPUT ═══
      this.cursors = this.input.keyboard.createCursorKeys();
      this.keyW = this.input.keyboard.addKey('W');
      this.keyA = this.input.keyboard.addKey('A');
      this.keyD = this.input.keyboard.addKey('D');
      this.keyE = this.input.keyboard.addKey('E');
      this.keyEnter = this.input.keyboard.addKey('ENTER');

      // ═══ HUD (fixed to camera) ═══
      this.hudHearts = this.add.text(12, 12, '', { fontSize: '18px' }).setScrollFactor(0).setDepth(10);
      this.hudCoins = this.add.text(12, 36, '', { fontSize: '14px', color: this.pal.coin }).setScrollFactor(0).setDepth(10);
      this.hudProgress = this.add.text(W - 12, 12, '', { fontSize: '12px', color: '#888' }).setOrigin(1, 0).setScrollFactor(0).setDepth(10);
      this.hudZone = this.add.text(W - 12, 30, this.zoneName, { fontSize: '11px', color: '#666' }).setOrigin(1, 0).setScrollFactor(0).setDepth(10);
      this.hudPrompt = this.add.text(W / 2, H - 30, '', { fontSize: '12px', color: this.pal.text }).setOrigin(0.5).setScrollFactor(0).setDepth(10);
      this.updateHUD();

      // ═══ QUIZ OVERLAY (created once, reused) ═══
      this.quizContainer = this.add.container(0, 0).setScrollFactor(0).setDepth(20).setVisible(false);
    }

    update() {
      if (this.isQuizOpen) return;

      const body = this.player.body;

      // Movement
      if (this.cursors.left.isDown || this.keyA.isDown) {
        body.setVelocityX(-180);
        this.facingRight = false;
      } else if (this.cursors.right.isDown || this.keyD.isDown) {
        body.setVelocityX(180);
        this.facingRight = true;
      } else {
        body.setVelocityX(0);
      }

      // Jump
      if ((this.cursors.up.isDown || this.keyW.isDown) && body.touching.down) {
        body.setVelocityY(-320);
      }

      // Update eyes
      const px = this.player.x;
      const py = this.player.y;
      const dir = this.facingRight ? 1 : -1;
      this.eyeL.setPosition(px - 4 * dir, py - 6);
      this.eyeR.setPosition(px + 4 * dir, py - 6);
      this.pupilL.setPosition(px - 4 * dir + dir, py - 6);
      this.pupilR.setPosition(px + 4 * dir + dir, py - 6);

      // Check proximity to question blocks
      let nearBlock = null;
      this.qBlocks.forEach(qb => {
        if (!qb.answered && Math.abs(px - qb.x) < 50 && Math.abs(py - qb.y) < 60) {
          nearBlock = qb;
        }
      });

      if (nearBlock) {
        this.hudPrompt.setText('Press E or ENTER to answer');
        if (Phaser.Input.Keyboard.JustDown(this.keyE) || Phaser.Input.Keyboard.JustDown(this.keyEnter)) {
          this.openQuiz(nearBlock);
        }
      } else {
        this.hudPrompt.setText('');
      }
    }

    updateHUD() {
      this.hudHearts.setText('❤️'.repeat(this.hearts) + '🖤'.repeat(3 - this.hearts));
      this.hudCoins.setText('⭐ ' + this.xpCollected + ' XP');
      this.hudProgress.setText(this.solved + '/' + this.challenges.length);
    }

    openQuiz(qb) {
      this.isQuizOpen = true;
      this.player.body.setVelocity(0, 0);

      const W = this.scale.width;
      const H = this.scale.height;
      const ch = qb.challenge;

      this.quizContainer.removeAll(true);

      // Dark backdrop
      const bg = this.add.rectangle(W/2, H/2, W - 40, H - 60, 0x000000, 0.9);
      bg.setStrokeStyle(2, hexToNum(this.pal.platform));
      this.quizContainer.add(bg);

      // Question text
      const q = (ch.question || ch.prompt || '?').replace(/\[.*?\]/g, ''); // strip Rich markup
      const qText = this.add.text(W/2, 60, q, {
        fontSize: '15px', fontFamily: 'sans-serif', color: '#ffffff',
        wordWrap: { width: W - 100 }, align: 'center', lineSpacing: 4,
      }).setOrigin(0.5, 0);
      this.quizContainer.add(qText);

      // Options
      const options = ch.options || [];
      const letters = ['A', 'B', 'C', 'D'];
      options.forEach((opt, i) => {
        const oy = 140 + i * 55;
        const optBg = this.add.rectangle(W/2, oy, W - 80, 42, 0x1a2a4a, 0.9)
          .setStrokeStyle(1, hexToNum(this.pal.platform))
          .setInteractive({ useHandCursor: true });
        const optText = this.add.text(W/2, oy, letters[i] + ') ' + opt, {
          fontSize: '13px', fontFamily: 'sans-serif', color: '#ffffff',
        }).setOrigin(0.5);

        optBg.on('pointerover', () => { optBg.setFillStyle(hexToNum(this.pal.platform), 0.8); });
        optBg.on('pointerout', () => { optBg.setFillStyle(0x1a2a4a, 0.9); });
        optBg.on('pointerdown', () => { this.submitAnswer(qb, letters[i].toLowerCase()); });

        this.quizContainer.add([optBg, optText]);
      });

      // Keyboard answer listeners
      this._quizKeys = [];
      ['A', 'B', 'C', 'D'].forEach((k, i) => {
        const key = this.input.keyboard.addKey(k);
        const handler = () => {
          if (this.isQuizOpen) this.submitAnswer(qb, ['a','b','c','d'][i]);
        };
        key.once('down', handler);
        this._quizKeys.push(key);
      });

      this.quizContainer.setVisible(true);
    }

    submitAnswer(qb, answer) {
      const correct = answer === (qb.challenge.answer || '').toLowerCase();

      this.quizContainer.setVisible(false);
      this.isQuizOpen = false;

      if (correct) {
        qb.answered = true;
        qb.block.setFillStyle(0x00cc44);
        qb.text.setText('✓');
        this.solved++;
        this.xpCollected += (qb.challenge.xp || 25);
        this.updateHUD();
        this.cameras.main.flash(150, 0, 200, 100);

        if (this.solved >= this.challenges.length) {
          this.time.delayedCall(600, () => {
            this.onComplete({ coins: this.xpCollected, hearts: this.hearts });
          });
        }
      } else {
        this.hearts--;
        this.updateHUD();
        this.cameras.main.shake(200, 0.008);
        this.player.setFillStyle(hexToNum(this.pal.hurt));
        this.time.delayedCall(300, () => {
          this.player.setFillStyle(hexToNum(this.pal.player));
        });

        if (this.hearts <= 0) {
          this.time.delayedCall(600, () => {
            this.onFail({ coins: this.xpCollected });
          });
        }
      }
    }
  }

  return {
    init(containerId) {
      const el = document.getElementById(containerId);
      if (!el) { console.error('Container not found:', containerId); return; }

      const w = Math.min(el.clientWidth || 800, 800);
      const h = Math.round(w * 9 / 16);

      game = new Phaser.Game({
        type: Phaser.AUTO,
        width: w,
        height: h,
        parent: containerId,
        backgroundColor: '#000',
        physics: {
          default: 'arcade',
          arcade: { gravity: { y: 500 }, debug: false },
        },
        scene: GameScene,
        scale: { mode: Phaser.Scale.FIT, autoCenter: Phaser.Scale.CENTER_BOTH },
      });
    },
    destroy() { if (game) { game.destroy(true); game = null; } },
  };
})();

if (typeof window !== 'undefined') window.QuestPlatformer = QuestPlatformer;
