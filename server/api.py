# -*- coding: utf-8 -*-

from flask import Blueprint, current_app, jsonify,request
import json
from server.repository import Repository

repo = Repository() 

api = Blueprint('api', __name__)


def data_path(filename):
    data_path = current_app.config['DATA_PATH']
    return u"%s/%s" % (data_path, filename)


@api.route('/search', methods=['GET'])
def search():
    lat=request.values.get('lat',None)
    lng=request.values.get('lng',None)
    radius=request.values.get('radius',None)
    count=request.values.get('count',None)
    user_tags=request.values.getlist('tags[]',None)

    if not lat or not lng or not radius or not count:
        return jsonify({'message':'Bad request'}), 400

    if not radius.isdigit() or not count.isdigit():
        return jsonify({'message':'Bad request'}), 400
    try:
        lat=float(lat)
        lng=float(lng)
    except ValueError:
        return jsonify({'message':'Bad request'}), 400
    radius=int(radius)
    count=int(count)

    result=repo.find_nearest_products(lat,lng, radius,count,user_tags)

    products=to_view_model(result)

    return jsonify({'products': products})

def to_view_model(products):
    '''Transforms the data in the structure expected by the client'''
    model=list()
    for p in products:
        product={}
        product['title']=p[1]
        product['popularity']=p[2]
        shop={}
        shop['lat']=p[5]
        shop['lng']=p[6]
        product['shop']=shop 
        model.append(product)  
    return model