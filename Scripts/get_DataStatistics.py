import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd
from pathlib import Path
import json, os

from IPython.display import display

def get_DataStatistics(dataset):
    outDir = git_OutDir()
    print('**Data Info**')
    print('________________________________')
    display(dataset.info())
    print('**Data Describtion**')
    print('________________________________')
    display(dataset.describe(include='all'))

    print('**Analysis Tools Frequency**')
    print('________________________________')
    get_ToolsFrequency(dataset,outDir)
    
    print('**Frequency of Samples Per Year**')
    print('_________________________________')
    get_TimestampFrequency(dataset,outDir)

    print('**Frequency of Samples Per Compiler Versions**')
    print('_______________________________________________')
    get_CompilerVersionsFrequency(dataset,outDir)
    return

def git_OutDir():
    config_file_name = 'config.json'
    
    self_dir = Path(__file__).resolve().parent
    config_file_path = self_dir / config_file_name
    self_main_dir = Path(__file__).resolve().parents[1]
    
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()

    StatisticsDir = self_main_dir/config_File['outDir']['Statistics']+'/'

    outDir = create_outDir(StatisticsDir)
    return outDir

def create_outDir(StatisticsDir):
    #Create new out dir inside StatisticsDir
    UniqueDirName = str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
    path = os.path.join(StatisticsDir, UniqueDirName)
    os.mkdir(path)

    outDir = StatisticsDir + UniqueDirName + '/'
    return outDir
     
def get_ToolsFrequency(dataset,outDir):
    print('Frequency of analysis tools in the labeled data:\n')
    ax=dataset['Analysis Tools'].value_counts().plot(kind='bar',figsize=[15,4])
    plt.title('Frequency of analysis tools in the labeled data')
    plt.xticks(rotation = 90)
    plt.grid(True, color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
    plt.grid(True, color="grey", which='minor', linestyle=':', linewidth="0.5");

    for p in ax.patches:
                if p.get_height() > 0:
                    ax.text(p.get_x()-0.1,
                    p.get_height()* 1 ,
                    '{0:.0f}'.format(p.get_height()),
                    color='black', size='large')
    plt.savefig(outDir + 'ToolsFrequency.png')
    plt.show()

def get_TimestampFrequency(dataset,outDir):
    timestamps = dataset['timeStamp']
    dates = []
    for timestamp in timestamps:
        dates.append(datetime.fromtimestamp(timestamp))
    
    years = []
    for date in dates:
        years.append(date.year)
    yearsCounte =pd.DataFrame(years)
    yearsCounte.value_counts()

    yearsCounte.value_counts().plot(kind='barh',ylabel='Year',xlabel='No of SC Samples')
    plt.title('Frequency of samples per year')
    plt.grid(True, color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
    plt.grid(True, color="grey", which='minor', linestyle=':', linewidth="0.5");
    plt.minorticks_on()
    plt.savefig(outDir + 'TimestampFrequency.png')
    plt.show()

def get_CompilerVersionsFrequency(dataset,outDir):
    dataset['CompilerVersion'] = dataset['CompilerVersion'].str.split('+').str[0]
    dataset['CompilerVersion'] = dataset['CompilerVersion'].str.split('-').str[0]
    compilerVersions= pd.DataFrame(dataset['CompilerVersion'].value_counts())
    
    display(compilerVersions)
    dataset['CompilerVersion'].value_counts().plot(kind='bar',figsize=(35,8))
    plt.title('Frequency of Samples Per Compiler Versions')
    plt.grid(True, color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
    plt.grid(True, color="grey", which='minor', linestyle=':', linewidth="0.5");
    plt.minorticks_on()
    plt.savefig(outDir + 'CompilerVersionsFrequency.png')
    plt.show()

#def get_LabelsFrequency(dataset):
     