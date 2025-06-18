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
def get_DataStatistics(datasetName, voteDataName, dataset_defaultDir = True, voteData_defaultDir = True, QuickReport = True):
    try:
        outDir = git_Dir(dataType ='Statistics')
        outDir = create_outDir(outDir,(datasetName.split('_')[-1].split('.')[0])) 

        #Read dataset
        if dataset_defaultDir:
            datasetPath = git_Dir(dataType = 'Dataset')
            dataset = pd.read_csv(str(datasetPath) + '/' + datasetName)    
        else:
            datasetPath = os.path.dirname(datasetName)
            datasetName = os.path.basename(datasetName)
            dataset = pd.read_csv(os.path.join(datasetPath, datasetName))
        
        if voteDataName !="":
            if voteData_defaultDir:
                voteData_Path = git_Dir(dataType = 'Labels')
                voteData = pd.read_csv(str(voteData_Path) + '/' + voteDataName) 
            else:
                voteDataPath = os.path.dirname(voteDataName)
                voteDataName = os.path.basename(voteDataName)
                voteData = pd.read_csv(os.path.join(voteDataPath, voteDataName))
        else:
            voteData = ""
    
        # Derive CategoricalColsMappings.json file path from dataset name
        parts = datasetName.replace('.csv', '').split('_')
        categories_path = os.path.join(datasetPath, f'{parts[0]}_CategoricalColsMappings_{"_".join(parts[-2:])}.json')

        get_datasetInfo(dataset,outDir)
        get_datasetSummary(dataset,outDir)   

        if len(voteData) > 0 and 'Tools' in voteData.columns:
            get_ToolsFrequency(voteData,outDir)
            
        get_TimestampFrequency(dataset,outDir)
        get_CompilerVersionsFrequency(dataset,outDir,categories_path)
        get_LabelsFrequency(dataset,outDir)
        get_ProfileReport(dataset,outDir,datasetName.split('_')[-1].split('.')[0],QuickReport)

        return

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------    
def git_Dir(dataType):
    try:
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
        elif dataType == 'Labels':
            Dir = self_main_dir/config_File['DataLabels']['Labels']
        else:
            Dir = self_main_dir
        return Dir
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------    
def create_outDir(StatisticsDir,datasetName):
    try:
        #Create new out dir inside StatisticsDir
        UniqueDirName = str(datetime.now().date()).replace('-', '') + '_' + str(datetime.now().time()).replace(':', '').split('.')[0]+ '_' + datasetName
        path = os.path.join(StatisticsDir, UniqueDirName)
        os.mkdir(path)

        outDir = str(StatisticsDir) + '/' + UniqueDirName + '/'
        return outDir
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------
def get_datasetInfo(dataset,outDir):
    try:    
        print('**Data Info**')
        print('________________________________')
        display(dataset.info())

        os.makedirs(outDir, exist_ok=True)
        datasetInfo_file_path = os.path.join(outDir, 'datasetInfo.txt')
        with open(datasetInfo_file_path, 'w') as f:
            dataset.info(buf=f)  
            f.flush()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------
def get_datasetSummary(dataset,outDir):
    try:
        print('**Data Describtion**')
        print('________________________________')
        summary = dataset.describe(include='all')
        display(summary)

        os.makedirs(outDir, exist_ok=True)
        summary.to_html(outDir + 'datasetSummary.html')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise   
#----------------------------------------------------------------       
def get_ToolsFrequency(voteData,outDir):
    try:
        print('**Analysis Tools Frequency**')
        print('________________________________')
        print('Frequency of analysis tools in the labeled data:\n')

        #Parse the Tools column into actual lists
        voteData['Tools'] = voteData['Tools'].apply(eval)

        #Add a new column to count the number of tools used for each sample
        voteData['Num Tools'] = voteData['Tools'].apply(len)

        #Group by unique tool sets
        voteData['Tool Set'] = voteData['Tools'].apply(lambda x: ', '.join(sorted(x)))
        tool_set_summary = voteData.groupby(['Tool Set', 'Num Tools']).size().reset_index(name='Count')

        #Group data by the number of tools
        grouped_data = tool_set_summary.groupby('Num Tools')
        grouped_totals = tool_set_summary.groupby('Num Tools')['Count'].sum()

        #Create the chart with bars and line plot
        fig, ax1 = plt.subplots(figsize=(16, 8))

        #Bar chart for tool sets using shades of blue
        x_positions = []
        x_labels = []
        current_position = 0
        group_positions = []
        for num_tools, group in grouped_data:
            for _, row in group.iterrows():
                ax1.bar(
                    current_position,
                    row['Count'],
                    width=0.8,
                    color=sns.color_palette('Blues', len(grouped_data))[num_tools - 2],
                    edgecolor='black',)
                x_positions.append(current_position)
                x_labels.append(row['Tool Set'])
                current_position += 1
            group_positions.append((current_position - len(group) + current_position - 1) / 2)
            current_position += 2  # Space between groups
            
        #Add number for each bar
        for p in ax1.patches:
                    if p.get_height() > 0:
                        ax1.text(p.get_x()-0.1,
                        p.get_height()* 1 ,
                        '{0:.0f}'.format(p.get_height()),
                        color='black', size='small')

        #Set bar chart properties
        ax1.set_xticks(x_positions)
        ax1.set_xticklabels(x_labels, rotation=45, ha='right')
        ax1.set_ylabel('Number of Samples per Analysis Tool Set', fontsize=12)
        ax1.set_xlabel('Analysis Tool Sets', fontsize=12)
        ax1.set_title('Number of Labeled Samples per Analysis Tool Set', fontsize=14)
        ax1.tick_params(axis="y", labelsize=10)

        #Secondary y-axis for the line chart (total samples per group)
        ax2 = ax1.twinx()
        ax2.plot(group_positions, grouped_totals, color='blue', marker="o", linestyle='-', linewidth=1, label='Total Samples')
        for pos, total in zip(group_positions, grouped_totals):
            ax2.text(pos, total + 180, f"{int(total)}", ha='center', fontsize=10, color='maroon')
        ax2.set_ylabel('Total Samples by Set Size', fontsize=12, color='grey')
        ax2.tick_params(axis='y', labelcolor='grey', labelsize=10)

        #Add legends
        #ax1.legend(title="Number of Tools", loc="upper left", bbox_to_anchor=(1.05, 1))
        #ax2.legend(loc="upper right", bbox_to_anchor=(1.05, 0.9))
        ax2.legend(loc="best")

        plt.grid(True, color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
        plt.grid(True, color="grey", which='minor', linestyle=':', linewidth="0.5");

        plt.tight_layout()
        plt.show()

        fig.savefig(outDir + "/Number_of_Samples_per_Analysis_Tool_Set.pdf", format="pdf", dpi=300)
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------    
def get_TimestampFrequency(dataset,outDir):
    try:
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
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------    
def get_CompilerVersionsFrequency(dataset,outDir,categories_path):
    try:
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
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#----------------------------------------------------------------    
def get_LabelsFrequency(dataset,outDir):
    print('**Distribution of Vulnerability Categories**')
    print('_______________________________________________')
   
    try:
        LabelsCols = get_Info('LabelsCols')
        existing_label_cols = [col for col in LabelsCols if col in dataset.columns]
        df = dataset[existing_label_cols]

        # Calculate the sum of 1s for each category
        sums = df.sum()

        # Plotting
        fig = plt.figure(figsize=(12, 6))
        ax1 = sums.plot(kind='bar', color='skyblue',edgecolor='black', width=0.6)
        plt.title('Distribution of Vulnerability Categories')
        plt.xlabel('Vulnerability Types')
        plt.ylabel('Samples')
        plt.xticks(rotation=45)

        #Add number for each bar
        for p in ax1.patches:
                    if p.get_height() > 0:
                        ax1.text(p.get_x()+0.1,
                        p.get_height()+ 20 ,
                        '{0:.0f}'.format(p.get_height()),
                        color='black', size='small')

        plt.grid(axis='y', color = "grey", which='major', linewidth = "0.3", linestyle = "-.")
        plt.grid(axis='y', color="grey", which='minor', linestyle=':', linewidth="0.5");
        plt.show()  

        fig.savefig(outDir + "Distribution of Vulnerability Categories.pdf", format="pdf", dpi=300) 
    except Exception as e:
        print(f"Failed to compute vulnerability distribution due to: {e}")
#----------------------------------------------------------------       
def get_ProfileReport(dataset,outDir, datasetName,QuickReport):
    print('**Data Profiling Report**')
    print('_______________________________________________')

    try:
        os.makedirs(outDir, exist_ok=True)

        profile = ProfileReport(dataset, title = datasetName + " Profiling Report", minimal=QuickReport)

        report_path = os.path.join(outDir, 'Profiling_DetailedReport.html')
        profile.to_file(output_file=report_path)

        relative_path = os.path.relpath(report_path, start=Path.cwd().parent)
        print(f'Done! The Data Profiling Report is available at: {relative_path}')

    except Exception as e:
        print(f"Failed to generate full profile report due to: {e}")
#--------------------------------------------------
def get_ConfigFile(config_file_name = 'config.json'):
    try:
        self_dir = Path(__file__).resolve().parents[1]
        config_file_path = self_dir / config_file_name
        configFile = open(config_file_path)
        config_File = json.load(configFile)
        configFile.close()
        return config_File
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#--------------------------------------------------
def get_Info(dataType):
    try:
        config_File = get_ConfigFile(config_file_name = 'config.json')
        self_main_dir = Path(__file__).resolve().parents[1]
        if dataType == 'self_main_dir':
            info = self_main_dir
        elif dataType == 'LabelsCols':
            info = config_File['DataLabels']['LabelsCols']
        return info
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise