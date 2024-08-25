import datetime

def get_CodeMetrics():
    UniqueFilename = generate_UniqueFilename('CodeMetrics')
    
    return

def generate_UniqueFilename(FeatureType):
    UniqueFilename = str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0] + FeatureType
    return UniqueFilename