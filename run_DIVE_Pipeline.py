import yaml, sys, os, subprocess
import tempfile, json
from pathlib import Path
#------------------------------------------
# Run Pipeline
#------------------------------------------
def run_pipeline(DIVE_FrameworkConfig,session_path):

    input_cfg = DIVE_FrameworkConfig.get("input", {})
    pipeline_cfg = DIVE_FrameworkConfig.get("pipeline", {})

    datasetName = input_cfg["datasetName"]
    if input_cfg.get("installRequirements", False):
        install_requirements()

    from Scripts.get_Addresses import get_Addresses
    from Scripts.get_ContractFeatures import get_ContractFeatures
    from Scripts.apply_FeatureExtraction import apply_FeatureExtraction
    from Scripts.construct_FinalData import construct_FinalData
    from Scripts.apply_DataPreprocessing import apply_DataPreprocessing
    from Scripts.get_DataStatistics import get_DataStatistics
    from Scripts.FeatureSelection.get_FilteredFeatures import get_FilteredFeatures

    Flag = False
    for step_name, step_cfg in pipeline_cfg.items():
        if str(step_cfg.get("enable", False)).lower() != "true":
            if step_name == "get_ContractFeatures":
                Flag= True
            if step_name == "constructFinalData":
                write_session(session_path, {"FinalLabeledData": input_cfg["FinalLabeledData"]})
            continue

        print(f"- Running step: {step_name}")

        match step_name:
            case "get_Addresses":
                addresses = get_Addresses(step_cfg["addressesFile"])

            case "get_ContractFeatures":
                featureTypes = {k: v for k, v in step_cfg["featureTypes"].items() if v}
                get_ContractFeatures(featureTypes, addresses=addresses, DatasetName = datasetName, session_path=session_path)

            case "apply_FeatureExtraction":
                if Flag:
                    write_session(session_path, {"AccountInfo": step_cfg["sources"]["AccountInfo"]})
                    write_session(session_path, {"ContractsInfo": step_cfg["sources"]["ContractsInfo"]})
                    write_session(session_path, {"Opcodes": step_cfg["sources"]["Opcodes"]})
                    write_session(session_path, {"Samples": step_cfg["sources"]["Samples"]})
                    write_session(session_path, {"SamplesDirPath": step_cfg["sources"]["SamplesDirPath"]})
                    write_session(session_path, {"BlockInfo": step_cfg["sources"]["BlockInfo"]})
                    
                    
                attributes = {k: v for k, v in step_cfg["attributes"].items() if v}
                dataset_or_SamplesFolderName = ""
                apply_FeatureExtraction(datasetName,dataset_or_SamplesFolderName,attributes,session_path)

            case "constructFinalData":
                filteredFeatureTypes = {k: v for k, v in step_cfg["FeatureTypes"].items() if v}
                construct_FinalData(FinalDatasetName=datasetName, Dataset=step_cfg["sourceDatasets"], 
                                    FeatureTypes=filteredFeatureTypes, applyPreprocessing=step_cfg["apply_DataPreprocessing"], 
                                    session_path=session_path)
    
            case "apply_DataPreprocessing":
                datasetNameFrom_cfg = step_cfg.get("datasetName", "").strip()
                if datasetNameFrom_cfg == "":
                    session = read_session(session_path)
                    finalLabeled_path = session.get("FinalLabeledData")
                    if finalLabeled_path is None:
                        raise ValueError("Missing 'FinalLabeledData' path in session.")
                    DatasetName = Path(finalLabeled_path).name
                else:
                    DatasetName = datasetNameFrom_cfg

                preprocessingTasks = {k: v for k, v in step_cfg["PreprocessingTasks"].items() if v}
                apply_DataPreprocessing(datasetName=DatasetName,dataDirPath=step_cfg["dataDirPath"],
                                        PreprocessingTasks=preprocessingTasks, session_path=session_path)

            case "get_DataStatistics":
                datasetNameFrom_cfg = step_cfg.get("datasetName", "").strip()
                if datasetNameFrom_cfg == "":
                    session = read_session(session_path)
                    PreprocessedData_path = session.get("PreprocessedData")
                    if PreprocessedData_path is None:
                        raise ValueError("Missing 'PreprocessedData' path in session.")
                    DatasetName = Path(PreprocessedData_path).name
                else:
                    DatasetName = datasetNameFrom_cfg

                session = read_session(session_path)
                get_DataStatistics(DatasetName, rawDataName=session.get("FinalLabeledData"), voteDataName = step_cfg["voteDataName"],
                                   dataset_defaultDir = step_cfg["dataset_defaultDir"], rawData_defaultDir = step_cfg["FinalLabeledData_defaultDir"], 
                                   voteData_defaultDir = step_cfg["voteData_defaultDir"], QuickReport = step_cfg["QuickReport"])
            case "get_FilteredFeatures":
                get_FilteredFeatures(step_cfg["filters"])

            case _:
                print(f"Unknown step '{step_name}' — skipping.")
#------------------------------------------
#Install Requirements
#------------------------------------------
'''def install_requirements():
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print("requirements.txt not found. Skipping installation.")
        return

    print("Installing required packages from requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        sys.exit(1)'''

def install_requirements():
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print("requirements.txt not found. Skipping installation.")
        return

    print("Installing required packages from requirements.txt...")
    try:
        # Use --no-cache-dir to avoid caching issues and enforce clean install
        # Use --upgrade-strategy only-if-needed to respect version pins
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "--no-cache-dir", "--upgrade-strategy", "only-if-needed",
            "-r", requirements_file
        ])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")
        sys.exit(1)
#------------------------------------------
#Load YAML Configuration
#------------------------------------------
def load_config(file_path):
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML config: {e}")
        sys.exit(1)
#------------------------------------------
def read_session(path):
    with open(path, "r") as f:
        return json.load(f)
#------------------------------------------
def write_session(path, updates):
    session = read_session(path)
    session.update(updates)
    with open(path, "w") as f:
        json.dump(session, f, indent=2)
#------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        DIVE_FrameworkConfigFile = sys.argv[1]
    else:
        DIVE_FrameworkConfigFile = "DIVE_pipeline.yaml"  # Default fallback

    if not os.path.exists(DIVE_FrameworkConfigFile):
        print(f"Pipeline configuration file '{DIVE_FrameworkConfigFile}' not found.")
        sys.exit(1)

    print("Loading configuration...")
    DIVE_FrameworkConfig = load_config(DIVE_FrameworkConfigFile)

    #Create a temp session registry file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp_file:
        session_path = temp_file.name
        json.dump({}, temp_file)
        temp_file.flush()

    try:
        print("Starting pipeline execution...")
        run_pipeline(DIVE_FrameworkConfig, session_path)
    finally:
        if os.path.exists(session_path):
            os.remove(session_path)
            print(f"Temporary session file deleted: {session_path}")