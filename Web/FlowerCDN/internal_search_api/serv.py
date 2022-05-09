from flask import Flask, request
from time import sleep

employees = [
    {
        "name":"Dominique",
        "surname":"Lavigne"
    }
]

app = Flask(__name__)
@app.route('/',methods=["GET"])
def index():
    return "Welcome to the internal employee search api. To use this service, please read the associated documentation on the associated private github repository."

@app.route('/search',methods=["GET"])
def search():
    if(request.args.get("name") and request.args.get("surname") and request.args.get("searchby")):
        if request.args.get("searchby") in ["name","surname"]:
            searchBy = request.args.get("searchby")
            for employee in employees:
                found = True
                for i in range(len(request.args[searchBy])):
                    if i >= len(employee[searchBy]): break
                    if(request.args[searchBy][i] == employee[searchBy][i]):
                        sleep(0.3)
                    else: 
                        found = False
                        break
            if(found):
                return f"Found an employee that match your research: {employees[0]['name']} {employees[0]['surname']}"
            else: return "Not found"
        else: return "Invalid value for parameter 'searchBy'"
    else: return "Missing parameter, please check the documentation."

app.run(host="0.0.0.0",port="80")
