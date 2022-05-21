import argparse
from pathlib import Path
import numpy as np
import pandas as pd

def define_argparser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--input_path', type=Path, required=True)
    parser.add_argument('--output_path', type=Path, required=True)
    parser.add_argument('--tokenize', type=str, choices=['character', 'word'], default="word")
    
    return parser.parse_args()

def data_stats_to_excel(config):
    """
    Args:
        config : 
        --input_path (str): the path of train dataset for gpt.
        --output_path (str): the path of data length statistics output.
        --tokenize (str, optional): choose tokenizing options from ('character', 'word'). Defaults to 'word'.

    Returns:
        data length statistics excel file (.xlsx) : 
            It includes various length statistics.
            The rows take name of data types and the columns take type of statistics.
    """
    
    # load data file
    data = pd.read_excel(config.input_path, index_col=0)
    
    # make output file
    df = pd.DataFrame(index=data.type.unique(),
                      columns=["nums", "min", "max", "mean", "median", "percentile_25", "percentile_75", "std", "qmarks", "fullstop", "alphabet_first", "numbers"])
    
    for type_name, type_data in data.groupby(['type']):
        type_data['text'] = type_data['text'].apply(str)
        if config.tokenize == 'word':
            each_type_length = type_data['text'].apply(lambda x: len(x.split(' ')))
        else:
            each_type_length = type_data['text'].apply(len)
        
        nb_data = len(each_type_length)
        
        min_length = np.min(each_type_length)
        max_length = np.max(each_type_length)
        mean_length = round(np.mean(each_type_length), 2)
        median_length = round(np.median(each_type_length), 2)
        percentile_25_length = round(np.percentile(each_type_length, 25), 2)
        percentile_75_length = round(np.percentile(each_type_length, 75), 2)
        std_of_length = round(np.std(each_type_length), 2)
        
        percentage_of_qmarks = round(np.mean(type_data['text'].apply(lambda x: '?' in x)), 4)
        percentage_of_fullstop = round(np.mean(type_data['text'].apply(lambda x: '.' in x)), 4)
        percentage_of_alphabet_first = round(np.mean(type_data['text'].apply(lambda x: x[0].encode().isalpha())), 4)
        percentage_of_numbers = round(np.mean(type_data['text'].apply(lambda x: max([y.isdigit() for y in x]))), 4)
        
        df.loc[type_name, :] = nb_data, \
            min_length, max_length, mean_length, median_length, percentile_25_length, percentile_75_length, std_of_length, \
            percentage_of_qmarks, percentage_of_fullstop, percentage_of_alphabet_first, percentage_of_numbers
    
    df.to_excel(config.output_path)

if __name__ == "__main__":
    config = define_argparser()
    data_stats_to_excel(config)