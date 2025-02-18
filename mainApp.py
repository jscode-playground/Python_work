#pip install pyautogui
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware    # CORS 오류 방지 위한 미들웨어 추가
import pyautogui as gui # 키보드 자동화
import os, sys
import cv2
from dotenv import load_dotenv  # 환경변수파일 관리자
from tracking import Tracker
import paho.mqtt.client as mqtt  # 브로커 추가

# 공통 경로/이름 정의(환경변수 값 사용)
load_dotenv()
TOPIC = os.environ.get('TOPIC')
WS_URI = os.environ.get('WS_URI')

# 앱 실행 관련 정의 : fastapi
app = FastAPI()
origin = ["http://192.168.0.212:80", "http://127.0.0.1:80"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
client = mqtt.Client()
client.connect(WS_URI, 1883, 60)
# 연결용 함수
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")


client.on_connect = on_connect

@app.get("/tracking/{sign}")
async def tracking_start(sign:str):
    tr = Tracker()  # cam연결, start
    msg = {}
    if sign == "start":
        msg={"message":"탐지중.... "}
        # comm = "python tracking.py" # 터미널 입력 명령어
        # os.system(comm) #터미널에서 tracking.py 실행
        payload=tr.tracker()
        client.publish(TOPIC, payload)
    elif sign == "end":
        msg = {"message": "탐지 종료.... "}
        tr.change_sign('end')
        client.disconnect()
    return msg




if __name__=='__main__':    # uvicorn main:app --reload
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)