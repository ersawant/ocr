import camelot
import pandas as pd

tables = camelot.read_pdf('29th july 2019 to 4th septe 2019_6-6.pdf',flavor='stream', strip_text=' .\n')
pdf_1=tables[0].df
pdf_2 = pdf_1.iloc[4:]

part_number_yn = []
for i in range(pdf_2.shape[0]):
    if pdf_2.iloc[i, 0] != '':
        part_number_yn.append(i)
   

part_number_df = pd.DataFrame(pdf_2.iloc[part_number_yn, 0])
qty_shipped_df = pd.DataFrame(pdf_2.iloc[part_number_yn, 4])
amount_df = pd.DataFrame(pdf_2.iloc[part_number_yn, 8])

qty_shipped_df_num = []
for i in range(qty_shipped_df.shape[0]):
    qty_shipped_df_num.append(int(qty_shipped_df.iloc[i,0])/1000)
qty_shipped_df_num = pd.DataFrame(qty_shipped_df_num)

amount_df_num = []
for i in range(amount_df.shape[0]):
    amount_df_num.append(int(amount_df.iloc[i,0])/100)
amount_df_num = pd.DataFrame(amount_df_num)

part_number_df2 = []
for i in range(part_number_df.shape[0]):
    part_number_df2.append(part_number_df.iloc[i,0])
part_number_df2 = pd.DataFrame(part_number_df2)

df_except_desc = pd.concat([part_number_df2, qty_shipped_df_num, amount_df_num], axis = 1)
df_except_desc.columns = ['Item', 'QTY', 'Line Amount']

import pandas as pd
desc_list = []
for i in range(len(part_number_yn)):
    start_i = part_number_yn[i]
    if i == len(part_number_yn) - 1:
        end_i = pdf_2.shape[0]
    else:
        end_i = part_number_yn[i+1]
 
    desc = ''
    d = 0
    for j in range(end_i)[start_i:end_i]:
        d = d +1
        if d == 1:
            desc = desc + str(pdf_2.iloc[j,2])
        else:
            desc = desc + ' ' + str(pdf_2.iloc[j,2])
    desc_list.append(desc)
   

desc_df = pd.DataFrame(desc_list)
desc_df = desc_df.rename(columns = {0 : "Description"})
final_df = pd.concat([df_except_desc, desc_df], axis = 1)
final_df.to_csv("C:/Users/Dell/Favorites/Flask/flaskblog/test.csv", index = False)