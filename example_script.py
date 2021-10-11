# -*- coding: utf-8 -*-

from synchCams.synchCams import synchCams
if __name__ == "__main__":
    exp = synchCams([0,1])
    exp.start_experiment()
    exp.releaseCams()