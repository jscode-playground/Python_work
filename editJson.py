## coco json 형태로 기존의 라벨링 json 파일을 바꾸어준다.
## annotationClass, labelClass -  하위 클래스
import datetime
import os
import json

import numpy as np

from annotationClass import Annotation, a_ids
from labelClass import labels

IMAGE_PATH = "D:\\dataset\\K-Fashion_sun\\Training\\image"  # 이미지 폴더
ORIGIN_PATH = "D:\\dataset\\K-Fashion_sun\\labels"  # 원본라벨링 폴더
COCO_PATH = "D:\\dataset\\K-Fashion_sun\\Training\\image"  # 수정라벨링 저장 폴더
licenses = [
    {
        "id": 1,
        "url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "name": "Public Domain"
    }
]
TARGET_KEYS= {"아우터":0, "상의":0}   # dataset 중 필요한 라벨링 정보 카테고리

# 불러온 json에서 dataset 정보만 분리


# 파일 불러오기 -> json 불러오기
def read_json(file_path):
    for tk in TARGET_KEYS.keys():   # 파일 읽을때마다 Target_keys 리셋
        TARGET_KEYS[tk] = 0
    path = os.path.join(ORIGIN_PATH, file_path)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data
    else:
        print("파일경로 확인!!")
        return ""



# info:dataset 전체에 대한 정보+파일 연결 정보
def make_info():
    info = dict()
    now = datetime.datetime.now()
    info["year"] = "2020"
    info["version"] = ""
    info["description"] = "K-Fashion Image dataset"
    info["contributor"] = "AI-hub"
    #info["url"] = "./image/"+f'{image_data.get("이미지 식별자")}'+".jpg"
    info["date_created"] = now.strftime("%Y-%m-%d %H:%M:%S")

    return info


def make_img(data:dict, img_id:int):  # image : 이미지 파일 관련 정보
    image_data = data["이미지 정보"]
    dataset_data = data["데이터셋 정보"]
    img = dict()
    img["id"] = img_id
    img["license"] = 1
    img["file_name"] = f'{image_data.get("이미지 식별자")}'+ ".jpg"
    img["height"] = image_data.get("이미지 높이")
    img["width"] = image_data.get("이미지 너비")
    img["date_captured"] = dataset_data.get("파일 생성일자")
    return img

def check_count(rect): #라벨링 영역 개수 체크
    for key in TARGET_KEYS.keys():
        if rect.get(key)[0]!={}:
            TARGET_KEYS[key]= TARGET_KEYS.get(key)+1

def make_bbox(box_list:[]):  # box 라벨링영역(x,y,w,h)
    # [{"X좌표":220.5,"Y좌표":1.5,"가로":538,"세로":738}]
    dic = box_list[0]
    bbox = []
    for k in dic.keys():
        bbox.append(dic.get(k))
    return bbox


def make_segmentation(box_list:[]):  # segmentation : 폴리곤 좌표영역
    # [{"Y좌표26":720.0,"Y좌표25":712.0,"Y좌표28":740.0,"Y좌표27":726.0,"Y좌표22":652.0,...}]
    dic = box_list[0]
    segmentation =[]
    for i in dic.keys():
        segmentation.append(dic.get(i))
    return segmentation


def switch(str_label: str):  # 한글 카테고리 받아서 category_id(int) 반환
    # 파이썬에 switch문이 없다!!
    match = {
        "코트": 2,
        "재킷": 3,
        "점퍼": 4,
        "패딩": 5,
        "베스트": 7,
        "가디건": 8,
        "짚업": 4,
        "탑": 11,
        "블라우스": 10,
        "티셔츠": 12,
        "니트웨어": 11,
        "셔츠": 12,
        "브라탑": 11,
        "후드티": 12
    }
    return match.get(str_label)


def find_label(json_data:dict):  # 라벨링 정보 찾기-> 한글 카테고리  switch-> category_id(int)
    # {"스타일":[{"스타일":"밀리터리","서브스타일":"스트리트"}],"아우터":[{"기장":"노말","색상":"브라운","카테고리":"재킷","디테일":["포켓","지퍼","자수"],"소매기장":"긴팔","소재":["우븐"],"프린트":["무지"],"핏":"노멀"}],"하의":[{}],"원피스":[{}],"상의":[{}]}}
    labeling=json_data["데이터셋 정보"].get("데이터셋 상세설명").get("라벨링")
    str_label = str
    for key in labeling.keys():
        t_labels = labeling.get(key)[0]
        t_keys = t_labels.keys()
        target = "카테고리"
        if len(t_labels) > 1 and target in t_keys:
            str_label = t_labels[target]

    return switch(str_label)


# 새 딕셔너리로 cocojson 형태 만들기
def remake_coco(images:[], annotations:[]):
    coco = dict()

    coco["info"] =  make_info()
    coco["licenses"] = licenses
    coco["categories"] = labels
    coco["images"] = images
    coco["annotations"] = annotations
    return json.dumps(coco, ensure_ascii=False)

# 새파일 쓰기
def write_coco(file_name, data):
    path = os.path.join(COCO_PATH, file_name)
    if not os.path.exists(COCO_PATH):
        os.makedirs(COCO_PATH)
    with open(path, "w") as f:
        f.write(data)

if __name__=='__main__':
    f_list = os.listdir(ORIGIN_PATH)    #원본라벨링 파일명 리스트
    img_ids = np.array(range(0, len(f_list)))   # img id : 파일번호 0~
    #ano_ids = np.array(range(0, len(f_list)*3)) # 라벨링 아이디 : 3배수
    # images 생성
    images = []
    annotations = []
    label_list = TARGET_KEYS.keys()
    for file, i in zip(f_list, img_ids):
        image_id = int(i)
        json_data = read_json(file)
        image = make_img(json_data, image_id)
        images.append(image)
        # annotation 생성 - dict 배열
        cate_id = find_label(json_data)
        rect = json_data["데이터셋 정보"].get("데이터셋 상세설명").get("렉트좌표")
        polygon = json_data["데이터셋 정보"].get("데이터셋 상세설명").get("폴리곤좌표")
        check_count(rect)
        keys = [k for k, v in TARGET_KEYS.items() if v == 1]
        key = keys[0]
        k_id = image_id
        ann = Annotation(k_id, image_id, cate_id)
        bbox = make_bbox(rect.get(key))
        seg = make_segmentation(polygon.get(key))
        ann_dic = ann.make_dic(bbox, seg)
        annotations.append(ann_dic)

    coco = remake_coco(images, annotations)
    write_coco("annotation.json", coco)


    # rect, polygon, image_data, date_created, labels= read_json(f_list[0])
    # print(type(rect))
    # cc = check_count(rect)
    # print(cc)
    # # bb = make_bbox(rect.get(cc[0]))
    # # print(bb)

