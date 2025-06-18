import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pandas as pd
import numpy as np
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
            datasetPath = os.path.dirname(datasetName)
            datasetName = os.path.basename(datasetName)
            dataset = pd.read_csv(os.path.join(datasetPath, datasetName))
        
        # Derive CategoricalColsMappings.json file path from dataset name
        parts = datasetName.replace('.csv', '').split('_')
        categories_path = os.path.join(datasetPath, f'{parts[0]}_CategoricalColsMappings_{"_".join(parts[-2:])}.json')

        get_datasetInfo(dataset,outDir)
        get_datasetSummary(dataset,outDir)   

        if 'Analysis Tools' in dataset.columns:
            get_ToolsFrequency(dataset,outDir)
            
        get_TimestampFrequency(dataset,outDir)
        get_CompilerVersionsFrequency(dataset,outDir,categories_path)
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

    outDir = str(StatisticsDir) + '/' + UniqueDirName + '/'
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

    df = pd.DataFrame(dataset['timeStamp'], columns=['timeStamp'])
    # Convert 'timeStamp' to numeric to ensure valid UNIX timestamps
    df['timeStamp'] = pd.to_numeric(df['timeStamp'], errors='coerce')
    # Convert numeric timestamps to datetime
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s', errors='coerce')
    # Extract the year from the datetime column
    df['Year'] = df['timeStamp'].dt.year
    # Count the occurrences of each year
    year_counts = df['Year'].value_counts().sort_index()

    # Create the bar chart
    fig = plt.figure(figsize=(8, 4))
    plt.bar(year_counts.index, year_counts.values, color='skyblue', edgecolor='black', width=0.6, label="Counts")
    # Add the line plot for the total count (cumulative sum)
    cumulative_sum = np.cumsum(year_counts.values)
    plt.plot(year_counts.index, cumulative_sum, color='blue', marker='o', label="Cumulative Total",linewidth=1,linestyle='-')

    # Add labels for the cumulative total above the line
    for i, total in enumerate(cumulative_sum):
        plt.text(year_counts.index[i], total + 190, str(total), ha='center', fontsize=8, color='maroon')

    plt.xlabel('Year',fontsize=10)
    plt.ylabel('No of Samples',fontsize=10)
    plt.title('Distribution of DIVE Samples per Year',fontsize=10) 
    plt.xticks(year_counts.index,fontsize = 8)
    plt.yticks(fontsize=8)

    plt.grid(axis='y', color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
    plt.grid(axis='y', color="grey", which='minor', linestyle=':', linewidth="0.5");
    #plt.grid(axis='y', color = "grey",  which='major', linestyle=':', linewidth = "0.5")
    plt.legend(fontsize=8)

    # Display the chart
    plt.tight_layout()
    plt.show()

    fig.savefig(outDir + "Distribution_of_DIVE_Samples_per_Year.pdf", format="pdf", dpi=300)
#----------------------------------------------------------------    
def get_CompilerVersionsFrequency(dataset,outDir,categories_path):
    print('**Frequency of Samples Per Compiler Versions**')
    print('_______________________________________________')

    # Conditionally map integers back to string versions
    #--------------------------------
    is_numeric = dataset['CompilerVersion'].apply(lambda x: isinstance(x, (int, float)) or (isinstance(x, str) and x.isdigit())).all()
    if is_numeric:
        # Load mapping
        with open(categories_path, 'r') as f:
            mapping_json = json.load(f)
        # Reverse the mapping: int → str
        int_to_compilerversion = {v: k for k, v in mapping_json["CompilerVersion"].items()}
        dataset['CompilerVersion'] = dataset['CompilerVersion'].astype(int)
        dataset['CompilerVersion'] = dataset['CompilerVersion'].map(int_to_compilerversion).astype(str)
    #--------------------------------

    #Extract simplified and base versions
    dataset['Simplified Version'] = dataset['CompilerVersion'].str.extract(r'(v0\.\d+\.\d+)')
    dataset['Base Version'] = dataset['Simplified Version'].str.extract(r'(v0\.\d+)')

    #Group and count
    version_summary = dataset.groupby(['Base Version', 'Simplified Version']).size().reset_index(name='Count')

    #Sort versions numerically
    def version_sort_key(version):
        return list(map(int, version[1:].split(".")))

    version_summary['Sort Key'] = version_summary['Simplified Version'].apply(version_sort_key)
    version_summary = version_summary.sort_values(by='Sort Key').drop(columns=['Sort Key'])

    #Recalculate base totals
    base_totals = version_summary.groupby('Base Version')['Count'].sum().reset_index()
    base_totals.columns = ['Base Version', 'Total Count']

    #Create the chart
    fig, ax1 = plt.subplots(figsize=(16, 8))

    # Bar chart for specific versions
    x_positions = []
    x_labels = []
    current_position = 0
    group_positions = []
    for base, group in version_summary.groupby('Base Version'):
        for _, row in group.iterrows():
            ax1.bar(
                current_position,
                row['Count'],
                width=0.8,
                color='skyblue',
                edgecolor='black'
            )
            x_positions.append(current_position)
            x_labels.append(row['Simplified Version'])
            current_position += 1
        group_positions.append((current_position - len(group)) + len(group) / 2)
        current_position += 2  # Space between groups

    #Add number for each bar
    for p in ax1.patches:
                if p.get_height() > 0:
                    ax1.text(p.get_x(),
                    p.get_height()+ 20 ,
                    '{0:.0f}'.format(p.get_height()),
                    color='black', size='small',rotation=90)

    #Set bar chart properties
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels(x_labels, rotation=90, ha="right",fontsize=8)
    ax1.set_ylabel("Number of Samples", fontsize=12)
    ax1.set_xlabel('Solidity Compiler Version', fontsize=12)
    ax1.set_title("Number of Samples per Compiler Version", fontsize=14)
    ax1.tick_params(axis="y", labelsize=10)

    #Line plot for base totals
    ax2 = ax1.twinx()
    ax2.plot(group_positions, base_totals["Total Count"], color="blue", marker="o", linestyle="-", linewidth=1, label='Base Version Totals')
    for pos, total in zip(group_positions, base_totals["Total Count"]):
        ax2.text(pos, total + 180, f"{int(total)}", ha="center", fontsize=10, color="maroon")
    ax2.set_ylabel("Total Samples by Base Version", fontsize=12, color="gray")
    ax2.tick_params(axis="y", labelcolor="gray", labelsize=10)
    ax2.legend(loc="best")
    plt.grid(True, color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
    plt.grid(True, color="grey", which='minor', linestyle=':', linewidth="0.5");

    plt.tight_layout()
    plt.show()

    fig.savefig(outDir + "Number_of_Samples_per_Compiler_Version.pdf", format="pdf", dpi=300)
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