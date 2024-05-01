import os
from flask import Flask, render_template, request

from qbraid.providers import QbraidProvider
from qbraid_core import QbraidSession


app = Flask(__name__)

@app.route("/submit_qasm", methods=["GET", "POST"])
def submit_qasm() -> str:
    """Submit a qasm file to the sv1 simulator on AWS.

    Returns:
        render_template: Render the submit_qasm.html template with the result of the qasm simulation.
    """
    # read the input qasm string from the user
    # initialize the qbraid session, it is expected that you have already logged in with the CLIs
    try:
        session = QbraidSession()
        session.save_config()
        if request.method == 'POST':
            file = request.files['qasm_file']
            if (file.filename is None) or (file.filename == ''):
                # add file name
                file.filename = 'qasm_file.qasm'
            # read the file
            qasm_string = file.read().decode('utf-8')
            # run the qasm string on the sv1 simulator
            provider = QbraidProvider()
            aws_sv1_sim = provider.get_device('aws_sv_sim')
            aws_job = aws_sv1_sim.run(qasm_string, shots=100)
            # return the result
            aws_result = aws_job.result()
            return render_template(f"submit_qasm.html", result=aws_result.__dict__)
    except Exception as e:
        print(e)
        return render_template(f"error.html")

@app.route("/")
def main() -> str:
    """Main page of the application.

    Returns:
        render_template: Render the index.html template.
    """
    if request.method == 'POST':
        file = request.files['qasm_file']
        # debug
    return render_template(f"index.html")


if __name__ == '__main__':
    app.run(debug=True)