import asyncio
import websockets
import pyautogui #マウス操作
import ssl
import threading
import time
from pathlib import Path

#mycrt=Path.joinpath(Path(__file__).parent,"cert.pem")
#mykey=Path.joinpath(Path(__file__).parent,"key.pem")
##print(open(mycrt,"r").read())
## SSLコンテキスト（証明書と秘密鍵は適宜パス指定）
#ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
#ssl_context.load_cert_chain(certfile=mycrt, keyfile=mykey)

num=[0,0,0]
miman=[0,0]
pyautogui.PAUSE=0.01

async def handle_client(websocket):
    global num
    try:
        print("クライアント接続OK！！")
        while True:
            message = await websocket.recv()
            print(f"受信メッセージ: {message}")
            #print(f"受信typr：{type(message)}")
            num=[float(num) for num in message.split(',')]
            #await websocket.send(f"エコー: {message}")
            threading.Thread(target=move).start()
            
    except websockets.exceptions.ConnectionClosed:
        print("クライアントが切断されました")

def move():
    global num
    global miman
    #while True:
    current_x, current_y = pyautogui.position()
    xx=num[0]+miman[0]
    yy=num[1]+miman[1]
    miman=[xx%1,yy%1]
    curr=[xx//1,yy//1]
    pyautogui.moveTo(current_x + curr[0], current_y + curr[1])
    if num[2]==1:
        pyautogui.click()
    num=[0,0,0]


async def main():
    #threading.Thread(target=move,daemon=True).start()
    print("めいん！")
    async with websockets.serve(handle_client, "0.0.0.0", 2001):#, ssl=ssl_context):
        print("鯖スタート！")
        await asyncio.Future() # サーバーを永続化

if __name__ == "__main__":
    asyncio.run(main())
    print("クローズド！！")