from Codes.Configuration import NUMBER_OF_ACTION
from Codes.RLUnit.RLAlgorithm import RLAlgorithm
from keras.layers import Dense, Input, LeakyReLU
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import numpy as np
import random
import os

class DQN(RLAlgorithm):
    def __init__(self, input_shape, epochs=25, neurons_num:list = [128,32], lr=0.001, gamma=0.7,
                 epsilon=0.95, decay=0.955, min_epsilon=0.001, batch_size=32):
        super().__init__(lr, gamma, epsilon, decay, min_epsilon)
        self.epochs = epochs
        self.algorithm_name = "DQN"
        self.batch_size = batch_size
        self.neurons_num_list = neurons_num
        self.input_shape = input_shape
        self.model = self.create_model()
        self.rewards = []

    def create_model(self):
        model = Sequential()
        model.add(Input(shape=(self.input_shape,)))
        for n in self.neurons_num_list:
            model.add(Dense(n, activation=LeakyReLU(alpha=0.01)))
        model.add(Dense(NUMBER_OF_ACTION, activation="sigmoid", name="Actions"))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.lr, decay=self.decay))
        return model

    def replay(self, memory, callbacks_list, model_info_path, model_name):
        x_batch, y_batch = [], []
        mini_batch = random.sample(memory, min(len(memory), self.batch_size))
        for state, action, reward, next_state in mini_batch:
            y_target = self.pred(state)
            y_target[0][0] = reward + self.gamma * self.Q_next(next_state)[0]
            x_batch.append(state.reshape(-1, state.size))
            y_batch.append(y_target[0].reshape(-1, y_target[0].size))
        self.model.fit(np.squeeze(x_batch), np.squeeze(y_batch), epochs=self.epochs, batch_size=len(x_batch), validation_split=0.20,
                       callbacks=callbacks_list, verbose=0)
        self.model.save(os.path.join(model_info_path, model_name + ".h5"))
        self.epsilon = max(self.epsilon * self.decay, self.min_epsilon)

    def Q_next(self, state):
        return self.pred(state)[0]

    def fit(self,state):
        return self.policy(state)

    def policy(self, state):
        rand = np.random.uniform(0, 1)
        if rand > self.epsilon:
            return self.value_function(state)
        return np.random.choice([1, 2, 3, 4, 5, 6])

    def pred(self, state):
        x = self.model.predict(state.reshape(-1, state.size), verbose=0)
        return x

    def value_function(self, state):
        return np.argmax(self.pred(state)[0])+1