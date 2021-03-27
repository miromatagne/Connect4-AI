import tensorflow as tf 
import numpy as np

class Training():
    
    def __init__(self):
        pass 

    def create_NN(self):
        inputs = tf.keras.Input(shape = (42,))
        x = tf.keras.layers.Dense(256, activation=tf.nn.relu)(inputs)
        self._outputs = tf.keras.layers.Dense(7, activation=tf.nn.relu)(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=self._outputs)

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
        #Reshape input samples 
        input_samples = input_samples.reshape(input_samples.shape[0], -1)  # .reshape((input_samples.shape[0], 42))
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
    

    def train_model(self, input_samples, output_samples, test_split):
        
        self.create_NN()
        # Define loss function, create optimizer and create accuracy evaluation
        self._model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        train_input_data, train_output_data, eval_input_data, eval_output_data = self.split_data(input_samples, output_samples, test_split)

        self._model.fit(train_input_data, train_output_data, epochs=600, batch_size=32, verbose=1)
        
        loss, acc = self._model.evaluate(eval_input_data, eval_output_data, verbose=1)

        print(loss, acc)
