
import pandas as pd

def calc_prob_distr(column_name, input_df, input_type):
    value_counts_dict = dict(input_df[column_name].value_counts())
    value_counts_probability = {k: v / total for total in (sum(value_counts_dict.values()),) for k, v in value_counts_dict.items()}
    print('')
    print('Probabilities and counts for ' + input_type + ' dataset:')
    print(value_counts_probability)
    print(list(value_counts_probability.values()))
    print(list(value_counts_probability.keys()))
    print(value_counts_dict)

    return (value_counts_dict, value_counts_probability)

def freq_analysis(main_count, aux_count):
    cdata = list(main_count.keys())
    adata = list(aux_count.keys())

    if len(adata) != len(cdata):
        print('List sizes do not match')
        return

    correct_count = 0
    correct = 0
    cur_index = 0
    for i in cdata:
        if adata[cur_index] == cdata[cur_index]:
            correct = correct + 1
            correct_count = correct_count + main_count[cdata[cur_index]]
        cur_index = cur_index + 1
    frequency_diag = correct * 100 / len(adata)
    frequency_records = correct_count * 100 / sum(main_count.values())

    print('The accuracy of diagnosis mapping is ' + str(frequency_diag) + '%' )
    print('The accuracy of records is ' + str(frequency_records) + '%')

if __name__ == '__main__':

    # you may need to change path according to the location of input and output files on your machine
    input_file = '/Users/ananya/Downloads/NYSDOH_HospitalInpatientDischarges_SPARCS_De-Identified_2017.csv'
    output_file = '/Users/ananya/Downloads/nydata_output.csv'

    # load input file in pandas data frame
    df = pd.read_csv(input_file)

    # Column indexes to be removed (starts at 0)
    columns_to_remove = [0,1,2,3,4,6,12,13,14,15,16,17,18,20,21,22,25,26,27,28,29,30,31]
    df.drop(df.columns[columns_to_remove], axis=1, inplace=True)

    df.to_csv(output_file, index=False)
    print(output_file)

    # drop any records that have missing values
    df.dropna(inplace=True)

    # Main and auxiliary files
    # random state is a seed value
    main_df = df.sample(frac=0.5, random_state=111)
    aux_df = df.drop(main_df.index)

    # from calculating probability distribution function
    val_cnt, prob_dict = calc_prob_distr('APR DRG Description', main_df, 'main')
    val_cnt_aux, prob_dict_aux = calc_prob_distr('APR DRG Description', aux_df, 'aux')

    # frequency analysis of diagnosis mappings and individual records
    freq_analysis(val_cnt, val_cnt_aux)