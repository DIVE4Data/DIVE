import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd
from pathlib import Path
import json, os
from IPython.display import display
from ydata_profiling import ProfileReport

# If the final preprocessed data is stored in the default directory, pass only the file name and set defaultDir=True.
# Otherwise, pass the full path to the file and set defaultDir=False.
def get_DataStatistics(datasetName,defaultDir = True):
    try:
        outDir = git_Dir(dataType ='Statistics')
        outDir = create_outDir(outDir,(datasetName.split('_')[-1].split('.')[0])) 

        #Read dataset
        if defaultDir:
            datasetPath = git_Dir(dataType = 'Dataset')
            dataset = pd.read_csv(str(datasetPath) + '/' + datasetName)
        else:
            dataset = pd.read_csv(datasetName)

        get_datasetInfo(dataset,outDir)
        get_datasetSummary(dataset,outDir)   

        if 'Analysis Tools' in dataset.columns:
            get_ToolsFrequency(dataset,outDir)
            
        get_TimestampFrequency(dataset,outDir)
        get_CompilerVersionsFrequency(dataset,outDir)
        get_ProfileReport(dataset,outDir,datasetName.split('_')[-1].split('.')[0])

        return

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------    
def git_Dir(dataType):
    config_file_name = 'config.json'
    self_main_dir = Path(__file__).resolve().parents[1]
    config_file_path = self_main_dir / config_file_name
    
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()

    if dataType == 'Statistics':
        Dir = self_main_dir/config_File['outDir']['Statistics']
    elif dataType == 'Dataset' :
        Dir = self_main_dir/config_File['FinalDS']['PreprocessedData']
    else:
        Dir = self_main_dir
    return Dir
#----------------------------------------------------------------    
def create_outDir(StatisticsDir,datasetName):
    #Create new out dir inside StatisticsDir
    UniqueDirName = str(datetime.now().date()).replace('-', '') + '_' + str(datetime.now().time()).replace(':', '').split('.')[0]+ '_' + datasetName
    path = os.path.join(StatisticsDir, UniqueDirName)
    os.mkdir(path)

    outDir = str(StatisticsDir) + UniqueDirName + '/'
    return outDir
#----------------------------------------------------------------
def get_datasetInfo(dataset,outDir):    
    print('**Data Info**')
    print('________________________________')
    display(dataset.info())

    os.makedirs(outDir, exist_ok=True)
    datasetInfo_file_path = os.path.join(outDir, 'datasetInfo.txt')
    with open(datasetInfo_file_path, 'w') as f:
        dataset.info(buf=f)  
        f.flush()
#----------------------------------------------------------------
def get_datasetSummary(dataset,outDir):
    print('**Data Describtion**')
    print('________________________________')
    summary = dataset.describe(include='all')
    display(summary)

    os.makedirs(outDir, exist_ok=True)
    summary.to_html(outDir + 'datasetSummary.html')
#----------------------------------------------------------------       
def get_ToolsFrequency(dataset,outDir):
    print('**Analysis Tools Frequency**')
    print('________________________________')
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
    
    os.makedirs(outDir, exist_ok=True)
    plt.savefig(outDir + 'ToolsFrequency.png')
    plt.show()
#----------------------------------------------------------------    
def get_TimestampFrequency(dataset,outDir):
    print('**Frequency of Samples Per Year**')
    print('_________________________________')

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

    os.makedirs(outDir, exist_ok=True)
    plt.savefig(outDir + 'TimestampFrequency.png')
    plt.show()
#----------------------------------------------------------------    
def get_CompilerVersionsFrequency(dataset,outDir):
    print('**Frequency of Samples Per Compiler Versions**')
    print('_______________________________________________')
    dataset['CompilerVersion'] = dataset['CompilerVersion'].str.split('+').str[0]
    dataset['CompilerVersion'] = dataset['CompilerVersion'].str.split('-').str[0]
    compilerVersions= pd.DataFrame(dataset['CompilerVersion'].value_counts())
    
    display(compilerVersions)
    dataset['CompilerVersion'].value_counts().plot(kind='bar',figsize=(35,8))
    plt.title('Frequency of Samples Per Compiler Versions')
    plt.grid(True, color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
    plt.grid(True, color="grey", which='minor', linestyle=':', linewidth="0.5");
    plt.minorticks_on()

    os.makedirs(outDir, exist_ok=True)
    plt.savefig(outDir + 'CompilerVersionsFrequency.png')
    plt.show()
#----------------------------------------------------------------    
#def get_LabelsFrequency(dataset):    
    
#----------------------------------------------------------------       
def get_ProfileReport(dataset,outDir, datasetName):
    print('**Data Profiling Report**')
    print('_______________________________________________')

    try:
        os.makedirs(outDir, exist_ok=True)

        profile = ProfileReport(dataset, title = datasetName + " Profiling Report", minimal=False)

        report_path = os.path.join(outDir, 'Profiling_DetailedReport.html')
        profile.to_file(output_file=report_path)

        relative_path = os.path.relpath(report_path, start=Path.cwd().parent)
        print(f'Done! The Data Profiling Report is available at: {relative_path}')

    except Exception as e:
        print(f"Failed to generate full profile report due to: {e}")