import os,sys
import numpy as np
import csv
import pandas as pd
from scipy.spatial import cKDTree
from math import cos,sin
from operator import itemgetter
import json


class Repository:
    shops_filename='shops.csv'
    products_filename='products.csv'
    tagging_filename='taggings.csv'
    tags_filename='tags.csv'

    def create_repository(self,data_path):
        self.read_shops(os.path.join(data_path, self.shops_filename))
        self.read_products(os.path.join(data_path, self.products_filename))
        self.read_tags(os.path.join(data_path, self.tags_filename),os.path.join(data_path, self.tagging_filename))
    
    def read_shops(self,shops_filename):
        '''Reads shops and loads their coordinates in a KDTree to search the neighbours'''
        self.shops={}
        with open(shops_filename,'r') as shops_file:
            reader = csv.reader(shops_file,delimiter=',',quotechar='"')
            try:
                for row in reader:
                    key=row[0]
                    self.shops[key]=row[1:]
            except csv.Error as e:
                sys.exit('Error in file {}, line {}: {}'.format(shops_filename, reader.line_num, e))
        try:
            self.dfshops = pd.read_csv(shops_filename)
        except:
            sys.exit('Error in file {}: {}'.format(shops_filename, sys.exc_info()[0]))
        self.dfshops['x'],self.dfshops['y'],self.dfshops['z'] = zip(*map(Repository.to_cartesian,self.dfshops['lat'],self.dfshops['lng']))
        shops_coordinates = list(zip(self.dfshops['x'], self.dfshops['y'], self.dfshops['z']))
        self.shops_tree = cKDTree(shops_coordinates)
    
    def read_products(self,products_filename):
        '''Read the products and store in a dictionary'''
        self.products={}
        with open(products_filename,'r') as products_file:
            reader = csv.reader(products_file,delimiter=',',quotechar='"')
            next(reader) # skip the header
            try:
                for row in reader:
                    key=row[1]
                    if self.products.get(key)==None:
                        self.products[key]={'products':list(),'tags':list()}
                    self.products[key]['products'].append((row[0],row[2],float(row[3]),float(row[4]),row[1],self.shops[key][1],self.shops[key][2]))
            except csv.Error as e:
                sys.exit('Error in file {}, line {}: {}'.format(products_filename, reader.line_num, e))
            for item in self.products:
                self.products[item]['products'].sort(key=itemgetter(2)) # Order products by popularity
    
    def read_tags(self,tags_filename, tagging_filename):
        '''Reads the tags, the relations with each shop, and add the tags to the dictionary holding products of each shop'''
        tags={}
        with open(tags_filename,'r') as tags_file:
            reader = csv.reader(tags_file,delimiter=',',quotechar='"')
            next(reader) # skip the header
            try:
                for row in reader:
                    key=row[0]
                    tags[key]=row[1]
            except csv.Error as e:
                sys.exit('Error in file {}, line {}: {}'.format(tags_filename, reader.line_num, e))
        with open(tagging_filename,'r') as tagging_file:
            reader = csv.reader(tagging_file,delimiter=',',quotechar='"')
            next(reader) # skip the header
            try:
                for row in reader:
                    key=row[1]
                    if self.products.get(key)==None:
                        self.products[key]={'products':list(),'tags':list()}
                    self.products[key]['tags'].append((tags[row[2]]))
            except csv.Error as e:
                sys.exit('Error in file {}, line {}: {}'.format(tagging_filename, reader.line_num, e))

    def find_nearest_shops(self,lat,lng,radius):
        '''Finds the nearest shops to the location inside a radius of ditance km.
            param: lat - latitude in degrees
            param: lng - longitude in degrees
            param: radius - distance from the location in kilometers
            returns: shops matching the criteria
        '''
        idx = self.shops_tree.query_ball_point(Repository.to_cartesian(lat,lng), radius)
        return [self.dfshops.loc[x,['id','lat','lng']] for x in idx]

    def find_nearest_products(self,lat,lng, radius,count, user_tags):
        '''Finds the <count> products at a <radius> distance from the <lat,lng> that have any of the <user_tags>'''
        #radius has to be in kilometers
        radius=radius/1000
        #Find the nearest shops
        nearest_shops=self.find_nearest_shops(lat,lng,radius)
        found_products=list()
        #Filters the products of the shops with the matching tags
        #and get the <count> products with highest popularity
        for i in nearest_shops:
            if len(user_tags)>0:
                if any(t in self.products[i[0]]['tags'] for t in user_tags):
                    found_products.extend(self.products[i[0]]['products'][-count:])
            else:
                found_products.extend(self.products[i[0]]['products'][-count:])
        #orders the filtered products by popularity
        found_products.sort(key=itemgetter(2))
        #return the <count> products with the highest popularity across all the shops
        return found_products[-count:]

    @staticmethod
    def deg2rad(degree):
        '''Convert from degrees to radians'''
        rad = degree * 2*np.pi / 360
        return(rad)

    @staticmethod
    def to_cartesian(lat, lng):
        '''Convert from geodetic to ECEF coordinates'''
        R = 6367 # radius of the Earth in kilometers
        rlat = Repository.deg2rad(lat)
        rlng = Repository.deg2rad(lng)
        x = R * cos(rlat) * cos(rlng)
        y = R * cos(rlat) * sin(rlng)
        z = R * sin(rlat)
        return x, y, z

