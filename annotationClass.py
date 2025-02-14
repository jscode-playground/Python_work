# coco - annotation  항목 만들기
# "annotations": [
#         {
#             "id": 0, --라벨링 id(순차 부여 0~)
#             "image_id": 0, --고정(images[id]=0)
#             "category_id": 2,---라벨링 결과
#             "bbox": [
#                 45,
#                 2,
#                 85,
#                 85
#             ],--x,y,w,h
#             "area": 7225, --mask.area https://github.com/cocodataset/cocoapi/issues/36
#             : 선택-주석의 영역
#             "segmentation": [],--좌표
#             "iscrowd": 0 -(필수 아님) 이미지에 많은 객체가 포함되어 있는지 여부를 지정
#         },]
import numpy as np

from labelClass import make_idNum
a_ids=[]
def make_imgID():   #객체 생성시마다 배열에 추가
    m_id = 0
    if len(a_ids) == 0:
        a_ids.insert(0,0)
    else:
        m_id = a_ids[-1] + 1
        a_ids.append(m_id)
    return m_id


class Annotation:
    id = int
    image_id = int
    category_id = int
    bbox = []
    segmentation = []

    def __init__(self, k_id, img_id, cate_id):
        self.id=k_id
        self.image_id = img_id
        self.category_id = cate_id

    def make_dic(self, box, seg):
        dic = dict()
        dic["id"] = self.id
        dic["image_id"] = self.image_id
        dic["category_id"] = self.category_id
        dic["bbox"] = box
        dic["segmentation"] = seg
        return dic