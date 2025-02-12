# img 폴더의 파일명을 읽어 리스트로 저장(경로명 예 : "C:\\Users\\jskim\\Desktop\\임시")
# label 폴더에서 파일명과 동일한 이름의 라벨링 파일만 복사하여 저장

# pip install numpy
import os
import shutil
from os import makedirs


# 파일명 리스트 생성
def file_names(folder_path):
    lists = os.listdir(folder_path)
    # 확장자 제거(파일명에 . 들어가면 오류)
    list_names = []
    for file in lists:
        file = file.rsplit(".")[0]
        list_names.append(file)
    return list_names


# 경로확인
def check_dir(folder_path):
    if os.path.exists(folder_path):
        pass
    else:
        makedirs(folder_path)


class SelectFiles:
    img_copied = ""
    label_origin = ""
    label_copied = ""

    def __init__(self, img_copied, label_origin, label_copied):
        self.img_copied = img_copied
        self.label_copied = label_copied
        self.label_origin = label_origin

    # 이미지명과 동일한 이름의 라벨링 파일 찾아 복사
    def find_labels(self):
        img_files = file_names(self.img_copied)  # 이미지 파일명 리스트
        label_files = file_names(self.label_origin)  # 라벨링 파일명 리스트

        for label in label_files:
            if label in img_files:
                copy_file = label + ".json"
                check_dir(self.label_copied)
                shutil.copy(os.path.join(self.label_origin, copy_file), os.path.join(self.label_copied, copy_file))
                # os.path.join : 파라미터만으로 경로 생성
            else:
                pass


if __name__ == '__main__':
    # 작업경로 정의
    img_copied = "D:\\00. 작업\\project02\\K-Fashion_sun\\Training\\image"  # 골라낸 이미지 폴더
    label_origin = "D:\\00. 작업\\project02\\K-Fashion 이미지\\Training\\라벨링데이터\\밀리터리"  # 원본 라벨링 폴더
    label_copied = "D:\\00. 작업\\project02\\K-Fashion_sun\\Training\\labels"  # 골라낸 라벨링 폴더

    f = SelectFiles(img_copied, label_origin, label_copied)
    f.find_labels()
