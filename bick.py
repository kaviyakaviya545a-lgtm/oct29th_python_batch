1
from flask import Flask, render_template_string

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SUPERBIKE 3D RACING</title>

<style>
* { box-sizing:border-box; margin:0; padding:0; }

body {
    overflow:hidden;
    background:#07101d;
    color:white;
    font-family:Arial,sans-serif;
}

canvas {
    position:fixed;
    inset:0;
    display:block;
}

#hud {
    position:fixed;
    z-index:5;
    top:15px;
    left:15px;
    right:15px;
    display:flex;
    justify-content:space-between;
    gap:10px;
    pointer-events:none;
}

.panel {
    background:rgba(3,12,28,.82);
    border:1px solid rgba(0,225,255,.4);
    border-radius:12px;
    padding:12px 17px;
    backdrop-filter:blur(8px);
}

.logo {
    font-size:21px;
    font-weight:900;
    letter-spacing:2px;
    color:#00eaff;
}

.stats {
    display:flex;
    gap:20px;
    text-align:center;
}

.stats small {
    display:block;
    color:#9db3cc;
    font-size:10px;
}

.stats strong {
    display:block;
    font-size:19px;
    margin-top:4px;
}

#levelBox {
    position:fixed;
    top:100px;
    left:17px;
    z-index:5;
    width:210px;
    pointer-events:none;
    font-size:12px;
    color:#00eaff;
    font-weight:bold;
}

#progress {
    height:6px;
    background:#26364a;
    margin-top:7px;
    border-radius:10px;
    overflow:hidden;
}

#progressFill {
    height:100%;
    width:0%;
    background:#00eaff;
}

#overlay {
    position:fixed;
    inset:0;
    z-index:20;
    display:flex;
    align-items:center;
    justify-content:center;
    background:rgba(1,7,18,.78);
    backdrop-filter:blur(7px);
}

#menu {
    width:min(92%,480px);
    padding:35px 25px;
    text-align:center;
    border:1px solid #00dfff;
    border-radius:18px;
    background:rgba(5,17,38,.96);
    box-shadow:0 0 35px rgba(0,225,255,.16);
}

#menu h1 {
    font-size:34px;
    color:#00eaff;
    letter-spacing:2px;
    margin-bottom:13px;
}

#menu p {
    color:#c6d5e9;
    line-height:1.7;
    margin-bottom:22px;
}

#startBtn {
    position:relative;
    z-index:25;
    pointer-events:auto;
    border:0;
    border-radius:9px;
    padding:15px 38px;
    background:linear-gradient(90deg,#00dfff,#0875ff);
    color:white;
    font-size:17px;
    font-weight:bold;
    letter-spacing:2px;
    cursor:pointer;
}

#startBtn:hover {
    transform:scale(1.05);
    box-shadow:0 0 22px #00dfff;
}

#help {
    margin-top:22px;
    font-size:12px;
    line-height:1.8;
    color:#9db3cc;
}

#message {
    color:#ffce55;
    margin-top:12px;
    min-height:18px;
}

#mobile {
    position:fixed;
    z-index:10;
    bottom:20px;
    left:0;
    right:0;
    display:flex;
    justify-content:space-between;
    padding:0 20px;
    pointer-events:none;
}

.group {
    display:flex;
    gap:10px;
}

.control {
    width:58px;
    height:58px;
    border-radius:50%;
    border:1px solid #00eaff;
    color:white;
    background:rgba(0,15,35,.8);
    font-size:22px;
    pointer-events:auto;
    touch-action:none;
}

@media(max-width:650px) {
    .logo {font-size:13px;}
    .panel {padding:9px;}
    .stats {gap:9px;}
    .stats strong {font-size:14px;}
    #levelBox {top:85px;}
    #menu h1 {font-size:27px;}
}
</style>
</head>

<body>

<div id="hud">
    <div class="panel">
        <div class="logo">SUPERBIKE 3D</div>
        <div style="font-size:10px;color:#9db3cc;margin-top:4px">
            EXTREME RACING
        </div>
    </div>

    <div class="panel stats">
        <div>
            <small>LEVEL</small>
            <strong id="level">1</strong>
        </div>
        <div>
            <small>SPEED</small>
            <strong><span id="speed">0</span> KM</strong>
        </div>
        <div>
            <small>SCORE</small>
            <strong id="score">0</strong>
        </div>
    </div>
</div>

<div id="levelBox">
    <div id="levelName">SNOW MOUNTAIN</div>
    <div id="progress"><div id="progressFill"></div></div>
</div>

<div id="overlay">
    <div id="menu">
        <h1 id="menuTitle">SUPERBIKE 3D</h1>
        <p id="menuText">
            Get ready for an extreme superbike adventure!
            Race through snow, mud and highway environments.
            Upgrade your superbike at every level.
        </p>

        <button id="startBtn" type="button">START RACE</button>

        <div id="help">
            W / UP ARROW – ACCELERATE<br>
            S / DOWN ARROW – BRAKE<br>
            A / LEFT ARROW – TURN LEFT<br>
            D / RIGHT ARROW – TURN RIGHT
        </div>
        <div id="message"></div>
    </div>
</div>

<div id="mobile">
    <div class="group">
        <button class="control" id="leftBtn">◀</button>
        <button class="control" id="rightBtn">▶</button>
    </div>
    <div class="group">
        <button class="control" id="brakeBtn">▼</button>
        <button class="control" id="gasBtn">▲</button>
    </div>
</div>

<script type="module">
import * as THREE from
'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';

// --------------------------------------------------
// BASIC THREE.JS SETUP
// --------------------------------------------------

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
    65, window.innerWidth/window.innerHeight, 0.1, 300
);

camera.position.set(0,5,11);

const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff,0x46566b,2));

const sunlight = new THREE.DirectionalLight(0xffffff,2.5);
sunlight.position.set(-5,12,8);
sunlight.castShadow = true;
scene.add(sunlight);

// --------------------------------------------------
// LEVEL DETAILS
// --------------------------------------------------

const levels = [
    {
        name:"SNOW MOUNTAIN",
        bike:"FROST R1",
        color:0x00aaff,
        ground:0xddeeff,
        road:0x596575,
        sky:0x9bc9ed,
        obstacle:0x263b55,
        speedLimit:30
    },
    {
        name:"MUD TERRITORY",
        bike:"DIRT BEAST X",
        color:0xff7518,
        ground:0x795633,
        road:0x493323,
        sky:0xb6a07b,
        obstacle:0x302115,
        speedLimit:40
    },
    {
        name:"NEON HIGHWAY",
        bike:"PHANTOM RR",
        color:0xb52aff,
        ground:0x080d1c,
        road:0x171d32,
        sky:0x080d1c,
        obstacle:0xff235b,
        speedLimit:50
    }
];

// --------------------------------------------------
// GAME VARIABLES
// --------------------------------------------------

let bike = null;
let currentLevel = 0;
let running = false;
let speed = 0;
let distance = 0;
let score = 0;
let steering = 0;
let spawnTimer = 0;

let obstacles = [];
let roadMarks = [];
let scenery = [];
let wheels = [];

const keys = {
    left:false,
    right:false,
    gas:false,
    brake:false
};

const ui = {
    overlay:document.getElementById("overlay"),
    title:document.getElementById("menuTitle"),
    text:document.getElementById("menuText"),
    button:document.getElementById("startBtn"),
    message:document.getElementById("message"),
    level:document.getElementById("level"),
    speed:document.getElementById("speed"),
    score:document.getElementById("score"),
    levelName:document.getElementById("levelName"),
    progress:document.getElementById("progressFill")
};

// --------------------------------------------------
// HELPER: CREATE BIKE PARTS
// --------------------------------------------------

function addPart(parent,geometry,material,x,y,z) {
    const mesh = new THREE.Mesh(geometry,material);
    mesh.position.set(x,y,z);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    parent.add(mesh);
    return mesh;
}

function makeBeam(parent,start,end,radius,material) {
    const a = new THREE.Vector3(...start);
    const b = new THREE.Vector3(...end);
    const direction = new THREE.Vector3().subVectors(b,a);
    const length = direction.length();

    const mesh = new THREE.Mesh(
        new THREE.CylinderGeometry(radius,radius,length,10),
        material
    );

    mesh.position.copy(a).add(b).multiplyScalar(0.5);
    mesh.quaternion.setFromUnitVectors(
        new THREE.Vector3(0,1,0),
        direction.normalize()
    );

    mesh.castShadow = true;
    parent.add(mesh);
    return mesh;
}

// --------------------------------------------------
// CREATE 3D SUPERBIKE
// --------------------------------------------------

function createBike(config) {
    const group = new THREE.Group();

    const paint = new THREE.MeshStandardMaterial({
        color:config.color,
        metalness:0.7,
        roughness:0.23
    });

    const black = new THREE.MeshStandardMaterial({
        color:0x090d13,
        metalness:0.35,
        roughness:0.45
    });

    const metal = new THREE.MeshStandardMaterial({
        color:0x9aa9b8,
        metalness:0.9,
        roughness:0.2
    });

    const glass = new THREE.MeshStandardMaterial({
        color:0x162d48,
        metalness:0.7,
        roughness:0.15
    });

    const headlight = new THREE.MeshStandardMaterial({
        color:0xffffff,
        emissive:0x9bdfff,
        emissiveIntensity:2
    });

    // Two wheels
    wheels = [];

    const wheelGeometry = new THREE.CylinderGeometry(
        0.43,0.43,0.22,32
    );

    for (const z of [-1.15,1.15]) {
        const wheel = addPart(
            group,wheelGeometry,black,0,0.45,z
        );

        wheel.rotation.z = Math.PI/2;
        wheels.push(wheel);

        const rim = addPart(
            group,
            new THREE.CylinderGeometry(0.23,0.23,0.24,24),
            metal,0,0.45,z
        );

        rim.rotation.z = Math.PI/2;
    }

    // Main frame
    makeBeam(group,[0,0.6,-0.8],[0,0.85,0.65],0.09,metal);
    makeBeam(group,[0,0.85,0.65],[0,0.5,1.15],0.08,metal);
    makeBeam(group,[0,0.6,-0.8],[0,0.5,1.15],0.06,black);

    // Engine
    addPart(
        group,
        new THREE.BoxGeometry(0.55,0.65,0.65),
        black,0,0.75,0.25
    );

    // Fuel tank
    addPart(
        group,
        new THREE.SphereGeometry(0.53,20,16),
        paint,0,1.15,-0.05
    );

    // Front body fairing
    addPart(
        group,
        new THREE.SphereGeometry(0.48,20,16),
        paint,0,1.15,-0.75
    ).scale.set(0.9,1.1,0.75);

    // Rear seat
    addPart(
        group,
        new THREE.BoxGeometry(0.5,0.16,0.75),
        black,0,1.15,0.75
    );

    // Tail body
    addPart(
        group,
        new THREE.BoxGeometry(0.55,0.3,0.65),
        paint,0,1.1,1.0
    );

    // Front forks
    makeBeam(group,[-0.16,0.48,-1.1],[-0.16,1.3,-0.75],0.055,metal);
    makeBeam(group,[0.16,0.48,-1.1],[0.16,1.3,-0.75],0.055,metal);

    // Handlebar
    makeBeam(group,[-0.55,1.45,-0.7],[0.55,1.45,-0.7],0.045,metal);

    // Mirrors
    for (const x of [-0.5,0.5]) {
        makeBeam(group,[x,1.4,-0.65],[x*1.3,1.7,-0.75],0.025,metal);

        addPart(
            group,
            new THREE.SphereGeometry(0.1,12,10),
            black,x*1.3,1.7,-0.75
        );
    }

    // Headlight
    addPart(
        group,
        new THREE.SphereGeometry(0.18,16,12),
        headlight,0,1.25,-1.0
    );

    // Exhaust
    makeBeam(group,[0.3,0.55,0.45],[0.4,0.5,1.05],0.09,metal);

    // Rider helmet
    addPart(
        group,
        new THREE.SphereGeometry(0.28,18,16),
        black,0,1.85,0.0
    );

    // Rider body
    addPart(
        group,
        new THREE.BoxGeometry(0.48,0.65,0.38),
        black,0,1.48,0.1
    );

    // Rider arms
    makeBeam(group,[-0.2,1.65,-0.05],[-0.45,1.42,-0.7],0.09,black);
    makeBeam(group,[0.2,1.65,-0.05],[0.45,1.42,-0.7],0.09,black);

    // Rider legs
    makeBeam(group,[-0.2,1.3,0.2],[-0.35,0.7,0.7],0.1,black);
    makeBeam(group,[0.2,1.3,0.2],[0.35,0.7,0.7],0.1,black);

    // Light effect
    const glow = new THREE.PointLight(config.color,2,5);
    glow.position.set(0,0.8,0);
    group.add(glow);

    group.position.set(0,0,4);
    scene.add(group);

    return group;
}

// --------------------------------------------------
// WORLD BUILDING
// --------------------------------------------------

function clearList(list) {
    list.forEach(obj => scene.remove(obj));
    list.length = 0;
}

function buildWorld() {
    clearList(obstacles);
    clearList(roadMarks);
    clearList(scenery);

    const config = levels[currentLevel];

    scene.background = new THREE.Color(config.sky);
    scene.fog = new THREE.Fog(config.sky,35,150);

    // Ground
    const ground = new THREE.Mesh(
        new THREE.PlaneGeometry(200,300),
        new THREE.MeshStandardMaterial({
            color:config.ground,
            roughness:1
        })
    );

    ground.rotation.x = -Math.PI/2;
    ground.position.z = -80;
    ground.receiveShadow = true;
    scene.add(ground);
    scenery.push(ground);

    // Racing road
    const road = new THREE.Mesh(
        new THREE.PlaneGeometry(12,300),
        new THREE.MeshStandardMaterial({
            color:config.road,
            roughness:0.9
        })
    );

    road.rotation.x = -Math.PI/2;
    road.position.set(0,0.02,-80);
    road.receiveShadow = true;
    scene.add(road);
    scenery.push(road);

    // Road edges
    for (const x of [-6,6]) {
        const edge = new THREE.Mesh(
            new THREE.BoxGeometry(0.18,0.12,300),
            new THREE.MeshStandardMaterial({color:0xffffff})
        );

        edge.position.set(x,0.1,-80);
        scene.add(edge);
        scenery.push(edge);
    }

    // Lane markings
    for (let z=-230;z<15;z+=12) {
        const mark = new THREE.Mesh(
            new THREE.BoxGeometry(0.12,0.04,5),
            new THREE.MeshStandardMaterial({
                color:currentLevel===2 ? 0x00eaff : 0xffffff,
                emissive:currentLevel===2 ? 0x0088ff : 0x000000,
                emissiveIntensity:1.5
            })
        );

        mark.position.set(0,0.08,z);
        scene.add(mark);
        roadMarks.push(mark);
    }

    // Environment
    for (let i=0;i<35;i++) {
        for (const side of [-1,1]) {
            let object;

            if (currentLevel===0) {
                object = new THREE.Mesh(
                    new THREE.ConeGeometry(1.4,5,7),
                    new THREE.MeshStandardMaterial({color:0x31513b})
                );
            } else if (currentLevel===1) {
                object = new THREE.Mesh(
                    new THREE.DodecahedronGeometry(1.4),
                    new THREE.MeshStandardMaterial({color:0x49331d})
                );
            } else {
                object = new THREE.Mesh(
                    new THREE.BoxGeometry(0.3,7,0.3),
                    new THREE.MeshStandardMaterial({
                        color:0x00eaff,
                        emissive:0x0077ff,
                        emissiveIntensity:2
                    })
                );
            }

            object.position.set(
                side*(9+Math.random()*5),
                currentLevel===2 ? 3.5 : 2,
                -i*8-5
            );

            scene.add(object);
            scenery.push(object);
        }
    }

    // New bike for each level
    if (bike) scene.remove(bike);

    bike = createBike(config);

    ui.level.textContent = currentLevel+1;
    ui.levelName.textContent = config.name;
}

// --------------------------------------------------
// OBSTACLE CREATION
// --------------------------------------------------

function spawnObstacle() {
    const config = levels[currentLevel];

    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.BoxGeometry(1.4,1.1,1.4),
        new THREE.MeshStandardMaterial({
            color:config.obstacle,
            metalness:0.35
        })
    );

    body.position.y=0.65;
    body.castShadow=true;
    group.add(body);

    // Obstacle warning light
    const light = new THREE.PointLight(0xff3333,1,4);
    light.position.y=1.5;
    group.add(light);

    group.position.set(
        [-3.5,0,3.5][Math.floor(Math.random()*3)],
        0,
        -110
    );

    scene.add(group);
    obstacles.push(group);
}

// --------------------------------------------------
// GAME START / RESTART
// --------------------------------------------------

function startGame() {
    currentLevel=0;
    speed=0;
    distance=0;
    score=0;
    steering=0;
    spawnTimer=0;

    keys.left=false;
    keys.right=false;
    keys.gas=false;
    keys.brake=false;

    buildWorld();

    ui.overlay.style.display="none";
    ui.title.textContent="SUPERBIKE 3D";
    ui.text.textContent="Get ready for an extreme superbike adventure!";
    ui.button.textContent="START RACE";
    ui.message.textContent="";

    running=true;
    updateUI();
}

// Direct button click event
ui.button.addEventListener("click",function(event) {
    event.preventDefault();
    event.stopPropagation();

    if (!running) {
        startGame();
    }
});

// --------------------------------------------------
// GAME OVER / WIN
// --------------------------------------------------

function gameOver() {
    if (!running) return;

    running=false;
    speed=0;

    ui.title.textContent="RACE OVER!";
    ui.text.innerHTML=
        "Final score: <b>"+Math.floor(score)+
        "</b><br>Distance: <b>"+Math.floor(distance)+" m</b>";

    ui.button.textContent="PLAY AGAIN";
    ui.overlay.style.display="flex";
}

function finishGame() {
    running=false;
    speed=0;

    ui.title.textContent="SUPERBIKE CHAMPION!";
    ui.text.innerHTML=
        "Amazing! You completed all three levels."+
        "<br>Final score: <b>"+Math.floor(score)+"</b>";

    ui.button.textContent="RACE AGAIN";
    ui.overlay.style.display="flex";
}

// --------------------------------------------------
// LEVEL UPGRADES
// --------------------------------------------------

function changeLevel(number) {
    if (number>=3) {
        finishGame();
        return;
    }

    currentLevel=number;
    buildWorld();

    ui.message.textContent="BIKE UPGRADED: "+levels[number].bike;
}

// --------------------------------------------------
// UI UPDATE
// --------------------------------------------------

function updateUI() {
    ui.speed.textContent=Math.floor(speed*4);
    ui.score.textContent=Math.floor(score);

    const start=currentLevel===0 ? 0 :
                 currentLevel===1 ? 300 : 700;

    const end=currentLevel===0 ? 300 :
               currentLevel===1 ? 700 : 1000;

    const percent=Math.min(
        100,Math.max(0,(distance-start)/(end-start)*100)
    );

    ui.progress.style.width=percent+"%";
}

// --------------------------------------------------
// KEYBOARD CONTROLS
// --------------------------------------------------

window.addEventListener("keydown",event=>{
    const k=event.key.toLowerCase();

    if (["arrowup","arrowdown","arrowleft","arrowright"," "].includes(k)) {
        event.preventDefault();
    }

    if (k==="a" || k==="arrowleft") keys.left=true;
    if (k==="d" || k==="arrowright") keys.right=true;
    if (k==="w" || k==="arrowup") keys.gas=true;
    if (k==="s" || k==="arrowdown") keys.brake=true;
});

window.addEventListener("keyup",event=>{
    const k=event.key.toLowerCase();

    if (k==="a" || k==="arrowleft") keys.left=false;
    if (k==="d" || k==="arrowright") keys.right=false;
    if (k==="w" || k==="arrowup") keys.gas=false;
    if (k==="s" || k==="arrowdown") keys.brake=false;
});

// --------------------------------------------------
// MOBILE BUTTONS
// --------------------------------------------------

function holdButton(id,key) {
    const button=document.getElementById(id);

    button.addEventListener("pointerdown",event=>{
        event.preventDefault();
        keys[key]=true;
    });

    function release() {
        keys[key]=false;
    }

    button.addEventListener("pointerup",release);
    button.addEventListener("pointerleave",release);
    button.addEventListener("pointercancel",release);
}

holdButton("leftBtn","left");
holdButton("rightBtn","right");
holdButton("gasBtn","gas");
holdButton("brakeBtn","brake");

// --------------------------------------------------
// MAIN GAME UPDATE
// --------------------------------------------------

function updateGame(delta) {
    const config=levels[currentLevel];

    // Speed
    if (keys.gas) speed+=12*delta;
    else speed-=2.5*delta;

    if (keys.brake) speed-=18*delta;

    speed=THREE.MathUtils.clamp(speed,0,config.speedLimit);

    // Steering
    if (keys.left) steering-=5*delta;
    if (keys.right) steering+=5*delta;

    if (!keys.left && !keys.right) {
        steering*=0.9;
    }

    steering=THREE.MathUtils.clamp(steering,-1,1);

    bike.position.x+=steering*speed*0.012;
    bike.position.x=THREE.MathUtils.clamp(bike.position.x,-4.8,4.8);

    bike.rotation.z=-steering*0.16;

    // Wheel rotation
    wheels.forEach(wheel=>{
        wheel.rotation.x-=speed*delta*0.15;
    });

    // Distance and score
    distance+=speed*delta*0.8;
    score+=speed*delta*2;

    // Move road lines
    roadMarks.forEach(mark=>{
        mark.position.z+=speed*delta*1.8;

        if (mark.position.z>12) {
            mark.position.z-=240;
        }
    });

    // Move environment
    scenery.forEach(object=>{
        if (object.position.z>15) {
            object.position.z-=280;
        }
    });

    // Spawn obstacles
    spawnTimer+=delta;

    if (spawnTimer>Math.max(0.7,2.5-speed*0.035)) {
        spawnObstacle();
        spawnTimer=0;
    }

    // Move obstacles and check collision
    for (let i=obstacles.length-1;i>=0;i--) {
        const obstacle=obstacles[i];

        obstacle.position.z+=speed*delta*1.8;

        const hitX=Math.abs(obstacle.position.x-bike.position.x)<1.25;
        const hitZ=Math.abs(obstacle.position.z-bike.position.z)<1.6;

        if (hitX && hitZ) {
            gameOver();
            return;
        }

        if (obstacle.position.z>15) {
            scene.remove(obstacle);
            obstacles.splice(i,1);
            score+=20;
        }
    }

    // Camera follows bike
    camera.position.x+=(bike.position.x*0.4-camera.position.x)*4*delta;
    camera.lookAt(bike.position.x*0.3,1,-5);

    // Level progression
    if (currentLevel===0 && distance>=300) {
        changeLevel(1);
    } else if (currentLevel===1 && distance>=700) {
        changeLevel(2);
    } else if (currentLevel===2 && distance>=1000) {
        finishGame();
        return;
    }

    updateUI();
}

// --------------------------------------------------
// ANIMATION LOOP
// --------------------------------------------------

let lastTime=0;

function animate(time=0) {
    requestAnimationFrame(animate);

    const delta=Math.min((time-lastTime)/1000,0.05);
    lastTime=time;

    if (running) {
        updateGame(delta);
    }

    renderer.render(scene,camera);
}

// --------------------------------------------------
// SCREEN RESIZE
// --------------------------------------------------

window.addEventListener("resize",()=>{
    camera.aspect=window.innerWidth/window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth,window.innerHeight);
});

// INITIAL GAME
buildWorld();
animate();

</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
