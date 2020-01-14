#import tensorflow as tf
import pandas as pd     # data frame manipleation
#import seaborn as sns   # perform auto plot images stat plots adv matplot lib
import numpy as np      # numerical analysis
import math
import matplotlib.pyplot as plt

import tensorflow as tf

from tensorflow.keras.layers import Dense, InputLayer
#from tensorflow.keras.layers import Dense, Flatten, Conv2D
from tensorflow.keras import Model

#x_train = data_df[0]['x0', 'x1']].as_matrix()
#x_train = data_df[['theta', 'thetaSqr']]
#
#y_train = data_df['sin'].as_matrix()
#x_train = data_df[['x0', 'x1']].as_matrix()

#y_train = y_train.values.reshape(-1,1)
#x_train = x_train.values.reshape(-1,1)

#print(y_train)
#print(x_train)
#assert(False == True)

#y_train = data_df['sin'].as_matrix(columns=None)
#x_train = data_df['theta'].as_matrix(columns=None)

#print(x_train[0:5])
#print(y_train[0:5])
#x_train = np.asarry(x_train)

#print(x_train.as_matrix(columns=None)) # .as_matrix will be removed soon use .values
#print(type(x_train))

#x0= (math.pi*6 * np.random.random_sample(100))
#x1= [x*x for x in x0]
#x_test = [x0, x1]
#y_test = [math.sin(q) for q in x0]
#
#x_test = np.asarray(x_test)
#y_test = np.asarray(y_test)

#x_test = x_test[..., tf.newaxis]
#x_train = x_train[..., tf.newaxis]

#assert(False == True)
#train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train))
#test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test))

#train_ds = [x_train, y_train]
#train_ds = np.asarray(train_ds)
##train_ds = tf.pack(train_ds)
#test_ds = [x_test, y_test]
#test_ds = np.asarray(test_ds)

#print(x_train.transpose())

data_df = np.split(pd.read_csv('data.csv'), [2000], axis=0)
#print(data_df.head(5))
#print(data_df.info())
#print(len(data_df))

y_train = data_df[0]['y'].values
x_train = data_df[0][['x0', 'x1']].values
#x_train = x_train.values()
#x_train = data_df[0][['x0', 'x1']]

y_test = data_df[1]['y'].values
x_test = data_df[1][['x0', 'x1']].values

#y_test = tf.convert_to_tensor(y_test)
#x_test = x_test.transpose()
#x_test = x_test.reshape(len(x_test), 2, 1)
#x_test = tf.convert_to_tensor(x_test)

print(type(x_train))
print(len(x_train))
#x_train = x_train.reshape(len(x_train), 2, 1)
print(type(x_train))
print(np.shape(x_train))

#y_train = tf.convert_to_tensor(y_train.values)
#x_train = tf.convert_to_tensor(x_train)

train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train)).shuffle(10000).batch(50)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32)

print(type(x_train))
print(type(x_test))
print(x_test.shape)
print(x_train.shape)
#train_ds = tf.convert_to_tensor(train_ds)
#print(type(train_ds))
#print(shape(train_ds))
#print(test_ds)
#print(type(test_ds))
#print(train_ds)
#print("here")

#assert(False == True)
#print(train_ds.info())
class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        #self.input = InputLayer(input_tensor=np.shape(x_train[0]))
        #self.inp= InputLayer()
        #self.inp= InputLayer(input_tensor=x_train[0])
        #self.d1 = Dense(5, activation='sigmoid')
        self.d1 = Dense(15, activation='tanh', input_shape = [2])
        #self.d1 = Dense(10,  activation='relu')
        self.d2 = Dense(10, activation='tanh')
        self.d3 = Dense(5, activation='tanh')
        #self.d3 = Dense(1, activation='sigmoid')
        #self.d3 = Dense(1, activation='sigmoid', use_bias=False)
        self.d5 = Dense(1)
        #self.d4 = Dense(1, activation='relu')

    def call(self, x):
        #x = self.inp(x)
        x = self.d1(x)
        x = self.d2(x)
        x = self.d3(x)
        #x = self.d4(x)
        return self.d5(x)

    #def predict(self, x):
    #    return super(MyModel, self).predict(x)

model = MyModel()

#assert(False == True)

loss_obj = tf.keras.losses.MeanSquaredError()
optimizer = tf.keras.optimizers.Adam(0.0001)

train_loss = tf.keras.metrics.Mean(name='test_loss')
train_accuracy = tf.keras.metrics.MeanSquaredError(name='test_accuracy')

test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.MeanSquaredError(name='test_accuracy')

@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        #print("x = {x} y = {y}")
        #tf.print(x, output_stream=sys.stdout)
        #print(f"x = {x} y = {y}")
        predictions = model(x)
        loss = loss_obj(y, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))

    train_loss(loss)
    train_accuracy(y, predictions)


@tf.function
def test_step(x, y):
    predictions = model(x)
    t_loss = loss_obj(y, predictions)

    test_loss(t_loss)
    test_accuracy(y, predictions)

print(x_test[0])
#predictions = model(x_test[0])
#xt = np.ndarray((2, 1))
#print(model(xt))
#assert(False == True)
EPOCHS = 1000
model_hist = []

for epoch in range(EPOCHS):
    # Reset the metrics at the start of the next epoch
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    #for x, y in zip(x_train, y_train):
    model.predict(x_train[:2])
    for x, y in train_ds:
        train_step(x, y)

    #for x, y in zip(x_test, y_test):
    for x, y in test_ds:
        test_step(x, y)
    model_hist.append(train_loss.result())

    template = 'Epoch {}, Loss: {}, Accuracy: {}, Test Loss: {}, Test Accuracy: {}'
    print(template.format(epoch+1,
                          train_loss.result(),
                          train_accuracy.result()*100,
                          test_loss.result(),
                          test_accuracy.result()*100))


model.save_weights('weights', save_format='tf')
ans = [model.predict(x_test)]
# cant call predict function here? but can call in before traning

#model.save('sincurveModel.h5')
colors = 'red'
area = 7
plt.plot(model_hist)
plt.show()

plt.scatter(tf.transpose(x_test)[0], y_test, c=colors, alpha=0.5)
plt.scatter(tf.transpose(x_test)[0], ans, c='blue', alpha=0.5)
plt.show()
