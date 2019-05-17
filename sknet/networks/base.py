#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..ops import Op
from ..layers import Layer
import tensorflow as tf

class Network:
    def __init__(self, layers=[], name = 'model',**kwargs):
        self.name       = name
        self.layers     = layers

    def __getitem__(self,key):
        if isinstance(key,slice):
            return Network(layers=self.layers[key],name='sub'+self.name)
        return self.layers[key]

    def __len__(self):
        return len(self.layers)

    def append(self,item):
        self.layers.append(item)

    def as_list(self):
        return [layer for layer in self]

    def deter_dict(self, value):
        feed_dict = dict()
        for layer in self.layers:
            if isinstance(layer,Op) or isinstance(layer,Layer):
                for d in layer.deterministic:
                    if d is not None:
                        feed_dict[d]=value
        return feed_dict

    @property
    def shape(self):
        s = [i.get_shape().as_list() for i in self]
        return s

    @property
    def reset_variables_op(self):
        var = []
        for layer in self.layers:
            if hasattr(layer,'variables'):
                var.append(layer.reset_variables_op)
        return tf.group(*var)

    def variables(self,trainable=True):
        var = []
        for layer in self.layers:
            if hasattr(layer,'variables'):
                var+=layer.variables(trainable)
        return var

    def backward(self,tensor):
        ops = self.as_list()[::-1]
        for op in ops:
            tensor = op.backward(tensor)
        return tensor

    @property
    def updates(self):
        updates = []
        for layer in self.layers:
            if hasattr(layer,'updates'):
                updates+=layer.updates
        return updates





