## Data Analysis Script
# Version 1.4
# Jeffrey Nguyen
# Purpose: will decrypt all output logs and compile all data into one file. Will also extract key points including
# Power cycles, WDTs, Generator errors, and power on times exceeding a certain parameter - includes multiple file analysis and
# multiple generator error counts
# New features include user-based condition log parsing -- minor change to allow for one statement of True/False

import os
import pandas as pd
import glob
import csv
import subprocess
from configparser import ConfigParser

##---------------------------------------
#Read config file
config_object = ConfigParser()
config_object.read("config.ini")
# Directory = config_object["DirectoryInfo"]
PowerCycle = config_object["PowerCycle"]

# for key in config_object.sections():
#     for (eachkey,eachval) in config_object.items(key):
#         print(eachval)
LogValue = [];
for (user,value) in config_object.items("LogParse"):
    LogValue.append(value)

# print(LogValue[0])
# print(LogValue[1])
posctr = 0;



## This will include method to loop through multiple ESGs to automate data retrieval and analysis -- input directories in config.ini
for (key,val) in config_object.items("DirectoryInfo"):
    try:
        Userchange = val # uses input(s) from config file
        # print(Userchange)
        # newdir = os.chdir(Userchange)

        newdir = os.chdir(Userchange)
        f = os.listdir(newdir)
        listdir = os.getcwd()
        # print(listdir)
        # print(f)
        extsyl = ('/**/*.syl')  # will recursively help to look into all directories + subdirectories for .syl
        extcsv = ('/**/*.csv')  # will recursively help to look into all directories + subdirectories for .csv
        truePathSyl = Userchange + extsyl
        truePathCsv = Userchange + extcsv
        ## -----------------------------------------------------
        ## Method to decrypt logs -- loops through all .syl files in directory and processes within the LogParser .exe

        files = glob.glob(truePathSyl, recursive=True)
        if LogValue[0] == "True":
            print("Will Parse")
            for file in files:
                subprocess.run(["LogParser.exe", file])


        ## -----------------------------------------------------------------
        # Data analysis method 2 -- will do individual counts through loops/conditions -- will integrate within a config file
        # This method is more individualized to a specific key word and will only print out specific values rather than all values
        if os.path.exists('ErrorstatsCounter.txt'):
            os.remove('ErrorstatsCounter.txt')


        collectfiles = glob.glob(truePathCsv, recursive=True)
        # print(collectfiles) #prints out csv files being analyzed
        # def merger(listfiles,outputfiles):
        #     result_file = pd.concat([pd.read_csv(file) for file in listfiles])
        #     result_file.to_csv(outputfiles, index = False, encoding ="utf-8")

        df = []
        for filename in collectfiles:  # will go through the collected .csv in the folder
            try:

                with open(filename, newline='') as csvfile:
                    reader = pd.read_csv(csvfile, header=None, skiprows=[0, 1], dtype={'uid': str}, usecols=range(0,
                                                                                                                  8))  # skips rows that give error when reading, does not read any columns not needed
                    # print(reader.head())
                    df.append(reader)
            except:
                print('Invalid CSV being analyzed: %s'%filename)
                pass
        frame = pd.concat(df)
        frame.columns = ['Time Stamp', 'RECORD ID', 'BLOCK SIZE', 'VERSION', 'BACKED UP', 'EVENT MOD', 'EVENT ID',
                         'EVENT TEXT']
        # print(frame.columns)
        print(key.upper())
        dfid = frame['EVENT ID']

        dfid = [key.strip() for key in dfid]  # removes spaces that makes conditional statements for comparison give errors

        # print(dftext)
        # print(df)
        keyword = PowerCycle["keyword"]  ## NOTE: this can be what changes in config file depending on what user wants to find

        ctr = 0  # initialize counter

        ##PowerCycle Counter loop
        for count in range(len(dfid)):
            if dfid[count] == keyword.upper():  # conditional matching of keyword
                ctr += 1

        print(keyword.upper(), ctr)
        # with open("Output.txt",w) as output_file:
        #     output_file.write(keyword,ctr);
        with open("ErrorstatsCounter.txt", "a") as obj:
            obj.write("The total power count is %d.\n" % ctr)
        ## This loop will look for the different generator errors based on user request (WDT is classified as 879)
        dftext = frame['EVENT TEXT']
        dftext = [keys.strip() for keys in dftext]
        for (k,v) in config_object.items("GeneratorError"):
            gerkeyword = v  # This can be manipulated through config file
            # print(len(gerkeyword))
            gerctr = 0  # establishes generator error counter and initializes

            ##GeneratorError Counter Loop
            for counts in range(len(dftext)):
                ct = 0  # initializes the midway counter for character comparison everytime it pulls a new word
                num = dftext[counts]  # takes one string from the main dataframe
                newnum = num[
                         0:6]  # takes specifically the first 7 characters (including parantheses) which will match the generator error numbers

                # print(newnum)
                # if (newnum == gerkeyword) or (newnums == gerkeyword):
                for l in range(len(
                        gerkeyword)):  # uses the comparison from the length of the input generator error user wants to count
                    if newnum[l] == gerkeyword[l]:  # will compare each character starting from l=0 of the string
                        # print(newnum[l])
                        ct += 1  # character counter
                    # gerctr +=1
                # print(ct)
                if ct >= 5:  # estabilshes the basis of the comparison to have a length greater than 5 (generator errors usually (879), (808), (1020)
                    gerctr += 1
            print(gerkeyword, gerctr)
            with open("ErrorstatsCounter.txt", "a") as obj:
                obj.write("The total amount of generator error %s is %d.\n" % (gerkeyword, gerctr))
    except:
        pass
    posctr += 1;
    # print(posctr)

    ##---------------------------------------------------
