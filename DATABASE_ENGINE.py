import mysql.connector
import matplotlib.pyplot as plt
import os 
import json

import pandas as pd


class database:

    def __init__(self):
        self.__uuids()
        self.__table_stations()

           
    # login method    
    def __login(self):
        con_data = {}
        # load connection data from corresponded JSON-File
        with open('./connect.conf') as fin:
            con_data = json.load(fin)
                               
            self.__mydb = mysql.connector.connect(**con_data)

       
    # logout method
    def __logout(self):
        self.__mydb.close()
                
               
    # table of all names (uuids) of all tables with ready price data extractions
    def __uuids(self):
        self.__login()
        cursor = self.__mydb.cursor()
        
        sql_q = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'fuel_prices' and table_name not in ('prices', 'stations');"
        cursor.execute(sql_q)
        
        self.uuids         = pd.DataFrame(cursor.fetchall())
        self.uuids.columns = ['uuid']
       
        cursor.close()
        
        self.__logout()
        
    # table of all stations and their meta data (in database it is the table `stations`)
    def __table_stations(self):
        self.__login()
        cursor = self.__mydb.cursor()
    
        sql_q = "SELECT * from stations;"
        
        cursor.execute(sql_q)
        
        self.table_stations = pd.DataFrame(cursor.fetchall())
        self.table_stations.columns = cursor.column_names
        
        ## the values of postcodes are actually stored as integer but pandas get them as float
        ## thats why we convert them to integers
        #self.table_station = self.table_stations['post_code'].notna().astype(int)
        self.table_stations['post_code'] = self.table_stations['post_code'].fillna(0).astype(int)
        
        cursor.execute(sql_q)
        
        self.__logout()
        
        
    # getter to get the table named `table_name` from database     
    def get_table_data(self, table_name, mp=True):
        
        self.__login()
        
        cursor = self.__mydb.cursor()
        
        sql_q = "SELECT * from `{}`;".format(table_name)
        
        cursor.execute(sql_q)
        

        table_stations         = pd.DataFrame(cursor.fetchall())
        table_stations.columns = cursor.column_names
        
        cursor.execute(sql_q)
        self.__logout()
        
        return table_stations