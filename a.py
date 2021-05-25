# start_new=start_prev+length_prev+1
import pandas


def avyansh(df):
    number_of_rows=227
    for row_num in range(number_of_rows):
        print(row_num)

        row= df.loc[row_num]
        block=row["unique_patient_block"]
        current=""
        i=0
        while current!=block:
            block_row=df.loc[i]
            current=block_row["patient_block"]
            i+=1
        district=block_row["patient_district_name"]
        df.at[row_num,"district"]=district
    return df
print("Start input")

input=pandas.read_excel("positive-datasince-2020.xlsx",sheet_name=8)
print("End input")

input.insert(1,'district','')
df=avyansh(input)
output_filename="may_input.xlsx"
df.to_excel(output_filename)


