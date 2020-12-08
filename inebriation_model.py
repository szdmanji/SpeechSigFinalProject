import glob
import re
import numpy as np
import pandas as pd
import librosa
import csv
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from keras.utils import to_categorical

def prepare_data():
    headers = ['chroma_stft','rms','spectral_centroid','spectral_bandwidth','rolloff','zero_crossing_rate','onset_strength','mfcc1','mfcc2','mfcc3','mfcc4','mfcc5','mfcc6','mfcc7','mfcc8','mfcc9','mfcc10','mfcc11','mfcc12','mfcc13','mfcc14','mfcc15','mfcc16','mfcc17','mfcc18','mfcc19','mfcc20']
    N = len(headers)
    sober_df = pd.read_csv(sober_data_path)
    del sober_df['filename']
    del sober_df['label']

    drunk_df = pd.read_csv(drunk_data_path)
    del drunk_df['filename']
    del drunk_df['label']

    npdata_sober = sober_df.to_numpy()
    npdata_drunk = drunk_df.to_numpy()

def make_predictions(data):
    scaler = StandardScaler()
    X = scaler.fit_transform(np.array(data.iloc[:, :-1], dtype = float))
    y = data.iloc[:, -1]
    encoder = LabelEncoder()
    y = encoder.fit_transform(y)
    accuracy = 0

for i in range(10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)

    model = Sequential()
    model.add(Dense(256, activation='relu', input_shape=(X_train.shape[1],)))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(2, activation='softmax'))
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=50, batch_size=120)
    test_loss, test_acc = model.evaluate(X_test,y_test)
    accuracy += test_acc

    print(accuracy / 10)

    predictions = model.predict(X_test)
    np.argmax(predictions[0])
