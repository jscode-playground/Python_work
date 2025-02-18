# 데이터 저장 관련
import os
import datetime
import json

import numpy as np

RESULT_PATH = "./tracking/"

def time_formater():
    now = datetime.datetime.now()
    time = now.strftime('%Y/%m/%d %H:%M:%S')
    return time

def make_set(track, label):
    now = time_formater()
    tr = SetData(label, track, now)
    data = tr.change_json()
    save_data(data)

def check_file(file_name):
    # 저장폴더 없을 시 폴더 생성
    if not os.path.exists(RESULT_PATH):
        os.makedirs(RESULT_PATH)
    # 파일 존재 확인 후 명령어 전송
    path = RESULT_PATH + file_name
    if not os.path.exists(path):
        comm = "w"
    else:
        comm = "a"
    return comm


# 파일명 생성
def make_file(m_name:str):
    today = datetime.datetime.now()
    name_str = today.strftime("%Y%m%d_%H_")+m_name+ ".txt"
    return name_str


def save_data(data, m_name):
    file_name = make_file(m_name)
    comm_str = check_file(file_name)
    path = RESULT_PATH + file_name
    with open(path, comm_str) as f:
        f.write(data)
# print(make_file())

class SetData:
    track_id = int
    name = str
    time = str

    def __init__(self, id, name, time):
        self.track_id = id
        self.name=name
        self.time=time

    def change_json(self):
        result = {
            "track_id":self.track_id,
            "name":self.name,
            "time":self.time
        }
        return json.dumps(result)