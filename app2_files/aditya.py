"""
Templates:
Flask looks for a directory called templates in the
root of the Flask application package for HTML Files
static:
Flask has reserved a separate folder where you should
put static files such as CSS, Javascript, images or other files
"""
import os
from flask import Flask, render_template, jsonify

aditya = Flask(__name__)         # create a new Flask app instance

# alpine os
get_container_ip_ = str(os.popen(
    "ifconfig | grep 'Bcast' | cut -d: -f2 | awk '{print $2}'").read()).splitlines()[0]

# mac os
# get_container_ip_ = str(os.popen(
#     "ifconfig | grep 'broadcast' | cut -d: -f2 | awk '{print $2}'").read()).splitlines()[0]
techs = [
    {
        "techs_id": 1,
        "backend_running_container_ip": get_container_ip_
    },
    {
        "techs_id": 2,
        "Cloud_Worked_On": ["AWS", "Azure"],
        "Cloud_Working": ["Azure", "GCP"],
        "Cloud_Pending": ["Alibaba", "Openshift"]
    },
    {
        "techs_id": 3,
        "Language_Woked_On": ["Python", "Powershell", "Groovy",
                              {"Ansible/Teraform": "YAML/HCL"}, "Dockerfile",
                              {"frontend": ["HTML", "Javascript", "css"]}],
        "Language_Woking_On": ["ARM", "Helm Chart", "Python", "Bash", "Powershell",
                               "Ansible", "ADO Pipelines", "Groovy", {"Ansible/Teraform": "YAML/HCL"}, "Dockerfile"]
    },
    {
        "techs_id": 4,
        "Monitoring": ["Dynatrace", "Datadog", "CloudWatch"],
        "Logging": ["Splunk", "SumoLogic"],
        "ITSM": ["Service Now", "Pagerduty", "Jira Service Management"]
    }
]


@aditya.route("/home/")
@aditya.route("/")
def home():
    """home page"""
    return render_template("html_files/home.html", name="Aditya Sinha")


@aditya.route("/fun/")
def name():
    """name page"""
    return render_template("html_files/fun.html")


@aditya.route("/where/")
def location():
    """
    NOTE:
        Have to Do os.popen as by default os.system("shell_command") executes right away stdout
        Need to store stdout in variable to pass later so used popen and .read()
        Since return function call gives nothing in os module
        and we know all function call always return None or null, if not explicitly returned
        spliting lines and at newline-Output was
        192.10.0.4 --> IP
        None       --> empty/None
    """
    get_hostname_ = str(os.popen('hostname').read()).splitlines()[0]
    # alpine os
    get_container_ip = str(os.popen(
        "ifconfig | grep 'Bcast' | cut -d: -f2 | awk '{print $1}'").read()).splitlines()[0]
    # mac os
    # get_container_ip = str(os.popen(
    #     "ifconfig | grep 'broadcast' | cut -d: -f2 | awk '{print $2}'").read()).splitlines()[0]
    return render_template("html_files/where.html",
                           get_hostname=get_hostname_,
                           get_container_ip=get_container_ip
                           )


@aditya.route("/techs/", methods=['GET'])
def get():
    """simple get method"""
    return jsonify({'Techs': techs})


@aditya.route("/techs/<int:techs_id>/", methods=['GET'])
def get_techs_id(techs_id):
    """
    <dataType:variable> part is required in flask route
    Have to Do Subtract [techs_id-1] as:
    List indices starts with 0 ALWAYS [0, 1, 2, ...]
    """
    return jsonify({'Techs': techs[techs_id-1]})


if __name__ == "__main__":
    """
    Flask Module is basic and Django is production grade app development module
    Issue in local test is that we are testing by binding to the "127.0.0.1:9092" inside our code.
    This makes the code work from inside the container during Docker RunTime BUT NOT OUTSIDE.
    127.0.0.1 -loopback and only returns to response from local not outside
    we need to bind to 0.0.0.0:9092 to bind to all interfaces inside the container.
    basically 0.0.0.0 is for outside request to serve
    So traffic coming from outside of the container is also accepted by this Python app
    """
    aditya.run(debug=True, host='0.0.0.0', port=9092)
