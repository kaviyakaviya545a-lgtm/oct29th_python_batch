
from flask import Flask, render_template_string

app = Flask(__name__)

GAME = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SUPERDRIVE 3D</title>

<style>
* { box-sizing: border-box; margin: 0; }

body {
    background: #07090f;
    color: white;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

#game { position: fixed; inset: 0; }
canvas { display: block; }

.hud {
    position: fixed;
    inset: 0;
    pointer-events: none;
    padding: 25px 35px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: linear-gradient(#0008, transparent 25%, transparent 70%, #0008);
}

.top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}

.logo {
    font-size: 27px;
    font-weight: 900;
    letter-spacing: 5px;
    text-shadow: 0 0 20px #00eaff;
}

.logo span { color: #00eaff; }

.subtitle {
    color: #9aa9bc;
    font-size: 10px;
    letter-spacing: 4px;
    margin-top: 7px;
}

.level {
    text-align: right;
    font-size: 12px;
    letter-spacing: 3px;
    color: #00eaff;
}

.level strong {
    display: block;
    font-size: 27px;
    color: white;
    margin-top: 5px;
}

.bottom {
    display: flex;
    justify-content: space-between;
    align-items: end;
}

.speed-box {
    display: flex;
    align-items: baseline;
    gap: 8px;
}

.speed {
    font-size: clamp(55px, 8vw, 95px);
    font-weight: 900;
    line-height: 1;
    text-shadow: 0 0 25px #00dfff88;
}

.unit {
    color: #00eaff;
    font-size: 13px;
    letter-spacing: 2px;
}

.info {
    text-align: right;
    color: #a8b8ca;
    font-size: 12px;
    line-height: 2;
    letter-spacing: 2px;
}

.info b { color: white; }

.progress {
    position: fixed;
    bottom: 8px;
    left: 0;
    height: 3px;
    background: #00eaff;
    box-shadow: 0 0 12px #00eaff;
    width: 0%;
    transition: width .2s;
}

.overlay {
    position: fixed;
    inset: 0;
    z-index: 5;
    background: #02050cbd;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20px;
}

.panel {
    max-width: 650px;
    padding: 40px;
    border: 1px solid #00dfff66;
    background: linear-gradient(145deg, #101a2beF, #070b13ef);
    box-shadow: 0 0 70px #00cfff22;
    border-radius: 14px;
}

.panel h1 {
    font-size: clamp(35px, 7vw, 65px);
    letter-spacing: 5px;
    margin-bottom: 12px;
}

.panel h1 span { color: #00eaff; }

.panel p {
    color: #a9b8c9;
    line-height: 1.8;
    margin: 15px 0 25px;
    font-size: 13px;
}

button {
    border: 0;
    background: linear-gradient(100deg, #00bcd4, #4169ff);
    color: white;
    padding: 16px 38px;
    font-weight: bold;
    letter-spacing: 3px;
    cursor: pointer;
    border-radius: 5px;
    pointer-events: auto;
}

button:hover { filter: brightness(1.25); }

#upgrade {
    position: fixed;
    top: 35%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #071723ee;
    border: 1px solid #00eaff;
    padding: 25px 45px;
    text-align: center;
    z-index: 4;
    display: none;
    box-shadow: 0 0 50px #00dfff55;
}

#upgrade h2 { color: #00eaff; letter-spacing: 4px; }
#upgrade p { margin-top: 12px; color: white; }

.controls {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    color: #d2e5ef;
    font-size: 10px;
    letter-spacing: 2px;
    white-space: nowrap;
    pointer-events: none;
}

@media(max-width:600px) {
    .hud { padding: 16px; }
    .logo { font-size: 19px; }
    .subtitle { font-size: 8px; }
    .controls { bottom: 18px; font-size: 8px; }
    .info { font-size: 9px; }
}
</style>
</head>

<body>
<div id="game"></div>

<div class="hud">
    <div class="top">
        <div>
            <div class="logo">SUPER<span>DRIVE</span> 3D</div>
            <div class="subtitle">ULTIMATE SUPERCAR EXPERIENCE</div>
        </div>

        <div class="level">
            CURRENT LEVEL
            <strong id="level">01 / 03</strong>
            <div id="environment">SNOW MOUNTAIN</div>
        </div>
    </div>

    <div class="bottom">
        <div>
            <div class="speed-box">
                <div class="speed" id="speed">000</div>
                <div class="unit">KM/H</div>
            </div>
            <div class="subtitle" id="carname">FALCON GT</div>
        </div>

        <div class="info">
            DISTANCE: <b id="distance">0000</b> M<br>
            SCORE: <b id="score">0000</b><br>
            BEST: <b id="best">0000</b>
        </div>
    </div>
</div>

<div class="progress" id="progress"></div>

<div id="upgrade">
    <h2>CAR UPGRADED!</h2>
    <p id="upgradeText">NEW SUPERCAR UNLOCKED</p>
</div>

<div class="controls">
    A / D OR ← / → : STEER &nbsp; | &nbsp;
    W / ↑ : ACCELERATE &nbsp; | &nbsp;
    S / ↓ : BRAKE
</div>

<div class="overlay" id="start">
    <div class="panel">
        <div class="subtitle">THREE WORLDS. THREE SUPERCARS.</div>
        <h1>SUPER<span>DRIVE</span></h1>
        <p>
            Conquer frozen mountains, dangerous muddy roads
            and a neon highway. Upgrade your supercar
            after every level. Become the ultimate driver.
        </p>
        <button id="startBtn">START ENGINE</button>
        <p>WASD / ARROW KEYS TO DRIVE</p>
    </div>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

const root = document.getElementById("game");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x091323);
scene.fog = new THREE.Fog(0x091323, 25, 150);

const camera = new THREE.PerspectiveCamera(
    65, innerWidth / innerHeight, 0.1, 400
);
camera.position.set(0, 7, 14);

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: "high-performance"
});
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.7));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
root.appendChild(renderer.domElement);

// LIGHTING
scene.add(new THREE.HemisphereLight(0xb8dfff, 0x27301e, 2));

const sun = new THREE.DirectionalLight(0xffffff, 3);
sun.position.set(-10, 20, 10);
sun.castShadow = true;
scene.add(sun);

// GAME DATA
const levels = [
    {
        name: "SNOW MOUNTAIN",
        car: "FALCON GT",
        color: 0x20c9ff,
        road: 0xdde9f1,
        ground: 0x9cb9d0,
        sky: 0x91b8d6,
        obstacle: 0x273b50,
        maxSpeed: 185
    },
    {
        name: "MUD TERRITORY",
        car: "RAPTOR X",
        color: 0xff5722,
        road: 0x493326,
        ground: 0x35291e,
        sky: 0x76604c,
        obstacle: 0x8d4e27,
        maxSpeed: 220
    },
    {
        name: "NEON HIGHWAY",
        car: "PHANTOM RS",
        color: 0x9b5cff,
        road: 0x171c29,
        ground: 0x090e1b,
        sky: 0x080c25,
        obstacle: 0xffd34e,
        maxSpeed: 280
    }
];

let level = 0;
let distance = 0;
let score = 0;
let speed = 0;
let playing = false;
let crashed = false;
let lane = 0;
let car;
let roadMarks = [];
let scenery = [];
let obstacles = [];
let snow = [];
let clock = new THREE.Clock();
let best = Number(localStorage.getItem("superdriveBest") || 0);

document.getElementById("best").textContent = best;

const keys = {};
let spawnTimer = 0;

// MATERIAL HELPER
function material(color, metalness=0, roughness=0.5) {
    return new THREE.MeshStandardMaterial({
        color, metalness, roughness
    });
}

// CREATE A PROCEDURAL 3D SUPERCAR
function createCar(config) {
    const group = new THREE.Group();

    const bodyMat = material(config.color, 0.8, 0.23);
    const dark = material(0x10151e, 0.5, 0.3);
    const glass = new THREE.MeshPhysicalMaterial({
        color: 0x101d2b,
        metalness: 0.5,
        roughness: 0.1,
        transparent: true,
        opacity: 0.85
    });
    const rubber = material(0x08090c);
    const rim = material(0xc7d8e8, 0.9, 0.2);
    const light = new THREE.MeshBasicMaterial({
        color: 0x8deaff
    });

    function box(w,h,d,x,y,z,mat) {
        const mesh = new THREE.Mesh(
            new THREE.BoxGeometry(w,h,d), mat
        );
        mesh.position.set(x,y,z);
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        group.add(mesh);
        return mesh;
    }

    // Main aerodynamic body
    box(2.05, 0.48, 4.25, 0, 0.65, 0, bodyMat);

    // Front hood
    box(1.9, 0.20, 1.15, 0, 0.92, -1.42, bodyMat);

    // Cockpit
    box(1.48, 0.62, 1.75, 0, 1.12, 0.25, glass);

    // Roof and rear section
    box(1.5, 0.12, 0.85, 0, 1.45, 0.3, bodyMat);
    box(1.95, 0.22, 0.65, 0, 0.92, 1.55, bodyMat);

    // Front splitter
    box(2.25, 0.10, 0.35, 0, 0.42, -2.13, dark);

    // Rear spoiler, bigger at higher levels
    box(2.3 + level * 0.2, 0.13, 0.25, 0, 1.5, 1.95, bodyMat);
    box(0.12, 0.35, 0.12, -0.75, 1.35, 1.95, dark);
    box(0.12, 0.35, 0.12, 0.75, 1.35, 1.95, dark);

    // Wheels
    for (const x of [-1.05, 1.05]) {
        for (const z of [-1.35, 1.35]) {
            const wheel = new THREE.Mesh(
                new THREE.CylinderGeometry(0.48,0.48,0.28,24),
                rubber
            );
            wheel.rotation.z = Math.PI/2;
            wheel.position.set(x,0.48,z);
            wheel.castShadow = true;
            group.add(wheel);

            const hub = new THREE.Mesh(
                new THREE.CylinderGeometry(0.23,0.23,0.30,16),
                rim
            );
            hub.rotation.z = Math.PI/2;
            hub.position.set(x*1.01,0.48,z);
            group.add(hub);
        }
    }

    // Headlights
    box(0.48,0.12,0.08,-0.68,0.79,-2.16,light);
    box(0.48,0.12,0.08,0.68,0.79,-2.16,light);

    // Taillights
    const red = new THREE.MeshBasicMaterial({color:0xff183e});
    box(0.5,0.12,0.08,-0.7,0.77,2.13,red);
    box(0.5,0.12,0.08,0.7,0.77,2.13,red);

    // Neon underglow
    const glow = new THREE.PointLight(config.color, 2, 7);
    glow.position.set(0,0.25,0);
    group.add(glow);

    group.position.set(0,0.15,5);
    scene.add(group);

    return group;
}

// WORLD
let groundMesh, roadMesh;

function clearWorld() {
    if (groundMesh) scene.remove(groundMesh);
    if (roadMesh) scene.remove(roadMesh);
    roadMarks.forEach(o => scene.remove(o));
    scenery.forEach(o => scene.remove(o));
    obstacles.forEach(o => scene.remove(o));

    roadMarks = [];
    scenery = [];
    obstacles = [];
}

function buildWorld() {
    const config = levels[level];
    clearWorld();

    scene.background = new THREE.Color(config.sky);
    scene.fog.color.set(config.sky);
    scene.fog.near = 30;
    scene.fog.far = level === 2 ? 170 : 110;

    groundMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(250,350),
        material(config.ground)
    );
    groundMesh.rotation.x = -Math.PI/2;
    groundMesh.position.set(0,-0.08,-90);
    groundMesh.receiveShadow = true;
    scene.add(groundMesh);

    roadMesh = new THREE.Mesh(
        new THREE.PlaneGeometry(12,350),
        material(config.road,0.1,0.8)
    );
    roadMesh.rotation.x = -Math.PI/2;
    roadMesh.position.set(0,0,-90);
    roadMesh.receiveShadow = true;
    scene.add(roadMesh);

    // Road lane markings
    for (let i=0; i<32; i++) {
        for (let x of [-2,2]) {
            const mark = new THREE.Mesh(
                new THREE.BoxGeometry(0.10,0.025,3),
                material(level === 2 ? 0x00eaff : 0xffffff)
            );
            mark.position.set(x,0.025,-i*10);
            scene.add(mark);
            roadMarks.push(mark);
        }
    }

    // Roadside objects
    for (let i=0; i<42; i++) {
        const z = -i*8;

        for (let side of [-1,1]) {
            if (level === 0) {
                // Snow mountain pine trees
                const tree = new THREE.Group();
                const trunk = new THREE.Mesh(
                    new THREE.CylinderGeometry(0.12,0.2,2,7),
                    material(0x47392f)
                );
                trunk.position.y=1;
                tree.add(trunk);

                for (let j=0;j<3;j++) {
                    const cone = new THREE.Mesh(
                        new THREE.ConeGeometry(1.2-j*0.22,2.1,8),
                        material(0xe5f5ff)
                    );
                    cone.position.y=2+j*0.8;
                    tree.add(cone);
                }
                tree.position.set(side*(9+Math.random()*12),0,z);
                scene.add(tree);
                scenery.push(tree);

            } else if (level === 1) {
                // Mud rocks
                const rock = new THREE.Mesh(
                    new THREE.DodecahedronGeometry(
                        0.7+Math.random(),0
                    ),
                    material(0x66503b)
                );
                rock.position.set(side*(10+Math.random()*12),
                    0.3,z);
                rock.castShadow=true;
                scene.add(rock);
                scenery.push(rock);

            } else {
                // Neon highway lights
                const pole = new THREE.Group();
                const stem = new THREE.Mesh(
                    new THREE.BoxGeometry(0.15,6,0.15),
                    material(0x53647d,0.8)
                );
                stem.position.y=3;
                pole.add(stem);

                const lamp = new THREE.Mesh(
                    new THREE.BoxGeometry(1.5,0.12,0.2),
                    new THREE.MeshBasicMaterial({color:0x00eaff})
                );
                lamp.position.set(side*0.65,5.8,0);
                pole.add(lamp);

                const glow = new THREE.PointLight(0x00cfff,3,15);
                glow.position.set(side*0.65,5.4,0);
                pole.add(glow);

                pole.position.set(side*9,0,z);
                scene.add(pole);
                scenery.push(pole);
            }
        }
    }

    // Level 1 snow particles
    snow.forEach(s => scene.remove(s));
    snow=[];

    if (level === 0) {
        for(let i=0;i<180;i++) {
            const flake = new THREE.Mesh(
                new THREE.SphereGeometry(0.045,5,5),
                new THREE.MeshBasicMaterial({color:0xffffff})
            );
            flake.position.set(
                (Math.random()-0.5)*45,
                Math.random()*20,
                -Math.random()*130
            );
            scene.add(flake);
            snow.push(flake);
        }
    }
}

// OBSTACLES
function spawnObstacle() {
    const group = new THREE.Group();
    const config = levels[level];

    const body = new THREE.Mesh(
        new THREE.BoxGeometry(1.8,0.9,3.3),
        material(config.obstacle,0.5)
    );
    body.position.y=0.8;
    group.add(body);

    // Wheels
    for (const x of [-0.95,0.95]) {
        for (const z of [-1,1]) {
            const w = new THREE.Mesh(
                new THREE.CylinderGeometry(0.36,0.36,0.18,12),
                material(0x090909)
            );
            w.rotation.z=Math.PI/2;
            w.position.set(x,0.4,z);
            group.add(w);
        }
    }

    const laneIndex = Math.floor(Math.random()*3)-1;
    group.position.set(laneIndex*3,0,-105);
    scene.add(group);
    obstacles.push(group);
}

// LEVEL MANAGEMENT
function changeLevel(next) {
    level = next;
    buildWorld();

    if(car) scene.remove(car);
    car = createCar(levels[level]);

    document.getElementById("level").textContent =
        "0"+(level+1)+" / 03";
    document.getElementById("environment").textContent =
        levels[level].name;
    document.getElementById("carname").textContent =
        levels[level].car;

    const box = document.getElementById("upgrade");
    document.getElementById("upgradeText").textContent =
        levels[level].car + " — " + levels[level].name;
    box.style.display="block";
    setTimeout(()=>box.style.display="none",2500);
}

// START
function startGame() {
    distance=0;
    score=0;
    speed=0;
    lane=0;
    crashed=false;
    playing=true;
    spawnTimer=0;

    document.getElementById("start").style.display="none";

    changeLevel(0);
    camera.position.set(0,7,14);
    camera.lookAt(0,1,-8);
}

// INPUT
window.addEventListener("keydown", e => {
    keys[e.key.toLowerCase()]=true;

    if(["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"," "].includes(e.key))
        e.preventDefault();
});

window.addEventListener("keyup", e => {
    keys[e.key.toLowerCase()]=false;
});

window.addEventListener("blur",()=>{
    Object.keys(keys).forEach(k=>keys[k]=false);
});

document.getElementById("startBtn").addEventListener("click",startGame);

// COLLISION
function crash() {
    playing=false;
    crashed=true;

    if(Math.floor(score)>best) {
        best=Math.floor(score);
        localStorage.setItem("superdriveBest",best);
        document.getElementById("best").textContent=best;
    }

    const panel=document.getElementById("start");
    panel.style.display="flex";
    panel.querySelector("h1").innerHTML="RACE <span>OVER</span>";
    panel.querySelector("p").textContent=
        "DISTANCE: "+Math.floor(distance)+" M  |  SCORE: "+
        Math.floor(score)+"  |  TRY AGAIN!";
    document.getElementById("startBtn").textContent="RESTART RACE";
}

// GAME LOOP
function animate() {
    requestAnimationFrame(animate);

    const dt=Math.min(clock.getDelta(),0.04);

    if(playing && car) {
        const config=levels[level];

        // Acceleration and braking
        if(keys["w"] || keys["arrowup"]) speed+=65*dt;
        else speed-=12*dt;

        if(keys["s"] || keys["arrowdown"]) speed-=110*dt;

        speed=THREE.MathUtils.clamp(speed,0,config.maxSpeed);

        // Steering
        if(keys["a"] || keys["arrowleft"]) lane-=5*dt;
        if(keys["d"] || keys["arrowright"]) lane+=5*dt;

        lane=THREE.MathUtils.clamp(lane,-4.2,4.2);

        car.position.x=THREE.MathUtils.damp(
            car.position.x,lane,7,dt
        );

        // Car vibration
        car.rotation.z=THREE.MathUtils.damp(
            car.rotation.z,
            (lane-car.position.x)*0.1,5,dt
        );

        // Distance
        distance+=speed*dt*0.12;
        score+=speed*dt*0.5;

        // Road movement
        const movement=speed*dt*0.09;

        roadMarks.forEach(mark=>{
            mark.position.z+=movement;
            if(mark.position.z>10) mark.position.z-=320;
        });

        scenery.forEach(obj=>{
            obj.position.z+=movement;
            if(obj.position.z>12) obj.position.z-=340;
        });

        snow.forEach(f=>{
            f.position.z+=movement*2+dt*4;
            f.position.x+=Math.sin(f.position.z)*dt*0.3;
            if(f.position.z>12) {
                f.position.z=-130;
                f.position.x=(Math.random()-0.5)*45;
            }
        });

        // Spawn traffic
        spawnTimer+=dt;
        if(spawnTimer>Math.max(0.75,2.3-speed/180)) {
            spawnObstacle();
            spawnTimer=0;
        }

        // Move obstacles and collision
        for(let i=obstacles.length-1;i>=0;i--) {
            const o=obstacles[i];
            o.position.z+=movement*2.6;

            const dx=Math.abs(car.position.x-o.position.x);
            const dz=Math.abs(car.position.z-o.position.z);

            if(dx<1.7 && dz<2.5) {
                crash();
                break;
            }

            if(o.position.z>18) {
                scene.remove(o);
                obstacles.splice(i,1);
                score+=50;
            }
        }

        // Level thresholds
        if(level===0 && distance>=300) changeLevel(1);
        if(level===1 && distance>=700) changeLevel(2);

        // Dashboard
        document.getElementById("speed").textContent=
            String(Math.round(speed)).padStart(3,"0");
        document.getElementById("distance").textContent=
            String(Math.floor(distance)).padStart(4,"0");
        document.getElementById("score").textContent=
            String(Math.floor(score)).padStart(4,"0");

        document.getElementById("progress").style.width=
            Math.min(distance/1000*100,100)+"%";

        // Camera follows car
        camera.position.x=THREE.MathUtils.damp(
            camera.position.x,car.position.x*0.35,3,dt
        );
        camera.lookAt(car.position.x*0.2,1,-8);
    }

    // Idle car display before starting
    renderer.render(scene,camera);
}

// Initial preview
buildWorld();
car=createCar(levels[0]);
animate();

window.addEventListener("resize",()=>{
    camera.aspect=innerWidth/innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth,innerHeight);
});
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(GAME)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
