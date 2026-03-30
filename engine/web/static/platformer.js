/**
 * platformer.js — Mario-style side-scrolling level engine for quest-engine.
 * Built on Phaser 3. Each zone becomes a platformer level where:
 * - Platforms contain quiz questions (answer to unlock the next platform)
 * - Coins (XP) scattered through the level
 * - Wrong answers = lose a heart
 * - Boss challenge at the end
 *
 * Usage:
 *   window.QUEST_PLATFORMER_CONFIG = { zone, challenges, theme, onComplete, onFail };
 *   QuestPlatformer.init('container-id');
 */

const QuestPlatformer = (() => {

  // Theme color palettes
  const PALETTES = {
    cyberpunk:  { sky: 0x08111f, ground: 0x0f2240, platform: 0x1a3a5f, player: 0x00e5a0, coin: 0xffd700, enemy: 0xff3c78, text: 0xe8f4ff },
    playful:    { sky: 0xd4e6ff, ground: 0x8b6914, platform: 0x6c5ce7, player: 0x6c5ce7, coin: 0xffd700, enemy: 0xff7043, text: 0x2d1b4e },
    neural:     { sky: 0x0c0c1e, ground: 0x1a1a40, platform: 0x7c6cf0, player: 0x7c6cf0, coin: 0xffd700, enemy: 0xf472b6, text: 0xededff },
    medieval:   { sky: 0x1a1209, ground: 0x2a1f10, platform: 0xd4a843, player: 0xd4a843, coin: 0xffd700, enemy: 0xcc3333, text: 0xf0e6d0 },
    unicorn:    { sky: 0x1a0825, ground: 0x251038, platform: 0xe040fb, player: 0xe040fb, coin: 0xffd700, enemy: 0xff6090, text: 0xf8f0ff },
    alien:      { sky: 0x050510, ground: 0x0a0a20, platform: 0x39ff14, player: 0x39ff14, coin: 0xffd700, enemy: 0xff1493, text: 0xe0e0ff },
    ocean:      { sky: 0x041825, ground: 0x082030, platform: 0x00c9db, player: 0x00c9db, coin: 0xffd700, enemy: 0xff7043, text: 0xe0f4ff },
    sunset:     { sky: 0x1a0a1e, ground: 0x28102a, platform: 0xff6b35, player: 0xff6b35, coin: 0xffd700, enemy: 0xff3366, text: 0xfff0f8 },
  };

  let game = null;

  class PlatformerScene extends Phaser.Scene {
    constructor() {
      super('PlatformerScene');
    }

    init() {
      const cfg = window.QUEST_PLATFORMER_CONFIG || {};
      this.challenges = cfg.challenges || [];
      this.themeName = cfg.theme || 'cyberpunk';
      this.palette = PALETTES[this.themeName] || PALETTES.cyberpunk;
      this.onComplete = cfg.onComplete || function() {};
      this.onFail = cfg.onFail || function() {};
      this.zoneName = cfg.zoneName || 'Level';
      this.currentChallenge = 0;
      this.hearts = 3;
      this.coins = 0;
      this.answering = false;
    }

    create() {
      const W = this.scale.width;
      const H = this.scale.height;
      const P = this.palette;

      // Sky gradient
      const skyGfx = this.add.graphics();
      skyGfx.fillGradientStyle(P.sky, P.sky, P.ground, P.ground);
      skyGfx.fillRect(0, 0, W * 4, H);
      skyGfx.setScrollFactor(0.3);

      // Camera
      this.cameras.main.setBounds(0, 0, W * 4, H);
      this.physics.world.setBounds(0, 0, W * 4, H);

      // Ground
      this.ground = this.physics.add.staticGroup();
      for (let x = 0; x < W * 4; x += 64) {
        const g = this.add.rectangle(x + 32, H - 16, 64, 32, P.ground);
        this.physics.add.existing(g, true);
        this.ground.add(g);
      }

      // Platforms — one per challenge, spread across the level
      this.platforms = this.physics.add.staticGroup();
      this.questionBlocks = [];
      const spacing = (W * 3) / (this.challenges.length + 1);

      this.challenges.forEach((ch, i) => {
        const px = spacing * (i + 1);
        const py = H - 120 - Math.sin(i * 0.7) * 60;

        // Platform
        const plat = this.add.rectangle(px, py, 100, 16, P.platform);
        this.physics.add.existing(plat, true);
        this.platforms.add(plat);

        // Question block on platform
        const qBlock = this.add.rectangle(px, py - 24, 32, 32, 0xffd700);
        qBlock.setStrokeStyle(2, 0xffa000);
        const qText = this.add.text(px, py - 24, '?', {
          fontSize: '18px', fontFamily: 'monospace', color: '#000', fontStyle: 'bold'
        }).setOrigin(0.5);

        // Floating animation
        this.tweens.add({
          targets: [qBlock, qText],
          y: py - 28,
          duration: 800 + i * 100,
          yoyo: true,
          repeat: -1,
          ease: 'Sine.easeInOut',
        });

        this.questionBlocks.push({
          block: qBlock, text: qText, platform: plat,
          challenge: ch, index: i, answered: false, x: px, y: py,
        });
      });

      // Coins between platforms
      this.coinGroup = this.physics.add.group();
      for (let i = 0; i < this.challenges.length * 3; i++) {
        const cx = 150 + i * (W * 3 / (this.challenges.length * 3));
        const cy = H - 100 - Math.random() * 80;
        const coin = this.add.circle(cx, cy, 6, P.coin);
        this.physics.add.existing(coin, true);
        this.coinGroup.add(coin);

        this.tweens.add({
          targets: coin,
          y: cy - 5,
          duration: 600 + Math.random() * 400,
          yoyo: true,
          repeat: -1,
          ease: 'Sine.easeInOut',
        });
      }

      // Player
      this.player = this.add.rectangle(80, H - 60, 24, 32, P.player);
      this.physics.add.existing(this.player);
      this.player.body.setBounce(0.1);
      this.player.body.setCollideWorldBounds(true);

      // Eyes
      this.playerEyes = this.add.group();
      const eyeL = this.add.circle(-4, -6, 3, 0xffffff).setOrigin(0.5);
      const eyeR = this.add.circle(4, -6, 3, 0xffffff).setOrigin(0.5);
      const pupilL = this.add.circle(-4, -6, 1.5, 0x000000).setOrigin(0.5);
      const pupilR = this.add.circle(4, -6, 1.5, 0x000000).setOrigin(0.5);
      this.eyeContainer = this.add.container(80, H - 60, [eyeL, eyeR, pupilL, pupilR]);

      // Collisions
      this.physics.add.collider(this.player, this.ground);
      this.physics.add.collider(this.player, this.platforms);
      this.physics.add.overlap(this.player, this.coinGroup, this.collectCoin, null, this);

      // Camera follow
      this.cameras.main.startFollow(this.player, true, 0.1, 0.1);

      // Controls
      this.cursors = this.input.keyboard.createCursorKeys();
      this.wasd = this.input.keyboard.addKeys('W,A,S,D');
      this.spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

      // HUD (fixed to camera)
      this.heartsText = this.add.text(16, 16, this.getHeartsDisplay(), {
        fontSize: '20px', fontFamily: 'monospace',
      }).setScrollFactor(0);

      this.coinsText = this.add.text(16, 42, '🪙 0', {
        fontSize: '16px', fontFamily: 'monospace', color: '#ffd700',
      }).setScrollFactor(0);

      this.zoneText = this.add.text(W - 16, 16, this.zoneName, {
        fontSize: '14px', fontFamily: 'monospace', color: '#' + P.text.toString(16).padStart(6, '0'),
      }).setOrigin(1, 0).setScrollFactor(0);

      this.progressText = this.add.text(W - 16, 36, `0/${this.challenges.length}`, {
        fontSize: '12px', fontFamily: 'monospace', color: '#888',
      }).setOrigin(1, 0).setScrollFactor(0);

      // Quiz overlay (hidden initially)
      this.quizOverlay = this.add.container(W / 2, H / 2).setScrollFactor(0).setVisible(false).setDepth(100);
    }

    update() {
      if (this.answering) return;

      const left = this.cursors.left.isDown || this.wasd.A.isDown;
      const right = this.cursors.right.isDown || this.wasd.D.isDown;
      const jump = Phaser.Input.Keyboard.JustDown(this.cursors.up) ||
                   Phaser.Input.Keyboard.JustDown(this.wasd.W) ||
                   Phaser.Input.Keyboard.JustDown(this.spaceKey);

      if (left) {
        this.player.body.setVelocityX(-200);
      } else if (right) {
        this.player.body.setVelocityX(200);
      } else {
        this.player.body.setVelocityX(0);
      }

      if (jump && this.player.body.touching.down) {
        this.player.body.setVelocityY(-350);
      }

      // Update eyes position
      this.eyeContainer.setPosition(this.player.x, this.player.y);

      // Check proximity to question blocks
      this.questionBlocks.forEach(qb => {
        if (!qb.answered && Math.abs(this.player.x - qb.x) < 50 && Math.abs(this.player.y - qb.y) < 60) {
          if (Phaser.Input.Keyboard.JustDown(this.input.keyboard.addKey('E')) ||
              Phaser.Input.Keyboard.JustDown(this.input.keyboard.addKey('ENTER'))) {
            this.showQuiz(qb);
          }
        }
      });
    }

    collectCoin(player, coin) {
      coin.destroy();
      this.coins++;
      this.coinsText.setText('🪙 ' + this.coins);
    }

    getHeartsDisplay() {
      return '❤️'.repeat(this.hearts) + '🖤'.repeat(3 - this.hearts);
    }

    showQuiz(qb) {
      this.answering = true;
      this.player.body.setVelocity(0, 0);

      const W = this.scale.width;
      const H = this.scale.height;
      const ch = qb.challenge;

      // Build overlay
      this.quizOverlay.removeAll(true);

      // Background
      const bg = this.add.rectangle(0, 0, W - 80, H - 100, 0x000000, 0.85);
      bg.setStrokeStyle(2, this.palette.platform);
      this.quizOverlay.add(bg);

      // Question
      const qText = this.add.text(0, -H / 2 + 80, ch.question || ch.prompt || '?', {
        fontSize: '16px', fontFamily: 'sans-serif', color: '#ffffff',
        wordWrap: { width: W - 140 }, align: 'center',
      }).setOrigin(0.5, 0);
      this.quizOverlay.add(qText);

      // Options
      const options = ch.options || [];
      const letters = ['A', 'B', 'C', 'D'];
      options.forEach((opt, i) => {
        const y = -20 + i * 50;
        const optBg = this.add.rectangle(0, y, W - 140, 40, 0x1a3a5f)
          .setStrokeStyle(1, this.palette.platform)
          .setInteractive({ useHandCursor: true });

        const optText = this.add.text(0, y, `${letters[i]}) ${opt}`, {
          fontSize: '14px', fontFamily: 'sans-serif', color: '#ffffff',
        }).setOrigin(0.5);

        optBg.on('pointerover', () => optBg.setFillStyle(this.palette.platform));
        optBg.on('pointerout', () => optBg.setFillStyle(0x1a3a5f));
        optBg.on('pointerdown', () => this.answerQuiz(qb, letters[i].toLowerCase(), optBg));

        this.quizOverlay.add([optBg, optText]);
      });

      // Also allow keyboard answers
      ['A', 'B', 'C', 'D', 'ONE', 'TWO', 'THREE', 'FOUR'].forEach((key, i) => {
        const letter = ['a', 'b', 'c', 'd'][i % 4];
        this.input.keyboard.once('keydown-' + key, () => {
          if (this.answering) this.answerQuiz(qb, letter);
        });
      });

      this.quizOverlay.setVisible(true);
    }

    answerQuiz(qb, answer) {
      const ch = qb.challenge;
      const correct = answer === (ch.answer || '').toLowerCase();

      if (correct) {
        // Correct!
        qb.answered = true;
        qb.block.setFillStyle(0x00ff00);
        qb.text.setText('✓');
        this.currentChallenge++;
        this.coins += ch.xp || 25;
        this.coinsText.setText('🪙 ' + this.coins);
        this.progressText.setText(`${this.currentChallenge}/${this.challenges.length}`);

        // Flash green
        this.cameras.main.flash(200, 0, 255, 100);

        // Check level complete
        if (this.currentChallenge >= this.challenges.length) {
          this.time.delayedCall(500, () => {
            this.onComplete({ coins: this.coins, hearts: this.hearts });
          });
        }
      } else {
        // Wrong!
        this.hearts--;
        this.heartsText.setText(this.getHeartsDisplay());
        this.cameras.main.shake(200, 0.01);

        if (this.hearts <= 0) {
          this.time.delayedCall(500, () => {
            this.onFail({ coins: this.coins });
          });
        }
      }

      // Close overlay
      this.quizOverlay.setVisible(false);
      this.answering = false;
    }
  }

  function init(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const width = Math.min(container.clientWidth || 800, 800);
    const height = Math.round(width * 9 / 16);

    game = new Phaser.Game({
      type: Phaser.AUTO,
      width: width,
      height: height,
      parent: containerId,
      backgroundColor: '#000000',
      physics: {
        default: 'arcade',
        arcade: { gravity: { y: 600 }, debug: false },
      },
      scene: PlatformerScene,
      scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH,
      },
    });
  }

  function destroy() {
    if (game) { game.destroy(true); game = null; }
  }

  return { init, destroy };
})();

if (typeof window !== 'undefined') window.QuestPlatformer = QuestPlatformer;
