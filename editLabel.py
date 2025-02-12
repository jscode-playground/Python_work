# pip install fiftyone 다양한 오픈 데이터셋을 관리할 수 있는 모듈 설치
# fiftyone launch_app : localhost:5151 웹으로 연결되며 dataset을 감상
import fiftyone as fo

# The directory containing the source images
data_path="D:\\00. 작업\\project02\\K-Fashion_sun"
# The path to the COCO labels JSON file - 생성된 라벨이 저장될 폴더
labels_path="D:\\00. 작업\\project02\\K-Fashion_sun\\115.json"

# Import the dataset
dataset = fo.Dataset.from_dir(
    dataset_type=fo.types.COCODetectionDataset,
    data_path=data_path,
    labels_path=labels_path,
)
if __name__ == "__main__":
    # Ensures that the App processes are safely launched on Windows
    session = fo.launch_app(dataset)
    session.wait()