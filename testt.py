## Ramp Automation Analysis Script
## Created by: Jeffrey Nguyen
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

folderpath = r"\\data1\engineering\T&D\SWTEST\Voyant2\RampTime\DryRun\RampAutomation_2.1H_SYSH_03\Output\ESG6152\SD_card\System\Mfg_Data\2021\05\07"

newdirectory = os.chdir(folderpath)
f = os.listdir(newdirectory)
listdir = os.getcwd()

extslg = ('/**/*.SLG')
extcsv = ('/**/*.csv')
truePathSLG = folderpath + extslg
truePathCSV = folderpath + extcsv
filesrecursive = glob.glob(truePathSLG, recursive=True)

for file in filesrecursive:
     subprocess.run(["LogParser.exe",file])

collectedfiles = glob.glob(truePathCSV, recursive=True)
# print(collectedfiles)

for filename in collectedfiles:
    x =[];
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
            dataframe.append(reader)
            print(f'Filename {x} being analyzed.')

            frame = pd.concat(dataframe)
            frame.fillna("")
            frame.columns = ['ROW #', 'ELAPSED TIME', 'STATE', 'DESCRIPTION', 'DATA 1', 'DATA2']

            dfid = frame['DESCRIPTION'].tolist()

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
            keywordstart = "Run Timeout"
            keywordend = "Triggered Event"
            rampstep = "Ramp Voltage Ramp Duration"
            # print(dftime)
            start = 0;
            end = 0;
            startstate = 0;
            rampstepcount = 0;
            counter = 0;
            filecounter = [];
            rampcounter = 0;
            count = 0;
            # print(len(dfid))

            if items > 7:
                with open("Defectoutput.txt", "a") as output1:
                    output1.write("Defect script analysis\n")
                    output1.write(filename + "\n")
                    for count1 in range(len(dfid)):
                        # print(x)
                        # print(newdfid[count])
                        # print(type(dfid))

                        if dfid[count1] == keywordstart:
                            start1 = int(dftime[count1]);
                            startstate1 = int(dfstate[count1]);

                            # print(type(start))
                            output1.write(f"This is {start1} start\n")
                        if dfid[count1] == keywordend:
                            end1 = int(dftime[count1]);

                            # print(type(end))
                            output1.write(f"This is {end1} end\n")
                            if int(end1) > int(start1):
                                result1 = numpy.subtract(end1, start1)
                                output1.write(f"In state {startstate1}, the elasped timeout is {result1}.\n")
                                items = 0;
                    # for count in range(len(dfid)):
                    #     try:
                    #         # print(newdfid[count])
                    #         if dfid[count] == keywordstart:
                    #             start = dftime[count];
                    #             startstate = int(dfstate[count]);
                    #             start = int(start)
                    #             # print(type(start))
                    #             output.write(f"This is {start} start\n")
                    #         if dfid[count] == keywordend:
                    #             end = dftime[count];
                    #             end = int(end)
                    #             # print(type(end))
                    #             output.write(f"This is {end} end\n")
                    #         if end > start:
                    #             result = numpy.subtract(end, start)
                    #             output.write(f"In state {startstate}, the elapsed timeout is {result}.\n")
                    #         if startstate == 6:
                    #             if result > 65 or result < 59:
                    #                 counter += 1;
                    #                 filecounter.append(filename)
                    #     except:
                    #         pass
                    # output1.write(str(counter))
                    # output1.write(str(filecounter))

            else:
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
    # try:
    #     with open(filename, newline='') as file2:
    #         reader2 = pd.read_csv(file2, header=None, dtype={'uid': str}, skip_blank_lines=True, nrows=76)
    #         dataframe2.append(reader2)
    # except:
    #     print(f'Invalid CSV {filename} being analyzed.')


# print(count)
#     print(f"Number of times timeout exceeded was {counter}.")
#     print(filecounter)