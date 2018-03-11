import numpy as np
from util.log import Log
from model_training.regression.single_output_regression.abstract_regressor import AbstractRegressor
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense


class AdditionalIndemnityMoney(AbstractRegressor):
    def __init__(self, dataset=None, outcome_index=0):
        AbstractRegressor.__init__(self, 'additional_indemnity_money', dataset, outcome_index)

    def train(self):
        """
            Trains the pipeline. After training the dataset is removed
            from the object to save space.
        """
        Log.write("Size of dataset: %d" % (len(self.dataset)))
        X = np.array([precedent['facts_vector'] for precedent in self.dataset])
        Y = np.array([precedent['outcomes_vector'][self.outcome_index]
                      for precedent in self.dataset])
        self.input_dimensions = len(X[0])
        regressor = KerasRegressor(
            build_fn=self._nn_architecture, epochs=6000, batch_size=128, verbose=0)
        scaler = StandardScaler()
        self.model = AbstractRegressor._create_pipeline(scaler, regressor)
        self.model.fit(X, Y)
        self.test()

    def _nn_architecture(self):
        """
            Defines Regressor architecture. To be used internally
        """
        model = Sequential()
        model.add(Dense(128, input_dim=self.input_dimensions,
                        kernel_initializer='normal', activation='relu'))
        model.add(Dense(128, kernel_initializer='normal', activation='relu'))
        model.add(Dense(64, kernel_initializer='normal', activation='relu'))
        model.add(Dense(64, kernel_initializer='normal', activation='relu'))
        model.add(Dense(32, kernel_initializer='normal', activation='relu'))
        model.add(Dense(32, kernel_initializer='normal', activation='linear'))
        model.add(Dense(1, kernel_initializer='normal'))
        model.compile(loss='mean_squared_error', optimizer='adam')
        return model