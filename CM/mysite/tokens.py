'''
Created on 2017��4��15��

@author: Administrator
'''
class jwtoken():
    header={
        "type": "JWT",
        "algorithm": "HS256"
        }
    
    playload={ "iss": "Chinese Medinine",
              "iat":0 ,
              "exp": 0,
              "userID":""
              }
