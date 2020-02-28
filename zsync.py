import os
import sys
import logging
import shutil
from pathlib import Path

#Create and configure logger 
logging.basicConfig(filename="/home/abhishek/cron_jobs/zsyncfiles.log", 
                    format='%(asctime)s - %(message)s', 
                    filemode='a')
#Creating an object 
logger=logging.getLogger()
#Setting the threshold of logger to DEBUG 
logger.setLevel(logging.INFO)

def printlog(msg):
	print(msg)
	logger.info(msg)

def say(cmd):
	os.system(f"say '{cmd}'")

def getAllFiles(path, avoid_pattern='_stoneit'):
    files = []
    abs_files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if avoid_pattern in os.path.basename(file): 
                printlog(f"avoided {os.path.basename(file)}")
                continue
            abs_files.append(os.path.join(r.replace(path, ''), file))
            files.append(os.path.join(r, file))
    return sorted(files), sorted(abs_files)

def diffAB(pathA, pathB, avoid_pattern='_stoneit'):
    filesA, abs_filesA = getAllFiles(pathA, avoid_pattern)
    filesB, abs_filesB = getAllFiles(pathB, avoid_pattern)
    abs_only_in_A = set(abs_filesA)-set(abs_filesB)
    abs_only_in_B = set(abs_filesB)-set(abs_filesA)
    only_in_A = [os.path.join(pathA, a) for a in abs_only_in_A]
    only_in_B = [os.path.join(pathB, b) for b in abs_only_in_B]
    return_dict = {'filesA':filesA,
                 'filesB':filesB,
                 'abs_filesA':abs_filesA,
                 'abs_filesB':abs_filesB,
                 "only_in_A": only_in_A,
                 "only_in_B": only_in_B,
                 "pathA":pathA,
                 "pathB":pathB}
    return return_dict

def DiffSync(files, method='AB'):
    if method=='AB':
        for f in files['only_in_A']:
            f_new = f.replace(pathA, pathB)
            os.makedirs(os.path.dirname(f_new), exist_ok=True)
            cmd = f"cp '{f}' '{f_new}'"
            print_cmd =  f"copying '{f}' to '{f_new}'"
            printlog(print_cmd)
            os.system(cmd)
        return None
    if method=='BA':
        for f in files['only_in_B']:
            f_new = f.replace(pathB, pathA)
            os.makedirs(os.path.dirname(f_new), exist_ok=True)
            cmd = f"cp '{f}' '{f_new}'"
            printlog(cmd)
            os.system(cmd)
        return None
    if method=='BOTH':
        DiffSync(files, method='AB')
        DiffSync(files, method='BA')
        return None


if __name__=="__main__":
	pathA = '/home/abhishek/abhi/SSD250/'
	pathB = '/H512/BACKUPFORREPROCESS/abhi/SSD250/'
	files = diffAB(pathA, pathB, avoid_pattern='_stoneit')
	DiffSync(files, 'BOTH')
	printlog(f"Done syncing {pathA} and {pathB}")
	say("Done syncing the master.")