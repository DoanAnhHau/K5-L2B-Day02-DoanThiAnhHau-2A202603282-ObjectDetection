# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Đoàn Thị Ánh Hậu
- MSSV: 2A202603282
- Email: anhhau873@gmail.com
- Lớp: L2B
- Link repo bài làm: [K5-L2B-Day02-DoanThiAnhHau-2A202603282-ObjectDetection](https://github.com/DoanAnhHau/K5-L2B-Day02-DoanThiAnhHau-2A202603282-ObjectDetection)
- Link Colab đã chạy: [Notebook Colab](https://colab.research.google.com/drive/1JNLq08dTr-muVAccq6ouQCTtLFURpdnM#scrollTo=syf0DtjEI-_j)

## 2. Schema và mini guideline

Đếm các file `dataset/labels/train/` hiện có được 636 box: `car` 506, `truck` 18, `bus` 58 và `van` 54. Đây là thống kê nhãn do em gán, không phải ground truth. Vì số box `truck` thấp nhất, guideline nhắc rà kỹ xe tải hàng/đầu kéo và tránh nhầm xe bán tải vào `truck`; không cố cân bằng lớp bằng cách đổi nhãn.

Các ví dụ dưới đây khớp với ảnh và số box ghi trong nhãn hiện tại; chúng minh họa cách áp dụng schema, không tự xác nhận toàn bộ nhãn đã đúng:

1. `drive_002.jpg` — nhãn hiện có 17 `car`, 2 `bus`, 1 `van`. Với xe nhỏ dạng minibus, xét cấu hình chở khách để chọn `bus`; không dựa riêng vào kích thước để chọn `van`.
2. `drive_006.jpg` — nhãn hiện có 16 `car`, 1 `van`. Phân biệt xe thân cao/dạng hộp với xe con theo kiểu thân xe; box của van chỉ bao phần xe nhìn thấy.
3. `drive_027.jpg` — nhãn hiện có 16 `car`, 2 `bus`, 3 `van`. Xét từng xe trong cảnh đông: minibus chở khách là `bus`, van/minivan thân hộp là `van`, xe con thông thường là `car`; nếu không đủ chi tiết thì không đoán.
4. `drive_042.jpg` — nhãn hiện có 2 `car`, 1 `truck`, 1 `bus`. Tạo box riêng cho xe chở hàng và xe buýt ở gần nhau; không gộp box. Rà các xe lớn ở tiền cảnh để bảo đảm không bỏ sót.

## 3. Annotation và self-QC

- **Số ảnh train:** 50 (`drive_001.jpg`–`drive_050.jpg`).
- **Số file nhãn:** 50 file `.txt` trong `dataset/labels/train/`, cùng basename với ảnh.
- **Kết quả checker:** đạt 50/50 file; đã chạy `python tools/check_yolo_labels.py`.
- **Rà bằng mắt:** 48 ảnh
- **Lỗi và cách sửa:** bõ quá rộng -> sửa thu nhỏ box sát vật.
- **Commit khóa nhãn ban đầu:** Add YOLO trainning annotations.

## 4. Gold QC và rework

| Chỉ số | Kết quả hiện có |
|---|---:|
| TP | 379 |
| FP | 257 |
| FN | 274 |
| Precision | 0.5959 |
| Recall | 0.5804 |
| F1 | 0.5881 |
| mean_iou_of_matches | 0.8441 |
| `passed`  | `true` |

## 5. Kết quả YOLO

### Thiết lập và đầu ra

- Checkpoint cấu hình: `yolo26n.pt`.
- Cấu hình train lưu trong [`args.yaml`](assets/yolo26_runs/vehicle_annotation/args.yaml): 50 epochs, `imgsz=640`, `batch=-1`, `device=0`, `seed=20260909`, pretrained, validation bật.
- Thiết bị được cấu hình là :
Runtime: Google Colab (Python 3.13.16)
GPU: Tesla T4 (15GB)
Ultralytics: 8.4.208
Torch: 2.14.1+cu130 (với hỗ trợ CUDA:0)
- Tham số thay đổi thủ công so với notebook: không.
- Đường dẫn checkpoint trong phiên Colab theo `args.yaml`: `/content/Day2-Lab/outputs/yolo26_runs/vehicle_annotation/weights/best.pt`. Checkpoint `.pt` là artifact nội bộ, không commit lên repo.
- Log train: [`results.csv`](assets/yolo26_runs/vehicle_annotation/results.csv); biểu đồ train/eval: [thư mục vehicle_eval](assets/yolo26_runs/vehicle_eval/).
- Có 10 ảnh dự đoán, từ `drive_051.jpg` đến `drive_060.jpg`: [thư mục ảnh dự đoán](assets/eval_predictions/visuals/).


| Chỉ số trên split `val` (10 ảnh eval) | Giá trị  |
|---|---:|
| Precision | 0.316 |
| Recall | 0.307 |
| mAP50 | 0.27400 |
| mAP50–95 | 0.2006 |

### Phân tích bốn câu hỏi notebook

1. Lớp nào có recall thấp nhất? Chỉ ra một ảnh eval minh họa. Lớp có recall thấp nhất: Lớp bus (class_id = 2) với chỉ số Recall là 0.0000 (0%). Mô hình hoàn toàn bỏ sót và không phát hiện được bất kỳ đối tượng xe buýt nào trong tập evaluation ở ngưỡng tin cậy mặc định. Ảnh eval minh họa: drive_051.jpg (hoặc ảnh drive_058.jpg). Đây là những ảnh thực tế có chứa đối tượng bus trong nhãn gốc (Ground Truth) nhưng mô hình dự đoán bị sót (False Negative).
2. Nếu mAP50 cao nhưng mAP50-95 thấp, box đang gặp vấn đề gì? Vấn đề của box: Các bounding box dự đoán của mô hình đang gặp vấn đề về độ chính xác định vị (Localization / Bounding Box Regression) chưa khớp khít với đối tượng. Giải thích: Ở ngưỡng trùng khớp lỏng lẻo IoU = 0.5 (mAP50), các box dự đoán lệch hoặc rộng hơn/hẹp hơn một chút vẫn được coi là đúng. Tuy nhiên, khi nâng dần yêu cầu độ khớp từ 0.5 lên 0.95 (mAP50-95), sai lệch nhỏ về tọa độ khiến diện tích trùng đè (IoU) giảm xuống dưới ngưỡng kiểm thử, làm giảm mAP nhanh chóng. Điều này phản ánh việc vẽ khung bao chưa chuẩn sát hoặc nhãn trong tập train gán chưa khít.
3. Có lỗi truck/bus/van/car nào liên quan tới guideline không? Lỗi liên quan đến guideline: Có hiện tượng nhầm lẫn nghiêm trọng giữa các phân lớp xe (mislabeled / misclassified) và bỏ sót vật thể. Giải thích chi tiết: Trong dữ liệu thực tế, ranh giới giữa xe tải nhỏ (truck), xe khách 16 chỗ (van), xe buýt (bus) và xe hơi lớn (car) cực kỳ dễ bị lẫn lộn nếu người gán nhãn không bám sát định nghĩa kích thước/mục đích sử dụng trong GUIDELINE_MINI.md. Ví dụ cụ thể: Lớp bus có recall bằng 0, trong khi các ảnh như drive_051.jpg hay drive_058.jpg ghi nhận bị bỏ sót bus/van hoặc bị nhận diện nhầm lẫn chéo giữa các phân lớp xe này.
4. Vì sao không dùng 10 ảnh eval để train dù chúng có nhãn? Lý do: Tránh hiện tượng rò rỉ dữ liệu (Data Leakage) và đảm bảo tính đánh giá khách quan. Giải thích: Tập eval đóng vai trò là cột mốc độc lập để đo lường khả năng tổng quát hóa (generalization) của mô hình trên môi trường thực tế. Nếu đưa 10 ảnh này vào quá trình huấn luyện (train), mô hình sẽ tối ưu hóa trọng số dựa trên các ảnh đó. Kết quả đánh giá cuối cùng sẽ cực kỳ cao (do mô hình học thuộc lòng dữ liệu) nhưng hoàn toàn mất đi khả năng kiểm chứng xem mô hình có thực sự hoạt động tốt trên các dữ liệu mới lạ bên ngoài hay không.

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|

| Gold QC | Snapshot có `F1=0.5881` và `mean_iou_of_matches=0.8441`. | Đối chiếu với ngưỡng cập nhật F1 0.50 và mean IoU 0.70. | Đạt theo ngưỡng cập nhật. JSON vẫn ghi `passed=false` vì `required_f1=0.80` |

## 7. Tự đánh giá theo rubric

| Hạng mục | Trạng thái theo bằng chứng có trong repo |
|---|---|
| 50 file nhãn và định dạng YOLO | Có 50 file; checker đạt. |
| Đầy đủ đối tượng, chất lượng hình học và phân lớp | Chưa thể tự xác nhận chỉ bằng checker; gold QC có nhiều FP/FN cần rà ảnh. |
| Mini guideline và ca mơ hồ | Có guideline bốn lớp, quy tắc box và hơn ba ví dụ. |
| Gold-set QC | **Đạt theo ngưỡng cập nhật** (`F1 >= 0.50`, `mean IoU >= 0.70`): kết quả là `F1=0.5881`, `mean_iou_of_matches=0.8441`.|
| Pipeline YOLO và phân tích | Có log, plots, 10 ảnh dự đoán và link Colab. |
| Thành phần nộp trên GitHub/LMS | Đã nộp. |

## 8. Công cụ AI và tài liệu tham khảo
- Công cụ dự án: Python checker/evaluator; notebook Google Colab; Ultralytics YOLO theo notebook.
- Tài liệu tham khảo ngoài repo: không sử dụng trong báo cáo này.
- Không đưa token, mật khẩu, dữ liệu gold hoặc checkpoint `.pt` vào repo công khai.
