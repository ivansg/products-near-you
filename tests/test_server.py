class TestServer(object):
    
    def test_request_incorrect_value_params(self,client):
        data={'radius':'','count':'','tags[]':'','lat':'','lng':''}
        resp = client.get('/search',query_string=data)
        assert resp.status_code==400

    def test_request_incorrect_number_of_params(self,client):
        data={'lat':'59.19896829230591','lng':'18.125666865941504'}
        resp = client.get('/search',query_string=data)
        assert resp.status_code==400 

    def test_request_param_are_not_digits(self,client):
        data={'radius':'500a','count':'b','lat':'59.19896829230591a','lng':'18.125666865941504!'}
        resp = client.get('/search',query_string=data)
        assert resp.status_code==400
    
    def test_request_1_results(self,client):
        data={'radius':'500','count':'1','lat':'59.33258','lng':'18.0649'}
        resp = client.get('/search',query_string=data)
        assert resp.status_code==200
        assert len(resp.json['products'])==1
        assert resp.json=={
                            "products": [
                                {
                                    "popularity": 1.0,
                                    "shop": {
                                        "lat": "59.33113492198011",
                                        "lng": "18.071769320322918"
                                    },
                                    "title": "Presenter/gifts"
                                }
                            ]
                        }
                        
    def test_request_10_results(self,client):
        data={'radius':'500','count':'10','lat':'59.33258','lng':'18.0649'}
        resp = client.get('/search',query_string=data)
        assert resp.status_code==200
        assert len(resp.json['products'])==10