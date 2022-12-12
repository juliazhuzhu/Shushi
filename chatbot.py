

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

sub_me_msg = '''
    {
        "sub":{
            "id":"3",
            "topic":"me",
            "get":{
                "what":"desc sub"
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
                        }
                    },
                    "private":{
                        "comment":"grp6tFxXbHdyuM"
                    }
                }
            }
        }
        '''
async def send_msg_and_await_rsp(req_msg, websocket):
    await websocket.send(req_msg)
    response_str = await websocket.recv()
    print('=>' + response_str)
    return response_str

async def wait_meta_msg(websocket):
    response_str = await websocket.recv()
    print('=>' + response_str)
    return response_str


def update_msg_info(msg, uid, grpid, displayname):
    obj = json.loads(msg)
    obj["acc"]["desc"]["public"]["photo"]["data"] = uid
    obj["acc"]["desc"]["public"]["fn"] = displayname
    obj["acc"]["desc"]["private"]["comment"] = grpid
    return json.dumps(obj)

async def main_logic():

    apiKey = 'AQEAAAABAAD_rAp4DJh05a1HAwFT3A6K'
    async with websockets.connect('ws://127.0.0.1:6060//im/v1/channels?apikey=' + apiKey) as websocket:
        print("ws connected to beluga.")
        await send_msg_and_await_rsp(hi_msg, websocket)
        _acc_msg = update_msg_info(acc_msg, "122333", "grp6tFxXbHdyuZ", "xiaoye")
        # print(_acc_msg)
        await send_msg_and_await_rsp(_acc_msg, websocket)
        await send_msg_and_await_rsp(sub_me_msg, websocket)
        await wait_meta_msg(websocket)
        await wait_meta_msg(websocket)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main_logic())
