<<<<<<< ours
# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | | |
| `truck` | | |
| `bus` | | |
| `van` | | |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: ...
- Vật thể bị che khuất: ...
- Vật thể bị cắt bởi rìa ảnh: ...
- Vật thể rất nhỏ/mơ hồ: ...

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_...` | | | |
| `drive_...` | | | |
| `drive_...` | | | |
=======
# Mini guideline — gán nhãn ảnh giao thông

> Áp dụng schema bốn lớp trong `README.md` cho 50 ảnh `dataset/images/train/`. Ghi lại các quyết định dưới đây trước khi gán nhãn và giữ nhất quán trong toàn bộ tập.

## Định nghĩa lớp

| Lớp | Quy tắc gán nhãn | Điểm phân biệt khi xem ảnh |
| --- | --- | --- |
| `car` (ID 0) | Xe con, sedan, SUV, taxi và xe bán tải/cabin nhỏ. | Dáng xe con thông thường hoặc bán tải; không gán xe tải hàng, xe buýt hay van. |
| `truck` (ID 1) | Xe tải chở hàng, xe tải thùng và xe đầu kéo. | Thân/chassis chở hàng lớn hoặc đầu kéo; xe bán tải nhỏ vẫn là `car`. |
| `bus` (ID 2) | Xe buýt và minibus có cấu hình chở khách. | Thân dài/rộng, nhiều cửa sổ hoặc dáng xe buýt; minibus chở khách xếp `bus`. |
| `van` (ID 3) | Van/minivan chở hàng hoặc chở người. | Thân hộp, nóc cao, khoang liền với cabin; van nhỏ gọn không xếp thành `bus`. |

Chỉ gán vật thể là xe thật trong cảnh và thuộc một trong bốn lớp. Không gán mô tô/xe máy, xe đạp, người, biển báo, đèn giao thông, hình xe trên quảng cáo hay ảnh phản chiếu. Xe đang dừng vẫn được gán.

## Quy tắc vẽ box

- Mỗi xe là một box riêng; không gộp các xe gần nhau hoặc chồng lấp.
- Box ôm sát phần thân xe nhìn thấy được, gồm các phần xe nhìn thấy; không lấy mặt đường, bóng đổ hay vật thể bên cạnh.
- Khi xe bị che, vẽ quanh phần nhìn thấy. Không kéo box qua xe đang che khuất.
- Khi xe bị cắt ở rìa ảnh, box kết thúc đúng mép ảnh; không ước lượng phần nằm ngoài khung.
- Chỉ gán xe nhỏ, xa hoặc nhòe khi hình dạng nhìn thấy đủ để nhận ra đó là xe và phân biệt được lớp. Nếu không chắc lớp, không đoán; ghi lại để rà soát/hỏi giảng viên.
- Giữ nguyên thứ tự ID lớp: `car=0`, `truck=1`, `bus=2`, `van=3`.

## Các ca cần chú ý trong ảnh train

| Ảnh | Tình huống quan sát được | Quyết định gán nhãn | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_002.jpg` | Một xe trắng cỡ nhỏ có nhiều cửa sổ, dáng minibus, nằm giữa các xe khác. | Gán `bus` nếu các cửa sổ/thân xe cho thấy cấu hình minibus chở khách; box riêng ôm phần nhìn thấy. | README xếp minibus chở khách vào `bus`; không chỉ dựa vào kích thước nhỏ để gọi là `van`. |
| `drive_006.jpg` | Xe màu xanh nhạt, thân cao và dạng hộp ở phía phải, bị các xe khác che một phần. | Gán `van` nếu phần thân còn thấy đủ nhận ra kiểu van; box chỉ bao quanh phần nhìn thấy. | Dáng van/minivan thuộc `van`; che khuất không phải lý do bỏ nhãn khi vẫn nhận diện được lớp. |
| `drive_027.jpg` | Xe màu sáng, nóc cao và thân hộp trong cụm xe ở giữa ảnh; dễ lẫn với xe con hoặc minibus ở kích thước thu nhỏ. | Gán `van` khi nhìn rõ dáng thân hộp/nóc cao; nếu không đủ chi tiết để phân biệt, phóng to kiểm tra và không tự đoán. | Van/minivan thuộc `van`; minibus có cấu hình chở khách thuộc `bus`, xe con thông thường thuộc `car`. |
| `drive_042.jpg` | Cảnh có xe chở hàng thân lớn và xe buýt/van ở gần nhau. | Tạo box tách riêng; xe thùng chở hàng là `truck`, xe buýt là `bus`, van nhỏ là `van`. | Phân loại theo loại phương tiện, không theo màu hoặc vị trí; không gộp các xe chồng lấp. |

## Tự kiểm tra trước khi xuất nhãn

- Mỗi xe thuộc schema và đủ nhận diện có đúng một box; không bỏ sót xe bị che/cắt nhưng vẫn nhận diện được.
- Box bám thân xe, không bao trùm xe bên cạnh; các box chồng lấp vẫn tách riêng.
- Rà lại các xe thân cao/cỡ nhỏ để nhất quán giữa `car`, `van` và `bus`, và các xe chở hàng để phân biệt `truck` với `car` bán tải.
- Mỗi ảnh có file nhãn cùng tên, ví dụ `drive_001.jpg` ↔ `drive_001.txt`; ảnh không có xe hợp lệ vẫn có file `.txt` rỗng.
- Chạy `python tools/check_yolo_labels.py` từ thư mục gốc repo sau khi hoàn tất.
>>>>>>> theirs
