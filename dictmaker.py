# start_new=start_prev+length_prev+1
import pandas
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

month=str(input("Enter month:"))

def calculate_coordinates(df):
    locator = Nominatim(user_agent="myGeocoder")
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
    index=df.index
    number_of_rows=len(index)
    for row_num in range(number_of_rows):
        row= df.loc[row_num]
        address=row["block"]+", "+row["district1"]+", Punjab, India"
        location = locator.geocode(address)
        if location==None:
            address=row["district1"]+", Punjab, India"
            location = locator.geocode(address)
        print(row_num , location)
        point=tuple(location.point)
        latitude=point[0]
        longitude=point[1]
      
        
        df.at[row_num,"final_address"]=address
        df.at[row_num,"latitude"]=latitude
        df.at[row_num,"longitude"]=longitude

          
    return df

def assign_coordinates(coordinates,df):
    index=df.index
    df_number_of_rows=len(index)
    for df_row_num in range(df_number_of_rows):
        print(df_row_num)
        df_row=df.loc[df_row_num]
        block=df_row["patient_block"]
        coordinate_row_num=coordinates[coordinates['block'] == block].index[0]
        coordinate_row=coordinates.loc[coordinate_row_num]
        latitude=coordinate_row["latitude"]
        longitude=coordinate_row["longitude"]
        df.at[df_row_num,"final_address"]=coordinate_row["final_address"]
        df.at[df_row_num,"latitude"]=latitude
        df.at[df_row_num,"longitude"]=longitude

        df_row=df.loc[df_row_num]
        print(df_row["ROWNUM"])
        print(df_row["final_address"])
    return df


# coordinates=pandas.read_excel("may_bd_list.xlsx")
# coordinates.insert(1,'longitude','')
# coordinates.insert(1,'latitude','')
# coordinates.insert(1,'final_address','')

# coordinates=calculate_coordinates(coordinates)

# coordinate_filename=month+"_coordinates"+".xlsx"
# coordinates.to_excel(coordinate_filename)


coordinates=pandas.read_excel("May_coordinates.xlsx")


print("Start Reading:")
input=pandas.read_excel("may_input.xlsx")
print("End Reading")
input.insert(1,'longitude','')
input.insert(1,'latitude','')
input.insert(1,'final_address','')

output=assign_coordinates(coordinates,input)

output_filename=month+"_output"+".xlsx"
output.to_excel(output_filename)