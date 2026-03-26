
from flask import Flask, request, render_template_string
import schedule, time, threading, subprocess

app=Flask(__name__)
SCHEDULED_QUERY=""
INTERVAL=30

TEMPLATE="""
<form method='post'>
  Căutare: <input name='query'><br>
  Interval minute: <input name='interval'><br>
  <button>Set</button>
</form>
<p>Curent: {{q}} la {{i}} min</p>
"""

def task():
    if SCHEDULED_QUERY:
        subprocess.run(["sldl","-i","/data/list.txt","--auto","--download"])

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

@app.route("/", methods=["GET", "POST"])
def index():
    global SCHEDULED_QUERY, INTERVAL

    if request.method == "POST":
        SCHEDULED_QUERY = request.form["query"].strip()

        # FIX pentru interval gol
        interval_str = request.form.get("interval", "").strip()
        if interval_str == "":
            INTERVAL = 30
        else:
            INTERVAL = int(interval_str)

        # salvăm query în listă
        with open("/data/list.txt", "w") as f:
            f.write(SCHEDULED_QUERY)

        # resetăm schedulerul
        schedule.clear()
        schedule.every(INTERVAL).minutes.do(task)

    return render_template_string(TEMPLATE, q=SCHEDULED_QUERY, i=INTERVAL)

threading.Thread(target=run_scheduler,daemon=True).start()

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)
