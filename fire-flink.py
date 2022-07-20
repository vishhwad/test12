import time
from aifc import Error

import requests
import json
import sys


class Test_Failed(Error):
    pass

token = sys.argv[1]

def login(token):
    s = requests.Session()
    head = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    head["Authorization"] = "Bearer " + token
    suiteid = 'SUITE1003'
    pes = s.post('https://app.flinko.com:8109/optimize/v1/dashboard/execution/suite/' + suiteid, headers=head)
    out = json.loads(pes.content)
    exid = out['responseObject']['id']

    time.sleep(3)
    sc = 0
    while (sc < 1):
        r1 = s.get('https://app.flinko.com:8109/optimize/v1/dashboard/execution/' + exid, headers=head)
        c1 = json.loads(r1.content)
        fr1 = c1['responseObject']['executionStatus']
        print('status : ' + fr1 + '......')
        if (fr1 == "Completed" or fr1 == "Terminated" or fr1 == "Warning"):
            if fr1 == 'Completed':
                r2 = s.get('https://app.flinko.com:8110/optimize/v1/executionResponse/result/' + exid, headers=head)
                c2 = json.loads(r2.content)
                fr2 = c2['responseObject']['suiteStatus']
                if fr2 == 'FAIL':
                    raise Test_Failed
                else:
                    print("End Result : " + "Test Passed")
                sc = 1
            elif (fr1 == "Terminated" or fr1 == 'Warning'):
                print("End Result : " + fr1)
                sc = 1
        time.sleep(10)

login(token)
