import pandas as pd
import numpy as np


def get_metrics(y_train, yhat_train, y_test, yhat_test, metrics, name_y=None, log_scale=False):
    if name_y is None:
        name_y = ['Confirmed', 'Deaths', 'Recovered']
    if log_scale:
        y_train = np.expm1(y_train)
        yhat_train = np.expm1(yhat_train)
        y_test = np.expm1(y_test)
        yhat_test = np.expm1(yhat_test)
    name_metrics = [metrics[i].__name__ for i in range(len(metrics))]
    errors_train = np.zeros(shape=(len(metrics), len(name_y)))
    errors_test = np.zeros(shape=(len(metrics), len(name_y)))

    for i in range(len(name_y)):
        for j in range(len(metrics)):
            errors_train[j, i] = metrics[j](y_train[:, i], yhat_train[:, i])
            errors_test[j, i] = metrics[j](y_test[:, i], yhat_test[:, i])
    pd_error_train = pd.DataFrame(errors_train, index=name_metrics, columns=name_y)
    pd_error_test = pd.DataFrame(errors_test, index=name_metrics, columns=name_y)
    return pd_error_train, pd_error_test


def construct_ts(name_y, name_y_pred, yhat, md, data):
    countries = np.unique(data['Country'])
    # name_y_pred = [i + '_pred' for i in name_y]
    y_df = pd.DataFrame(yhat, columns=name_y_pred)

    y_df = pd.concat([y_df, md.reset_index(drop=True)], axis=1)

    min_date = y_df.groupby('Country').agg({'Date': ['min']})  # для кумулятивной суммы
    min_date.columns = ['min_date']
    min_date = pd.to_datetime(min_date['min_date']) - pd.DateOffset(1)

    data['Date'] = pd.to_datetime(data['Date'])

    co_shift = {}
    for i, c in enumerate(countries):
        co_shift[c] = data.loc[(data['Date'] == min_date.loc[c]) & (data['Country'] == countries[i])][name_y].values

    for c, v in co_shift.items():
        y_df.loc[y_df['Country'] == c, name_y_pred] = \
            np.cumsum(y_df.loc[y_df['Country'] == c, name_y_pred], axis=0) + v

    y_df['Date'] = pd.to_datetime(y_df['Date'])

    y_df = pd.merge(data, y_df, how='inner', left_on=['Country', 'Date'], right_on=['Country', 'Date'])

    return y_df


def get_metrics_from_df(y_df, metrics, name_y, name_y_pred):
    name_metrics = [metrics[i].__name__ for i in range(len(metrics))]
    res = pd.DataFrame(0.0, columns=name_y, index=name_metrics)
    for i in range(len(name_y)):
        for j in range(len(metrics)):
            res.at[name_metrics[j], name_y[i]] = metrics[j](y_df[name_y[i]], y_df[name_y_pred[i]])

    return res
