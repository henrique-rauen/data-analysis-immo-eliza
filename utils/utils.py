#! /usr/bin/python3

#Created by Henrique Rauen (rickgithub@hsj.email)
import numpy as np
import pandas as pd

def clean_df(data):
    if isinstance(data,str): #Assumed to be file Path
        df = pd.read_csv(data)
    elif isinstance(data,pd.DataFrame):
        df = data
    else:
        print("unable to recognize argument")
        return None
    NaN_defaults = ({False :  ["Furnished", "Garden"]
                    ,-1 : ["Listing_ID", "Price", "Bedroom", "Living_area",
                           "Surface_of_land", "Facade","Garden_area"]
                    , "not_available" : ["Kitchen", "State of the building", "District"]
                    })
    df = fill_NaN(df, NaN_defaults)
    unwanted_data = ({"Type" : "apartment group"
                     ,"Listing_ID" : -1})
    df = remove_unwanted_data(df, unwanted_data)
    unwanted_partial = ({"Postal_code" : " "
                        ,"Price" : "-"
                       })
    df = remove_unwanted_partial(df, unwanted_partial)
    convert_column = ({int : ["Listing_ID", "Bedroom", "Living_area",
                      "Surface_of_land", "Facade", "Garden_area"]
                    })
    df = convert_column_type(df,convert_column)
    df = remove_empty_spaces(df,["Type", "Subtype", "Listing_address",
                                 "Locality", "District", "Kitchen",
                                 "State of the building"])
    return df

def fill_NaN(df,dic_defaults={}):
    for key,value in dic_defaults.items():
        for column in value:
            df[column]=df[column].fillna(key)
    print("Filled NaN")
    return df

def remove_unwanted_partial(df,dic_partial):
    for key,value in dic_partial.items():
        df = df[~df[key].str.contains(value)]
    print("Removed partial unwanted")
    return df

def remove_unwanted_data(df,dic_unwanted):
    for key,value in dic_unwanted.items():
        df = df[df[key] != value]
    print("Removed unwanted")
    return df

def convert_column_type(df,dic_convert):
    for key,value in dic_convert.items():
        for column in value:
            df[column] = df[column].apply(key)
    print("Converted Columns")
    return df

def remove_empty_spaces(df, columns):
    for col in columns:
        df[col] = df[col].apply(str.strip)
    return df
