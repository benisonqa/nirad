""" Flask Based Module to provide Server-Client Application for Nirad devices"""

import platform
from urllib.parse import quote
from flask import *
# from libs.device import Device
from libs.utils import *
from libs.interface import *
# from libs.template import HtmlParser
from libs.logger import NiradLogger
from libs.csv_parser import *
from werkzeug.utils import secure_filename
import secrets


logger = NiradLogger.set_logger()

UPLOAD_FOLDER = './'
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
secret = secrets.token_urlsafe(32)
app.secret_key = secret
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


@app.route("/", methods=['GET', 'POST'])
def home():
    # logger.info("Fetched summary for {0}".format(EMULATED_DEVICE.name))
    # HtmlParser(device_info)
    return render_template('login.html'), 200


@app.route("/favicon.ico")
def h():
    return jsonify(success=True)


@app.route('/login', methods=['POST'])
def login():
    ipaddress = request.form.get("ipaddr")
    username = "root" if request.form.get("uname") == '' else request.form.get("uname")
    password = "NiRaD$123$" if request.form.get("psw") == '' else request.form.get("psw")
    session.update({"ipaddress": ipaddress, "username": username, "password": password})

    if Utils.check_ping(ipaddress):
        if 'ipaddress' in session:
            data = Interface(session).get_hw_details()
            return render_template('landing.html', details_list=data)
        else:
            return render_template('login.html')
    else:
        flash("Device Not Reachable")
        return render_template('login.html')

    # return f'{ipaddress, username, password}'
    # your code
    # return a response


@app.route('/landing', methods=["POST"])
def landing():
    if "ipaddress" in session:
        return redirect(url_for('process'))
    else:
        return render_template('login.html')


@app.route('/process', methods=['GET', 'POST'])
def process():
    if "ipaddress" in session:
        data = Interface(session).download_and_parse_files()
        print(data)
        visible_field_list = csv_parser('ONGC.csv')
        filtered_data = filter_data(data, visible_field_list)
        return render_template('process.html', combined_segment=data)
    else:
        return redirect(url_for('home'))


ALLOWED_EXTENSIONS = set(['csv'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/files-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')

    errors = {}
    success = False
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 206
        return resp
    if success:
        resp = jsonify({'message': 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 400
        return resp


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.cache_control.public = True
    return response


@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('home'))


def FlaskAppRun(obj: Flask):
    # local debugging has 443 blocked due to other apps using port so defaulting to 5000
    FLASK_PORT = 8000 #if platform.system().lower() == 'darwin' else EMULATED_DEVICE.rest_port
    # logger.info(f"Initialized {device_object.name} rest app on port {FLASK_PORT}")

    obj.run(debug=True, use_reloader=False, host="127.0.0.1", port=FLASK_PORT)#, ssl_context='adhoc')


if __name__ == "__main__":

    # device = Utils.read_file('./.current_emulator_device')
    # EMULATED_DEVICE = Device(name=device)
    FlaskAppRun(app)
