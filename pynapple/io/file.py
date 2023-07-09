#!/usr/bin/env python

# -*- coding: utf-8 -*-
# @Author: Guillaume Viejo
# @Date:   2023-07-05 16:03:25
# @Last Modified by:   Guillaume Viejo
# @Last Modified time: 2023-07-09 17:44:41

import os

import numpy as np

from .. import core as nap

class NPZFile(object):
    """

    """

    def __init__(self, path):
        """Summary

        Parameters
        ----------
        path : str
            Valid path to a NPZ file
        """
        self.path = path
        self.name = os.path.basename(path)
        self.file = np.load(self.path, allow_pickle=True)        
        self.type = ""

        # First check if type is explicitely defined
        possible = ["Ts", "Tsd", "TsdFrame", "TsGroup", "IntervalSet"]
        if "type" in self.file.keys():
            if isinstance(self.file["type"], "str"):
                if self.file["type"] in possible:
                    self.type = self.file

        # Second check manually 
        if self.type == "":
            k = set(self.file.keys())
            if {'t', 'd', 'start', 'end', 'index'}.issubset(k):
                self.type = "TsGroup"
            elif {'t', 'd', 'start', 'end', "columns"}.issubset(k):
                self.type = "TsdFrame"
            elif {'t', 'd', 'start', 'end'}.issubset(k):
                self.type = "Tsd"
            elif {'t', 'start', 'end'}.issubset(k):
                self.type = "Ts"
            elif {'start', 'end'}.issubset(k):
                self.type = "IntervalSet"
            else:
                self.type = "npz"

    def load(self):
        if self.type == "npz":
            return self.file
        else:
            time_support = nap.IntervalSet(self.file["start"], self.file["end"])
            if self.type == "TsGroup":
                tsd = nap.Tsd(
                    t=self.file["t"], d=self.file["index"], time_support=time_support
                )
                tsgroup = tsd.to_tsgroup()
                tsgroup.set_info(group=self.file["group"], location=self.file["location"])
                return tsgroup

            elif self.type == "TsdFrame":
                return nap.TsdFrame(
                    t=self.file["t"],
                    d=self.file["d"],
                    time_support=time_support,
                    columns=self.file["columns"],
                )

            elif self.type == "Tsd":
                return nap.Tsd(
                    t=self.file["t"], d=self.file["d"], time_support=time_support
                )
            elif self.type == "Ts":
                return nap.Ts(t=self.file["t"], time_support=time_support)
            elif self.type == "IntervalSet":
                return time_support
            else:
                return self.file


class NWBFile(object):
    def __init__(self, path):
        """Summary

        Parameters
        ----------
        path : str
            Valid path to a NWB file
        """
        self.path = path
        self.name = os.path.basename(path)

    def load(self):
        print("yo")