
import time
import random
import asyncio
import websockets
import json
import uuid

hi_msg = '''
            {
                "hi":{
                    "id":"1",
                    "ver":"0.15.14",
                    "ua":"Mac OS",
                    "dev":"dev",
                    "lang":"Chinese"
                }
            }
        '''

sub_topic_msg = '''
    {
        "sub":{
            "id":"5",
            "topic":"grpCc6q_4C4TJT",
            "get":{
                "desc":{
                    "ims":"2019-11-01T03:14:58.641Z"
                },
                "data":{
                    "limit":48
                },
                "what":"desc sub data"
            }
            
        }
    }
'''

sub_me_msg = '''
    {
        "sub":{
            "id":"3",
            "topic":"me",
            "get":{
                "what":"desc sub data"
            },
            "set":{
                "desc":{
                    "defacs":{
                        "auth":"",
                        "anon":""
                    },
                    "public":{
                        "fn":""
                    },
                    "private":{
                        "comment":""
                    }
                }
            }
        }
    }
    '''

data_msg = '''
    {
        "pub":{
            "id":"7",
            "topic":"grpAkoHHE0u3Tc",
            "content":"{\\"data\\": \\"我是匿名\\", \\"data_version\\": 1, \\"type\\": \\"txt\\"}",
            "noecho":true
        }
    }
    '''

acc_msg = '''
        {
            "acc":{
                "id":"2",
                "scheme":"anonymous",
                "user":"new",
                "login":true,
                "desc":{
                    "public":{
                        "fn":"linlinli",
                        "photo":{
                            "data":"422629990",
                            "type":"uid"
                        },
                        "role":"host" 
                        
                    },
                    
                    "private":{
                        "comment":"grp6tFxXbHdyuM"
                    }
                }
            }
        }
        '''
async def send_msg_and_await_rsp(req_msg, websocket):
    print("<=" + req_msg)
    await websocket.send(req_msg)
    response_str = await websocket.recv()
    print('=>' + response_str)
    return response_str

async def wait_meta_msg(websocket):
    response_str = await websocket.recv()
    print('=>' + response_str)
    return response_str


async def wait_data_msg(websocket):
    while True:
        response_str = await websocket.recv()
        print('=>' + response_str)
        obj = json.loads(response_str)
        if ("ctrl" in obj):
            print(obj["ctrl"]["params"]["what"])
            print(obj["ctrl"]["params"]["count"])
            if obj["ctrl"]["params"]["count"] >= 0 and obj["ctrl"]["params"]["what"] == "data":
                print("all message received!")
                break
    return response_str

def update_acc_msg_info(msg, uid, grpid, displayname, role):
    obj = json.loads(msg)
    obj["acc"]["desc"]["public"]["photo"]["data"] = uid
    obj["acc"]["desc"]["public"]["fn"] = displayname
    obj["acc"]["desc"]["public"]["role"] = role
    obj["acc"]["desc"]["private"]["comment"] = grpid
    return json.dumps(obj)


def update_sub_topic_msg(msg, grpid):
    obj = json.loads(msg)
    obj["sub"]["topic"] = grpid
    return json.dumps(obj)


def update_data_msg(msg, grpid):
    obj = json.loads(msg)
    obj["pub"]["topic"] = grpid
    return json.dumps(obj)

async def main_logic():

    apiKey = 'AQEAAAABAAD_rAp4DJh05a1HAwFT3A6K'
    async with websockets.connect('ws://127.0.0.1:6060//im/v1/channels?apikey=' + apiKey) as websocket:
        print("ws connected to beluga.")
        await send_msg_and_await_rsp(hi_msg, websocket)
        _acc_msg = update_acc_msg_info(acc_msg, "122343", "grpCc6q_4C4TJE", "xiaoye_host", "host")
        # print(_acc_msg)
        rsp = await send_msg_and_await_rsp(_acc_msg, websocket)
        obj = json.loads(rsp)
        userId = obj["ctrl"]["params"]["user"]
        print(userId)
        await send_msg_and_await_rsp(sub_me_msg, websocket)
        await wait_meta_msg(websocket)
        await wait_meta_msg(websocket)
        _sub_topic_msg = update_sub_topic_msg(sub_topic_msg, "grpCc6q_4C4TJE")
        await send_msg_and_await_rsp(_sub_topic_msg, websocket)
        await wait_meta_msg(websocket)
        await wait_meta_msg(websocket)
        await wait_meta_msg(websocket)
        await wait_meta_msg(websocket)
        await wait_meta_msg(websocket)
        await wait_data_msg(websocket)

        _data_msg = update_data_msg(data_msg, "grpCc6q_4C4TJE")
        await send_msg_and_await_rsp(_data_msg, websocket)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main_logic())
