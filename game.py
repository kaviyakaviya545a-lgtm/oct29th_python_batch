
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AFTER DARK | Dino Runner</title>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: #050712;
    color: #fff;
    font-family: "Segoe UI", Arial, sans-serif;
    min-height: 100vh;
    display: grid;
    place-items: center;
    overflow-x: hidden;
}

.game-shell {
    width: min(1100px, 96%);
    padding: 24px 0;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 22px;
    gap: 15px;
}

.logo {
    font-size: 13px;
    letter-spacing: 5px;
    color: #a4b4d8;
}

.logo strong {
    display: block;
    color: #fff;
    font-size: 24px;
    letter-spacing: 3px;
    margin-top: 5px;
}

.status {
    color: #9af7d1;
    font-size: 11px;
    letter-spacing: 2px;
    border: 1px solid #234b4b;
    padding: 10px 14px;
    border-radius: 30px;
    background: #0c2427;
}

.stage {
    position: relative;
    overflow: hidden;
    border: 1px solid #303b62;
    border-radius: 16px;
    background: #090d20;
    box-shadow: 0 0 70px #4555aa22,
                0 25px 90px #0009;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    cursor: pointer;
    touch-action: manipulation;
}

.hud {
    position: absolute;
    top: 22px;
    left: 24px;
    right: 24px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
}

.label {
    font-size: 10px;
    letter-spacing: 3px;
    color: #9caad0;
    margin-bottom: 6px;
}

.value {
    font-size: 27px;
    font-weight: 700;
    text-shadow: 0 0 20px #88baff66;
}

.center-message {
    position: absolute;
    top: 43%;
    left: 5%;
    width: 90%;
    text-align: center;
    pointer-events: none;
    text-shadow: 0 3px 20px #000;
}

.center-message h1 {
    font-size: clamp(25px, 5vw, 48px);
    letter-spacing: 7px;
    font-weight: 800;
}

.center-message p {
    margin-top: 13px;
    color: #bac7e8;
    font-size: 12px;
    letter-spacing: 2px;
    line-height: 1.8;
}

.controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 14px;
    margin-top: 20px;
    flex-wrap: wrap;
}

.hint {
    color: #8c99bb;
    font-size: 12px;
    line-height: 1.8;
}

.hint b {
    color: #e3eaff;
}

button {
    border: 1px solid #8a9cff;
    background: linear-gradient(135deg, #7389ff, #9a63ed);
    color: white;
    font-weight: 700;
    letter-spacing: 1px;
    padding: 13px 24px;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 0 24px #786dff44;
    transition: transform .2s, filter .2s;
}

button:hover {
    transform: translateY(-2px);
    filter: brightness(1.15);
}

.footer {
    text-align: center;
    color: #596582;
    font-size: 10px;
    letter-spacing: 3px;
    margin-top: 25px;
}

@media (max-width: 600px) {
    .game-shell { width: 94%; }
    .hud { top: 12px; left: 12px; right: 12px; }
    .value { font-size: 20px; }
    .label { font-size: 8px; }
    .status { font-size: 9px; padding: 8px; }
    .center-message h1 { letter-spacing: 3px; }
    .controls { align-items: flex-start; }
}
</style>
</head>

<body>
<div class="game-shell">

    <header class="topbar">
        <div class="logo">
            AN OFFLINE ARCADE EXPERIENCE
            <strong>AFTER DARK<span style="color:#8d8cff">.</span></strong>
        </div>
        <div class="status">● OFFLINE READY</div>
    </header>

    <section class="stage">
        <canvas id="game" width="1000" height="440"></canvas>

        <div class="hud">
            <div>
                <div class="label">DISTANCE</div>
                <div class="value" id="score">00000</div>
            </div>
            <div style="text-align:right">
                <div class="label">BEST RUN</div>
                <div class="value" id="best">00000</div>
            </div>
        </div>

        <div class="center-message" id="message">
            <h1>THE NIGHT RUN</h1>
            <p>THE WORLD IS SILENT. THE RUN BEGINS.<br>
            PRESS SPACE OR TAP TO START</p>
        </div>
    </section>

    <div class="controls">
        <div class="hint">
            <b>SPACE / ↑</b> &nbsp; JUMP<br>
            <b>TOUCH / CLICK</b> &nbsp; JUMP<br>
            AVOID THE OBSTACLES. SURVIVE THE NIGHT.
        </div>
        <button id="restart">↻ &nbsp; NEW RUN</button>
    </div>

    <div class="footer">RUN INTO THE UNKNOWN &nbsp; • &nbsp; NO INTERNET REQUIRED</div>
</div>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const message = document.getElementById("message");
const scoreEl = document.getElementById("score");
const bestEl = document.getElementById("best");

const W = canvas.width;
const H = canvas.height;
const ground = 350;

let player, obstacles, particles;
let score = 0;
let best = 0;
let speed = 6;
let started = false;
let dead = false;
let last = 0;
let spawn = 0;
let world = 0;
let stars = [];

try {
    best = Number(localStorage.getItem("afterDarkBest")) || 0;
} catch (e) {}

bestEl.textContent = String(best).padStart(5, "0");

for (let i = 0; i < 100; i++) {
    stars.push({
        x: Math.random() * W,
        y: Math.random() * 260,
        size: Math.random() * 1.8 + 0.3,
        phase: Math.random() * 6
    });
}

function reset() {
    player = {
        x: 115,
        y: ground - 54,
        w: 42,
        h: 54,
        vy: 0,
        jumping: false
    };

    obstacles = [];
    particles = [];
    score = 0;
    speed = 6;
    spawn = 0;
    world = 0;
    started = false;
    dead = false;

    scoreEl.textContent = "00000";
    message.style.display = "block";
    message.innerHTML =
        "<h1>THE NIGHT RUN</h1>" +
        "<p>THE WORLD IS SILENT. THE RUN BEGINS.<br>" +
        "PRESS SPACE OR TAP TO START</p>";

    draw();
}

function jump() {
    if (dead) return;

    if (!started) {
        started = true;
        message.style.display = "none";
    }

    if (!player.jumping) {
        player.vy = -15.5;
        player.jumping = true;

        for (let i = 0; i < 7; i++) {
            particles.push({
                x: player.x + 15,
                y: ground - 4,
                vx: -Math.random() * 3,
                vy: -Math.random() * 2,
                life: 1
            });
        }
    }
}

function endGame() {
    dead = true;
    started = false;
    message.style.display = "block";
    message.innerHTML =
        "<h1 style='color:#ff879d'>RUN ENDED</h1>" +
        "<p>DISTANCE: " + Math.floor(score) +
        "<br>PRESS NEW RUN TO TRY AGAIN</p>";

    if (Math.floor(score) > best) {
        best = Math.floor(score);
        try {
            localStorage.setItem("afterDarkBest", best);
        } catch (e) {}
        bestEl.textContent = String(best).padStart(5, "0");
    }
}

function roundedRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
    ctx.fill();
}

function drawBackground() {
    const sky = ctx.createLinearGradient(0, 0, 0, H);
    sky.addColorStop(0, "#070a20");
    sky.addColorStop(0.55, "#171c43");
    sky.addColorStop(1, "#34415c");

    ctx.fillStyle = sky;
    ctx.fillRect(0, 0, W, H);

    // Moon glow
    const glow = ctx.createRadialGradient(760, 110, 8, 760, 110, 120);
    glow.addColorStop(0, "#b8d8ff33");
    glow.addColorStop(1, "#91b8ff00");
    ctx.fillStyle = glow;
    ctx.fillRect(620, 0, 280, 250);

    // Moon
    ctx.fillStyle = "#e4edff";
    ctx.shadowColor = "#9cbfff";
    ctx.shadowBlur = 35;
    ctx.beginPath();
    ctx.arc(760, 110, 32, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0;

    // Distant stars
    stars.forEach(s => {
        ctx.globalAlpha = 0.45 + Math.sin(world * 0.02 + s.phase) * 0.25;
        ctx.fillStyle = "#dce8ff";
        ctx.fillRect(s.x, s.y, s.size, s.size);
    });
    ctx.globalAlpha = 1;

    // Distant mountains
    ctx.fillStyle = "#171c38";
    ctx.beginPath();
    ctx.moveTo(0, 300);

    for (let x = 0; x <= W; x += 80) {
        const y = 230 + Math.sin(x * 0.013 + world * 0.0008) * 28;
        ctx.lineTo(x, y);
    }

    ctx.lineTo(W, ground);
    ctx.lineTo(0, ground);
    ctx.closePath();
    ctx.fill();

    // Near hills
    ctx.fillStyle = "#202a48";
    ctx.beginPath();
    ctx.moveTo(0, 325);

    for (let x = 0; x <= W; x += 55) {
        ctx.lineTo(x, 295 + Math.sin(x * 0.018 + world * 0.0015) * 18);
    }

    ctx.lineTo(W, ground);
    ctx.lineTo(0, ground);
    ctx.closePath();
    ctx.fill();

    // Ground
    const floor = ctx.createLinearGradient(0, ground, 0, H);
    floor.addColorStop(0, "#1c2944");
    floor.addColorStop(1, "#080b18");
    ctx.fillStyle = floor;
    ctx.fillRect(0, ground, W, H - ground);

    ctx.strokeStyle = "#849cff";
    ctx.shadowColor = "#788cff";
    ctx.shadowBlur = 14;
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, ground);
    ctx.lineTo(W, ground);
    ctx.stroke();
    ctx.shadowBlur = 0;

    // Moving ground marks
    ctx.strokeStyle = "#617094";
    ctx.globalAlpha = 0.45;

    for (let x = -(world * 2 % 90); x < W; x += 90) {
        ctx.beginPath();
        ctx.moveTo(x, ground + 30);
        ctx.lineTo(x + 30, ground + 30);
        ctx.stroke();
    }

    ctx.globalAlpha = 1;

    // Cinematic fog
    const fog = ctx.createLinearGradient(0, ground - 30, 0, ground + 50);
    fog.addColorStop(0, "#879ecf00");
    fog.addColorStop(0.5, "#879ecf19");
    fog.addColorStop(1, "#879ecf00");
    ctx.fillStyle = fog;
    ctx.fillRect(0, ground - 30, W, 80);
}

function drawDinosaur() {
    const p = player;
    const runningLeg = started && !p.jumping
        ? Math.sin(world * 0.22) * 7 : 0;

    ctx.save();

    // Character glow
    ctx.shadowColor = "#71f7d1";
    ctx.shadowBlur = 14;
    ctx.fillStyle = "#76e8c3";

    // Body
    roundedRect(p.x + 5, p.y + 18, 28, 29, 6);

    // Head
    roundedRect(p.x + 18, p.y + 2, 27, 25, 5);

    // Snout
    roundedRect(p.x + 34, p.y + 13, 14, 10, 3);

    // Eye
    ctx.shadowBlur = 0;
    ctx.fillStyle = "#071324";
    ctx.fillRect(p.x + 36, p.y + 8, 4, 4);

    // Tiny back spikes
    ctx.fillStyle = "#a0ffe0";
    ctx.beginPath();
    ctx.moveTo(p.x + 11, p.y + 19);
    ctx.lineTo(p.x + 15, p.y + 10);
    ctx.lineTo(p.x + 20, p.y + 20);
    ctx.fill();

    // Legs
    ctx.fillStyle = "#76e8c3";
    ctx.fillRect(p.x + 8, p.y + 42, 9, 12 + runningLeg);
    ctx.fillRect(p.x + 24, p.y + 42, 9, 12 - runningLeg);

    // Tail
    ctx.beginPath();
    ctx.moveTo(p.x + 7, p.y + 29);
    ctx.lineTo(p.x - 8, p.y + 22);
    ctx.lineTo(p.x + 6, p.y + 38);
    ctx.fill();

    ctx.restore();
}

function drawCactus(o) {
    ctx.save();
    ctx.fillStyle = "#ff779c";
    ctx.shadowColor = "#ff4d86";
    ctx.shadowBlur = 16;

    // Main stem
    roundedRect(o.x + 9, o.y, 14, o.h, 4);

    // Side branches
    roundedRect(o.x, o.y + 14, 11, 7, 3);
    roundedRect(o.x, o.y + 9, 6, 13, 3);
    roundedRect(o.x + 20, o.y + 25, 12, 7, 3);
    roundedRect(o.x + 26, o.y + 19, 6, 13, 3);

    ctx.restore();
}

function draw() {
    drawBackground();

    obstacles.forEach(drawCactus);
    drawDinosaur();

    // Dust particles
    particles.forEach(p => {
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.fillStyle = "#c1d5ff";
        ctx.fillRect(p.x, p.y, 4, 4);
    });

    ctx.globalAlpha = 1;
}

function update(dt) {
    if (!started || dead) return;

    world += dt;
    score += dt * 0.55;
    speed = Math.min(6 + score / 100, 14);

    scoreEl.textContent = String(Math.floor(score))
        .padStart(5, "0");

    // Jumping physics
    player.vy += 0.72 * dt;
    player.y += player.vy * dt;

    if (player.y >= ground - player.h) {
        player.y = ground - player.h;
        player.vy = 0;
        player.jumping = false;
    }

    // Spawn obstacles at intervals
    spawn += dt;

    if (spawn > Math.max(48, 95 - speed * 2) + Math.random() * 35) {
        const height = 30 + Math.random() * 24;

        obstacles.push({
            x: W + 20,
            y: ground - height,
            w: 32,
            h: height
        });

        spawn = 0;
    }

    obstacles.forEach(o => {
        o.x -= speed * dt;

        const hit =
            player.x + 9 < o.x + o.w - 3 &&
            player.x + player.w - 2 > o.x + 3 &&
            player.y + player.h - 4 > o.y + 4;

        if (hit) endGame();
    });

    obstacles = obstacles.filter(o => o.x + o.w > -10);

    particles.forEach(p => {
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        p.vy += 0.1 * dt;
        p.life -= 0.025 * dt;
    });

    particles = particles.filter(p => p.life > 0);
}

function loop(time) {
    const dt = last ? Math.min((time - last) / 16.67, 2) : 1;
    last = time;

    update(dt);
    draw();
    requestAnimationFrame(loop);
}

document.addEventListener("keydown", e => {
    if (e.code === "Space" || e.code === "ArrowUp") {
        e.preventDefault();
        if (!e.repeat) jump();
    }
});

canvas.addEventListener("pointerdown", jump);

document.getElementById("restart").addEventListener("click", reset);

reset();
requestAnimationFrame(loop);
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
