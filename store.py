
from flask import Flask, jsonify, render_template_string
import psutil, shutil, os

app = Flask(__name__)

def get_storage():
    disk = shutil.disk_usage(os.path.abspath(os.sep))
    total = disk.total / (1024**3)
    used = disk.used / (1024**3)
    free = disk.free / (1024**3)
    percent = disk.used / disk.total * 100

    if percent >= 90:
        status = "Critical"
        insight = "Storage is almost full! Delete unnecessary files or move large files."
    elif percent >= 75:
        status = "Warning"
        insight = "Storage is getting full. Consider cleaning unused files."
    else:
        status = "Healthy"
        insight = "Storage is healthy. You have enough free space."

    return dict(total=round(total, 2), used=round(used, 2),
                free=round(free, 2), percent=round(percent, 1),
                status=status, insight=insight)

@app.route("/api/storage")
def api_storage():
    return jsonify(get_storage())

@app.route("/")
def home():
    return render_template_string(HTML)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Storage Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
*{box-sizing:border-box}
body{margin:0;font-family:Segoe UI,Arial;background:#090e1b;color:#fff;
background:radial-gradient(circle at top left,#192c50,#090e1b 60%)}
main{max-width:1100px;margin:auto;padding:30px}
h1{margin-bottom:5px}
.sub{color:#9eabc5}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin:25px 0}
.card{padding:23px;border:1px solid #ffffff18;border-radius:20px;
background:linear-gradient(135deg,#ffffff12,#ffffff04);
box-shadow:0 10px 35px #0005;backdrop-filter:blur(14px)}
.label{color:#a8b5d0;font-size:14px}
.value{font-size:30px;font-weight:700;margin-top:12px}
.blue{color:#63a9ff}.green{color:#56e0bd}.pink{color:#cf8cff}
.panel{display:grid;grid-template-columns:1.2fr 1fr;gap:18px}
button{border:0;border-radius:12px;padding:12px 20px;color:white;
background:linear-gradient(90deg,#477bff,#a15bff);cursor:pointer}
.insight{padding:20px;border-radius:15px;background:#14233d;color:#c9d8f5;
line-height:1.7}
@media(max-width:700px){.panel{grid-template-columns:1fr}main{padding:17px}}
</style>
</head>
<body>
<main>
<h1>💾 Storage Intelligence</h1>
<p class="sub">AI-powered style computer storage monitor</p>

<div class="grid">
 <div class="card"><div class="label">Total Storage</div>
 <div class="value blue" id="total">-- GB</div></div>
 <div class="card"><div class="label">Used Storage</div>
 <div class="value pink" id="used">-- GB</div></div>
 <div class="card"><div class="label">Free Storage</div>
 <div class="value green" id="free">-- GB</div></div>
 <div class="card"><div class="label">Storage Usage</div>
 <div class="value" id="percent">--%</div><div id="status">Loading...</div></div>
</div>

<div class="panel">
 <div class="card"><h3>Storage Usage Chart</h3>
 <canvas id="chart"></canvas></div>
 <div class="card"><h3>🤖 Smart Storage Analysis</h3>
 <div class="insight" id="insight">Analyzing storage...</div>
 <p style="margin-top:22px"><button onclick="refresh()">↻ Refresh Storage</button></p>
 </div>
</div>
</main>

<script>
let chart;
async function refresh(){
 try{
  const r=await fetch('/api/storage');
  const d=await r.json();
  document.getElementById('total').textContent=d.total+' GB';
  document.getElementById('used').textContent=d.used+' GB';
  document.getElementById('free').textContent=d.free+' GB';
  document.getElementById('percent').textContent=d.percent+'%';
  document.getElementById('status').textContent='● '+d.status;
  document.getElementById('insight').textContent=d.insight;

  if(chart){
   chart.data.datasets[0].data=[d.used,d.free];
   chart.update();
  }else{
   chart=new Chart(document.getElementById('chart'),{
    type:'doughnut',
    data:{labels:['Used','Free'],datasets:[{
     data:[d.used,d.free],backgroundColor:['#9b69ff','#32d6bd'],
     borderWidth:0,hoverOffset:10}]},
    options:{plugins:{legend:{labels:{color:'white'}}},
    cutout:'72%'}
   });
  }
 }catch(e){
  document.getElementById('insight').textContent='Could not read storage. Please refresh.';
 }
}
refresh();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
