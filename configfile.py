## This python file will create a config.ini to estabilsh initial parameters
from configparser import ConfigParser

config_object = ConfigParser()


config_object["DirectoryInfo"] = {
    "ESG1": r'\\data1\engineering\T&D\SWTEST\Voyant2\SmokeTests\ErrorStats_TestFolder\System3',
    "ESG2": r'\\data1\engineering\T&D\SWTEST\Voyant2\SmokeTests\ErrorStats_TestFolder\System4'
}

config_object["LogParse"] = {
    "Parse1": True,
    "Parse2": True
}

config_object["PowerCycle"] = {
    "keyword":'PWR_ON'
}

config_object["GeneratorError"] = {
    "gerkeyword": '(879)',
    "gerkeyword1": '(1020)',
    "gerkeyword2": '(361)'
}

with open('config.ini','w') as configfile:
    config_object.write(configfile)