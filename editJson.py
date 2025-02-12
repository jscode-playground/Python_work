## coco json 형태로 기존의 라벨링 json 파일을 바꾸어준다.
## annotationClass, labelClass -  하위 클래스
import os
import json

from annotationClass import Annotation, a_ids
from labelClass import labels

IMAGE_PATH = "D:\\dataset\\K-Fashion_sun\\Training\\image"  # 이미지 폴더
ORIGIN_PATH = "D:\\dataset\\K-Fashion_sun\\labels"  # 원본라벨링 폴더
COCO_PATH = "D:\\dataset\\K-Fashion_sun\\Training\\labels"  # 수정라벨링 저장 폴더
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
    path = os.path.join(ORIGIN_PATH, file_path)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        return json_data
    else:
        print("파일경로 확인!!")
        return ""



# info:dataset 전체에 대한 정보+파일 연결 정보
def make_info(image_data, date_created):
    info = dict()
    j_file = f'{image_data.get("이미지 식별자")}'+ ".json"
    info["year"] = "2020"
    info["version"] = ""
    info["description"] = "K-Fashion Image dataset"
    info["contributor"] = "AI-hub"
    info["url"] = "./image/"+f'{image_data.get("이미지 식별자")}'+".jpg"
    info["date_created"] = date_created

    return info


def make_img(image_data, date_created):  # image : 이미지 파일 관련 정보
    images = []
    img = dict()
    img["id"] = 0
    img["license"] = 1
    img["file_name"] = f'{image_data.get("이미지 식별자")}'+ ".jpg"
    img["height"] = image_data.get("이미지 높이")
    img["width"] = image_data.get("이미지 너비")
    img["date_captured"] = date_created
    images.append(img)
    return images

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


def find_label(labeling):  # 라벨링 정보 찾기-> 한글 카테고리  switch-> category_id(int)
    # {"스타일":[{"스타일":"밀리터리","서브스타일":"스트리트"}],"아우터":[{"기장":"노말","색상":"브라운","카테고리":"재킷","디테일":["포켓","지퍼","자수"],"소매기장":"긴팔","소재":["우븐"],"프린트":["무지"],"핏":"노멀"}],"하의":[{}],"원피스":[{}],"상의":[{}]}}
    str_label = str
    for key in labeling.keys():
        t_labels = labeling.get(key)[0]
        t_keys = t_labels.keys()
        target = "카테고리"
        if len(t_labels) > 1 and target in t_keys:
            str_label = t_labels[target]

    return switch(str_label)


# 새 딕셔너리로 cocojson 형태 만들기
def remake_coco(info, categories, images, annotations):
    coco = dict()

    coco["info"] = info
    coco["licenses"] = licenses
    coco["categories"] = categories
    coco["images"] = images
    coco["annotations"] = annotations
    return coco

# 새파일 쓰기
def write_coco(file_name, data):
    path = os.path.join(COCO_PATH, file_name)
    if not os.path.exists(COCO_PATH):
        os.makedirs(COCO_PATH)
    with open(path, "w") as f:
        f.write(data)

if __name__=='__main__':
    f_list = os.listdir(ORIGIN_PATH)    #원본라벨링 파일명 리스트
    for file in f_list:
        json_data = read_json(file)
        rect = json_data["데이터셋 정보"].get("데이터셋 상세설명").get("렉트좌표")
        polygon = json_data["데이터셋 정보"].get("데이터셋 상세설명").get("폴리곤좌표")
        image_data = json_data.get("이미지 정보")
        date_created = json_data["데이터셋 정보"].get("파일 생성일자")
        labeling = json_data["데이터셋 정보"].get("데이터셋 상세설명").get("라벨링")

        info = make_info(image_data, date_created)
        categories = labels
        images = make_img(image_data, date_created)
        # annotation 생성 - dict 배열
        annotations = []
        cate_id = find_label(labeling)
        label_list = TARGET_KEYS.keys()
        a_ids.clear()  # annotation id 파일별 리셋
        for key in label_list:
            if rect.get(key)!={}:
                bbox = make_bbox(rect.get(key))
                seg = make_segmentation(polygon.get(key))
                ann = Annotation()
                ann_dic = ann.make_dic(cate_id, bbox, seg)
                annotations.append(ann_dic)

        coco = remake_coco(info, categories, images, annotations)
        json_parsing = json.dumps(coco, ensure_ascii=False)
        write_coco(file, json_parsing)

    # rect, polygon, image_data, date_created, labels= read_json(f_list[0])
    # print(type(rect))
    # cc = check_count(rect)
    # print(cc)
    # # bb = make_bbox(rect.get(cc[0]))
    # # print(bb)

