import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from sklearn import preprocessing

# locate and read the csv file
df = pd.read_csv(
    '/Users/youssefhemimy/Development /Python /TensorFlow-Pokemon/pokemon_alopez247.csv')
df.columns

# choosing the categories
df = df[['isLegendary', 'Generation', 'Type_1', 'Type_2', 'HP', 'Attack', 'Defense',
         'Sp_Atk', 'Sp_Def', 'Speed', 'Color', 'Egg_Group_1', 'Height_m', 'Weight_kg', 'Body_Style']]
# converting islegendary from boolean to values 0 and 1
df['isLegendary'] = df['isLegendary'].astype(int)

# create dummy variables


def dummy_creation(df, dummy_categories):
    for i in dummy_categories:
        df_dummy = pd.get_dummies(df[i])
        df = pd.concat([df, df_dummy], axis=1)
        df = df.drop(i, axis=1)
    return(df)


df = dummy_creation(df, ['Egg_Group_1', 'Body_Style',
                         'Color', 'Type_1', 'Type_2'])

# this function takes any Pokémon whose "Generation" label is equal to 1 and putting it into the test dataset,
# and putting everyone else in the training dataset.
# It then drops the Generation category from the dataset


def train_test_splitter(DataFrame, column):
    df_train = DataFrame.loc[df[column] != 1]
    df_test = DataFrame.loc[df[column] == 1]

    df_train = df_train.drop(column, axis=1)
    df_test = df_test.drop(column, axis=1)

    return(df_train, df_test)


df_train, df_test = train_test_splitter(df, 'Generation')

# data seperation

def label_delineator(df_train, df_test, label):

    train_data = df_train.drop(label, axis=1).values
    train_labels = df_train[label].values
    test_data = df_test.drop(label, axis=1).values
    test_labels = df_test[label].values
    return(train_data, train_labels, test_data, test_labels)


train_data, train_labels, test_data, test_labels = label_delineator(
    df_train, df_test, 'isLegendary')

# normalizing the data to be on same scale


def data_normalizer(train_data, test_data):
    train_data = preprocessing.MinMaxScaler().fit_transform(train_data)
    test_data = preprocessing.MinMaxScaler().fit_transform(test_data)
    return(train_data, test_data)


train_data, test_data = data_normalizer(train_data, test_data)


# crating the model using Keras
length = train_data.shape[1]

model = keras.Sequential()
model.add(keras.layers.Dense(500, activation='relu', input_shape=[length, ]))
model.add(keras.layers.Dense(2, activation='softmax'))

# compile the model
model.compile(optimizer='sgd',
              loss='sparse_categorical_crossentropy', metrics=['accuracy'])
# get the model to fit our data
model.fit(train_data, train_labels, epochs=400)
loss_value, accuracy_value = model.evaluate(test_data, test_labels)
# printing our test accuracy
print(f'Our test accuracy was {accuracy_value}')

# predict specific Pokémon


def predictor(test_data, test_labels, index):
    prediction = model.predict(test_data)
    if np.argmax(prediction[index]) == test_labels[index]:
        print(
            f'This was correctly predicted to be a \"{test_labels[index]}\"!')
    else:
        print(
            f'This was incorrectly predicted to be a \"{np.argmax(prediction[index])}\". It was actually a \"{test_labels[index]}\".')
        return(prediction)


# preditcting Mewtwo
predictor(test_data, test_labels, 149)
