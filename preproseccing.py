import numpy as np
import pandas as pd


def split_sequence(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the sequence
        if end_ix > len(sequence) - 1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)


def get_data(name_file='Covid_19_aggregated.csv', data_end='26/06/2020', min_confirmed=25, min_day_include_country=70,
             return_only_labels=True, labels=None):
    if labels == None:
        labels = ['Confirmed', 'Deaths', 'Recovered', 'Date', 'Country']
    data = pd.read_csv(name_file)
    data = data.loc[(data['Date'] <= data_end) & (data['Confirmed'] >= min_confirmed)]
    d_count = data.groupby(['Country']).agg({'Date': ['count']})
    d_count.columns = ['count']
    include_countries = d_count.loc[(d_count['count'] >= min_day_include_country)].index
    if return_only_labels:
        data = data[['Confirmed', 'Deaths', 'Recovered', 'Date', 'Country']]
    return (data.loc[data['Country'].isin(include_countries)]).reset_index(drop=True)


def get_data_diff(data, features=None, flag_percent=True):
    if features is None:
        features = ['Confirmed', 'Deaths', 'Recovered']
    countries = np.unique(data['Country'])
    data_diff = []
    for c in countries:
        data_c = data.loc[data['Country'] == c].sort_values(['Date'])
        data_d = data_c.copy()
        data_d[features] = data_c[features].diff()
        data_d = data_d.iloc[1:]
        if flag_percent:
            data_d[features] = data_d[features] / data_c[features].iloc[:-1]
        data_diff.append(data_d)

    return pd.concat(data_diff, axis=0, ignore_index=True)  # .drop(['index', 'level_0'], axis=1)


def get_data_division(data, features=None):
    if features is None:
        features = ['Confirmed', 'Deaths', 'Recovered']
    countries = np.unique(data['Country'])
    data_diff = []
    for c in countries:
        data_c = data.loc[data['Country'] == c].sort_values(['Date'])
        data_c[features] = data_c[features] / np.concatenate(
            [data_c[features].values[0:1], data_c[features].values[:-1]])
        data_diff.append(data_c.iloc[1:])
    return pd.concat(data_diff, axis=0, ignore_index=True)  # .drop(['index', 'level_0'], axis=1)


# def scale_data

def create_ts_train_test_data(data, n_steps=5, count_test_size=31):
    countries = np.unique(data['Country'].values)
    data_X = []
    data_y = []
    meta_data = []
    for c in countries:
        data_co = data.loc[data['Country'] == c]
        data_co = data_co.sort_values(['Date'])
        country_date = data_co[['Country', 'Date']].iloc[n_steps:]
        data_co = data_co.drop(['Country', 'Date'], axis=1)
        count_samples = data_co.shape[0]
        count_features = data_co.shape[1]
        data_co_ts = np.zeros(shape=(count_samples - n_steps, n_steps, count_features))
        y_co = np.zeros(shape=(count_samples - n_steps, count_features))
        for i in range(count_features):
            data_co_ts[:, :, i], y_co[:, i] = split_sequence(data_co.values[:, i], n_steps)
        data_X.append(data_co_ts)
        data_y.append(y_co)
        meta_data.append(country_date)
    X_train = []
    X_test = []
    meta_data_train = []
    y_train = []
    y_test = []
    meta_data_test = []
    for i in range(len(data_X)):
        X_train.append(data_X[i][:-count_test_size])
        X_test.append(data_X[i][-count_test_size:])

        y_train.append(data_y[i][:-count_test_size])
        y_test.append(data_y[i][-count_test_size:])

        meta_data_train.append(meta_data[i].iloc[:-count_test_size])
        meta_data_test.append(meta_data[i].iloc[-count_test_size:])
    X_train = np.concatenate(X_train, axis=0)
    X_test = np.concatenate(X_test, axis=0)

    y_train = np.concatenate(y_train, axis=0)
    y_test = np.concatenate(y_test, axis=0)

    meta_data_train = pd.concat(meta_data_train, axis=0)
    meta_data_test = pd.concat(meta_data_test, axis=0)
    return X_train, X_test, y_train, y_test, meta_data_train, meta_data_test
