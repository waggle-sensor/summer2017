
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def memInfoPage():
        memFile = open('/proc/meminfo')
        memInfo = [line.split('\n') for line in memFile.readlines()]
        cpuFile = open('/proc/cpuinfo')
        cpuInfo = [line.split('\n') for line in cpuFile.readlines()]
        return render_template('myTemplate.html', memInfo=memInfo, cpuInfo=cpuInfo)

if __name__ == "__main__":
    app.run()
