from parselmouth.praat import call, run_file
import glob
import pandas as pd
import numpy as np
import scipy
from scipy.stats import binom
from scipy.stats import ks_2samp
from scipy.stats import ttest_ind
import os

def myspsr(m, p):
    sound = p + "/" + m + ".wav"
    sourcerun = p + "/myspsolution.praat"
    path = p + "/"
    try:
        objects = run_file(sourcerun, -20, 2, 0.3, "yes", sound, path, 80, 400, 0.01, capture_output=True)
        z1 = str(objects[1])
        z2 = z1.strip().split()
        z3 = float(z2[2])
        z4 = float(z2[3])
        rate_of_speech = z3
        print("rate_of_speech=", z3, "# syllables/sec original duration")
    except Exception as e:
        print("Error:", e)
        rate_of_speech = None
    return rate_of_speech

def mysppron(m,p):
    sound=p+"/"+m+".wav"
    sourcerun=p+"/myspsolution.praat"
    path=p+"/"
    try:
        objects= run_file(sourcerun, -20, 2, 0.3, "yes",sound,path, 80, 400, 0.01, capture_output=True)
        print (objects[0]) 
        z1=str( objects[1]) 
        z2=z1.strip().split()
        z3=int(z2[13]) 
        z4=float(z2[14]) 
        db= binom.rvs(n=10,p=z4,size=10000)
        a=np.array(db)
        b=np.mean(a)*100/10
        pronunciation_score_percentage = b
    except Exception as e:
        print("Error:", e)
        return None

    return pronunciation_score_percentage


