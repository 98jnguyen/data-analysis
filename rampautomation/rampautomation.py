## Ramp Automation Analysis Script
## Created by: Jeffrey Nguyen
## Version 1.0
## Purpose: Will be run to analyze the script logs for different activations of Voyant scripts. Will analyze ramp duration
## DAC steps, and compare to expected values. Additional purposes will also analyze a defect script to see if it exceeds
## it's defined timeout value of 60ms.

import os
import pandas as pd
import glob
import csv
import subprocess
from configparser import ConfigParser
import numpy
from collections import Counter

#change the folder path depending on which MFG folder to analyze
folderpath = r"C:\Users\jn16902\Desktop\RampTestFolder\Newfolder"

#change to current directory established above
newdirectory = os.chdir(folderpath)
f = os.listdir(newdirectory)
listdir = os.getcwd()

extslg = ('/**/*.SLG')
extcsv = ('/**/*.csv')
truePathSLG = folderpath + extslg
truePathCSV = folderpath + extcsv
filesrecursive = glob.glob(truePathSLG, recursive=True) #gathers all .slg files into one area

for file in filesrecursive:
     subprocess.run(["LogParser.exe",file])

collectedfiles = glob.glob(truePathCSV, recursive=True) #gathers all .csv files into one area
# print(collectedfiles)

for filename in collectedfiles:
    x =[]; #initialize all variables/dataframes every new file being looked at
    x = filename
    frame = [];
    dataframe = [];
    dataframe2 = [];
    dfid = [];
    dftime = [];
    dfstate = [];
    print(x)
    try:
        with open(x, newline ='') as csvfile:
            reader = pd.read_csv(csvfile, header = None,dtype={'uid': str}, skiprows = 113, usecols=range(0,6))
            dataframe.append(reader) #opens up .csv file and stores contents into a dataframe
            print(f'Filename {x} being analyzed.')

            frame = pd.concat(dataframe)
            frame.fillna("")
            frame.columns = ['ROW #', 'ELAPSED TIME', 'STATE', 'DESCRIPTION', 'DATA 1', 'DATA2']

            dfid = frame['DESCRIPTION'].tolist() #method to grab specific columns

            dfid1 = frame['DESCRIPTION']
            dftime = frame['ELAPSED TIME'].tolist()
            dfstate = frame['STATE'].tolist()
            dfitem1 = frame['DATA 1']
            countdfstate = len(set(dfstate))
            items = len(Counter(dfstate).keys()) - 2;
            print(items)

            # print(dfstate)
            # print(countdfstate)
            # dfid = [key.strip() for key in dfid]
            keywordstart = "Run Timeout" #keywords that will be used to find ramp related contents
            keywordend = "Triggered Event"
            rampstep = "Ramp Voltage Ramp Duration"
            # print(dftime)
            start = 0; #initialize counts
            end = 0;
            startstate = 0;
            rampstepcount = 0;
            counter = 0;
            filecounter = [];
            rampcounter = 0;
            count = 0;
            # print(len(dfid))

            if items > 7: #if user states exceeds 7, this classifies it as the defect script
                with open("Defectoutput.txt", "a") as output1: #begins text file to log defectoutput script runs
                    output1.write("Defect script analysis\n")
                    output1.write(filename + "\n")
                    for count1 in range(len(dfid)):
                        # print(x)
                        # print(newdfid[count])
                        # print(type(dfid))

                        if dfid[count1] == keywordstart: #matches keyword for Run Timeout
                            start1 = int(dftime[count1]); #logs the time when the keyword is noted in script log
                            startstate1 = int(dfstate[count1]); #logs the state when the keyword is hit

                            # print(type(start))
                            output1.write(f"This is {start1} start\n") #displays the starting time
                        if dfid[count1] == keywordend:
                            end1 = int(dftime[count1]); #end time for when the keyword Triggered Event is hit

                            # print(type(end))
                            output1.write(f"This is {end1} end\n")
                            if int(end1) > int(start1):
                                result1 = numpy.subtract(end1, start1) #if the start and end time are correct, find the elapsed duration
                                output1.write(f"In state {startstate1}, the elasped timeout is {result1}.\n")
                                items = 0;

                    # output1.write(str(counter))
                    # output1.write(str(filecounter))

            else: # for any user state under 7, this classifies for any of the ramping scripts
                with open("Rampingtest.txt", "a") as output:
                    output.write("Ramping Test Script\n")
                    output.write(filename + "\n")
                    for count in range(len(dfid)):
                        # print(x)
                        # print(newdfid[count])
                        # print(type(dfid))

                        if dfid[count] == keywordstart:
                            start = int(dftime[count]);
                            startstate = int(dfstate[count]);

                            # print(type(start))
                            output.write(f"This is {start} start\n")
                        if dfid[count] == keywordend:
                            end = int(dftime[count]);

                            # print(type(end))
                            output.write(f"This is {end} end\n")
                            if int(end) > int(start):
                                result = numpy.subtract(end, start)
                                output.write(f"In state {startstate}, the ramp duration is {result}.\n")
                                items = 0;

                        if dfid[count] == rampstep:
                            rampstepcount = dfitem1[count]
                    output.write(rampstepcount + "\n")


    except:
        print(f'Invalid CSV {filename} being analyzed.')
        pass

# print(count)
#     print(f"Number of times timeout exceeded was {counter}.")
#     print(filecounter)