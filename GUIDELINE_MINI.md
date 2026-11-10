# Guideline gán nhãn ảnh giao thông — bộ train cá nhân

> Áp dụng cho 50 ảnh `dataset/images/train/` và nhãn tương ứng trong `dataset/labels/train/`. ID lớp tuân theo [`data.yaml`](data.yaml) và schema trong [`README.md`](README.md). Các ví dụ dưới đây được chọn từ ảnh và nhãn train hiện có; chúng ghi lại quy tắc cần áp dụng nhất quán, không phải xác nhận độc lập rằng mọi nhãn hiện tại đều đúng.

## 1. Phạm vi và mục tiêu

Gán nhãn các phương tiện giao thông nhìn thấy trong ảnh, nếu phương tiện thuộc một trong bốn lớp quy định và đủ dấu hiệu để nhận diện. Mỗi phương tiện là một đối tượng riêng. Nhãn thể hiện loại phương tiện, không thể hiện màu sắc, hướng di chuyển hay việc xe đang dừng/đỗ.

Không gán người, mô tô/xe máy, xe đạp, biển báo, đèn giao thông, hình xe trên quảng cáo, ảnh phản chiếu hoặc vật thể ngoài bốn lớp. Nếu không thể chắc vật thể là xe thuộc schema hoặc không đủ dấu hiệu phân biệt lớp, không đoán; ghi lại ảnh để rà soát/hỏi giảng viên.

## 2. Schema lớp và ID cố định

| ID | Lớp | Gán cho | Cách phân biệt / không gán cho |
|---:|---|---|---|
| 0 | `car` | Xe con, sedan, SUV, taxi và xe bán tải/cabin nhỏ. | Xe bán tải thuộc `car` theo schema bài lab. Không dùng `car` cho xe tải chở hàng, xe buýt/minibus hoặc van/minivan. |
| 1 | `truck` | Xe tải chở hàng, xe tải thùng và xe đầu kéo. | Dựa trên cấu hình xe chở hàng/thân thùng hoặc đầu kéo. Xe bán tải/cabin nhỏ vẫn là `car`. |
| 2 | `bus` | Xe buýt và minibus có cấu hình chở khách. | Dựa trên thiết kế thân xe và dấu hiệu cấu hình xe buýt/chở khách; minibus chở khách vẫn là `bus`, không chỉ dựa vào kích thước để đổi thành `van`. |
| 3 | `van` | Van/minivan chở hàng hoặc chở người. | Thường có thân cao/dạng hộp và khoang liền với cabin. Van nhỏ không thành `bus` chỉ vì chở người; không dùng `van` cho xe con thông thường. |

### Thứ tự quyết định khi xe dễ nhầm

1. Xác nhận vật thể là xe thật trong cảnh và có đủ phần nhìn thấy để nhận diện.
2. Tìm dấu hiệu cấu tạo thân xe/cabin và cấu hình phương tiện; không dựa riêng vào màu sắc, kích thước trong ảnh, vị trí hay trạng thái.
3. Xe bán tải/cabin nhỏ xếp `car`; xe tải chở hàng/thùng hoặc đầu kéo xếp `truck`.
4. Xe buýt/minibus có cấu hình chở khách xếp `bus`; van/minivan thân cao, dạng hộp xếp `van`.
5. Nếu vẫn không phân biệt được, không tự đặt lớp mới và không đoán. Đánh dấu ảnh để hỏi giảng viên; giữ nguyên schema và ID.

## 3. Quy tắc vẽ bounding box

- **Một xe, một box:** không gộp hai xe cạnh nhau, nối các box hoặc tạo nhiều box cho cùng một xe.
- **Bám phần xe nhìn thấy:** ôm sát thân xe, gồm các bộ phận nhìn thấy thuộc xe; loại phần đường, bóng đổ, khoảng trống và vật thể khác. Không nới box để bao vùng nền.
- **Bị che khuất:** vẽ quanh phần nhìn thấy, không vẽ xuyên qua vật thể che và không ước lượng phần bị khuất. Chỉ gán khi phần hiện ra đủ nhận diện xe và lớp.
- **Bị cắt ở rìa ảnh:** box dừng đúng biên ảnh, không mở rộng ra ngoài khung.
- **Nhỏ/xa/mờ:** chỉ gán nếu nhận ra được là xe và có đủ dấu hiệu phân lớp. Không tạo box cho đốm ảnh không thể nhận diện.
- **Xe gần nhau/chồng lấp:** vẫn vẽ riêng từng xe. Rà điểm giao nhau để box này không ăn sang thân xe bên cạnh.
- **Kiểm tra độ khít:** xem cả bốn cạnh ở mức phóng to phù hợp; tránh box quá rộng, quá thấp/cao, lệch khỏi thân xe hoặc cắt mất phần xe đang nhìn thấy.
- **Giữ quy tắc nhất quán:** áp dụng cùng chuẩn cho xe cùng loại ở tiền cảnh/hậu cảnh và cho mọi ảnh trong tập.

## 4. Ví dụ gắn với ảnh và nhãn train hiện có

Các con số trong ngoặc là số box theo class ID trong file nhãn train hiện tại. Chúng giúp nhận diện các trường hợp cần áp dụng quy tắc; không thay thế việc mở ảnh và kiểm tra từng box.

| Ảnh | Dấu hiệu trong ảnh / nhãn hiện tại | Quy tắc cần áp dụng |
|---|---|---|
| `drive_002.jpg` | File nhãn hiện có 17 `car`, 2 `bus`, 1 `van`; ảnh có nhiều xe và xe cỡ nhỏ dạng minibus. | Phân biệt minibus theo cấu hình chở khách để xếp `bus`; van thân hộp xếp `van`. Không lấy kích thước nhỏ làm tiêu chí duy nhất. Mỗi xe có box riêng. |
| `drive_006.jpg` | File nhãn hiện có 16 `car`, 1 `van`; ảnh có xe con và xe thân cao/dạng hộp. | Giữ `van` cho xe có kiểu thân van nhận ra được; không đổi sang `car` chỉ vì kích thước trong ảnh nhỏ. Box chỉ bao thân xe được nhìn thấy. |
| `drive_027.jpg` | File nhãn hiện có 16 `car`, 2 `bus`, 3 `van`; nhiều xe nhỏ và thân cao trong cùng cảnh. | Phân loại từng xe theo kiểu thân/cấu hình: minibus chở khách là `bus`, van/minivan thân hộp là `van`, xe con thông thường là `car`. Khi chi tiết không đủ, không đoán lớp. |
| `drive_042.jpg` | File nhãn hiện có 2 `car`, 1 `truck`, 1 `bus`; xe tải và xe buýt xuất hiện gần nhau trong cảnh. | Tách box theo từng phương tiện; xe chở hàng/thùng là `truck`, xe chở khách dạng buýt là `bus`. Không gộp các xe chỉ vì gần hoặc chồng lấp. Rà riêng mọi xe lớn ở tiền cảnh để tránh bỏ sót. |

Các mô tả trên phản ánh file nhãn của người học hiện tại. Khi rà, nếu ảnh cho thấy quyết định chưa nhất quán với schema, cần sửa nhãn do mình tạo và ghi lại lý do; không coi số lượng box trong file là bằng chứng nhãn đã đúng.

## 5. Hồ sơ nhãn train hiện tại và ưu tiên self-QC

Đếm trực tiếp 50 file trong `dataset/labels/train/` cho kết quả 636 box:

| Lớp | ID | Số box hiện có | Tỷ lệ trong nhãn hiện tại |
|---|---:|---:|---:|
| `car` | 0 | 506 | 79.6% |
| `truck` | 1 | 18 | 2.8% |
| `bus` | 2 | 58 | 9.1% |
| `van` | 3 | 54 | 8.5% |
| **Tổng** |  | **636** | **100%** |

Đây chỉ là thống kê các nhãn đang có, không phải phân bố ground truth. Vì `truck` hiện có ít box nhất, nên rà kỹ các xe chở hàng/đầu kéo để tránh bỏ sót hoặc nhầm với `car`; đồng thời không ép xe con thành `truck` để cân bằng số lượng. Rà `bus` và `van` theo cấu hình thân xe, nhất là minibus và xe thân cao ở xa.

### Checklist xem lại từng ảnh

1. Quét toàn ảnh theo cùng hướng để tìm cả xe ở xa, sát rìa và bị che.
2. Với mỗi xe nhìn thấy, hỏi: có thuộc bốn lớp không; đủ dấu hiệu nhận diện xe và lớp không; đã có đúng một box chưa?
3. Kiểm tra lớp theo bảng schema, không dựa vào màu hoặc mong muốn cân bằng số lượng.
4. Kiểm tra box ôm phần nhìn thấy, không lấy nền, không kéo qua vật che, không tràn khỏi ảnh và không gộp xe.
5. So sánh các xe cùng kiểu giữa nhiều ảnh để đảm bảo quyết định `car`/`truck`/`bus`/`van` nhất quán.
6. Ghi lại ảnh mơ hồ và quyết định/điểm cần hỏi. Không âm thầm thay đổi định nghĩa lớp.

## 6. Định dạng nhãn YOLO và cách đọc tọa độ

Mỗi ảnh train có một file `.txt` cùng basename trong `dataset/labels/train/`; ví dụ `drive_001.jpg` ↔ `drive_001.txt`. Mỗi dòng là một box, đúng năm trường:

```text
class_id x_center y_center width height
```

Ví dụ minh họa định dạng (không phải nhãn tham chiếu của ảnh cụ thể):

```text
0 0.500000 0.500000 0.200000 0.300000
```

Ví dụ trên biểu diễn `car` (ID 0), tâm ở giữa ảnh, rộng 20% chiều rộng ảnh và cao 30% chiều cao ảnh.

| Trường | Ý nghĩa | Quy tắc |
|---|---|---|
| `class_id` | ID lớp nguyên. | Chỉ dùng `0`, `1`, `2`, `3` theo bảng schema; không ghi tên lớp. |
| `x_center` | Tọa độ tâm theo chiều ngang, chuẩn hóa theo chiều rộng ảnh. | Từ 0 đến 1; 0 là mép trái, 1 là mép phải. |
| `y_center` | Tọa độ tâm theo chiều dọc, chuẩn hóa theo chiều cao ảnh. | Từ 0 đến 1; 0 là mép trên, 1 là mép dưới. |
| `width` | Chiều rộng box chia cho chiều rộng ảnh. | Lớn hơn 0; box nằm trong khung ảnh. |
| `height` | Chiều cao box chia cho chiều cao ảnh. | Lớn hơn 0; box nằm trong khung ảnh. |

Với ảnh rộng `W` pixel và cao `H` pixel, đổi sang góc box pixel như sau:

```text
x_center_px = x_center * W       y_center_px = y_center * H
box_width_px = width * W         box_height_px = height * H
x_min = x_center_px - box_width_px / 2
x_max = x_center_px + box_width_px / 2
y_min = y_center_px - box_height_px / 2
y_max = y_center_px + box_height_px / 2
```

Các góc phải thỏa `0 <= x_min < x_max <= W` và `0 <= y_min < y_max <= H`. Mỗi dòng tương ứng một xe; không thêm tiêu đề. Ảnh không có xe thuộc schema vẫn phải có file `.txt` rỗng. Không được thiếu file hoặc có file nhãn không khớp ảnh.

## 7. Xuất, kiểm tra và đánh giá

Chạy checker cấu trúc từ thư mục gốc repo:

```bash
python tools/check_yolo_labels.py
```

Checker kiểm tra số file so với ảnh, năm cột mỗi dòng, ID lớp, tọa độ normalized và box vượt biên. Checker không thể phát hiện xe bị bỏ sót, nhầm lớp về mặt hình ảnh hay box chưa ôm sát; các lỗi đó cần self-QC bằng mắt.

Sau khi giảng viên phát gold và cho phép đánh giá, chạy:

```bash
python tools/evaluate_annotations.py \
  --student-labels dataset/labels/train \
  --gold-labels gold_train_labels
```

Evaluator ghép một-một các box cùng lớp khi IoU đạt ngưỡng mặc định 0.50. Theo README, cần đồng thời `F1 >= 0.80` và `mean_iou_of_matches >= 0.70`. Dùng `FP`/`FN` để xác định ảnh cần xem lại, nhưng không kết luận nguyên nhân chỉ từ tổng số; mở ảnh và kiểm từng box. Nếu sửa, chỉ sửa nhãn do mình tạo, lưu lại lý do và chạy đánh giá lại. Kết quả này đo chất lượng annotation, không phải mAP của mô hình.

## 8. Quy tắc giữ dữ liệu và split

- Không đổi tên ảnh hoặc thứ tự class ID.
- Nhãn train lưu tại `dataset/labels/train/`; không dùng ảnh/nhãn `eval` để train.
- Không sửa gold labels, không đưa gold train hoặc tài liệu giảng viên vào repo/Colab công khai.
- Không thêm ảnh cá nhân, biển số, dữ liệu khách hàng hoặc dữ liệu nhạy cảm vào bộ bài.
