class ExperimentInfo:
  def __init__(self, id, sample_weight,
                   project_id, user_id,
                   time_stamp, epochs,
                   batch_size, Framework,
                    input_shape, layers_count,
                    output_shape, Optimizer,
                   LossFunction, callbacks_log,
                    model_file, accuracy_value,
                   loss_value, predict_function,
               list_of_accuracy_over_epochs, list_of_loss_over_epochs,
                auto_predict_function):
    self.id = id
    self.sample_weight = sample_weight
    self.project_id = project_id
    self.user_id = user_id
    self.time_stamp = time_stamp
    self.epochs = epochs
    self.batch_size = batch_size
    self.Framework = Framework
    self.input_shape = input_shape
    self.layers_count = layers_count
    self.output_shape = output_shape
    self.optimizer = Optimizer
    self.lossfunction = LossFunction
    self.accuracy_value = accuracy_value
    self.loss_value = loss_value
    self.callbacks_log = callbacks_log
    self.model_file = model_file
    self.predict_function = predict_function
    self.list_of_accuracy_over_epochs = list_of_accuracy_over_epochs
    self.list_of_loss_over_epochs = list_of_loss_over_epochs
    list_of_epochs = []
    current_counter = 1
    for v in self.list_of_accuracy_over_epochs:
      list_of_epochs.append(current_counter)
      current_counter = current_counter + 1
    self.list_of_epochs = list_of_epochs
    self.auto_predict_function = auto_predict_function