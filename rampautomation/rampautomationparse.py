## Automation Parser
## Created by: Jeffrey N
## Version 1.0
## Purpose: will automatically look into folder and subfolders of specified path to decrypt certain logs. Depending on the type of file
## that the user wants to parse, they can change the extension to match the file they want. This specific script analyzes .SLG files
## and decrypts all .SLG files (script logs) within the specified path.

import os
import pandas as pd
import glob
import csv
import subprocess
from configparser import ConfigParser
import numpy
from collections import Counter

#defined folder path user can input
folderpath = r"\\data1\Engineering\T&D\SWTEST\Voyant2\RampTime\DryRun\RampAutomation_2.1H_SYSH_03\Output\ESG3422-good-PASS\Ramp_9000ms_NoSuppression\Wknd_9000ms_run_SD_card\System\Mfg_Data\2021\05\13"

newdirectory = os.chdir(folderpath)
f = os.listdir(newdirectory)
listdir = os.getcwd()

extslg = ('/**/*.SLG')
extcsv = ('/**/*.csv')
truePathSLG = folderpath + extslg
truePathCSV = folderpath + extcsv
filesrecursive = glob.glob(truePathSLG, recursive=True)

#will track all .SLG files in a folder directory and run the logparser.exe on them
for file in filesrecursive:
     subprocess.run(["LogParser.exe",file])
