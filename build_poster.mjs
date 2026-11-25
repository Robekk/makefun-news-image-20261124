// Hybrid renderer for make.fun image entries — v10 proof.
// Architecture: Skia Canvas (vector scenes, native gradients/shadows, real font
// shaping) at 2048x2048 -> Sharp (libvips) lanczos3 downscale to 1024 final.
// No per-pixel JS loops anywhere. Layout/data mirror build_poster9.py (v9).
import { Canvas, FontLibrary } from 'skia-canvas';
import sharp from 'sharp';
import { readFileSync } from 'fs';

const FD = '/usr/share/fonts/truetype/noto/';
FontLibrary.use('SerifXB', FD + 'NotoSerif-ExtraBold.ttf');
FontLibrary.use('SerifB', FD + 'NotoSerif-Bold.ttf');
FontLibrary.use('SansB', FD + 'NotoSans-Bold.ttf');
FontLibrary.use('SansSB', FD + 'NotoSans-SemiBold.ttf');
FontLibrary.use('Sans', FD + 'NotoSans-Regular.ttf');

const S = 2, W = 1024, H = 1024;
const canvas = new Canvas(W * S, H * S);
const ctx = canvas.getContext('2d');
ctx.scale(S, S);

const BG = '#f6f1e3', INK = '#14304f', RED = '#c52d28', NAVY = '#102a46', GREY = '#777777';
const GOLD = '#b77a12', GOLDL = '#d9a83f';
const ZA = '#174b80', ZB = '#c52d28', ZC = '#b77a12';
const LAND = '#f3ecd7', SEA = '#c7d8ea';

const F = (fam, px) => `${px}px "${fam}"`;
function text(str, x, y, font, fill, align = 'left') {
  ctx.font = font; ctx.fillStyle = fill; ctx.textAlign = align; ctx.textBaseline = 'top';
  ctx.fillText(str, x, y);
}
function tw(str, font) { ctx.font = font; return ctx.measureText(str).width; }
function wrap(str, font, width) {
  const words = str.split(' '); const lines = []; let cur = '';
  for (const w of words) {
    const t = cur ? cur + ' ' + w : w;
    if (tw(t, font) <= width) cur = t; else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  return lines;
}
function wrap2(str, font, wFirst, wRest) {
  const words = str.split(' '); const lines = []; let cur = ''; let width = wFirst;
  for (const w of words) {
    const t = cur ? cur + ' ' + w : w;
    if (tw(t, font) <= width) cur = t; else { lines.push(cur); cur = w; width = wRest; }
  }
  if (cur) lines.push(cur);
  return lines;
}
function block(str, x, y, font, width, leading, fill) {
  for (const ln of wrap(str, font, width)) { text(ln, x, y, font, fill); y += leading; }
  return y;
}
function rect(x, y, w, h, fill) { ctx.fillStyle = fill; ctx.fillRect(x, y, w, h); }
function srect(x, y, w, h, fill, lw = 1) { ctx.strokeStyle = fill; ctx.lineWidth = lw; ctx.strokeRect(x, y, w, h); }
function ell(cx, cy, rx, ry, fill) { ctx.fillStyle = fill; ctx.beginPath(); ctx.ellipse(cx, cy, rx, ry, 0, 0, Math.PI * 2); ctx.fill(); }
function line(pts, stroke, lw = 1) {
  ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.beginPath();
  pts.forEach(([px, py], i) => i ? ctx.lineTo(px, py) : ctx.moveTo(px, py)); ctx.stroke();
}
function poly(pts, fill) {
  ctx.fillStyle = fill; ctx.beginPath();
  pts.forEach(([px, py], i) => i ? ctx.lineTo(px, py) : ctx.moveTo(px, py)); ctx.closePath(); ctx.fill();
}
function vgrad(x, y, w, h, top, bot) { ctx.fillStyle = top; ctx.fillRect(x, y, w, h); } // FLAT: solid fill only
function rrs(x, y, w, h, r, fill, lw = 1) { ctx.strokeStyle = fill; ctx.lineWidth = lw; ctx.beginPath(); ctx.roundRect(x, y, w, h, r); ctx.stroke(); }
function rr(x, y, w, h, r, fill) {
  ctx.fillStyle = fill; ctx.beginPath(); ctx.roundRect(x, y, w, h, r); ctx.fill();
}

// ---------------- illustration scenes (native vector, gradient + shadow) ----------------
function illo(kind, x, y, w, h, zone, zlabel) {
  rect(x, y, w, h, '#e9e3d3'); // FLAT: no shadow
  ctx.save();
  ctx.beginPath(); ctx.roundRect(x, y, w, h, 5); ctx.clip();
  const cx = x + w / 2, cy = y + h / 2;
  if (kind === 'chart') {
    vgrad(x, y, w, h, '#d8eed6', '#f0f8ec');
    for (let i = 0; i < 3; i++) line([[x + 8, y + h - 10 - i * (h - 18) / 2], [x + w - 8, y + h - 10 - i * (h - 18) / 2]], '#c4d8c2', 1);
    ell(x + w - 22, y + 14, 8, 8, '#fad66e');
    const pts = [[x + 8, y + h - 12], [x + w * 0.35, y + h * 0.6], [x + w * 0.55, y + h * 0.68], [x + w * 0.82, y + h * 0.2]];
    poly([...pts, [x + w * 0.82, y + h], [x + 8, y + h]], '#bae4ba');
    line(pts, '#1a7832', 3);
    poly([[x + w * 0.82, y + h * 0.2], [x + w * 0.82 - 13, y + h * 0.2 + 2], [x + w * 0.82 - 2, y + h * 0.2 + 13]], '#1a7832');
    [[0.1, 1], [0.24, 0], [0.38, 1], [0.52, 1], [0.66, 0], [0.8, 1]].forEach(([fx, up], i) => {
      const bx = x + w * fx, col = up ? '#1e8c3c' : '#c43c32', bh = h * (0.2 + 0.05 * (i % 3));
      line([[bx + 4, y + h - 11 - bh], [bx + 4, y + h - 2]], col, 1);
      rect(bx, y + h - 6 - bh, 8, bh, col);
    });
  } else if (kind === 'pharma') {
    vgrad(x, y, w, h, '#d6eaf4', '#eef6fa');
    rect(x + w * 0.08, y + h * 0.24, w * 0.26, h * 0.76, '#6082a0');
    for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++)
      rect(x + w * (0.11 + c * 0.075), y + h * (0.32 + r * 0.2), w * 0.045, h * 0.12, '#e2f0f8');
    rect(x + w * 0.17, y + h * 0.08, w * 0.08, h * 0.16, '#6082a0');
    const fx = x + w * 0.6, fy = y + h * 0.12;
    poly([[fx - 7, fy], [fx + 7, fy], [fx + 3, fy + h * 0.24], [fx + 14, fy + h * 0.66], [fx - 14, fy + h * 0.66], [fx - 3, fy + h * 0.24]], 'rgba(0,0,0,0)');
    ctx.strokeStyle = '#465a6e'; ctx.lineWidth = 2;
    ctx.beginPath();
    [[fx - 7, fy], [fx + 7, fy], [fx + 3, fy + h * 0.24], [fx + 14, fy + h * 0.66], [fx - 14, fy + h * 0.66], [fx - 3, fy + h * 0.24]].forEach(([px, py], i) => i ? ctx.lineTo(px, py) : ctx.moveTo(px, py));
    ctx.closePath(); ctx.stroke();
    rect(fx - 11, fy + h * 0.44, 22, h * 0.2, '#5aa0c8');
    ell(fx - 5, fy + h * 0.5, 2, 2, '#d2ecf8'); ell(fx + 3, fy + h * 0.56, 3, 3, '#d2ecf8'); ell(fx + 6, fy + h * 0.48, 2, 2, '#d2ecf8');
    ell(x + w * 0.875, y + h * 0.3, 13, 13, '#fafaf8');
    ctx.strokeStyle = '#c43c3c'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x + w * 0.875, y + h * 0.3, 13, 13, 0, 0, Math.PI * 2); ctx.stroke();
    rect(x + w * 0.875 - 2.5, y + h * 0.3 - 7, 5, 14, '#c83232');
    rect(x + w * 0.875 - 7, y + h * 0.3 - 2.5, 14, 5, '#c83232');
  } else if (kind === 'tanker') {
    vgrad(x, y, w, h * 0.58, '#b2d4ea', '#deF0f8'.toLowerCase());
    vgrad(x, y + h * 0.58, w, h * 0.42, '#6092b8', '#3a6a9c');
    ell(x + w * 0.06 + 8, y + h * 0.1 + 8, 8, 8, '#fad66e');
    ell(x + w * 0.3 + 17, y + h * 0.12, 17, 5, '#fafafa'); ell(x + w * 0.3 + 22, y + h * 0.09, 10, 5, '#fafafa');
    rect(x + w * 0.12, y + h * 0.5, w * 0.56, h * 0.14, '#30363e');
    poly([[x + w * 0.68, y + h * 0.5], [x + w * 0.8, y + h * 0.64], [x + w * 0.68, y + h * 0.64]], '#30363e');
    ['#b23c28', '#246ea0', '#346e46'].forEach((c, i) => rect(x + w * (0.17 + i * 0.14), y + h * 0.36, w * 0.12, h * 0.14, c));
    rect(x + w * 0.6, y + h * 0.22, w * 0.08, h * 0.28, '#e8e6de');
    poly([[x + w * 0.26, y + h * 0.36], [x + w * 0.32, y + h * 0.12], [x + w * 0.38, y + h * 0.36]], '#f08228');
    const mx2 = x + w * 0.88, my2 = y + h * 0.34;
    line([[mx2, my2 - 10], [x + w * 0.72, y + h * 0.56]], '#3c3c40', 1);
    ell(mx2, my2, 7, 7, '#26262a');
    for (let a = 0; a < 360; a += 45) line([[mx2, my2], [mx2 + 11 * Math.cos(a * Math.PI / 180), my2 + 11 * Math.sin(a * Math.PI / 180)]], '#26262a', 2);
    ctx.strokeStyle = '#dcf0fa'; ctx.lineWidth = 2;
    for (let i = 0; i < 5; i++) { ctx.beginPath(); ctx.arc(x + 4 + i * w * 0.19 + w * 0.066, y + h * 0.83, w * 0.066, Math.PI, 2 * Math.PI); ctx.stroke(); }
  } else if (kind === 'gaza') {
    vgrad(x, y, w, h, '#e8dec6', '#f4eedc');
    ell(x + w * 0.84, y + h * 0.14, 7, 7, '#f6ce82');
    [[0.06, 0.17, 0.6], [0.27, 0.14, 0.44], [0.46, 0.19, 0.66], [0.7, 0.15, 0.5]].forEach(([bx, bw, bh]) => {
      rect(x + w * bx, y + h - h * bh, w * bw, h * bh, '#7a7262');
      for (let r = 0; r < 3; r++) for (let c = 0; c < 2; c++)
        rect(x + w * (bx + 0.03 + c * 0.07), y + h - h * bh + 4 + r * (h * bh / 3.4), w * 0.025, 4, '#4a443a');
    });
    poly([[x + w * 0.27, y + h - h * 0.44], [x + w * 0.34, y + h - h * 0.3], [x + w * 0.41, y + h - h * 0.44]], '#686052');
    [[0.52, 0.3, 10], [0.58, 0.18, 13], [0.12, 0.24, 9], [0.17, 0.12, 12]].forEach(([sx, sy, sr]) => ell(x + w * sx, y + h * sy, sr, sr * 0.6, '#9e9a92'));
    poly([[x + 2, y + h], [x + w * 0.2, y + h - 6], [x + w * 0.4, y + h]], '#968c78');
    poly([[x + w * 0.55, y + h], [x + w * 0.75, y + h - 7], [x + w * 0.95, y + h]], '#968c78');
  } else if (kind === 'rocket') {
    vgrad(x, y, w, h, '#182644', '#34486e');
    [[0.12, 0.18], [0.7, 0.12], [0.86, 0.36], [0.3, 0.08], [0.55, 0.26], [0.92, 0.14]].forEach(([sx, sy]) => ell(x + w * sx, y + h * sy, 1.5, 1.5, '#f0f0e6'));
    rect(x + w * 0.14, y + h * 0.2, w * 0.05, h * 0.66, '#969eae');
    poly([[cx - 8, y + h * 0.58], [cx, y + h * 0.06], [cx + 8, y + h * 0.58]], '#eeeee8');
    rect(cx - 8, y + h * 0.58, 16, h * 0.18, '#eeeee8');
    ell(cx, y + h * 0.33, 3, 3, '#c83232');
    rect(cx - 8, y + h * 0.5, 16, h * 0.06, '#346eaa');
    poly([[cx - 8, y + h * 0.76], [cx, y + h * 0.98], [cx + 8, y + h * 0.76]], '#f08c28');
    [[-0.3, 14], [-0.12, 18], [0.08, 16], [0.26, 12]].forEach(([ex, er]) => ell(cx + w * ex, y + h * 0.86, er / 2, er * 0.28, '#e2e4e8'));
    rect(x + w * 0.68, y + h * 0.3, w * 0.22, h * 0.08, '#ced4dc');
    line([[x + w * 0.79, y + h * 0.38], [x + w * 0.79, y + h * 0.55]], '#ced4dc', 2);
  } else if (kind === 'drone') {
    vgrad(x, y, w, h, '#c4d4e8', '#e8ecf0');
    [[0.02, 0.14, 0.3], [0.18, 0.11, 0.42], [0.31, 0.15, 0.26], [0.48, 0.12, 0.38], [0.62, 0.16, 0.3], [0.8, 0.12, 0.44], [0.93, 0.09, 0.28]].forEach(([bx, bw, bh]) => {
      rect(x + w * bx, y + h - h * bh, w * bw, h * bh, '#586070');
      for (let wy = 0; wy < 2; wy++) for (let wx = 0; wx < 2; wx++)
        rect(x + w * (bx + 0.025 + wx * 0.05), y + h - h * bh + 4 + wy * 8, w * 0.02, 3, '#fade82');
    });
    [[-30, -12], [30, -12], [-30, 13], [30, 13]].forEach(([dx, dy]) => {
      line([[cx, cy - 4], [cx + dx, cy - 4 + dy]], '#2c3038', 2);
      ctx.strokeStyle = '#2c3038'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(cx + dx, cy - 4 + dy, 11, 3, 0, 0, Math.PI * 2); ctx.stroke();
    });
    rect(cx - 11, cy - 9, 22, 11, '#2c3038');
    ell(cx, cy + 3, 2.5, 2, '#a61c1c');
  } else if (kind === 'oil') {
    vgrad(x, y, w, h, '#f0e6cc', '#faf4e2');
    ell(x + w * 0.82 + 7, y + h * 0.08 + 7, 7, 7, '#f6c45c');
    rect(x, y + h - 5, w, 5, '#968058');
    [[0.16, 0.85], [0.4, 1.05], [0.64, 0.7]].forEach(([fx, s]) => {
      const bx = x + w * fx, by = y + h - 4;
      line([[bx - 12 * s, by], [bx, by - h * 0.66 * s]], '#423e36', 2);
      line([[bx + 12 * s, by], [bx, by - h * 0.66 * s]], '#423e36', 2);
      line([[bx - 12 * s, by], [bx + 12 * s, by - h * 0.32 * s]], '#423e36', 1);
      line([[bx + 12 * s, by], [bx - 12 * s, by - h * 0.32 * s]], '#423e36', 1);
      line([[bx, by - h * 0.66 * s], [bx + 17 * s, by - h * 0.66 * s]], '#423e36', 2);
    });
    const px = x + w * 0.84, py = y + h - 4;
    poly([[px - 10, py], [px + 2, py - h * 0.44], [px + 12, py]], '#423e36');
    line([[px + 2, py - h * 0.44], [px - 14, py - h * 0.56]], '#423e36', 3);
    rect(px - 16, py - h * 0.6, 5, h * 0.1, '#423e36');
    [0.9, 0.95].forEach(bx => { rect(x + w * bx, y + h - 11, 7, 7, '#964628'); line([[x + w * bx, y + h - 8], [x + w * bx + 7, y + h - 8]], '#6e321c', 1); });
  } else if (kind === 'ship') {
    vgrad(x, y, w, h * 0.6, '#badc ee'.replace(' ', ''), '#e2f2fa');
    vgrad(x, y + h * 0.6, w, h * 0.4, '#6496ba', '#40709e');
    ell(x + w * 0.08 + 15, y + h * 0.13, 15, 4.5, '#fafafa'); ell(x + w * 0.08 + 20, y + h * 0.1, 10, 4.5, '#fafafa');
    poly([[x + w * 0.08, y + h * 0.56], [x + w * 0.88, y + h * 0.56], [x + w * 0.8, y + h * 0.76], [x + w * 0.18, y + h * 0.76]], '#2a3c52');
    ['#b23c28', '#346e46', '#246ea0'].forEach((c, i) => rect(x + w * (0.18 + i * 0.16), y + h * 0.4, w * 0.14, h * 0.16, c));
    rect(x + w * 0.72, y + h * 0.28, w * 0.08, h * 0.28, '#e8e6de');
    line([[x + w * 0.62, y + h * 0.4], [x + w * 0.62, y + h * 0.16]], '#3c3c3c', 1);
    poly([[x + w * 0.62, y + h * 0.16], [x + w * 0.7, y + h * 0.2], [x + w * 0.62, y + h * 0.24]], '#c83232');
    [0.24, 0.36, 0.48, 0.56].forEach((fx, i) => {
      const hx = x + w * fx, hy = y + h * 0.31;
      ell(hx, hy, 3, 3, '#463428');
      rect(hx - 4, hy + 3, 8, 6, i % 2 ? '#345478' : '#965a32');
    });
    ctx.strokeStyle = '#e0f0fa'; ctx.lineWidth = 2;
    for (let i = 0; i < 4; i++) { ctx.beginPath(); ctx.arc(x + 6 + i * w * 0.24 + w * 0.084, y + h * 0.88, w * 0.084, Math.PI, 2 * Math.PI); ctx.stroke(); }
  } else if (kind === 'radar') {
    vgrad(x, y, w, h, '#16281f', '#223830');
    poly([[cx, cy], [cx + w * 0.3, cy - h * 0.46], [cx + w * 0.36, cy - h * 0.3]], '#346e54');
    [[0.11, 0.22], [0.2, 0.4], [0.29, 0.58]].forEach(([rx, ry]) => {
      ctx.strokeStyle = '#4cc88a'; ctx.lineWidth = 1; ctx.beginPath(); ctx.ellipse(cx, cy, w * rx, h * ry, 0, 0, Math.PI * 2); ctx.stroke();
    });
    line([[cx, cy], [cx + w * 0.26, cy - h * 0.44]], '#60dc9c', 2);
    [[0.13, -0.22], [-0.18, -0.3], [0.05, 0.26]].forEach(([bx, by]) => ell(cx + w * bx, cy + h * by, 2.5, 2.5, '#f46054'));
    line([[x + 4, cy], [x + w - 4, cy]], '#387e62', 1);
    line([[cx, y + 4], [cx, y + h - 4]], '#387e62', 1);
    poly([[x + w * 0.68, y + h * 0.16], [x + w * 0.78, y + h * 0.12], [x + w * 0.76, y + h * 0.2], [x + w * 0.7, y + h * 0.2]], '#b4dcc8');
    poly([[x, y + h], [x + w * 0.3, y + h * 0.8], [x + w * 0.55, y + h]], '#12201c');
    poly([[x + w * 0.5, y + h], [x + w * 0.78, y + h * 0.84], [x + w, y + h]], '#12201c');
  } else if (kind === 'candle') {
    vgrad(x, y, w, h, '#2c2632', '#423846');
    ctx.strokeStyle = '#786e80'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.roundRect(x + w * 0.1, y + h * 0.08, w * 0.8, h * 0.92, 10); ctx.stroke();
    [[0.24, 0.5], [0.38, 0.66], [0.52, 0.44], [0.66, 0.6], [0.79, 0.48]].forEach(([fx, fh]) => {
      const bx = x + w * fx, top = y + h - 4 - h * fh;
      ell(bx, top - 3, 13, 12, 'rgba(150,110,80,0.35)');
      ell(bx, top - 2, 8, 8, 'rgba(190,140,90,0.4)');
      rect(bx - 5, top, 10, h * fh, '#eae6dc');
      rect(bx - 5, top, 3, 6, '#d6d0c6');
      poly([[bx, top - 13], [bx + 4.5, top - 3], [bx, top + 2], [bx - 4.5, top - 3]], '#f8b63e');
      ell(bx, top - 4, 1.8, 3, '#fceab0');
    });
  } else if (kind === 'factory') {
    vgrad(x, y, w, h, '#d8e2ea', '#eef2f6');
    ell(x + w * 0.72, y + h * 0.12, 16, 8, '#c4c6c8'); ell(x + w * 0.79, y + h * 0.07, 18, 7, '#d0d2d4');
    rect(x + w * 0.1, y + h * 0.48, w * 0.54, h * 0.52, '#6c747e');
    poly([[x + w * 0.1, y + h * 0.48], [x + w * 0.24, y + h * 0.3], [x + w * 0.38, y + h * 0.48], [x + w * 0.5, y + h * 0.3], [x + w * 0.64, y + h * 0.48]], '#606873');
    for (let i = 0; i < 4; i++) rect(x + w * (0.15 + i * 0.12), y + h * 0.58, w * 0.05, h * 0.14, '#e2ecf4');
    rect(x + w * 0.68, y + h * 0.18, w * 0.1, h * 0.82, '#5e666f');
    rect(x + w * 0.68, y + h * 0.18, w * 0.1, h * 0.08, '#964632');
    [[0.3, 0.2], [0.42, 0.3], [0.54, 0.16]].forEach(([fx, fh]) => {
      const bx = x + w * fx;
      poly([[bx, y + h * 0.44], [bx + 6, y + h * 0.44 - h * fh], [bx + 12, y + h * 0.44]], '#ea7a28');
      poly([[bx + 3, y + h * 0.44], [bx + 6, y + h * 0.44 - h * fh * 0.55], [bx + 9, y + h * 0.44]], '#fac850');
    });
  } else if (kind === 'gavel') {
    vgrad(x, y, w, h, '#f0e8d4', '#f8f2e2');
    rect(x + w * 0.08, y + h * 0.12, w * 0.36, h * 0.5, '#fcfaf4');
    srect(x + w * 0.08, y + h * 0.12, w * 0.36, h * 0.5, '#c4baa6', 1);
    for (let i = 0; i < 4; i++) line([[x + w * 0.12, y + h * (0.22 + i * 0.1)], [x + w * 0.4, y + h * (0.22 + i * 0.1)]], '#cec6b4', 2);
    line([[cx - 4, cy - 16], [cx + 30, cy + 16]], '#765228', 6);
    rect(cx - 16, cy - 24, 18, 14, '#926834');
    rect(cx - 16, cy - 24, 5, 14, '#6e4c22'); rect(cx - 1, cy - 24, 3, 14, '#6e4c22');
    ctx.strokeStyle = '#b29669'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(cx - 12, cy - 20, 16, -0.9, 1.1); ctx.stroke();
    ctx.beginPath(); ctx.arc(cx - 12, cy - 20, 22, -0.9, 1.1); ctx.stroke();
    rect(x + w * 0.2, y + h - 10, w * 0.64, 5, '#765228');
    rect(x + w * 0.3, y + h - 14, w * 0.44, 4, '#926834');
  } else if (kind === 'bomb') {
    vgrad(x, y, w, h, '#e4decf', '#f2eee2');
    rect(x + w * 0.08, y + h * 0.3, w * 0.26, h * 0.7, '#807868');
    rect(x + w * 0.68, y + h * 0.42, w * 0.22, h * 0.58, '#8c8474');
    [[0.08, 0.26], [0.68, 0.22]].forEach(([base, bw]) => {
      for (let r = 0; r < 3; r++) for (let c = 0; c < 3; c++)
        rect(x + w * (base + 0.03 + c * 0.07), y + h * (0.38 + r * 0.18), w * 0.025, h * 0.08, '#584f44');
    });
    const bx = x + w * 0.51, by = y + h * 0.34, pts = [];
    for (let i = 0; i < 16; i++) {
      const a = i * Math.PI / 8, r = i % 2 === 0 ? w * 0.15 : w * 0.07;
      pts.push([bx + r * Math.cos(a), by + r * Math.sin(a) * 0.82]);
    }
    poly(pts, '#ec7e26');
    ell(bx, by, 8, 6, '#fcd460');
    [[-0.3, -0.2], [0.28, -0.26], [-0.2, 0.24], [0.34, 0.12]].forEach(([dx, dy]) => {
      line([[bx, by], [bx + w * dx * 0.5, by + h * dy]], '#786e60', 2);
      ell(bx + w * dx * 0.5, by + h * dy, 2, 2, '#786e60');
    });
    ell(x + w * 0.65, y + h * 0.13, 18, 9, '#acaaa0'); ell(x + w * 0.72, y + h * 0.07, 20, 7, '#bab8ae');
  }
  ctx.restore();
  if (zone && zlabel) {
    const pf = F('SansB', 7), pw = tw(zlabel, pf) + 13;
    ctx.save();
    ctx.shadowColor = 'rgba(40,32,16,0.4)'; ctx.shadowBlur = 3; ctx.shadowOffsetY = 1;
    rr(x + 6, y + 6, pw, 13, 6.5, zone);
    ctx.restore();
    text(zlabel, x + 6 + (pw - tw(zlabel, pf)) / 2, y + 9, pf, '#ffffff');
  }
  rrs(x, y, w, h, 5, '#968e7e', 1);
}

// ---------------- page ----------------
rect(0, 0, W, H, BG);
const MX = 24, CW = W - 2 * MX;

// masthead
rect(0, 0, W, 106, NAVY);
rect(0, 106, W, 3, GOLD);
const mt = 'THE WORLD IN ONE DAY';
text(mt, (W - tw(mt, F('SerifXB', 40))) / 2, 13, F('SerifXB', 40), '#f5eedd');
line([[MX, 60], [W - MX, 60]], GOLD, 0.75);
const sub = 'TUESDAY 24 NOVEMBER 2026 · 38 STORIES · 3 COLOUR ZONES · EVERY ONE FROM THIS ONE DAY';
text(sub, (W - tw(sub, F('SansB', 11))) / 2, 72, F('SansB', 11), GOLDL);
const sub2 = 'EVERY STORY TAGGED FOR HOW SURE WE ARE — AND SOURCED';
text(sub2, (W - tw(sub2, F('Sans', 9.5))) / 2, 88, F('Sans', 9.5), '#b9c4d0');

// zone bar
const zones = [['ASIA-PACIFIC 16', ZA, 16], ['EUROPE · AFRICA · MIDDLE EAST 12', ZB, 12], ['AMERICAS 10', ZC, 10]];
let zx = MX;
for (const [lab, col, n] of zones) {
  const zw = CW * n / 38;
  rr(zx, 118, zw - 3, 20, 3, col);
  text(lab, zx + (zw - 3 - tw(lab, F('SansB', 11.5))) / 2, 122, F('SansB', 11.5), '#fcfaf4');
  zx += zw;
}

// UTC timeline
let tx = MX;
text('TUESDAY IN UTC', tx, 146, F('SansB', 10.5), RED);
tx += tw('TUESDAY IN UTC', F('SansB', 10.5)) + 12;
[['00:30', 'Kyiv talks'], ['01:04', 'Korea ADIZ'], ['01:32', 'Nepal quake'], ['02:30', 'Villavicencio'], ['06:36', 'Sanofi $41bn'], ['07:52', 'Ulleung alert'], ['14:00', 'Chess G1']].forEach(([tm, lab], i, arr) => {
  text(tm, tx, 146, F('SansB', 10.5), INK); tx += tw(tm, F('SansB', 10.5)) + 4;
  text(lab, tx, 146, F('Sans', 10.5), '#34302a'); tx += tw(lab, F('Sans', 10.5)) + (i < arr.length - 1 ? 10 : 0);
  if (i < arr.length - 1) { text('·', tx, 146, F('Sans', 10.5), GREY); tx += 8; }
});

// numbers band
rr(MX, 164, CW, 50, 5, NAVY);
const stats = [['$41bn', 'SANOFI–INSMED DEAL'], ['699', 'DRONES DOWNED'], ['47,000', 'WOMEN KILLED BY KIN'], ['6,500+', 'ROHINGYA TO RETURN'], ['26', 'BANTEN FIRE TOLL'], ['23', 'HURT IN VILLAVICENCIO']];
stats.forEach(([num, lab], i) => {
  const sx = MX + i * CW / 6, sw = CW / 6;
  if (i > 0) line([[sx, 172], [sx, 206]], '#33506f', 1);
  text(num, sx + (sw - tw(num, F('SerifXB', 22))) / 2, 170, F('SerifXB', 22), '#f5eedd');
  text(lab, sx + (sw - tw(lab, F('SansB', 8))) / 2, 197, F('SansB', 8), GOLDL);
});

// cards
function card2(x, y, w, num, zone, ill, headline, dek, tag, source, big = false) {
  const ih = big ? 76 : 52;
  const phf = F('SansB', big ? 15.5 : 11.5), pnw = (big ? 9 : 7.5) * 2 + 6;
  const phl = wrap2(headline, phf, w - pnw, w).length;
  const pdl = wrap(dek, F('Sans', big ? 10 : 9), w).length;
  const pH = ih + 5 + phl * (big ? 19 : 15) + 1 + pdl * (big ? 13 : 11.5) + 3 + 12;
  rr(x - 6, y - 6, w + 12, pH + 12, 6, '#ffffff');
  rrs(x - 6, y - 6, w + 12, pH + 12, 6, '#ddd3ba', 1);
  illo(ill, x, y, w, ih, zone, { [ZA]: 'ASIA-PACIFIC', [ZB]: 'EUROPE · AFRICA · MIDEAST', [ZC]: 'AMERICAS' }[zone]);
  let ty = y + ih + 5;
  const cr = big ? 9 : 7.5;
  ell(x + cr, ty + cr, cr, cr, zone);
  const nf = F('SansB', big ? 10 : 8.5), nt = String(num);
  text(nt, x + cr - tw(nt, nf) / 2, ty + cr - (big ? 5.5 : 4.5), nf, '#ffffff');
  const nw = cr * 2 + 6;
  const hf = F('SansB', big ? 15.5 : 11.5);
  wrap2(headline, hf, w - nw, w).forEach((ln, i) => { text(ln, x + (i === 0 ? nw : 0), ty, hf, INK); ty += big ? 19 : 15; });
  ty += 1;
  ty = block(dek, x, ty, F('Sans', big ? 10 : 9), w, big ? 13 : 11.5, '#34302a');
  ty += 3;
  const tf = F('SansB', 7.5), twd = tw(tag, tf);
  rr(x, ty, twd + 10, 12, 6, tag === 'CLAIM' ? RED : INK);
  text(tag, x + 5, ty + 2.5, tf, '#fcfaf4');
  text('— ' + source, x + twd + 14, ty + 1.5, F('Sans', 8.5), GREY);
}
const CW3 = Math.floor((CW - 20) / 3), R1Y = 222;
card2(MX, R1Y, CW3, 1, ZA, 'chart', "ASIA'S CHIP STOCKS SURGE",
  "Kospi leapt about 7% and the Nikkei about 4% as chip shares caught fire; Taiwan's Taiex jumped 9.15% intraday — a record 3,368 points — as TSMC hit its daily limit.", 'CONFIRMED', 'Reuters · CNBC', true);
card2(MX + CW3 + 10, R1Y, CW3, 2, ZB, 'pharma', 'SANOFI BUYS INSMED FOR $41 BILLION',
  "France's Sanofi agreed its biggest deal in years — $41bn in cash, $175 a share — for the US biotech Insmed and its lung-disease drugs.", 'OFFICIAL', 'Sanofi · PR Newswire', true);
card2(MX + 2 * (CW3 + 10), R1Y, CW3, 3, ZB, 'tanker', 'IRAN CLAIMS TANKERS HIT MINES IN HORMUZ',
  "The Revolutionary Guards say two or three tankers caught fire after breaking the strait's rules; Washington has not confirmed. Brent held near $69.", 'CLAIM', 'IRNA via Reuters', true);
const CW5 = Math.floor((CW - 32) / 5);
const row2 = [
  [4, ZB, 'drone', 'RUSSIA SAYS IT DOWNED 699 DRONES', '355 near the capital, Moscow says; a strike on Zaporizhzhia killed two and wounded 40. NATO sent an AWACS after a drone crossed into Poland.', 'CONFIRMED', 'Al Jazeera · FMT'],
  [5, ZB, 'oil', 'BAGHDAD SEIZES KURDISH-HELD OILFIELDS', "PM Ali al-Zaidi put four provinces under the federal Oil Ministry, taking the region's border crossings and oil exports.", 'REPORTED', 'Al Jazeera'],
  [6, ZA, 'ship', 'MALAYSIA TO RETURN 6,500 ROHINGYA', 'Anwar told parliament 6,500+ will go back to Myanmar: 1,500 by navy ship on 6–7 Dec, 5,303 by air.', 'OFFICIAL', 'Al Jazeera'],
  [7, ZB, 'gaza', 'ISRAELI STRIKES KILL SEVEN IN GAZA', 'Three died near a Khan Younis outpost, medics said; a Gaza City strike killed Hamas security chief Abu Nahel.', 'CONFIRMED', 'Reuters'],
  [8, ZA, 'radar', "RUSSIAN JETS ENTER KOREA'S ADIZ", 'Seoul scrambled jets; Ulleung islanders sheltered at 7:52 a.m. and were stood down three minutes later.', 'CONFIRMED', 'Yonhap'],
];
row2.forEach((c, i) => card2(MX + i * (CW5 + 8), 418, CW5, ...c));
const row3 = [
  [9, ZC, 'candle', '47,000 WOMEN KILLED BY PARTNERS', "Five women an hour die at the hands of partners or kin, the UN's annual count found. Africa is worst hit.", 'OFFICIAL', 'UNODC · UN Women'],
  [10, ZA, 'factory', 'BANTEN FACTORY-FIRE TOLL RISES TO 26', "The toll from Saturday's candy-factory blaze rose again on Tuesday; eight workers are still missing.", 'CONFIRMED', 'Xinhua · AP'],
  [11, ZA, 'rocket', 'FIRST FOREIGNER TO FLY TO TIANGONG', "Shenzhou-24 crew: Tang Hongbo, Wu Yi and Pakistan's M. Zeeshan Ali. Launch is set for Wednesday.", 'OFFICIAL', 'Xinhua · CMSA'],
  [12, ZC, 'gavel', "MEXICO TO TRY 'EL CHAPO ISIDRO' AT HOME", 'It turns down the US extradition request for the captured cartel boss, the attorney general says.', 'OFFICIAL', 'Mexico AG'],
  [13, ZC, 'bomb', "CAR BOMB HITS GOVERNOR'S OFFICE", '23 hurt in the 02:30 UTC blast in Villavicencio, Colombia; gangs are blamed for the attack.', 'CONFIRMED', 'El Tiempo · AFP'],
];
row3.forEach((c, i) => card2(MX + i * (CW5 + 8), 584, CW5, ...c));

// bottom: map + ALSO (top-4 style)
const BY = 746;
text('WHERE IT HAPPENED', MX, BY, F('SansB', 12.5), INK);
text('ALSO ON TUESDAY 24 NOVEMBER — 25 MORE DATED STORIES', MX + 400, BY, F('SansB', 12.5), INK);
const MAPX = MX, MAPY = BY + 20, MAPW = 376, MAPH = 176;
rect(MAPX, MAPY, MAPW, MAPH, SEA);
const mapdata = JSON.parse(readFileSync(new URL('./mapdata.json', import.meta.url)));
const ll = (lon, lat) => [MAPX + (lon + 180) / 360 * MAPW, MAPY + (80 - lat) / 140 * MAPH];
const coast = JSON.parse(readFileSync(new URL('./mapdata2.json', import.meta.url)));
ctx.save(); ctx.beginPath(); ctx.rect(MAPX, MAPY, MAPW, MAPH); ctx.clip();
for (const ring of coast.rings) {
  const clat = ring.reduce((a, p) => a + p[1], 0) / ring.length;
  if (clat < -56) continue;
  const pts = ring.map(([lon, lat]) => ll(lon, lat));
  poly(pts, LAND);
  ctx.strokeStyle = '#b39b63'; ctx.lineWidth = 0.75; ctx.beginPath();
  pts.forEach(([px, py], i) => i ? ctx.lineTo(px, py) : ctx.moveTo(px, py));
  ctx.closePath(); ctx.stroke();
}
ctx.restore();
rrs(MAPX, MAPY, MAPW, MAPH, 4, '#968e7e', 1);
const ZMAP = { ZA, ZB, ZC };
for (const [num, lon, lat, z] of mapdata.pins) {
  const [px, py] = ll(lon, lat);
  ell(px, py, 6.5, 6.5, ZMAP[z]);
  ctx.strokeStyle = '#faf8f0'; ctx.lineWidth = 1; ctx.beginPath(); ctx.ellipse(px, py, 6.5, 6.5, 0, 0, Math.PI * 2); ctx.stroke();
  const nt = String(num), fnt = F('SansB', num < 10 ? 7 : 6);
  text(nt, px - tw(nt, fnt) / 2, py - 3.5, fnt, '#ffffff');
}
text('Pins 1–13 = the illustrated stories; pin colours match the three zones above.', MAPX, MAPY + MAPH + 4, F('Sans', 8.5), GREY);

const liners = [
  [14, ZA, 'DHAKA — Hasina sets Dec 16 return; arrest vowed (BBC).'],
  [15, ZB, 'DAKAR — CAS restores Senegal as AFCON champions (wires).'],
  [16, ZA, 'HIMALAYA — M5.6 quake hits Nepal–Sikkim border (USGS).'],
  [17, ZA, 'PORT MORESBY — Bougainville vote on nationhood (Conv.).'],
  [18, ZB, 'GENEVA — Chess title match G1: Gukesh v Sindarov (FIDE).'],
  [19, ZB, 'BRUSSELS — EU caps tariff-free Chinese hybrids (GDN).'],
  [20, ZA, 'HANOI — Hot-pot eatery blast kills 6, hurts 10 (Reuters).'],
  [21, ZA, 'SINGAPORE — Q3 GDP +6.1%; 2026 outlook raised (CNA).'],
  [22, ZA, 'SINGAPORE — StarHub–M1 S$5bn merger agreed (CNA).'],
  [23, ZA, 'TOKYO — Factory PMI climbs to 53.7 (S&P Global).'],
  [24, ZA, 'CANBERRA — Tech giants face 5% revenue fines (Guardian).'],
  [25, ZA, 'HONIARA — Solomons ends China security pact (ABC).'],
  [26, ZB, 'KYIV — Zelensky ready for four-way talks (Ukrinform).'],
  [27, ZB, 'PARIS — Macron weighs constitutional spending cap (wires).'],
  [28, ZB, 'ROME — WFP: wars block food aid for 7.3m people (WFP).'],
  [29, ZA, 'JAKARTA — Ex-police chief charged with treason (CNA).'],
  [30, ZC, 'WASHINGTON — Trump urges faster executions (wires).'],
  [31, ZC, "PHILADELPHIA — Avdija's 31 sinks 76ers, 128–111 (AP)."],
  [32, ZC, 'WASHINGTON — Megaspeed blacklisted in Nvidia case (BIS).'],
  [33, ZC, 'GALÁPAGOS — El Niño floods force boat rescues (AFN).'],
  [34, ZC, 'PENNSYLVANIA — Ninth death in measles outbreak (wires).'],
  [35, ZC, 'IOWA — Army lead-explosives detonation goes ahead (wires).'],
  [36, ZB, 'CAPE TOWN — Cities tighten water curbs amid drought (wires).'],
  [37, ZC, 'NEW YORK — Gaza war cut 77 years of development (UNDP).'],
  [38, ZA, 'GOLD COAST — England beat Australia, level T20 (wires).'],
];
const LW2 = Math.floor((CW - 400 - 16) / 2);
for (let col = 0; col < 2; col++) {
  let yy = BY + 21;
  for (let r = 0; r < 13; r++) {
    const idx = col * 13 + r;
    if (idx >= liners.length) break;
    const [n, zc, txt] = liners[idx];
    const lx = MX + 400 + col * (LW2 + 16);
    rr(lx, yy, 16, 11, 2, zc);
    const nt = String(n), fnt = F('SansB', 7.5);
    text(nt, lx + 8 - tw(nt, fnt) / 2, yy + 1.5, fnt, '#ffffff');
    const [lab, rest] = txt.split(' — ');
    text(lab, lx + 20, yy, F('SansB', 8.5), INK);
    text('— ' + rest, lx + 20 + tw(lab, F('SansB', 8.5)) + 3, yy, F('Sans', 8.5), '#34302a');
    yy += 15.5;
  }
}

// date check
const DY = 974;
rrs(MX, DY, CW, 42, 4, RED, 2);
rect(MX, DY, 104, 42, RED);
text('DATE', MX + 9, DY + 6, F('SansB', 13), '#ffffff');
text('CHECK', MX + 9, DY + 23, F('SansB', 13), '#ffffff');
block("Left out — earlier days: Nvidia rehires Huang, Wall Street's rally (Mon 23) · NATO space pledge, Sputnik-S reports (Mon 23) · Iran shadow-banking sanctions (Mon 23) · COP31 collapses (Sun 22) · Las Vegas GP (Sun 22) · the Banten fire itself (Sat 22) — only Tuesday's toll rise counts · ICJ Rohingya ruling (19 Nov).   TAGS: CONFIRMED = 2+ wires · OFFICIAL = on the record · REPORTED = one outlet · CLAIM = one side says · ONGOING = still unfolding.",
  MX + 116, DY + 5, F('Sans', 8.5), CW - 128, 11, '#34302a');

// export: Skia master 2048 -> Sharp lanczos3 -> final 1024
const master = await canvas.png;
await sharp(master).png().toFile(new URL('./poster-2048.png', import.meta.url).pathname);
await sharp(master).resize(1024, 1024, { kernel: 'lanczos3' }).png().toFile(new URL('./entry.png', import.meta.url).pathname);
console.log('rendered: poster-2048.png + poster-1024.png');
