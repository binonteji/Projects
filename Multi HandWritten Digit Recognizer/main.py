
import tensorflow as tf
#import matplotlib.pyplot as plt
            
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(60000, 28, 28, 1); print(x_train.shape, y_train.shape) # 60000
x_train = x_train / 255.0
x_test = x_test.reshape(10000, 28, 28, 1); print(x_test.shape, y_test.shape) # 10000
x_test = x_test / 255.0

classes = 10
 
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(28, 28, 1)),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(classes, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.fit(x_train, y_train, epochs=5)

model.save('mdl.h5')
