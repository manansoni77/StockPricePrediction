from app.cache import manual_cache
import os
import base64
import io
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import pandas
pandas.options.mode.chained_assignment = None
import numpy
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

import matplotlib.pyplot as plt
plt.figure(figsize=(16,8))

@manual_cache
def prediction(symbol):
    data = pandas.read_csv(symbol+'.csv')
    data['time'] = pandas.to_datetime(data.timestamp,format='%Y-%m-%d')
    data = data[['time','close']]
    data.index = data.time
    data.drop('time', axis=1, inplace=True)
    data = data.sort_index(ascending=True)

    scaler = MinMaxScaler(feature_range=(0, 1))
    fdata = scaler.fit_transform(data.values)

    l = int(len(fdata)*0.7)
    r = len(fdata) - l

    x_train, y_train = [], []
    x_test,y_test = [], []

    for i in range(60, l):
        x_train.append(fdata[i-60:i])
        y_train.append(fdata[i])

    for i in range(l,l+r):
        x_test.append(fdata[i-60:i])
        y_test.append(fdata[i])

    x_train = numpy.array(x_train)
    y_train = numpy.array(y_train)
    x_test = numpy.array(x_test)
    y_test = numpy.array(y_test)

    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(Dropout(0.1)) 
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.1)) 
    model.add(LSTM(units=50))
    model.add(Dense(25))
    model.add(Dense(5))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=5, batch_size=10, verbose=2)
    model.save('/mnt/d/Major Project/project1/backend/output.h5')

    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    rmse=numpy.sqrt(numpy.mean(numpy.power((y_test-predictions),2)))

    train = data[:l]
    valid = data[l:]
    valid['Predictions'] = predictions

    plt.plot(train['close'])
    plt.plot(valid[['close','Predictions']])
    
    input = input = fdata[-60:]
    todays_prediction = model.predict(numpy.array([input]))
    todays_prediction = scaler.inverse_transform(todays_prediction)[0][0]

    buffer = io.BytesIO()
    plt.savefig(buffer, format='jpg')
    buffer.seek(0)
    converted_string = base64.b64encode(buffer.read())
    plt.close()

    return (rmse,todays_prediction,converted_string.decode('utf-8'))