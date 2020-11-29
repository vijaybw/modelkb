import os
import pymysql
from structures.ExperimentInfo import ExperimentInfo

hostname = 'XXX'
username = 'XXX'
password = 'XXX'
database = 'XXX'

def create_connection_remote():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = pymysql.connect( host=hostname, user=username, passwd=password, db=database )
    except ConnectionError as e:
        print(e)

    return conn

def create_experiment_remote( current_experiment,share_id):
    conn = create_connection_remote()
    """
    Create a new experiment into the experiments table
    :param conn:
    :param project:
    :return: project id
    """
    data_tuple = (current_experiment[0][0], current_experiment[0][1],
                    current_experiment[0][2], current_experiment[0][3],
                    current_experiment[0][4], current_experiment[0][5],
                    current_experiment[0][6], current_experiment[0][7],
                    current_experiment[0][8], current_experiment[0][9],
                    current_experiment[0][10], current_experiment[0][11],
                    current_experiment[0][12], current_experiment[0][13],
                    current_experiment[0][14], current_experiment[0][15],
                    current_experiment[0][16], current_experiment[0][17],
                    current_experiment[0][18], current_experiment[0][19], current_experiment[0][20], share_id)

    sql = ''' INSERT INTO `experiments` (`id`, `sample_weight`, `project_id`, `user_id`, `time_stamp`, `epochs`, `batch_size`, `Framework`, `input_shape`, `layers_count`, `output_shape`, `optimizer`, `lossfunction`, `callbacks_log`, `model_file`, `accuracy_value`, `loss_value`, `predict_function`, `list_of_accuracy_over_epochs`, `list_of_loss_over_epochs`, `auto_predict_function`, `share_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s); '''
    with conn.cursor() as cur:
        cur.execute(sql, data_tuple)

    conn.commit()
    return cur.lastrowid

def readExperiments_remote(username):
    try:
        # test all data
        database = r"database/sqlite.db"

        # create a database connection
        conn = create_connection_remote()
        cursor = conn.cursor()
        print("Connected to Mysql")
        sql_fetch_blob_query = """SELECT * from experiments where share_id='""" + username +"""' order by time_stamp desc"""
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
    except ConnectionError as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if (conn):
            conn.close()

def readExperimentsIntoCsv():
    try:
        # test all data
        database = r"database/sqlite.db"

        # create a database connection
        conn = create_connection_remote(database)
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
    except ConnectionError as error:
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

