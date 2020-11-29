import datetime
import inspect
import string
import time
import random
import uuid
from Parser import AST
import re
import requests
import os, sys
import glob
from distutils.sysconfig import get_python_lib
import uuid
from keras.models import load_model
from jinja2 import Environment, FileSystemLoader
from sql_helper import *
from structures import *
from structures.ExperimentInfo import ExperimentInfo
from app import *
class Experiment:
    experiment_metadata = {}

    def __init__(self, project_title, user):
        self.project_title = project_title
        self.user = user
        self.experiment_metadata = dict()
        # self.

    #For tracking experiment
    def track(self):
        self.experiment_metadata['project_name'] = self.project_title
        self.project_title += '_' + time.strftime("%m%d%y-%H%M%S") + '_'
        self.experiment_metadata['project_id'] = self.project_title + str(uuid.uuid4())
        self.experiment_metadata['experiment_id'] = self.experiment_metadata['project_id']
        self.experiment_metadata['user_name'] = self.user

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        self.extract_hyperparameters(module.__file__, module)
        activate(self.user)
        a = 1
    #Retrieving parameters from
    def extract_hyperparameters(self, filename, module):
        astObj = AST()
        hyperParams = astObj.ParseAst(filename)
        for i in range(0, len(hyperParams)):
            if 'epochs' in hyperParams[i] :
                self.experiment_metadata['epochs'] = hyperParams[i].split('=')[1]
            if 'batch_size' in hyperParams[i]:
                self.experiment_metadata['batch_size'] = hyperParams[i].split('=')[1]
            #Extract metadata from the model file.

        #Adding Callbacks and Checkpoint Code Dynamically
        self.experiment_metadata['id'] = str(uuid.uuid1())
        flag = 1
        temp = module
        with open(filename) as myfile:
            if 'CSVLogger' in myfile.read():
                    return
            temp_file_location = get_python_lib()
            temp_file_location = temp_file_location.replace('\\', '/')
            with open(temp_file_location + '/temp.py', 'w') as file:
                source_lines = inspect.getsourcelines(temp)
                for code in source_lines:
                    if (isinstance(code, (list))):
                        for line in range(0, len(code)):
                            #Adding import functions and call backs
                            if 'import' in code[line] and flag == 1:
                                file.write(str('from keras.callbacks import CSVLogger, ModelCheckpoint\n'))
                                file.write(str(file.write(code[line])) + '\n')
                                flag = 0
                            elif '.fit(' in code[line]:
                                logfilename = self.experiment_metadata['id'] + '_training.log'
                                csv_file_path = Path(TRAININGLOG_FOLDER, logfilename)
                                h5filename = self.experiment_metadata['id'] + '.hdf5'
                                file.write("csv_logger = CSVLogger("+repr(csv_file_path.as_posix())+")" + '\n')
                                weights_file_path = Path(MODEL_FOLDER, h5filename)
                                file.write(str('filepath='+repr(weights_file_path.as_posix())) + '\n')
                                file.write(str("checkpoint = ModelCheckpoint(filepath, monitor='acc', verbose=1, save_best_only=False, mode='max')" + '\n'))
                                file.write(str("callbacks_list = checkpoint" + '\n'))
                                code[line] = code[line].replace(')', ',callbacks=[csv_logger, callbacks_list])')
                                file.write(code[line])
                            else:
                                file.write(code[line])

        #Executing the temp file
        os.system(sys.executable + ' ' + temp_file_location+'/temp.py')

        model_file = weights_file_path.as_posix()
        epochs = int(self.experiment_metadata['epochs'])

        #Loading model and parameters
        model = load_model(model_file)
        self.experiment_metadata['input_shape'] = model.input_shape
        self.experiment_metadata['layers_count'] = len(model.layers)
        self.experiment_metadata['output_shape'] = model.output_shape
        self.experiment_metadata['Optimizer'] = model.optimizer.__class__.__name__
        self.experiment_metadata['LossFunction'] = model.loss

        #Model and Log file
        self.experiment_metadata['callbacks_log'] = Path(TRAININGLOG_FOLDER,self.experiment_metadata['id'] + '_training.log').as_posix()
        self.experiment_metadata['model_file'] = model_file

        #Generate Predict Function
        autopredictlocation = Path(AUTOPREDICT_FOLDER ,self.experiment_metadata['id'] + '_auto_predict.py').as_posix()
        output = self.generate_predict(model)
        with open(autopredictlocation, 'w') as file:
             file.write(output)

        self.experiment_metadata['auto_predict_function'] = autopredictlocation

        #Generate Predict Function
        autopredictlocation_container = Path(FLASK_CONTAINER_FOLDER ,self.experiment_metadata['id'] + '_flask_container.py').as_posix()
        output = self.generate_predict_for_container(model, "'" + model_file + "'")
        with open(autopredictlocation_container, 'w') as file:
             file.write(output)

        self.experiment_metadata['flask_container_function'] = autopredictlocation_container

        print(self.experiment_metadata)


        self.experiment_metadata['sample_weight'] = ''
        self.experiment_metadata['accuracy_value'] = ''
        self.experiment_metadata['Framework'] = ''
        self.experiment_metadata['loss_value'] = ''
        self.experiment_metadata['user_id'] = self.user
        self.experiment_metadata['Framework'] = 'Keras'
        currentDT = datetime.datetime.now()
        self.experiment_metadata['time_stamp'] = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        input_shape = ''
        for var in self.experiment_metadata['input_shape']:
            if var is None:
                input_shape = input_shape + ',' + ' '
            else:
                input_shape = input_shape + ',' + str(var)
        output_shape = ''
        for var in self.experiment_metadata['output_shape']:
            if var is None:
                output_shape = output_shape + ',' + ' '
            else:
                output_shape = output_shape + ',' + str(var)

        with open(self.experiment_metadata['callbacks_log'], 'rb') as file:
            blobData_callbacks_log = file.read()
        with open(self.experiment_metadata['model_file'], 'rb') as file:
            blobData_model_file = file.read()
        # find the last line, change to a file you have
        fileHandle = open(self.experiment_metadata['callbacks_log'], "r")
        lineList = fileHandle.readlines()
        fileHandle.close()
        listOfAccurcyValues = []
        listOfLossValues = []
        firstline = 1
        for currentLine in lineList:
            #This logic would skip the first line.
            if firstline > 1:
                listOfFeatures = currentLine.split(',')
                listOfAccurcyValues.append(float(listOfFeatures[1]))
                listOfLossValues.append(float(listOfFeatures[2]))
            firstline = 2

        listOfFeatures = lineList[len(lineList)-1].split(',')
        self.experiment_metadata['accuracy_value'] = str(listOfFeatures[1])
        self.experiment_metadata['loss_value'] = str(listOfFeatures[2])

        self.experiment_metadata['list_of_accuracy_over_epochs'] = str(listOfAccurcyValues).strip('[]')
        self.experiment_metadata['list_of_loss_over_epochs'] = str(listOfLossValues).strip('[]')
        with open(self.experiment_metadata['auto_predict_function'], 'rb') as file:
            blobData_predict_function = file.read()
        copyToDatabase = ExperimentInfo(self.experiment_metadata['id'], self.experiment_metadata['sample_weight'],
                                                   self.experiment_metadata['project_id'], self.experiment_metadata['user_id'],
                                                   self.experiment_metadata['time_stamp'], self.experiment_metadata['epochs'],
                                                   self.experiment_metadata['batch_size'], self.experiment_metadata['Framework'],
                                                    input_shape, self.experiment_metadata['layers_count'],
                                                    output_shape, self.experiment_metadata['Optimizer'],
                                                   self.experiment_metadata['LossFunction'], blobData_callbacks_log,
                                                    blobData_model_file, self.experiment_metadata['accuracy_value'],
                                                   self.experiment_metadata['loss_value'], blobData_callbacks_log,
                                                self.experiment_metadata['list_of_accuracy_over_epochs'], self.experiment_metadata['list_of_loss_over_epochs'], blobData_predict_function )
        database = r"database/sqlite.db"

        # create a database connection
        conn = create_connection(database)
        with conn:
            # create a new experiment

            project_id = create_experiment(conn, copyToDatabase)

        #Deleting all the files that are generated by ModelKB
        os.remove(temp_file_location+ '/temp.py')
        #os.remove(temp_file_location+'/training.log')
        #os.remove(autopredictlocation)
        #for i in range(0, len(model_file)):
        #    os.remove(model_file[i])
        activate_final(self.user)
        sys.exit(0)

    def randomString2(stringLength=8):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.sample(letters, stringLength))

    def uploadFiles(self,expData):
        files = ['callbacks_log', 'model_file', 'predict_function']
        for key in expData.keys():
            if key in files:
                res = Experiment.uploader.UploadFile(expData[key])
                if 'file_uploaded' in res.keys():
                    Experiment.uploader.filesArray.append(res['file_id'])

    def generate_predict(self, model):
        # Template Files
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template('predict_template.txt')

        # Dictionary that includes the parameters to pass through the tempalte
        inference_data = {}
        inference_data['input_shape'] = model.input_shape[1:]

        if (inference_data['input_shape'][0] == 3):
            inference_data['color_image'] = True
        else:
            inference_data['color_image'] = False
        inference_data['data_augumentation'] = True

        output = template.render(inference_data=inference_data)

        return output

    def generate_predict_for_container(self, model, path):
        # Template Files
        file_loader = FileSystemLoader("templates")
        env = Environment(loader=file_loader)
        template = env.get_template('flask_template.txt')

        # Dictionary that includes the parameters to pass through the tempalte
        inference_data = {}
        inference_data['input_shape'] = model.input_shape[1:]

        if (inference_data['input_shape'][0] == 3):
            inference_data['color_image'] = True
        else:
            inference_data['color_image'] = False
        inference_data['data_augumentation'] = True

        inference_data['model_path'] = path

        output = template.render(inference_data=inference_data)

        return output
class ExploreModels:
    def __init__(self, user):
        self.user = user
    def start(self):
        exoloremodels(self.user)












