from flask import Flask, render_template
import os
import logging

"""
templates:
Flask looks for a directory called templates in the root of the Flask application package for HTML Files
static:
Flask has reserved a separate folder where you should put static files such as CSS, Javascript, images or other files
"""

aditya = Flask(__name__)         # create a new Flask app instance

# simple Logging --> Need to convert to logs.json instead of python_app1.log
# logging.basicConfig(
#     filename='python_app1.log',
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s')  # Pushing Logs to file for monitoring


@aditya.route("/home/")
@aditya.route("/")
def this_is_home_page():
    return render_template("html_files/home.html", full_name="Aditya Sinha")


@aditya.route("/where/")
def this_is_where_page():
    return render_template("html_files/where.html")


@aditya.route("/server_info/")
def this_is_server_info():
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
    # alpine
    get_container_ip_ = str(os.popen(
        "ifconfig | grep 'Bcast' | cut -d: -f2 | awk '{print $1}'").read()).splitlines()[0]
    # mac
    # get_container_ip_ = str(os.popen(
    #     "ifconfig | grep 'broadcast' | cut -d: -f2 | awk '{print $2}'").read()).splitlines()[0]
    return render_template("html_files/server_info.html",
                           get_hostname=get_hostname_,
                           get_container_ip=get_container_ip_
                           )


if __name__ == "__main__":  # only when running python aditya.py
    """
    Flask Module is basic and Django is production grade app development module
    Issue in local test is that we are testing by binding to the "127.0.0.1:8082" inside our code. 
    This makes the code work from inside the container during Docker RunTime BUT NOT OUTSIDE.
    127.0.0.1 -loopback and only retuns to response from local not outside
    we need to bind to 0.0.0.0:8082 to bind to all interfaces inside the container. 
    basically 0.0.0.0 is for outside request to serve
    So traffic coming from outside of the container is also accepted by our Python app
    """
    aditya.run(debug=True, host='0.0.0.0', port=8082)
