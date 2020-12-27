import tensorflow.keras as keras
import tensorflow as tf
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
# from RNN.preproseccing import get_confirmed_ru


import tensorflow as tf
import keras as keras
# import tensorflow as tf
import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from matplotlib import pyplot as plt

TDA = pd.read_csv('TDA_confirmed_anomalies.csv')
TDA['TDA_final_short'].value_counts()
TDA = TDA.replace('United States', 'US')

include_country = list(TDA.loc[TDA['TDA_final_short'] == 'Medium infection', 'Country'].values)

from keras import backend as K

from keras.callbacks import ModelCheckpoint
from preproseccing import get_data, create_ts_train_test_data, get_data_diff, get_data_division
from calculate_metrics import get_metrics, construct_ts, get_metrics_from_df
from models import get_model_fc
from keras import backend as K

from preproseccing import get_data, create_ts_train_test_data, get_data_diff, get_data_division
from calculate_metrics import get_metrics, construct_ts, get_metrics_from_df
from models import get_model_fc

log_scale = False
n_steps = 5

only_labels = False

drop_country = ['Afghanistan', 'Luxembourg', 'Liechtenstein', 'Iceland',
                'Trinidad and Tobago', 'Peru', 'Guatemala', 'Qatar',
                'Saint Kitts and Nevis', 'Chile', 'Costa Rica', 'San Marino',
                'Barbados', 'Australia', 'Argentina', 'Andorra', 'Saint Lucia',
                'Mauritius', 'MS Zaandam', 'Diamond Princess', 'Holy See']

target = ['Confirmed', 'Deaths', 'Recovered']
md_features = ['Country', 'Date']
# X_features= ['Population', 'GrowthRate', 'Area', 'Density', 'Airports', 'GDP']
X_features = ['C1_School closing', 'C2_Workplace closing', 'C3_Cancel public events',
              'C4_Restrictions on gatherings', 'C5_Close public transport',
              'C6_Stay at home requirements', 'C7_Restrictions on internal movement',
              'C8_International travel controls',  # 'E1_Income support',
              #        'E2_Debt/contract relief', 'E3_Fiscal measures',
              #        'E4_International support', 'H1_Public information campaigns',
              #        'H2_Testing policy', 'H3_Contact tracing',
              #        'H4_Emergency investment in healthcare', 'H5_Investment in vaccines',#, 'Population']
              #           'GrowthRate', 'Area', 'Density', 'Airports', 'GDP',
              #              'embeddingval1', 'embeddingval2', 'embeddingval3',
              #        'embeddingval4', 'embeddingval5', 'embeddingval6', 'embeddingval7',
              #        'embeddingval8', 'embeddingval9', 'embeddingval10', 'embeddingval11',
              #        'embeddingval12', 'embeddingval13', 'embeddingval14', 'embeddingval15',
              #        'embeddingval16', 'embeddingval17', 'embeddingval18', 'embeddingval19',
              #        'embeddingval20',
              'Population']
X_features = ['C2_Workplace closing', 'Population']
# embed_features = [ 'embeddingval1', 'embeddingval2', 'embeddingval3',
#        'embeddingval4', 'embeddingval5', 'embeddingval6', 'embeddingval7',
#        'embeddingval8', 'embeddingval9', 'embeddingval10', 'embeddingval11',
#        'embeddingval12', 'embeddingval13', 'embeddingval14', 'embeddingval15',
#        'embeddingval16', 'embeddingval17', 'embeddingval18', 'embeddingval19',
#        'embeddingval20']

data = get_data(return_only_labels=only_labels)

# include_country = ['US']
# data = data.loc[~data['Country'].isin(drop_country)]

data.columns

data = data[md_features + target + X_features]
# data = data.loc[data['Country'].isin(include_country)]

# data.isnull().sum(axis = 0)
# data = data.fillna(method='ffill')

data = data.dropna()
data.isnull().sum(axis=0)

data = data.dropna()

data = data.loc[data['C2_Workplace closing'].isin([2.0, 3.0])]
data['C2_Workplace closing'] = data['C2_Workplace closing'] - 2.0
# for i in target:
# #     data[i] = data[i]/population
#     data[i] = data[i]/data['Population']

data.head()

data = data[md_features + target + X_features]

data.isnull().sum(axis=0)

data.mean()

data['Country'].value_counts()

data_diff = get_data_diff(data)

data_diff = data_diff.dropna(axis='columns')

data_diff.mean()

X_features = list(data_diff.columns[5:])

only_labels = True
embed = False
if only_labels:
    if embed == True:
        data_mean = data_diff[target + embed_features].mean()
    else:
        data_mean = data_diff[target].mean()
else:
    data_mean = data_diff[target + X_features].mean()

if only_labels:
    if embed == True:
        data_std = data_diff[target + embed_features].std()
    else:
        data_std = data_diff[target].std()
else:
    data_std = data_diff[target + X_features].std()

# data_mean = pd.Series(0.0, index= [target + X_features])
# data_std = pd.Series(1.0, index= [target + X_features])

if only_labels:
    if embed == True:
        data_diff[target + embed_features] = (data_diff[target + embed_features] - data_mean[target + embed_features]) \
                                             / data_std[target + embed_features]
    else:
        data_diff[target] = (data_diff[target] - data_mean[target]) \
                            / data_std[target]
else:
    data_diff[target + X_features] = (data_diff[target + X_features] - data_mean[target + X_features].values) \
                                     / data_std[target + X_features].values

only_labels = False

data_diff.head()

data_diff.shape

data.shape

data_diff.mean()

# plt.plot(data.loc[data['Country'] == 'US', 'C1_School closing'])

X_train, X_test, y_train, y_test, md_train, md_test = create_ts_train_test_data(data_diff, n_steps=n_steps)

X_train.shape

np.min(np.abs(X_train))

np.mean(X_test)

# X_train

md_train

md_test.groupby(['Country']).agg({'Date': ['min']})

data_diff.head()

data_diff.boxplot(column=target)

# Scaler

# Multi Target log and fill na

print(X_train.shape)
print(X_test.shape)

y_train.shape

count_features = X_train.shape[2]
# count_samples = X.shape[1]
print(count_features)

y_train = y_train[:, :3]
y_test = y_test[:, :3]

# from tensorflow.keras.optimizers import Adam, RMSprop
# from tensorflow.keras.layers import Input, concatenate, Dropout
# from tensorflow.keras.layers import PReLU
# from tensorflow.keras import Model
# from tensorflow.keras.layers import BatchNormalization

from keras.optimizers import Adam, RMSprop
from keras.layers import Input, concatenate, Dropout
from keras.layers import PReLU
from keras import Model
from keras.layers import BatchNormalization


def get_model_fc(n_steps, n_features, n_output=3, lr=0.001):
    #     model = Sequential()
    #     model.add(keras.Input(shape=(15,)))
    #     model.add(Dense(3, activation='relu', input_shape=(n_steps * n_features,)))
    input1 = Input((n_steps * n_features,))
    hidden = Dense(32, activation=PReLU())(input1)
    outputs = Dense(3, activation='linear')(hidden)

    #     if n_output == 3:
    #         output1 = Dense(1, activation='linear')(hidden)
    #         output2 = Dense(1, activation='linear')(hidden)
    #         output3 = Dense(1, activation='linear')(hidden)
    #         outputs = concatenate([output1, output2, output3])
    #     elif n_output == 1:
    #         outputs =  Dense(1, activation='linear')(hidden)
    #     else:
    #         assert False
    model = keras.Model(inputs=input1, outputs=outputs)
    opt = Adam(lr=lr)
    model.compile(optimizer=opt, loss='mse')
    return model


def get_model_rnn(n_steps, n_features, n_output=3, lr=0.001):
    model = Sequential()
    model.add(LSTM(16, activation='relu', return_sequences=False, input_shape=(n_steps, n_features)))
    #     model.add(LSTM(16, activation='relu', return_sequences=False, ))
    #     model.add(Dropout(0.2))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(n_output))
    opt = Adam(lr=lr)
    model.compile(optimizer=opt, loss='mse')
    return model


def get_model_rnn_2(n_steps, n_features, n_output=3, lr=0.001):
    hidden_size = 24

    #     model = Sequential()
    input1 = Input((n_steps, 3))
    input2 = Input((n_features - 3,))

    hidden1 = LSTM(hidden_size, activation='relu', return_sequences=False, input_shape=(n_steps, 3))(input1)
    # hidden2_0 = Dense(hidden_size // 2, activation='relu')(input2)
    # hidden2_1 = Dense(hidden_size, activation='relu')(hidden2_0)
    # hidden2_2 = Dropout(0.05)(hidden2_1)
    # con = concatenate([hidden1, hidden2_2])
    con = concatenate([hidden1, input2])
    # do1 = Dropout(0.15)(con)
    # d1 = Dense(hidden_size, activation='relu')(do1)

    # output = Dense(n_output)(d1)
    output = Dense(n_output)(con)
    opt = Adam(lr=lr)
    model = keras.Model(inputs=[input1, input2], outputs=output)
    model.compile(optimizer=opt, loss='mse')
    return model


# Fit predict

n_output = 3

# model = get_model_fc(n_steps, count_features, lr = 0.005)
# model = get_model_fc(n_steps, count_features, lr = 0.005, n_output=n_output)
# model = get_model_rnn(n_steps, count_features, lr = 0.005, n_output=1)
model = get_model_rnn_2(n_steps, count_features-1, lr=0.005, n_output=n_output)

y_test.shape

md_train.shape

X_train.shape

X_train.shape

y_train.shape

np.mean(X_train)

X_train[:, n_steps - 1, 3:].shape

X_test[:, n_steps - 1, 3:].shape

count_train = X_train.shape[0]
count_test = X_test.shape[0]

np.mean(X_train)

np.mean(X_test)

np.mean(y_train)

np.mean(y_test)

keras.backend.set_value(model.optimizer.lr, 0.001)
keras.backend.get_value(model.optimizer.lr)

tf.keras.backend.set_floatx('float64')

X_train.shape

mcp_save = ModelCheckpoint('mdl_wts', save_best_only=True, monitor='val_loss', mode='min')
history = model.fit([X_train[:, :, :3], X_train[:, n_steps - 1, 3:count_features-1]], y_train[:, :n_output],
                    validation_data=([X_test[:, :, :3], X_test[:, n_steps - 1, 3:count_features-1]],
                                     y_test[:, :n_output]),
                    epochs=20, verbose=2, callbacks=[mcp_save])

model.save('model')
