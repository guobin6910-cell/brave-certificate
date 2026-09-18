/*:
 * @target MZ
 * @plugindesc v1.0 免費版動態側視圖敵人 - 讓 sv_enemies 多幀圖自動播放揮刀
 * @author MetaAI Free
 * @help
 * === 免費版 Animated SV Enemies ===
 * 讓 img/sv_enemies/ 裡的 1536x512 (3幀) 自動切片播放。
 *
 * 在 資料庫 > 敵人 > 備註 寫：
 *
 *   <Sideview Battler: 01_goblin_warrior_attack_sheet_RIGHT>
 *   <Sideview Battler Frames: 3>
 *   <Sideview Battler Speed: 12>
 *   <Scale: 25%>
 *
 * 說明：
 * - Sideview Battler: 檔名 (不含.png)，放在 img/sv_enemies/
 * - Frames: 幾幀，橫向切，你的 3合1 就寫 3
 * - Speed: 數字越大越慢，8=快 12=正常 20=慢
 * - Scale: 可沿用之前的縮放，25% 適合你的 20隻怪
 */

(() => {
  function parseNote(note, regex, defVal) {
    const m = note.match(regex);
    return m ? m[1].trim() : defVal;
  }

  const _Sprite_Enemy_setBattler = Sprite_Enemy.prototype.setBattler;
  Sprite_Enemy.prototype.setBattler = function(battler) {
    _Sprite_Enemy_setBattler.call(this, battler);
    if (!battler || !battler.enemy) return;
    try {
      const enemy = battler.enemy();
      const note = enemy.note || "";

      let scale = null;
      let sm = note.match(/<\s*Scale\s*:\s*(\d+)\s*%?\s*>/i);
      if (sm) {
        let v = parseFloat(sm[1]);
        scale = v > 1 ? v / 100 : v;
      } else {
        sm = note.match(/<\s*Scale\s*:\s*([\d.]+)\s*>/i);
        if (sm) {
          let v = parseFloat(sm[1]);
          scale = v > 1 ? v / 100 : v;
        }
      }
      this._enemyScale = scale;

      const battlerName = parseNote(note, /<\s*Sideview Battler\s*:\s*(.+?)\s*>/i, null);
      if (battlerName) {
        this._svBattlerName = battlerName;
        const frames = parseInt(parseNote(note, /<\s*Sideview Battler Frames\s*:\s*(\d+)\s*>/i, "3"), 10);
        const speed = parseInt(parseNote(note, /<\s*Sideview Battler Speed\s*:\s*(\d+)\s*>/i, "12"), 10);
        this._svFrames = Math.max(1, frames);
        this._svSpeed = Math.max(1, speed);
        this._svAnimated = this._svFrames > 1;
        this._svFrameIndex = 0;
        this._svTick = 0;

        if (ImageManager.loadSvEnemy) {
          this.bitmap = ImageManager.loadSvEnemy(this._svBattlerName, 0);
        } else {
          this.bitmap = ImageManager.loadBitmap("img/sv_enemies/", this._svBattlerName, 0, true);
        }
      } else {
        this._svAnimated = false;
        this._svBattlerName = null;
      }
    } catch (e) {
      console.error("AnimatedSVEnemiesFree parse error", e);
    }
  };

  const _Sprite_Enemy_update = Sprite_Enemy.prototype.update;
  Sprite_Enemy.prototype.update = function() {
    _Sprite_Enemy_update.call(this);
    if (this._enemyScale) {
      this.scale.x = this._enemyScale;
      this.scale.y = this._enemyScale;
    }
    if (this._svAnimated && this.bitmap && this.bitmap.isReady()) {
      this._svTick++;
      if (this._svTick >= this._svSpeed) {
        this._svTick = 0;
        this._svFrameIndex = (this._svFrameIndex + 1) % this._svFrames;
      }
      const totalW = this.bitmap.width;
      const totalH = this.bitmap.height;
      const frameW = Math.floor(totalW / this._svFrames);
      const frameH = totalH;
      const frameX = this._svFrameIndex * frameW;
      this.setFrame(frameX, 0, frameW, frameH);
    }
  };
})();
