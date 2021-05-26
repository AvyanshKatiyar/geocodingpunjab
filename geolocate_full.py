import pandas
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from tqdm import tqdm
import logging

'''
==============
ASSIGN ADDRESS
==============
'''
def assign_address(df,start,length,order,till_end):
    exceptions=[]
    locator = Nominatim(user_agent="myGeocoder")
    geocode = RateLimiter(locator.geocode, min_delay_seconds=0,max_retries=0)
    index=df.index
    number_of_rows=len(index)
    end=number_of_rows

    if not till_end:
        end=start+length

    for row_num in tqdm(range(start,end)):
        try:
            row= df.loc[row_num]
            address=str(row["patient_address"])+", "+str(row["patient_block"])+", "+str(row["patient_district_name"])+", Punjab, India"
            location = locator.geocode(address)
            if location==None:
                address=str(row["patient_block"])+", "+str(row["patient_district_name"])+", Punjab, India"
                location = locator.geocode(address)
            if location==None:
                address=str(row["patient_district_name"])+", Punjab, India"
                location = locator.geocode(address) 
            if location==None:
                exceptions.append(row_num)
                pass
            else:
                point=tuple(location.point)
                latitude=point[0]
                longitude=point[1]
                df.at[row_num,"final_address"]=address
                df.at[row_num,"latitude"]=latitude
                df.at[row_num,"longitude"]=longitude
                print(location,latitude,longitude)
        except Exception as e:
            with open("log.txt","a") as f:
                f.write("----------------\n")
                f.write("Error occured at line "+str(row_num)+"\n")
                f.write("Error message : "+str(e)+"\n")
                f.write("----------------")

    exceptions_filename=str(order)+"_exceptions"+".txt"
    with open(exceptions_filename,"w") as f:
        for item in exceptions:
            f.write(f"{item}\n")
    return df

'''
=============
MAIN FUNCTION
=============
'''
if __name__ == "__main__":
 # Read in file, Reset Log file
    df=pandas.read_excel("sample.xlsx")
    with open("log.txt","w") as f:
        f.write("")
 # Inputs
    start=int(input("Start:"))
    till_end=input("Run till the end? (y/n)")
    if till_end==y:
        till_end=True
        length=0
        index=df.index
        number_of_rows=len(index)
        end=number_of_rows-1
    else:
        till_end=False
        length=int(input("Length:"))
        end=start+length-1

    order=int(input("Order:"))

    print(f"File will start from {start} and end at {end}")
    print(f"For the next iteration, use the value {end+1} as the start value")

 # Insert columns
    df.insert(1,'longitude','')
    df.insert(1,'latitude','')
    df.insert(1,'final_address','')

 # Assign Addresses
    df=assign_address(df1,start,length,order,till_end)
    df=df[start:end+1]

# Output 
    output_filename=str(order)+"start"+str(start)+"end"+str(end)+".xlsx"
    df.to_excel(output_filename)