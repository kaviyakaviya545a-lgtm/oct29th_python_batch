
from flask import Flask, render_template_string

app = Flask(__name__)

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Task Master AI</title>
<style>
*{box-sizing:border-box}
body{
 margin:0;font-family:Segoe UI,Arial,sans-serif;color:#f4f6ff;
 background:radial-gradient(circle at top,#202c55,#0b1020 60%);
 min-height:100vh;padding:24px
}
.container{max-width:950px;margin:auto}
header{text-align:center;margin:15px 0 28px}
header h1{font-size:34px;margin:0;color:#8ee9ff}
header p{color:#aab5d1}
.panel{
 background:#151d35;border:1px solid #2e3b60;
 border-radius:20px;padding:22px;margin-bottom:18px;
 box-shadow:0 10px 35px #0003
}
.stats{display:flex;gap:12px;flex-wrap:wrap}
.stat{flex:1;min-width:110px;background:#202b49;padding:16px;border-radius:14px;text-align:center}
.stat strong{display:block;font-size:27px;color:#72e4ff}
.stat span{font-size:13px;color:#bac6e2}
input,select{
 width:100%;padding:13px;background:#0e152a;border:1px solid #354367;
 border-radius:10px;color:white;margin:8px 0
}
button{
 border:0;border-radius:11px;padding:12px 16px;font-weight:600;
 cursor:pointer;background:#49c9ed;color:#081423;margin:5px 4px 5px 0
}
button:hover{filter:brightness(1.1)}
.secondary{background:#303c5c;color:white}
.callbtn{background:#62e3a5;color:#09251a}
.danger{background:#ff7085;color:#2b0910}
.task{
 display:flex;align-items:center;justify-content:space-between;
 gap:12px;background:#202b49;margin:9px 0;padding:13px;border-radius:12px
}
.task.done{opacity:.55;text-decoration:line-through}
.task span{flex:1;overflow-wrap:anywhere}
.task button{padding:8px 10px}
#callBox{display:none;text-align:center}
.avatar{
 width:95px;height:95px;margin:12px auto;border-radius:50%;
 display:grid;place-items:center;font-size:40px;
 background:linear-gradient(140deg,#55d5ff,#8667ff);
 box-shadow:0 0 30px #6a90ff66
}
#status{color:#8ee9ff;margin:10px}
#log{min-height:24px;color:#c1cbea;margin-top:8px}
.small{color:#aebbd6;font-size:13px}
@media(max-width:550px){body{padding:12px}.panel{padding:15px}header h1{font-size:27px}}
</style>
</head>
<body>
<div class="container">
<header>
 <h1>⚡ TASK MASTER AI</h1>
 <p>Your friendly daily productivity voice companion</p>
</header>

<div class="panel">
 <div class="stats">
  <div class="stat"><strong id="total">0</strong><span>Total Tasks</span></div>
  <div class="stat"><strong id="completed">0</strong><span>Completed</span></div>
  <div class="stat"><strong id="remaining">0</strong><span>Remaining</span></div>
 </div>
</div>

<div class="panel">
 <h2>📝 My Tasks</h2>
 <input id="taskInput" placeholder="Add a task (e.g. Practice Python)">
 <button onclick="addTask()">＋ Add Task</button>
 <button class="secondary" onclick="clearDone()">Clear Completed</button>
 <div id="taskList"></div>
</div>

<div class="panel">
 <h2>📞 Voice Companion</h2>
 <p class="small">Choose a language, then start your motivating voice session.</p>
 <select id="language">
  <option value="mix">Tamil + English (Tanglish style)</option>
  <option value="en">English</option>
  <option value="ta">Tamil</option>
 </select>
 <button class="callbtn" onclick="startCall()">📞 Start AI Call</button>
 <button class="secondary" onclick="stopCall()">🔴 End Call</button>

 <div id="callBox">
  <div class="avatar">🤖</div>
  <h2>Task Master is talking...</h2>
  <div id="status">Connected</div>
  <button onclick="talkAgain()">🔊 Speak Again</button>
  <button class="secondary" onclick="listen()">🎤 Reply to AI</button>
  <div id="log"></div>
 </div>
</div>
<p class="small" style="text-align:center">Your tasks are saved in this browser on this device.</p>
</div>

<script>
let tasks = JSON.parse(localStorage.getItem("tm_tasks") || "[]");
let currentMessage = "";
let recognition;
let isCalling = false;

function save(){
 localStorage.setItem("tm_tasks",JSON.stringify(tasks));
 render();
}
function addTask(){
 let input=document.getElementById("taskInput");
 let text=input.value.trim();
 if(!text)return;
 tasks.push({text:text,done:false});
 input.value="";
 save();
}
document.getElementById("taskInput").addEventListener("keydown",e=>{
 if(e.key==="Enter")addTask();
});
function toggleTask(i){tasks[i].done=!tasks[i].done;save();}
function removeTask(i){tasks.splice(i,1);save();}
function clearDone(){tasks=tasks.filter(t=>!t.done);save();}
function render(){
 let list=document.getElementById("taskList");
 list.innerHTML="";
 tasks.forEach((t,i)=>{
  let div=document.createElement("div");
  div.className="task"+(t.done?" done":"");
  let span=document.createElement("span");
  span.textContent=(t.done?"✅ ":"☐ ")+t.text;
  let check=document.createElement("button");
  check.className="secondary";
  check.textContent=t.done?"Undo":"Done";
  check.onclick=()=>toggleTask(i);
  let del=document.createElement("button");
  del.className="danger";
  del.textContent="✕";
  del.onclick=()=>removeTask(i);
  div.append(span,check,del);
  list.appendChild(div);
 });
 document.getElementById("total").textContent=tasks.length;
 document.getElementById("completed").textContent=tasks.filter(t=>t.done).length;
 document.getElementById("remaining").textContent=tasks.filter(t=>!t.done).length;
}
render();

function getLanguage(){return document.getElementById("language").value;}
function getVoiceLang(){
 let l=getLanguage();
 return l==="ta"?"ta-IN":"en-IN";
}
function speak(text){
 if(!("speechSynthesis" in window)){
  alert("Speech is not supported. Try Chrome browser.");return;
 }
 speechSynthesis.cancel();
 let utter=new SpeechSynthesisUtterance(text);
 utter.lang=getVoiceLang();
 utter.rate=0.92;
 utter.pitch=1.08;
 utter.volume=1;
 let voices=speechSynthesis.getVoices();
 let preferred=voices.find(v=>v.lang.toLowerCase().startsWith(getVoiceLang().toLowerCase()));
 if(preferred)utter.voice=preferred;
 speechSynthesis.speak(utter);
 currentMessage=text;
}
function greeting(){
 let pending=tasks.filter(t=>!t.done);
 let done=tasks.filter(t=>t.done);
 let lang=getLanguage();
 if(lang==="ta"){
  return `வணக்கம்! நான் உங்க Task Master AI. ${pending.length} வேலைகள் இன்னும் இருக்கின்றன. கவலைப்படாதீங்க. ஒவ்வொன்றாக செய்வோம். நீங்க முடியும்!`;
 }
 if(lang==="en"){
  return `Hello! This is your Task Master. You have ${pending.length} tasks remaining and ${done.length} completed. Let's take one small step at a time. You can do this!`;
 }
 return `வணக்கம்! Hi! I'm your Task Master. இன்று ${pending.length} tasks pending இருக்கு. ${done.length} tasks complete பண்ணிட்டீங்க. Super! Let's do one task at a time. நீங்க கண்டிப்பா முடிப்பீங்க!`;
}
function startCall(){
 isCalling=true;
 document.getElementById("callBox").style.display="block";
 document.getElementById("status").textContent="🟢 Voice session active";
 document.getElementById("log").textContent="";
 speak(greeting());
}
function talkAgain(){
 if(!isCalling)return;
 speak(greeting());
}
function stopCall(){
 isCalling=false;
 speechSynthesis.cancel();
 if(recognition){try{recognition.stop()}catch(e){}}
 document.getElementById("callBox").style.display="none";
 document.getElementById("log").textContent="Call ended. Keep going—you've got this!";
}

function listen(){
 if(!isCalling)return;
 const SpeechRecognition=window.SpeechRecognition||window.webkitSpeechRecognition;
 if(!SpeechRecognition){
  document.getElementById("log").textContent="Voice recognition not supported. Use Chrome.";
  return;
 }
 recognition=new SpeechRecognition();
 recognition.lang=getVoiceLang();
 recognition.continuous=false;
 recognition.interimResults=false;
 document.getElementById("status").textContent="🎤 Listening... Speak now";
 recognition.onresult=e=>{
  let reply=e.results[0][0].transcript.toLowerCase();
  document.getElementById("log").textContent="You: "+reply;
  respond(reply);
 };
 recognition.onerror=()=>{
  document.getElementById("status").textContent="Mic error. Check microphone permission.";
 };
 recognition.onend=()=>{
  if(isCalling)document.getElementById("status").textContent="🟢 Voice session active";
 };
 recognition.start();
}
function respond(reply){
 let lang=getLanguage();
 let doneWords=["done","finished","completed","முடிச்ச","முடித்த","ஆச்சு"];
 let yes=doneWords.some(w=>reply.includes(w));
 let msg;
 if(yes){
  msg=lang==="ta"?"அருமை! நீங்க நல்லா செய்றீங்க. அடுத்த வேலையை முயற்சி செய்யலாமா?":
      lang==="en"?"Awesome! Well done. You're making progress. Pick your next task and keep going!":
      "அருமை! Super job! One task complete. அடுத்த task-க்கு போலாம். நீங்க நல்லா முன்னேறிட்டு இருக்கீங்க!";
 }else{
  msg=lang==="ta"?"பரவாயில்லை. சின்னதாக ஆரம்பியுங்கள். உங்களால் முடியும்!":
      lang==="en"?"That's okay. Start with just five minutes. Small progress is still progress!":
      "பரவாயில்லை! It's okay. 5 minutes மட்டும் try பண்ணுங்க. Small steps தான் பெரிய progress. நீங்க முடியும்!";
 }
 speak(msg);
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(PAGE)

if __name__ == "__main__":
    app.run(debug=True)
