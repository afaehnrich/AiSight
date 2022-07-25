import homework
import unittest
import json
import pandas as pd
from datetime import datetime


class TestHomework(unittest.TestCase):

    def test_getRawData(self):
        srcUrl = 'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json/'
        rawData = homework.getRawData(srcUrl)
        try:
            json.loads(rawData)
        except:
            self.fail('no valid JSON')

    def test_loadData(self):
        rawData = """{ "records" : [ 
                       {"dateRep" : "20/12/2020" ,
                        "cases" : 12345,
                        "deaths" : 123,
                        "countriesAndTerritories" : "Germany",
                        "popData2020" : "1000000"} ] }"""
        data = homework.transformData(rawData)
        assert data['date'][0] == datetime( year = 2020, month = 12, day = 20)
        assert data['country'][0] == 'Germany'
        assert data['cases per 100000'][0] == 12345/10
        assert data['deaths per 100000'][0] == 123/10
        assert data['cases'][0] == 12345
        assert data['deaths'][0] == 123

    def test_main(self):
        homework.main()
