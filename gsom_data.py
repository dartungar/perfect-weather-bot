import csv
import os
import pandas

stations = {}
needed_columns = ['TSUN', 'PSUN', 'PRCP', 'AWNS', 'TAVG', 'TMIN', 'TMAX']

def build_needed_columns_check():
    with open('gsom_needed_columns.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        for filename in os.listdir('./gsom'):
            df = pandas.read_csv('./gsom/'+filename)
            #stations['filename'] = []
            present_cols = []
            for colname in needed_columns:
                if colname in df.columns:
                    #stations['filename'].append(colname)
                    present_cols.append(colname)

            row = [filename, ','.join(present_cols)]
            writer.writerow(row)
            print(f'processed {filename}')








