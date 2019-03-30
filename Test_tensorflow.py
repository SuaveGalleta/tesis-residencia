#importar tensorflow
import tensorflow as tf
 
#definir una sesion para ejecutar tensorflow
sess = tf.Session()

#ver si podemos imprimir un string

hello = tf.constant("Hola mundo estoy usando tensorflow")
print(sess.run(hello))

#realizar una operación simple de matematicas
a = tf.constant(20)
b = tf.constant(22)

print('a + b = {0}'.format(sess.run(a+b)))