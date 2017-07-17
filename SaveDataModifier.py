#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: Beeven Yip
# Created on 2015-6-26

import hashlib
import base64
import argparse
import os.path
import io
import struct
import xml.etree.ElementTree as ET

class Modifier(object):

    def __init__(self, byte_order, data, properties):
        """ byte_order: '>' big_endian for Android
                        '<' little_endian for iOS
        """
        self._data = bytearray(data)
        self._byte_order = byte_order
        self._known_properties = properties



    def __getattr__(self, name):
        if self._known_properties.has_key(name):
            v = self._known_properties[name]
            d = struct.unpack_from(self._byte_order+v[0],self._data,v[1])
            if len(d) > 1:
                return d
            else:
                return d[0]
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if self.__dict__.has_key("_known_properties") and self.__dict__["_known_properties"].has_key(name):
            v = self._known_properties[name]
            struct.pack_into(self._byte_order+v[0], self._data, v[1], value)
        else:
            super(Modifier,self).__setattr__(name, value)


    @property
    def signature(self):
        return self._data[-32:]

    @signature.setter
    def signature(self, value):
        self._data[-32:] = value

    @property
    def computed_hash(self):
        return hashlib.md5("battlecatskr"+self._data[:-32]).hexdigest()

    @property
    def known_properties(self):
        return dict( (k,self.__getattr__(k)) for k in self._known_properties.keys())

    def save_to_file(self, filename):
        self.signature = self.computed_hash
        pass

    def extract_data(self, filename):
        with open(filename, "wb") as f:
            f.write(self._data)

    def replace_data(self, filename):
        with open(filename, "rb") as f:
            self._data = bytearray(f.read())

    def modify(self, dt, pos, val):
        struct.pack_into(self._byte_order + dt, self._data, pos, val)



class iOS(Modifier):
    def __init__(self, filename=None):
        if filename is None:
            filename = "SAVE_DATA"
        with open(filename, "rb") as f:
            data = bytearray(f.read())

        properties = {
            "cat_food": ("L",7),
            "xp": ("L",75),
            "rare_ticket": ("L",8374),
            "ticket": ("L",8370),
            "tracking_id": ("9s", 104154),
            "medal":("192L",2504)
        }
        Modifier.__init__(self, "<", data, properties)

    def save_to_file(self, filename):
        Modifier.save_to_file(self, filename)
        with open(filename, "wb") as f:
            f.write(self._data)

class Android(Modifier):
    def __init__(self, filename=None):
        if filename is None:
            filename = "save.xml"
        self._xmltree = ET.parse(filename)
        data = base64.b64decode(self._xmltree.getroot().find("./string[@name='SAVE_DATA']").text)
        properties = {
            "cat_food": ("L",7),
            "xp": ("L",75),
            "rare_ticket": ("L",8368),
            "ticket": ("L",8364),
            "tracking_id": ("9s", 104154)
        }

        Modifier.__init__(self, ">",data, properties)

    def save_to_file(self, filename):
        Modifier.save_to_file(self, filename)
        node = self._xmltree.getroot().find("./string[@name='SAVE_DATA']")
        node.text = base64.b64encode(self._data)
        self._xmltree.write(filename)

