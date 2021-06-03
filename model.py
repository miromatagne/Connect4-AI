import tensorflow as tf
import numpy as np


class Model():

    def __init__(self, model_filename=None):
        """
            Constructor of the Model class.

            :param model_filename: file name of corresponding model
        """
        if model_filename is not None:
            self._model = tf.keras.models.load_model(model_filename)

    def create_NN(self):
        """
            Create a neural network model.
        """
        inputs = tf.keras.Input(shape = (42,))
        x = tf.keras.layers.Dense(256, activation=tf.nn.relu)(inputs)
        self._outputs = tf.keras.layers.Dense(7, activation=tf.nn.relu)(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=self._outputs)

        # Define loss function, create optimizer and create accuracy evaluation
        self._model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def split_data(self, input_samples, output_samples, test_split):
        """
            Split the input and output samples into set of evaluation and training.

            :param input_samples: input samples to be splitted
            :param output_samples: output samples to be splitted
            :param test_split: percentage of samples used for the evaluation
            :return: the input and output training sets and evaluation sets
        """
        #Reshape input samples
        input_samples = input_samples.reshape(input_samples.shape[0], -1)
        num_eval = int(input_samples.shape[0] * test_split)
        num_train = input_samples.shape[0] - num_eval

        #Create an array from 0 -> total number of samples
        all_idx = np.arange(0, input_samples.shape[0], 1)

        #Randomly shuffle the index's
        np.random.shuffle(all_idx)

        #Assign training/evaluation index's
        train_idx = all_idx[:num_train]
        eval_idx = all_idx[num_train:]

        #Create Training/Evaluation data by assigning the data from input_samples at each index
        train_input_data, train_output_data = input_samples[train_idx], output_samples[train_idx]
        eval_input_data, eval_output_data = input_samples[eval_idx], output_samples[eval_idx]

        return train_input_data, train_output_data, eval_input_data, eval_output_data

    def train_model(self, train_input_data, train_output_data):
        """
            Train the model with given input and output training sets.

            :param train_input_data: input training set used to train the model
            :param train_output_data: output training set used to train the model
        """
        self._model.fit(train_input_data, train_output_data, epochs=512, batch_size=32, verbose=1)
        
    def evaluate_model(self, eval_input_data, eval_output_data):
        """
            Evaluate the model with given input and output evaluation sets.

            :param eval_input_data: input evaluation set used to evaluate the model
            :param eval_output_data: output evaluation set used to evaluate the model
        """
        loss, acc = self._model.evaluate(eval_input_data, eval_output_data, verbose=1)
        print(loss, acc)

    def save_model(self):
        """
            Save the model.
        """
        self._model.save('./model_Minmax_vs_MonteCarlo_3layers_no_duplicate')
