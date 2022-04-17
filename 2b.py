import numpy as np
import pandas as pd
#import tensorflow as tf
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


def create_feature_matrix(x, nb_f):
    tmp_features = []
    for deg in range(1, nb_f + 1):
        tmp_features.append(np.power(x, deg))
    return np.column_stack(tmp_features)


# Korak 1: Učitavanje i obrada podataka.
filename = './2a.xls'
all_data = pd.read_csv(filename, sep="\t", skiprows=1, usecols=[1, 2, 3, 6], encoding="utf-8")
all_data = all_data.to_numpy()
data = dict()
data['x'] = all_data[:, :3]
data['y'] = all_data[:, 3]

# print(len(data['x']), len(data['y']))
# print(data['x'][:5])
# print(data['y'][:5])

# Nasumično mešanje.
nb_samples = data['x'].shape[0]
indices = np.random.permutation(nb_samples)
data['x'] = data['x'][indices]
data['y'] = data['y'][indices]

# Normalizacija (obratiti pažnju na axis=0).
data['x'] = (data['x'] - np.mean(data['x'], axis=0)) / np.std(data['x'], axis=0)
data['y'] = (data['y'] - np.mean(data['y'])) / np.std(data['y'])

print('Originalne vrednosti (prve 3):')
print(data['x'][:3])
print('Feature matrica (prva 3 reda):')
nb_features = 3
nb_cols = 3
data['x'] = create_feature_matrix(data['x'], nb_features)
print(data['x'][:3, :])


# Korak 2: Model.
# Primetiti 'None' u atributu shape placeholdera i -1 u 'tf.reshape'.
X = tf.placeholder(shape=(None, nb_features * nb_cols), dtype=tf.float32)
Y = tf.placeholder(shape=(None), dtype=tf.float32)
w = tf.Variable(tf.zeros(nb_features * nb_cols))
bias = tf.Variable(0.0)

w_col = tf.reshape(w, (nb_features * nb_cols, 1))
hyp = tf.add(tf.matmul(X, w_col), bias)

# Korak 3: Funkcija troška i optimizacija.
Y_col = tf.reshape(Y, (-1, 1))

# Regularizacija
lmbd = 0.01
l2_reg = lmbd * tf.reduce_mean(tf.square(w))

mse = tf.reduce_mean(tf.square(hyp - Y_col))
loss = tf.add(mse, l2_reg)

# Prelazimo na AdamOptimizer jer se prost GradientDescent lose snalazi sa
# slozenijim funkcijama.
opt_op = tf.train.AdamOptimizer().minimize(loss)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    # Izvršavamo 100 epoha treninga.
    nb_epochs = 1000
    for epoch in range(nb_epochs):

        # Stochastic Gradient Descent.
        epoch_loss = 0
        for sample in range(nb_samples):
            feed = {X: data['x'][sample].reshape((1, nb_features * nb_cols)), Y: data['y'][sample]}
            _, curr_loss = sess.run([opt_op, loss], feed_dict=feed)
            epoch_loss += curr_loss

        # U svakoj desetoj epohi ispisujemo prosečan loss.
        epoch_loss /= nb_samples
        if (epoch + 1) % 100 == 0:
            print('Epoch: {}/{}| Avg loss: {:.5f}'.format(epoch + 1, nb_epochs, epoch_loss))

    # Ispisujemo i plotujemo finalnu vrednost parametara.
    w_val = sess.run(w)
    bias_val = sess.run(bias)
    print('w = ', w_val, 'bias = ', bias_val)

