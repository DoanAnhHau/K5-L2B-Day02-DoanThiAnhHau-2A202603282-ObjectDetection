import cv2
from pathlib import Path

# Đường dẫn dữ liệu
BASE_DIR = Path(__file__).resolve().parent

# Ảnh train
IMAGE_DIR = BASE_DIR / "dataset" / "images" / "train"

# Nhãn Gold nằm ngoài dataset
LABEL_DIR = BASE_DIR / "gold_train_labels"

# Ảnh sau khi vẽ Bounding Box
OUTPUT_DIR = BASE_DIR / "visualized"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Tên class - sửa theo classes.txt của bạn
CLASS_NAMES = {
    0: "car",
    1: "truck",
    2: "bus",
    3: "van",
   
}

# Các định dạng ảnh hỗ trợ
extensions = [".jpg", ".jpeg", ".png"]

for image_path in IMAGE_DIR.iterdir():

    if image_path.suffix.lower() not in extensions:
        continue

    label_path = LABEL_DIR / (image_path.stem + ".txt")

    image = cv2.imread(str(image_path))

    if image is None:
        continue

    height, width = image.shape[:2]

    if label_path.exists():
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            values = line.strip().split()

            if len(values) != 5:
                continue

            class_id = int(float(values[0]))
            x_center, y_center, box_width, box_height = map(float, values[1:])

            # Chuyển tọa độ YOLO sang pixel
            x_center *= width
            y_center *= height
            box_width *= width
            box_height *= height

            x1 = int(x_center - box_width / 2)
            y1 = int(y_center - box_height / 2)
            x2 = int(x_center + box_width / 2)
            y2 = int(y_center + box_height / 2)

            # Vẽ Bounding Box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            class_name = CLASS_NAMES.get(class_id, f"Class {class_id}")

            cv2.putText(
                image,
                class_name,
                (x1, max(y1 - 5, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # Lưu ảnh đã vẽ box
    output_path = OUTPUT_DIR / image_path.name
    cv2.imwrite(str(output_path), image)

    print(f"Da xu ly: {image_path.name}")

print("Hoan thanh! Kiem tra thu muc visualized.")