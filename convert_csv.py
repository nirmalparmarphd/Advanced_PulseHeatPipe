import csv

input_file = 'PHP_T_40FR_120W_90A_0B.csv'
output_file = 'PHP_T_40FR_120W_90A_0B_1.csv'

with open(input_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
    reader = csv.reader(csv_in)
    writer = csv.writer(csv_out, delimiter='\t')
    
    for row in reader:
        writer.writerow(row)