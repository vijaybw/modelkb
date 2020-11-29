import datetime
import errno
import os, json
import string
import sys
from pathlib import Path
import netron
import requests
import json
from flask import Flask, render_template, request, send_from_directory, send_file, session, url_for
from werkzeug.utils import secure_filename, redirect
from sql_helper_ui import *
from sql_helper_ui_remote import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'
data = ''
metadata = dict()
dirs = dict()
IMAGE_FOLDER = Path(os.path.abspath(__file__)).parent / "rawdata"
UPLOAD_FOLDER = Path(os.path.abspath(__file__)).parent / "testdata"
MODEL_FOLDER = Path(os.path.abspath(__file__)).parent / "rawdata" / "modelfile"
TRAININGLOG_FOLDER = Path(os.path.abspath(__file__)).parent / "rawdata"  / "traininglog"
AUTOPREDICT_FOLDER = Path(os.path.abspath(__file__)).parent / "rawdata" / "autopredict"
FLASK_CONTAINER_FOLDER = Path(os.path.abspath(__file__)).parent / "rawdata" / "flasktemplate"
ALLOWED_EXTENSIONS = set(['h5', 'HDF5', 'pdf', 'doc', 'md', 'docx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
dir_path = Path(os.path.abspath(__file__)).parent

def exoloremodels(username):
    activate_final(username)
def xFit(username):

    res = readExperiments(username)
    dataRcvd = res

    dirs = make_tree(dataRcvd)
    # pass data to FLask
    sendData(dirs)

    # run the app -Flask
    #activate()
def xFitRemote(username):
    # sample data to be sent to View

    res = readExperiments_remote(username)
    dataRcvd = res

    dirs = make_tree(dataRcvd)
    # pass data to FLask
    sendData(dirs)

def sendData(z):
    global dirs
    dirs = z

@app.route('/')
def load_home():
    if 'username' in session:
        xFit(session['username'])
        z = dirs
        if session['username'] == 'vijaybw':
            name = "Vijay"
        elif session['username'] == 'gharibg':
            name = "Gharib"
        elif session['username'] == 'rakana':
            name = "Rakan"
        elif session['username'] == 'yugil':
            name = "Yugi"
        elif session['username'] == 'sirir':
            name = "Siri"
        elif session['username'] == 'duyh':
            name = "Duy"
        elif session['username'] == 'test':
            name = "Test"
        else:
            return render_template("login.html")
        session['name'] = name
        return render_template('home.html', z=z, name=session['name'])
    return render_template("login.html")
@app.route('/home', methods=['GET', 'POST'])
def load_home_from_login():
    if 'username' in session:
        z = dirs
        return render_template('home.html', z=z, name=session['name'])

    return render_template("login.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        xFit(session['username'])
        z = dirs
        if request.form.get("password") == 'password' and request.form.get("username") == 'vijaybw':
            name = "Vijay"
        elif request.form.get("password") == 'password' and request.form.get("username") == 'gharibg':
            name = "Gharib"
        elif request.form.get("password") == 'password' and request.form.get("username") == 'rakana':
            name = "Rakan"
        elif request.form.get("password") == 'password' and request.form.get("username") == 'yugil':
            name = "Yugi"
        elif request.form.get("password") == 'password' and request.form.get("username") == 'sirir':
            name = "Siri"
        elif request.form.get("password") == 'password' and request.form.get("username") == 'duyh':
            name = "Duy"
        elif request.form.get("password") == 'password' and request.form.get("username") == 'test':
            name = "Test"
        else:
            return render_template("login.html")
        session['name'] = name
        return render_template("home.html",z=z, name=name)
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return render_template("login.html")

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgot-password.html')
@app.route('/view')
def viewproject():
    id = request.values.get("project")
    x = data
    y = metadata
    z = {}

    z[id] = dirs[id]
    exp = dict()

    return render_template('viewproject.html', x=x, y=y, z=z, t=exp, id=id)

@app.route('/upload')
def upload_file():
    proj = request.values.get("project")
    expt = request.values.get("experiment")
    m = dict()
    return render_template('uploadtest.html', f=proj, m=m, e=expt)

@app.route('/viewmetadata')
def view_metadata():
    values = request.values.get("values")
    import json
    json_acceptable_string = values.replace("'", "\"")
    values = json.loads(json_acceptable_string)
    return render_template('viewmetadata.html', values=values)
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file1():
    if request.method == 'POST':
        project = request.values.get("project")
        experiment = session['s_experiment']

        model_path = Path(MODEL_FOLDER , experiment + ".hdf5").as_posix()
        testscript_path = Path(AUTOPREDICT_FOLDER , experiment + '_auto_predict.py').as_posix()

        f = request.files['file']
        filename = secure_filename(f.filename)
        directory = Path(app.config['UPLOAD_FOLDER'] , project).as_posix()
        if not os.path.exists(directory):
            os.makedirs(directory)

        now = datetime.datetime.now()
        dt = str(now.month).zfill(2) + str(now.day).zfill(2) + str(now.year).zfill(2) + "-" + str(now.hour).zfill(
            2) + str(now.minute).zfill(2) + str(now.second).zfill(2)

        filenameforview = dt + ".jpg"
        if not os.path.exists(directory):
            os.makedirs(directory)
        open(os.path.join(directory, filenameforview),
             'wb').write(f.read())

        filename = Path(directory , filenameforview).as_posix()

        testpredict = os.popen(sys.executable + ' ' + testscript_path + ' ' + model_path + ' ' + filename).readlines()

        testpredicttext = ""
        for ln in testpredict:
            testpredicttext = testpredicttext + ln.rstrip('\n')
        testpredicttext = testpredicttext.replace('[', '')
        testpredicttext = testpredicttext.replace(']', '')
        testpredicttext = testpredicttext.replace('  ', ' ')
        testpredictf = testpredicttext.split(" ")
        while ("" in testpredictf):
            testpredictf.remove("")

        for ln in testpredictf:
            testpredicttext = testpredicttext + ln.rstrip('\n')
        dict = {}
        my_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        key = 0
        for value in testpredictf:
            dict[key] = value
            key = key + 1

        testpredicttext = "uploaded successfully. and categorized as shown in table."

        return render_template('uploadtest.html', f=project, m=dict, filename=filename, foldername=directory,
                               uploadstatues=testpredicttext)


@app.route('/image')
def get_image():
    experiment = request.values.get("experiment")
    image = request.values.get("type")
    project = experiment.split("_")[0]
    filename = IMAGE_FOLDER / experiment / experiment + "_" + image + ".png"

    return send_file(filename, mimetype='image/jpg')

@app.route('/testimage')
def get_testimage():
    project = request.values.get("project")
    timestamp = request.values.get("timestamp")
    testimage = request.values.get("testimage")
    if testimage == '':
        testimage = UPLOAD_FOLDER / "sample.png"
    filename = testimage

    return send_file(filename, mimetype='image/jpg')

@app.route('/downloadh5')
def get_h5():
    experiment = request.values.get("experiment")
    project = experiment.split("_")[0]
    filename1 = IMAGE_FOLDER / experiment / experiment + "_model.h5"
    fname = experiment + "_model.h5"
    return send_file(filename1, mimetype='application/octet-stream', attachment_filename=fname, as_attachment=True)
@app.route('/shareexperiment', methods=['GET', 'POST'])
def shareexperiment():
    if request.method == 'POST':
        experiment = request.values.get("experiment")
        projectid = request.values.get("project")
        share_username = request.form['shareusername']
        record = readExperimentbyid(experiment)
        res = create_experiment_remote(record, share_username)
        session['s_experiment'] = experiment

        return render_template('share_experiment_popup.html', experiment=experiment, project=projectid, sharestatus="Shared succcessfully")
    experiment = request.values.get("experiment")
    projectid = request.values.get("project")
    return render_template('share_experiment_popup.html', experiment=experiment, project=projectid)
@app.route('/viewexperiment')
def viewexperiment():
    experiment = request.values.get("experiment")
    projectid= request.values.get("project")
    remote = request.values.get('remote')

    session['s_experiment'] = experiment
    values = {}
    values["projectname"] = projectid
    if remote:
        values["remote"] = "REMOTE"
    for row in dirs[values["projectname"]]["history"].items():
        if row[0] == experiment:
            print(row[1]['timestamptext'])
            values["timestamp"] = row[1]['timestamptext']
            values["experiment"] = experiment
            x = experiment
            ttext = row[1]['timestamptext']

            values["Framework"] = row[1]['framework']
            values["Epochs"] = row[1]['epochs']
            values["BatchSize"] = row[1]['batch_size']
            values["Layers"] = row[1]['layers_Count']
            values["InputTensors"] = row[1]['input_shape']
            values["Optimizer"] = row[1]['Optimizer']
            values["OutputTensor"] = row[1]['output_shape']
            values["LossFunction"] = row[1]['LossFunction']
            values["list_of_accuracy_over_epochs"] = row[1]['list_of_accuracy_over_epochs']
            values["list_of_epochs"] = row[1]['list_of_epochs']
            values["list_of_loss_over_epochs"] = row[1]['list_of_loss_over_epochs']
            values["list_of_epochs"] = row[1]['list_of_epochs']

    project = projectid
    y = project
    z = {}

    z[project] = dirs[project]

    exp = dict()

    zf = False
    zp = 5005
    zl = 'localhost'

    model_path = Path(MODEL_FOLDER, experiment + '.hdf5').as_posix()

    netron.server.stop()
    netron.server.start(model_path, zf, zf, zp, zl)

    return render_template('viewexperiment.html', y=y, z=z, t=exp, values = values, successstatus=0)

@app.route("/get_chart")
def chart():
    legend = request.values.get("legend")
    values = json.loads(request.values.get("datapassed"))
    labels = json.loads(request.values.get("labels"))
    #legend = 'Monthly Data'
    #labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    #values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)


@app.route('/viewchart')
def viewchart():
    z = dirs
    return render_template('viewchart.html', z=z)

@app.route('/projects')
def viewprojects():
    z = dirs
    return render_template('projects.html', z=z)

@app.route('/experiments')
def viewexperiments():
    xFit()
    z = dirs
    return render_template('experiments.html', z=z)

@app.route('/remoteexperiments')
def viewremoteexperiments():
    xFitRemote(session['username'])
    z = dirs
    return render_template('remoteexperiments.html', z=z)
def activate(username):
    xFit(username)

def activate_final(username):
    xFit(username)
    app.run()

def activate_remote():
    xFitRemote(session['username'])
    app.run()

def path_hierarchy(path):

    hierarchy = {
        'type': 'folder',
        'name': os.path.basename(path),
        'path': path,
    }

    try:
        hierarchy['children'] = [
            path_hierarchy(os.path.join(path, contents))
            for contents in os.listdir(path)
        ]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['type'] = 'file'

    return hierarchy

def make_tree(databaseExperiments):
    tree = {}
    exp = {}

    currentproject = ""
    countofexperiments=1
    owner = ""
    project = {}
    for currentExperiment in databaseExperiments:

        projname = currentExperiment.project_id
        runtimestamp = currentExperiment.time_stamp
        owner = currentExperiment.user_id
        framework = currentExperiment.Framework

        if currentproject == "":
            exp = dict()

        if currentproject != projname and currentproject != "":

            exp = dict()
            countofexperiments=1
            tree[currentproject] = project
            currentproject = projname
            project = {
                'type': 'folder',
                'name': projname,
                'path': "",
                'history': exp
            }

            if projname == "MNIST_Digits":
                project.update({'owner': owner})
                project.update({'expcount': countofexperiments})
                project.update({'application': 'Computer Vision Models'})

            if projname == "Malaria_Detection":
                project.update({'owner': owner})
                project.update({'expcount': countofexperiments})
                project.update({'application': 'Computer Vision Models'})

            if projname == 'LSTM':
                project.update({'application': 'Image Classification'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'ImageCaptioning':
                project.update({'application': 'Image Classification'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'FashionMnist':
                project.update({'application': 'Image Classification'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'CNN':
                project.update({'application': 'Image Classification'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'siri':
                project.update({'application': 'Text Generation'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            else:
                project.update({'application': 'Unknown'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
        else:

            currentproject = projname
            project = {
                'type': 'folder',
                'name': projname,
                'path': "",
                'history': exp
            }

            if projname!= '':
                project.update({'owner': owner})
                project.update({'expcount': countofexperiments})
                project.update({'application': 'Computer Vision Models'})
            if projname == 'LSTM':
                project.update({'application': 'Image Classification'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'ImageCaptioning':
                project.update({'application': 'Image Classification'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'FashionMnist':
                project.update({'application': 'Image Classification'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'CNN':
                project.update({'application': 'Text Generation'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})
            if projname == 'siri':
                project.update({'application': 'Text Generation'})
                project.update({'expcount': countofexperiments})
                project.update({'owner': owner})

        contents = {}

        contents.update({'timestamptext': runtimestamp})
        contents.update({'timestamp': runtimestamp})
        contents.update({'framework': framework})
        contents.update({'project': projname})
        contents.update({'experiment': currentExperiment})
        contents.update({'owner': owner})
        contents.update({'framework': currentExperiment.Framework})
        contents.update({'batch_size': currentExperiment.batch_size})
        contents.update({'epochs': currentExperiment.epochs})
        contents.update({'layers_Count': currentExperiment.layers_count})
        contents.update({'input_shape': currentExperiment.input_shape})
        contents.update({'output_shape': currentExperiment.output_shape})
        contents.update({'Optimizer': currentExperiment.optimizer})
        contents.update({'LossFunction': currentExperiment.lossfunction})
        contents.update({'AccuracyValue': currentExperiment.accuracy_value})
        contents.update({'LossValue': currentExperiment.loss_value})
        contents.update({'list_of_accuracy_over_epochs': currentExperiment.list_of_accuracy_over_epochs})
        contents.update({'list_of_loss_over_epochs': currentExperiment.list_of_loss_over_epochs})
        contents.update({'list_of_epochs': currentExperiment.list_of_epochs})

        exp[currentExperiment.id] = contents
        countofexperiments=countofexperiments+1
    tree[currentproject] = project
    return tree