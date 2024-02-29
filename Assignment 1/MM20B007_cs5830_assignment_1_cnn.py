# -*- coding: utf-8 -*-
"""cs5830-assignment-1-cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19qEktT5GzEyJwnkuUyfAQiYvzGjJMq5x

# MM20B007 Assignment 1
"""

import pandas as pd
import matplotlib.pyplot as plt
from random import randrange, randint
from sklearn.model_selection import train_test_split

# pytorch import
import torchvision
import torch
from torchvision import transforms
from torch.utils.data import Dataset
from torchvision.transforms import functional

# keras import
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, AveragePooling2D, Flatten
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping

n_epochs = 30 # 30
n_epochs_cv = 10 # 10  # reduce number of epochs for cross validation for performance reason
n_cv = 10
validation_ratio = (1 / 6)
ANGLES = [-30, -20, -10, 10, 20, 30]

"""# Dataset"""

train_mnist = torchvision.datasets.MNIST(root='data/', train=True, download=True, transform=transforms.ToTensor())
test_mnist = torchvision.datasets.MNIST(root='data/', train=False, download=True, transform=transforms.ToTensor())
print(train_mnist.data.shape, train_mnist.targets.shape)
print(test_mnist.data.shape, test_mnist.targets.shape)

def prepare_dataset(dataset):
    img_size = 28
    img = torch.stack([item[0] for item in dataset])
    data = tf.reshape(img, (len(dataset), img_size, img_size, 1)).numpy()

    numpy_array = torch.tensor([items[1] for items in dataset]).numpy()
    targets = pd.Series(numpy_array)

    return (data, targets)

"""## Task 1"""

def rotate_image(img_tensor, angle):

    # Ensure the input dataset has the correct shape
    assert img_tensor.shape == (1, 28, 28), "Input dataset must have shape (1, 28, 28)"

    # Rotate the Image
    rotated_tensor = functional.rotate(img_tensor, angle)

    return rotated_tensor

"""## Task 2"""

def generate_dataset(dataset, oversample_rate, angle):

    oversample_rate = 2 if oversample_rate <= 1 else oversample_rate
    to_generate_count = int(len(dataset)*(oversample_rate - 1.0))

    rotated_data = []

    for i in range(to_generate_count):

        # Randomly pick a data point from the dataset
        random_image_index = randint(0, len(dataset) - 1)
        img, l = dataset[random_image_index]

        # Rotate the image using the function defined earlier
        rotated_img = rotate_image(img, angle)

        # Add the rotated image and corresponding label in the new dataset
        rotated_data.append((rotated_img, l))

    return rotated_data

"""## Task 3"""

def create_cnn_model(pool_type='max', conv_activation='sigmoid', dropout_rate=0.10):
    # create model
    model = Sequential()

    # first layer: convolution
    model.add(Conv2D(16, kernel_size=(5, 5), activation='relu', input_shape=(28, 28, 1)))

    # second series of layers: convolution, pooling, and dropout
    model.add(Conv2D(32, kernel_size=(5, 5), activation=conv_activation))
    if pool_type == 'max':
        model.add(MaxPooling2D(pool_size=(2, 2)))
    if pool_type == 'average':
        model.add(AveragePooling2D(pool_size=(2, 2)))
    if dropout_rate != 0:
        model.add(Dropout(rate=dropout_rate))

    # third series of layers: convolution, pooling, and dropout
    model.add(Conv2D(64, kernel_size=(3, 3), activation=conv_activation))   # 32
    if pool_type == 'max':
        model.add(MaxPooling2D(pool_size=(2, 2)))
    if pool_type == 'average':
        model.add(AveragePooling2D(pool_size=(2, 2)))
    if dropout_rate != 0:
        model.add(Dropout(rate=dropout_rate))

    # fourth series
    model.add(Flatten())
    model.add(Dense(64, activation='sigmoid')) # 64
    # add a dropout layer if rate is not null
    if dropout_rate != 0:
        model.add(Dropout(rate=dropout_rate))

    model.add(Dense(10, activation='softmax'))

    # Compile model
    model.compile( optimizer='adam',
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])

    return model

def learn_model(dataset):

    # extract train and validation set
    X, y = prepare_dataset(dataset)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size = validation_ratio)

    # Parameter values
    pool_type = ['max', 'average'],
    conv_activation = ['sigmoid', 'tanh']

    # Initialize variables to store the best hyperparameters and their corresponding performance
    best_pool_type = None
    best_conv_activation = None
    best_accuracy = 0.0

    #define callbacks
    early_stop = EarlyStopping(monitor = 'val_accuracy',
                               mode = 'max',
                               patience=5,
                               restore_best_weights=True)

    # Perform the for loop to search for the best hyperparameters
    for pt in pool_type:
        for ca in conv_activation:
            # Create the model with the current hyperparameters
            model = create_cnn_model(pool_type = pt,
                                     conv_activation = ca,
                                     dropout_rate=0.10)

            # Train the model with the current hyperparameters
            model.fit(X_train, to_categorical(y_train),
                      batch_size = 32,
                      epochs = n_epochs_cv,
                      callbacks = [early_stop])

            # Evaluate the model with the current hyperparameters
            _, accuracy = model.evaluate(X_val, to_categorical(y_val), verbose=0)

            # Check if the current hyperparameters are the best so far
            if accuracy > best_accuracy:
                best_pool_type = pt
                best_conv_activation = ca
                best_accuracy = accuracy

    # Print the best hyperparameters and their corresponding performance
    print(f"Best pool type: {best_pool_type}.")
    print(f"Best convolution activation: {best_conv_activation}.")
    print("Best validation accuracy: {:.2f}%".format(best_accuracy * 100))

    model = create_cnn_model(pool_type = best_pool_type,
                             conv_activation = best_conv_activation,
                             dropout_rate = 0.10)
    return model

"""## Task 4"""

def monitor_perf(model, ground_truth_dataset, threshold):
    X, y = prepare_dataset(ground_truth_dataset)
    loss, accuracy = model.evaluate(X, to_categorical(y))
    print(f'The test accuracy is {accuracy}')

    if loss > threshold:
        drift_flag = True
    else:
        drift_flag = False
    return drift_flag

train = train_mnist
model = learn_model(train)
for angles in ANGLES:
    if monitor_perf(model, test_mnist, 2.5):
        oversampled_data = generate_dataset(train_mnist, 2, angles)
        train = train + oversampled_data
        model = learn_model(train)
    else:
        print('******************************************************')
        print('The model will work')
        break