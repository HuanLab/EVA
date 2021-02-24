#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Yibo Jiao, Jian Guo
"""
import argparse
import os
import tensorflow as tf
import numpy as np
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image

if  __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', required=True)
    io_args = parser.parse_args()
    mode = io_args.mode
    
    def create_model():
        cnn = tf.keras.models.Sequential()
        cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu', input_shape=[64, 64, 1]))
        cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
        cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
        cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))
        cnn.add(tf.keras.layers.Flatten())
        cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))
        cnn.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))
        cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
        return cnn
    
    if mode == 'train':
        # get training data
        train_datagen = ImageDataGenerator(rescale = 1./255, horizontal_flip = True, width_shift_range = 0.1)
        train = train_datagen.flow_from_directory('dataset/train',
                                                    # resize
                                                    target_size = (64, 64),
                                                    class_mode = 'binary',
                                                    color_mode = 'grayscale')
        # cnn
        cnn = create_model()
        cnn.fit(x = train, epochs = 10)
        # save cnn
        cnn.save_weights('model/model')
        
    if mode == 'test':
        # load cnn
        cnn = create_model()
        cnn.load_weights('model/model')
        # predict
        entries = os.listdir('dataset/test')
        res = []
        for entry in entries:
            if entry.endswith('.png'):
                path = 'dataset/test/' + entry
                test_image = image.load_img(path, color_mode='grayscale', target_size = (64, 64))
                test_image = image.img_to_array(test_image)
                test_image = np.expand_dims(test_image, axis = 0)
                result = cnn.predict(test_image).squeeze()
                b = False
                if result >= 0.5:
                    b = True
                res.append(np.array([entry, result, b]))
        res = np.asarray(res)
        df = pd.DataFrame(res)
        df.columns = ['image', 'score', 'prediction']
        df.to_csv('outcome.csv', index=False)
