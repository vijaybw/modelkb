import os
import sqlite3

from flask import session

from structures.ExperimentInfo import ExperimentInfo


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)

    return conn

def create_experiment(conn, current_experiment):
    """
    Create a new experiment into the experiments table
    :param conn:
    :param project:
    :return: project id
    """
    data_tuple = (current_experiment.id, current_experiment.sample_weight,
                    current_experiment.project_id, current_experiment.user_id,
                    current_experiment.time_stamp, current_experiment.epochs,
                    current_experiment.batch_size, current_experiment.Framework,
                    current_experiment.input_shape, current_experiment.layers_count,
                    current_experiment.output_shape, current_experiment.optimizer,
                    current_experiment.lossfunction, current_experiment.callbacks_log,
                    current_experiment.model_file, current_experiment.accuracy_value,
                    current_experiment.loss_value, current_experiment.predict_function,
                    current_experiment.list_of_accuracy_over_epochs, current_experiment.list_of_loss_over_epochs, current_experiment.auto_predict_function)

    sql = ''' INSERT INTO 'experiments' (id, sample_weight, project_id, user_id, time_stamp, epochs, batch_size, Framework, input_shape, layers_count, output_shape, optimizer, lossfunction, callbacks_log, model_file, accuracy_value, loss_value, predict_function, list_of_accuracy_over_epochs, list_of_loss_over_epochs, auto_predict_function) VALUES (
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
          ?,
		  ?,
		  ?,
		  ?,
		  ?,
		  ?,
		  ?
        ); '''
    cur = conn.cursor()
    cur.execute(sql, data_tuple)
    return cur.lastrowid

def readExperiments(username):
    try:
        # test all data
        database = r"database/sqlite.db"
        # create a database connection
        conn = create_connection(database)
        cursor = conn.cursor()
        print("Connected to SQLite")
        sql_fetch_blob_query = """SELECT * from experiments where user_id='""" + username + """' order by time_stamp desc"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        allExperiments = []
        for row in record:
            listOfAccuracyFloat = []
            listOfLossFloat = []
            listOfAccuracyStr= str(row[18]).replace(" ", "").split(',')
            listOfLossStr = str(row[19]).replace(" ", "").split(',')
            projectid = str(row[2]).replace(" ", "").split('_')[0]
            for a in listOfAccuracyStr:
                listOfAccuracyFloat.append(float(a))
            for a in listOfLossStr:
                listOfLossFloat.append(float(a))
            currentRecord = ExperimentInfo(row[0], row[1],
                                            projectid, row[3],
                                            row[4], row[5],
                                            row[6],
                                            row[7],
                                            row[8], row[9],
                                            row[10], row[11],
                                            row[12], row[13],
                                            row[14], row[15][:6],
                                            row[16][:6], row[17],
                                            listOfAccuracyFloat , listOfLossFloat, row[20])

            #    id, sample_weight,
            #    project_id, user_id,
            #    time_stamp, epochs,
            #    batch_size, Framework,
            #    input_shape, layers_count,
            #    output_shape, Optimizer,
            #   LossFunction, callbacks_log,
            #   model_file, accuracy_value,
            #   loss_value, predict_function
            #  list_of_accuracy_over_epochs list_of_loss_over_epochs
            allExperiments.append(currentRecord)
        cursor.close()
        return allExperiments
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (conn):
            conn.close()

def readExperimentbyid(experimentid):
    try:
        # test all data
        database = r"database/sqlite.db"

        # create a database connection
        conn = create_connection(database)
        cursor = conn.cursor()
        print("Connected to SQLite")
        cursor.execute("SELECT * from experiments where id='"+experimentid+"'")
        record = cursor.fetchall()
        cursor.close()
        return record
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (conn):
            conn.close()
def readExperimentsIntoCsv():
    try:
        # test all data
        database = r"database/sqlite.db"

        # create a database connection
        conn = create_connection(database)
        cursor = conn.cursor()
        print("Connected to SQLite")
        sql_fetch_blob_query = """SELECT * from experiments order by time_stamp desc"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        allExperiments = []
        for row in record:
            currentRecord = ExperimentInfo(row[0], row[1],
                                            row[2], row[3],
                                            row[4], row[5],
                                            row[6],
                                            row[7],
                                            row[8], row[9],
                                            row[10], row[11],
                                            row[12], row[13],
                                            row[14], row[15][:6],
                                            row[16][:6], row[17],
                                            row[18], row[19], row[20])

            #    id, sample_weight,
            #    project_id, user_id,
            #    time_stamp, epochs,
            #    batch_size, Framework,
            #    input_shape, layers_count,
            #    output_shape, Optimizer,
            #   LossFunction, callbacks_log,
            #   model_file, accuracy_value,
            # loss_value, predict_function
            #  list_of_accuracy_over_epochs list_of_loss_over_epochs
            allExperiments.append(currentRecord)
        cursor.close()

        import csv

        with open('experiments_data.csv', mode='w') as experiments_file:
            employee_writer = csv.writer(experiments_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(['id', 'sample_weight','project_id', 'user_id','time_stamp', 'epochs','batch_size',
                                      'Framework','input_shape',
                                      'layers_count','output_shape', 'optimizer','lossfunction','accuracy_value','loss_value', 'list_of_accuracy_over_epochs', 'list_of_loss_over_epochs'])
            for row in allExperiments:
                employee_writer.writerow([row.id, row.sample_weight,row.project_id, row.user_id,row.time_stamp, row.epochs,
                                          row.batch_size, row.Framework,row.input_shape,
                                          row.layers_count,row.output_shape, row.optimizer,row.lossfunction,
                                          row.accuracy_value[:6],row.loss_value[:6], row.list_of_accuracy_over_epochs, row.list_of_loss_over_epochs])

        print(os.getcwd() + '\experiments_data.csv')
    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (conn):
            conn.close()

#test all data
#database = r"database/sqlite.db"

# create a database connection
#conn = create_connection(database)
#allExperiments = []
#allExperiments = readExperiments()

#for row in allExperiments:
#    print(row.id)

