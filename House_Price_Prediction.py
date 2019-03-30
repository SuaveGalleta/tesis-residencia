#
#House Price Prediction.py
#
# This is a simple prediction of house prices based on house size, implemented in tensorflow. this #code is part of pluralsight´s course tesorflow getting started
#

import tensorflow as tf 
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation #import animation support

#generation some house sizes beetween 1000 and 3500 (typical sq ft of house)
num_house =  160
np.random.seed(42)
house_size = np.random.randint(low=1000, high=3500, size=num_house)

#Generate house prices frome house size with a random noise added
np.random.seed(42)
house_price = house_size * 100.0 + np.random.randint(low=20000, high=70000, size= num_house)

#plot generated house and size
plt.plot(house_size, house_price, "bx") #bx = blue x
plt.ylabel("Price")
plt.xlabel("Size")
plt.show()

#Training model with tensorflow 

#you need to normalize values to prevent under/overflows
def normalize(array):
    return (array - array.mean()) / array.std()

#define number of training samples, 0.7= 70%. We can take the first 70% since the values are randomized
num_train_samples = math.floor(num_house * 0.7)

#define train data
train_house_size = np.asarray(house_size[:num_train_samples])
train_prices = np.asarray(house_price[:num_train_samples:])

train_house_size_norm = normalize(train_house_size)
train_price_norm = normalize(train_prices)

#define test data
test_house_size = np.array(house_size[num_train_samples:])
test_house_price = np.array(house_price[num_train_samples:])

test_house_size_norm = normalize(test_house_size)
test_house_price_norm = normalize(test_house_price)

#set up the tensorflow placeholders that get the updated as we descend down the gradient
tf_house_size = tf.placeholder("float", name="house_price")
tf_price = tf.placeholder("float", name="price")

#define the variables holding the size_factor and price we set during training 
#we inicialize them to some random values based on the normal distribution
tf_size_factor = tf.Variable(np.random.randn(), name="size_factor")
tf_price_offset = tf.Variable(np.random.randn(), name="price_offset")

#2. Define operations for the prediction values - prediction price = (size_factor * house_size) + #price_offset
#Notice , the use of the tensorflow add and multiply functions, these add the operations to the computing #graph
#And the tensorflow methods undestand how to deal with tensors, therefore do not use numpy or other #library methods.

tf_price_pred = tf.add(tf.multiply(tf_size_factor, tf_house_size), tf_price_offset)

#3. Define the loss function (how much error) - Mean squared error 
tf_cost = tf.reduce_sum(tf.pow(tf_price_pred - tf_price, 2))/(2*num_train_samples)

#optimizer learning rate. the size of the steps down the gradient
learning_rate = 0.1

#4. define a gradient descent optimazer that will minimize the loss defined in the opration "cost"
optimazer = tf.train.GradientDescentOptimizer(learning_rate).minimize(tf_cost)

#Initializing all variables
init = tf.global_variables_initializer()

#launch the graph in the session
with tf.Session() as sess:
    sess.run(init)

    #set how often to display training progress and number of trainig iterations
    display_every = 2
    num_training_iter = 50

    #keep iterating the training data
    for iteration in range(num_training_iter):

        #fit all training data 
        for(x,y) in zip(train_house_size_norm, train_price_norm):
            sess.run(optimazer, feed_dict={tf_house_size: x, tf_price:y})
        

        #Display current status
        if(iteration + 1 ) % display_every == 0:
            c = sess.run(tf_cost, feed_dict={tf_house_size: train_house_size_norm, tf_price: train_price_norm})
            print("iteration #:", '%04d' % (iteration+1), "cost=", "{:.9f}".format(c), "size factor=", sess.run(tf_size_factor), "price_offset=", sess.run(tf_price_offset))
    
    print("Optimazation Finished")
    training_cost = sess.run(tf_cost, feed_dict={tf_house_size: train_house_size, tf_price: train_price_norm})
    print("Train cost=", training_cost, "size factor=", sess.run(tf_size_factor), "price offset=", sess.run(tf_price_offset))

    train_house_size_mean = train_house_size.mean()
    train_house_size_std = train_house_size.std()

    train_price_mean = train_prices.mean()
    train_prices_std = train_prices.std()

    #plot the graph
    plt.rcParams["figure.figsize"] = (10,8)
    plt.figure()
    plt.ylabel("prices")
    plt.xlabel("size (sq.ft)")
    plt.plot(train_house_size, train_prices, 'go', label = 'training data')
    plt.plot(test_house_size, test_house_price, 'mo', label='testing data')
    plt.plot(train_house_size_norm * train_house_size_std + train_house_size_mean, (sess.run(tf_size_factor)*train_house_size_norm+sess.run(tf_price_offset))*train_prices_std+train_price_mean, label = 'learned regretion')

    plt.legend(loc='upper left')
    plt.show()
