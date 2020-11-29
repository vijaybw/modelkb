import sqlite3

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
