import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

#create input object which reads data from MNIST dataset. Perform one-hot encoding to define the digit 
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

#Using interactive session makes it the default session so we do not pass sess
sess = tf.InteractiveSession()

#define placeholders for MNIST input data
x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])

#change the MNIST input data from a list of values to 28 pixel x 28 pixel x 1 grayscale value cube 
#which the convolution NN can use
x_image = tf.reshape(x, [-1,28,28,1], name="x_image")

#define helper fuctions to created weights and baises variables, and covolution, and pooling layers
#we are using RELU as our activation fuction. These must be initialized to a small positive number 
#and with some noise so you dont end up going to zero when comparing diffs
def weight_variables(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

#convolution and pooling - we do convolution and the pooling to control overfitting 
def conv2d(x, W):
    return tf.nn.conv2d(x,W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')


#define layers

#1st Convolution layer
#32 features for each 5x5 patch of image

W_conv1= weight_variables([5,5,1,32])
b_conv1= weight_variables([32])

#do convolution of images, add bias and push through relu activation
h_conv1= tf.nn.relu(conv2d(x_image, W_conv1 )+b_conv1)

#take results and run through max_pool
h_pool1 = max_pool_2x2(h_conv1)

#second convolution layer
#process the 32 features from convolution layer 1, in 5x5 patch. Return 64 features weights and biases 
W_conv2 = weight_variables([5,5,32,64])
b_conv2= bias_variable([64])

#do convolution of the output of the list convolutio layer. Pool results
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

#fully conected later
W_fc1 = weight_variables([7*7*64,1024])
b_fc1 = bias_variable([1024])

#conect output of pooling layer 2  as input to full conected layer
h_pool2_flat = tf.reshape(h_pool2, [-1,7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1)+b_fc1)

#dropout some neurons to reduce  overfitting 
keep_prob = tf.placeholder(tf.float32) #get dropout probability as a training input
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

#readout layer
W_fc2 = weight_variables([1024,10])
b_fc2 = bias_variable([10])

#define model
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2

#loss measurement
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv, labels= y_))

#loss optimazer
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

#what is correct
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))

#how accurate is it
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#initialize variables
sess.run(tf.global_variables_initializer())

#train model
import time

#define number of steps and how often we display progress
num_steps = 3000
display_every = 100

#start timer 
start_time = time.time()
end_time = time.time()

for i in range(num_steps):
    batch = mnist.train.next_batch(50)
    train_step.run(feed_dict = {x:batch[0], y_:batch[1], keep_prob: 0.5})

    #periodic status display
    if i%display_every == 0:
        train_accuracy = accuracy.eval(feed_dict={x:batch[0], y_:batch[1], keep_prob:1.0})
        end_time = time.time()
        print("step {0}, elapsed time {1:.2f} seconds, training accuracy {2:.3f}%".format(i,end_time-start_time, train_accuracy*100.0))

#display sumary
#time to train
end_time = time.time()
print("total training time for {0} batches: {1:.2f} seconds".format(i+1, end_time-start_time))

#accuracy on test data
print("test accuracy {0:.3f}%".format(accuracy.eval(feed_dict={x:mnist.test.images, y_:mnist.test.labels, keep_prob:1.0})*100.0))

sess.close()
    

