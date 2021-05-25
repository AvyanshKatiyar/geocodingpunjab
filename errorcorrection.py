import pandas
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from tqdm import tqdm
import math

input_filename=input("Enter input filename:")

output_filename=input("Enter output filename:")


def correct(df,order):
    locator = Nominatim(user_agent="myGeocoder")
    geocode = RateLimiter(locator.geocode, min_delay_seconds=0)
    index=df.index
    number_of_rows=len(index)
    for row_num in tqdm(range(number_of_rows)):
        row= df.loc[row_num]
        print(row["latitude"])
        if(math.isnan(row["latitude"])):
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
    
    return df

df=pandas.read_excel(input_filename)

df1=df
df1=correct(df1,order)

df1.to_excel(output_filename)