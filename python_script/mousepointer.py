import asyncio
import websockets
import pyautogui #マウス操作
import threading
import time
from pathlib import Path
import traceback
import sys
import numpy as np

miman=[0,0]
#pyautogui.PAUSE=0.01

async def handle_client(websocket):
    num=[0,0,0]
    try:
        print("クライアント接続OK！！")
        while True:
            message = await websocket.recv()
            print(f"受信メッセージ: {message}")
            #print(f"受信typr：{type(message)}")
            try:
                num=[float(num) for num in message.split(',')]
            except: #NaN対策
                num[0]=0
                num[1]=1
            #await websocket.send(f"エコー: {message}")
            threading.Thread(target=move,args=(num,)).start()
            
    except websockets.exceptions.ConnectionClosed:
        print("クライアントが切断されました")

def move(num):
    #try:
        global miman
        #while True:
        current_x, current_y = pyautogui.position()
        xx=num[0]+miman[0]
        yy=num[1]+miman[1]
        miman=[xx%1,yy%1]
        curr=[int(xx//1),int(yy//1)]
        pyautogui.moveTo(current_x + curr[0], current_y + curr[1])
        pyautogui.move(curr[0],curr[1])
        #pydirectinput.move(curr[0],curr[1])
        if num[2]==1:
            pyautogui.click()
        num=[0,0,0]
    #except:
    #    print(traceback.format_exc())
    #    sys.exit()


async def main():
    #threading.Thread(target=move,daemon=True).start()
    print("めいん！")
    async with websockets.serve(handle_client, "0.0.0.0", 2001):#, ssl=ssl_context):
        print("鯖スタート！")
        await asyncio.Future() # サーバーを永続化

if __name__ == "__main__":
    asyncio.run(main())
    print("クローズド！！")