import tensorflow as tf
import numpy as np


class Training():

    def __init__(self, model_filename=None):
        if model_filename is not None:
            self._model = tf.keras.models.load_model(model_filename)

    def create_NN(self):
        
        # print(tf.__path__)  
        # print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
        # tf.debugging.set_log_device_placement(True)
        # with tf.device('/GPU:0'):
        inputs = tf.keras.Input(shape = (42,))
        x = tf.keras.layers.Dense(256, activation=tf.nn.relu)(inputs)
        #hidden = tf.keras.layers.Dense(256, activation=tf.nn.relu)(x)
        self._outputs = tf.keras.layers.Dense(7, activation=tf.nn.relu)(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=self._outputs)

        # Define loss function, create optimizer and create accuracy evaluation
        self._model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # def define_loss_function(self):
    #     loss_function = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self._outputs, labels=y)
    #     self._loss = tf.reduce_mean(loss_function)

    # def create_optimizer(self):
    #     learning_step = tf.train.AdamOptimizer(0.0001)
    #     optimiser = learning_step.minimize(self._loss)

    # def create_accuracy_evaluation(self):
    #     correct = tf.equal(tf.argmax(self._outputs, axis=1), tf.argmax(y, axis=1))
    #     acc = tf.reduce_mean(tf.cast(correct, 'float'))

    def split_data(self, input_samples, output_samples, test_split):
        # Reshape input samples
        # .reshape((input_samples.shape[0], 42))
        input_samples = input_samples.reshape(input_samples.shape[0], -1)
        print(input_samples.shape)
        num_eval = int(input_samples.shape[0] * test_split)
        num_train = input_samples.shape[0] - num_eval

        # Create an array from 0 -> total number of samples
        all_idx = np.arange(0, input_samples.shape[0], 1)

        # Randomly shuffle the index's (Just the array we created, not the actual data)
        np.random.shuffle(all_idx)

        # Assign training/evaluation index's
        train_idx = all_idx[:num_train]
        eval_idx = all_idx[num_train:]

        # Create Training/Evaluation Data by assigning the data from input_samples at each index
        train_input_data, train_output_data = input_samples[train_idx], output_samples[train_idx]
        eval_input_data, eval_output_data = input_samples[eval_idx], output_samples[eval_idx]

        return train_input_data, train_output_data, eval_input_data, eval_output_data

    def train_model(self, train_input_data, train_output_data, test_split):
        self._model.fit(train_input_data, train_output_data, epochs=350, batch_size=32, verbose=1)
        
        

    def evaluate_model(self, eval_input_data, eval_output_data):
        loss, acc = self._model.evaluate(
            eval_input_data, eval_output_data, verbose=1)
        print(loss, acc)

    def save_model(self):
        self._model.save('./model_better_bot_type2_4layers')
        # self._model.save('./saved_model/my_model')
