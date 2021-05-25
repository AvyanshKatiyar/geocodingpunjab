import pandas
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
import threading

start=int(input("Start:"))
length=int(input("Length:"))

def cleanup(df):
    newdf=df
    return(newdf)

def assign_address(df,start,length):
    locator = Nominatim(user_agent="myGeocoder")
    geocode = RateLimiter(locator.geocode, min_delay_seconds=0)
    index=df.index
    number_of_rows=len(index)
    for row_num in range(start,start+length):
        row= df.loc[row_num]
        address=row["patient_address"]+", "+row["patient_block"]+", "+row["patient_district_name"]+", Punjab, India"
        location = locator.geocode(address)
        if location==None:
            address=row["patient_block"]+", "+row["patient_district_name"]+", Punjab, India"
            location = locator.geocode(address)
        if location==None:
            address=row["patient_district_name"]+", Punjab, India"
            location = locator.geocode(address)  

        point=tuple(location.point)
        latitude=point[0]
        longitude=point[1]
        df.at[row_num,"final_address"]=address
        df.at[row_num,"latitude"]=latitude
        df.at[row_num,"longitude"]=longitude
        print(location,latitude,longitude)

    return df



locator = Nominatim(user_agent="myGeocoder")

df=pandas.read_excel("sample.xlsx")

df.insert(1,'longitude','')
df.insert(1,'latitude','')
df.insert(1,'final_address','')

df1=df
df1=cleanup(df1)
df1=assign_address(df1,start,length)
df1.to_excel("output.xlsx")