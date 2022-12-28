#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Projecte : PyCharm
# @Date     : 2022-12-07 10:35
# @Author   : paperclub
# @Desc     : paperclub@163.com


####################################################################
#
#     1. TensorFlow 1.x h5模型转 pb 模型 及调用（tf1.5,tf1.3 已测试）
#     2. TensorFlow 2.1 h5模型转 pb 模型 及调用
#
####################################################################


#  tf1.x  h5转 pb model


import keras
import os,sys
import numpy as np
import tensorflow as tf
from keras.models import load_model
from keras import backend as K
from tensorflow.python.framework import graph_io
import os.path as osp
from tensorflow.python.framework.graph_util import convert_variables_to_constants


def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
	graph = session.graph
	with graph.as_default():
		freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
		output_names = output_names or []
		output_names += [v.op.name for v in tf.global_variables()]
		input_graph_def = graph.as_graph_def()
		if clear_devices:
			for node in input_graph_def.node:
				node.device = ""
		frozen_graph = convert_variables_to_constants(session, input_graph_def, output_names, freeze_var_names)
		return frozen_graph

#  h5转pb
def h5_to_tf_model(modelfile, out_dir, pb_model):
	net_model = load_model(modelfile)
	print('input :', net_model.input.name)
	print('output :', net_model.output.name)
	sess = K.get_session()
	frozen_graph = freeze_session(sess, output_names=[net_model.output.op.name])
	graph_io.write_graph(frozen_graph,out_dir, pb_model, as_text=False)
	print('结果保存: ',osp.join(out_dir,pb_model))
	print(K.get_uid())

# 调用模型
def load_pb(pd_path, img_input):

	with tf.Graph().as_default():
		output_graph_def = tf.GraphDef()
		with open(pd_path, "rb") as f:
			output_graph_def.ParseFromString(f.read())
			tensors = tf.import_graph_def(output_graph_def, name="")

		with tf.Session() as sess:
			init = tf.global_variables_initializer()
			sess.run(init)
			sess.graph.get_operations()
			feed_input = sess.graph.get_tensor_by_name("input_1:0")
			pd_model = sess.graph.get_tensor_by_name("dense_3/Softmax:0")
			# 这一步不要想的太复杂
			scores = sess.run(pd_model, feed_dict={feed_input: img_input})
			indx = np.argmax(scores[0])
			score = scores[0][indx]
			categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

			print(indx, categories[indx], score)

h5_path = r'./saved_model.h5'
pb_path = "saved_model.pb"
out_dir = './'
dim = 299
img_path = "./1.png"
image = keras.preprocessing.image.load_img(img_path, target_size=(dim, dim))
image = keras.preprocessing.image.img_to_array(image)
image /= 255
img_input = np.asarray([image]) # 维度需要一致
load_pb(pb_path, img_input)




###############  tf2:

import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2

def h5_to_tf2_model():
    #  有兼容性问题，只能tf2.1.0
    # 参考： https://stackoverflow.com/questions/63690901/how-to-convert-model-from-hdf5-format-to-pb
    ## https://stackoverflow.com/questions/56646940/how-to-properly-saving-loaded-h5-model-to-pb-with-tf2

    h5_path = 'mobilenet_v2_140_224.1/mobilenet_v2_140_224/saved_model.h5'
    model = tf.keras.models.load_model(h5_path, custom_objects={'KerasLayer':hub.KerasLayer})

    # full_model = tf.function(lambda x: model(x))
    # full_model = full_model.get_concrete_function(
    #     x=tf.TensorSpec(model.inputs[0].shape,model.inputs[0].dtype))

    # x可以修改为 =>>>>>>  keras_layer_input
    full_model = tf.function(lambda keras_layer_input: model(keras_layer_input))
    full_model = full_model.get_concrete_function(
        keras_layer_input=tf.TensorSpec(model.inputs[0].shape, model.inputs[0].dtype))


    # Get frozen ConcreteFunction
    frozen_func = convert_variables_to_constants_v2(full_model)
    frozen_func.graph.as_graph_def()

    layers = [op.name for op in frozen_func.graph.get_operations()]

    print("-" * 50)
    print("Frozen model layers: ")
    for layer in layers:
        print(layer)

    print("-" * 50)
    print("Frozen model inputs: ")
    print(frozen_func.inputs)
    print("Frozen model outputs: ")
    print(frozen_func.outputs)

    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir="./frozen_models2",
                      name="simple_frozen_graph.pb",
                      as_text=False)


# 预测
def load_tf2_model(pb_model_file):
    """ 重构，防止多次重载模型 """

    graph = tf.Graph()
    with graph.as_default():
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(open(pb_model_file, 'rb').read())
        tensors = tf.import_graph_def(graph_def, name="")

    session = tf.Session(graph=graph)
    with session.as_default():
        with graph.as_default():
            init = tf.global_variables_initializer()
            session.run(init)
            session.graph.get_operations()

    return session


h5_to_tf2_model()
pb_model_file = './frozen_models2/simple_frozen_graph.pb'
tf_session = load_tf2_model(pb_model_file)
feed_input = tf_session.graph.get_tensor_by_name("keras_layer_input:0")
feches = tf_session.graph.get_tensor_by_name("Identity:0")
scores = tf_session.run(feches, feed_dict={feed_input: img_input})

print("scores: ", scores)
scores = scores[0].tolist()
indx = np.argmax(scores)
categories = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']
print(indx, categories[indx], scores[indx])