import tensorflow as tf 


class Training():
    
    def __init__(self):
        pass 

    def create_NN(self):
        inputs = tf.keras.Input(shape = (42,))
        x = tf.keras.layers.Dense(256, activation=tf.nn.relu)(inputs)
        self._outputs = tf.keras.layers.Dense(7, activation=tf.nn.relu)(x)
        self._model = tf.keras.Model(inputs=inputs, outputs=self._outputs)

        # print(inputs)
        # print(x)
        # print(self._outputs)
        # print(model)
        # model.summary()

    # def define_loss_function(self):
    #     loss_function = tf.nn.softmax_cross_entropy_with_logits_v2(logits=self._outputs, labels=y)
    #     self._loss = tf.reduce_mean(loss_function)

    # def create_optimizer(self):
    #     learning_step = tf.train.AdamOptimizer(0.0001)
    #     optimiser = learning_step.minimize(self._loss)

    # def create_accuracy_evaluation(self):
    #     correct = tf.equal(tf.argmax(self._outputs, axis=1), tf.argmax(y, axis=1))
    #     acc = tf.reduce_mean(tf.cast(correct, 'float'))

    def train_model(self, x_train, y_train):
        
        self.create_NN()
        self._model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        self._model.fit(x_train.reshape(21000, 42), y_train.reshape(21000, 7), epochs=150, batch_size=32, verbose=0)
        
        loss, acc = self._model.evaluate(x_train.reshape(21000, 42)[:200,:], y_train.reshape(21000, 7)[:200,:], verbose=0)

        print(loss, acc)

    
    #moi 