Dự án 2: Thuật toán định tuyến trong miền
Mục tiêu
Triển khai các thuật toán định tuyến distance-vector hoặc link-state.
Bắt đầu
Để bắt đầu dự án này, bạn cần thiết lập môi trường hạ tầng và clone repository này cùng với các submodule:
git clone --recurse-submodules "<repository của bạn>"

Khi có các bản cập nhật cho mã nguồn ban đầu, các trợ giảng (TFs) sẽ mở pull request trong repository của bạn. Bạn nên merge pull request và kéo các thay đổi về máy cục bộ. Có thể bạn sẽ cần giải quyết xung đột thủ công (khi merge PR hoặc khi kéo về máy). Tuy nhiên, hầu hết các trường hợp sẽ không có quá nhiều xung đột nếu bạn không thay đổi các script kiểm tra, hạ tầng, v.v. Nếu gặp khó khăn khi merge, hãy liên hệ với trợ giảng.

Giới thiệu
Internet được tạo thành từ nhiều mạng độc lập (gọi là hệ thống tự trị - autonomous systems) cần hợp tác để các gói tin có thể đến được đích. Điều này đòi hỏi các giao thức và thuật toán khác nhau để định tuyến gói tin trong các hệ thống tự trị (intra-domain) và giữa các hệ thống tự trị (inter-domain), nơi các thỏa thuận kinh doanh và các yếu tố chính sách khác ảnh hưởng đến quyết định định tuyến.

Dự án này tập trung vào các thuật toán định tuyến trong miền được sử dụng bởi các router trong một hệ thống tự trị duy nhất. Mục tiêu của định tuyến trong miền là chuyển tiếp gói tin dọc theo đường đi ngắn nhất hoặc có chi phí thấp nhất qua mạng.

Nhu cầu xử lý nhanh các lỗi router hoặc liên kết bất ngờ, thay đổi chi phí liên kết (thường phụ thuộc vào lưu lượng), và kết nối từ các router và client mới thúc đẩy việc sử dụng các thuật toán phân tán cho định tuyến trong miền. Trong các thuật toán này, các router bắt đầu với trạng thái cục bộ của chúng và phải giao tiếp với nhau để tìm ra các đường đi có chi phí thấp nhất.

Hầu hết các thuật toán định tuyến trong miền được sử dụng trong mạng thực tế thuộc một trong hai loại: distance-vector hoặc link-state. Trong dự án này, bạn sẽ triển khai các thuật toán định tuyến phân tán này bằng Python và kiểm tra chúng với trình mô phỏng mạng được cung cấp.

Lưu ý:
Bạn chỉ cần triển khai distance-vector hoặc link-state. Nếu bạn triển khai cả hai, bạn sẽ nhận được 20 điểm thưởng.

Bạn sẽ thực hiện dự án này trong cùng máy ảo (VM) như dự án trước.

Kiến thức nền tảng
Ở mức độ cao, các thuật toán hoạt động như sau. Mục tiêu của bạn trong dự án này là chuyển đổi mô tả cấp cao này thành mã hoạt động thực tế. Bạn có thể thấy hữu ích khi xem lại chi tiết của các thuật toán trong sách giáo khoa (xem giáo trình khóa học để biết các khuyến nghị về sách giáo khoa).

Distance-Vector Routing
Mỗi router giữ một vector khoảng cách của riêng mình, chứa khoảng cách đến tất cả các đích.
Khi một router nhận được vector khoảng cách từ một router lân cận, nó cập nhật vector khoảng cách của mình và bảng chuyển tiếp.
Mỗi router phát sóng vector khoảng cách của mình đến tất cả các lân cận khi vector khoảng cách thay đổi. Việc phát sóng cũng được thực hiện định kỳ ngay cả khi không có thay đổi được phát hiện.
Mỗi router không phát sóng vector khoảng cách nhận được từ các lân cận. Nó chỉ phát sóng vector khoảng cách của chính mình.
Link-State Routing
Mỗi router giữ trạng thái liên kết của riêng mình và trạng thái liên kết của các nút khác mà nó nhận được. Trạng thái liên kết của một router chứa các liên kết và trọng số của chúng giữa router và các lân cận.
Khi một router nhận được trạng thái liên kết từ một lân cận, nó cập nhật trạng thái liên kết đã lưu trữ và bảng chuyển tiếp. Sau đó, nó phát sóng trạng thái liên kết đến các lân cận khác.
Mỗi router phát sóng trạng thái liên kết của mình đến tất cả các lân cận khi trạng thái liên kết thay đổi. Việc phát sóng cũng được thực hiện định kỳ ngay cả khi không có thay đổi được phát hiện.
Một số thứ tự được thêm vào mỗi thông điệp trạng thái liên kết để phân biệt giữa thông điệp mới và cũ. Mỗi router lưu trữ số thứ tự cùng với trạng thái liên kết. Nếu một router nhận được thông điệp trạng thái liên kết với số thứ tự nhỏ hơn (tức là thông điệp cũ), thông điệp trạng thái liên kết sẽ bị bỏ qua.
Mã nguồn được cung cấp
Làm quen với trình mô phỏng mạng
Mã nguồn được cung cấp triển khai một trình mô phỏng mạng trừu tượng hóa nhiều chi tiết của một mạng thực, cho phép bạn tập trung vào các thuật toán định tuyến trong miền. Mỗi file .json trong thư mục này là một cấu hình cho một mô phỏng mạng khác nhau với số lượng router, liên kết và chi phí liên kết khác nhau. Một số mô phỏng này cũng chứa các thay đổi liên kết (thêm hoặc xóa) xảy ra tại các thời điểm được chỉ định trước.

Trình mô phỏng mạng có thể chạy với hoặc không có giao diện đồ họa. Ví dụ, lệnh:
python visualize_network.py 01_small_net.json

sẽ chạy trình mô phỏng trên một mạng đơn giản với 2 router và 3 client. Mặc định, triển khai router trả lại tất cả lưu lượng qua liên kết mà nó nhận được. Đây rõ ràng là một thuật toán định tuyến tệ, mà bạn sẽ sửa bằng cách triển khai của mình.

Kiến trúc mạng được hiển thị ở phía bên trái của giao diện đồ họa. Router được tô màu đỏ, client được tô màu xanh dương. Mỗi client định kỳ gửi các gói tin "traceroute" màu xám đến tất cả các client khác trong mạng. Các gói tin này ghi nhớ chuỗi các router mà chúng đi qua, và tuyến đường gần đây nhất đến mỗi client được in trong hộp văn bản ở góc trên bên phải. Đây là một công cụ gỡ lỗi quan trọng.

Chi phí của mỗi liên kết được in trên các kết nối.

Nhấp vào một client sẽ ẩn tất cả các gói tin ngoại trừ những gói tin được gửi đến client đó, để bạn có thể thấy đường đi được chọn bởi các router. Nhấp lại vào client sẽ hiển thị tất cả các gói tin.

Nhấp vào một router sẽ in một chuỗi thông tin về router đó trong hộp văn bản ở góc dưới bên phải. Bạn có thể đặt nội dung của chuỗi này để gỡ lỗi triển khai router của mình.

Cùng một mô phỏng mạng có thể được chạy mà không có giao diện đồ họa bằng lệnh sau:

python network.py 01_small_net.json

Mô phỏng sẽ chạy nhanh hơn mà không cần phải hiển thị đồ họa. Nó sẽ dừng sau một khoảng thời gian được xác định trước, in các tuyến đường cuối cùng được các gói tin "traceroute" sử dụng đến và từ tất cả các client, và cho biết liệu các tuyến đường này có đúng với các đường đi có chi phí thấp nhất đã biết qua mạng hay không.

Hướng dẫn triển khai
Nhiệm vụ của bạn là hoàn thành các lớp DVrouter và LSrouter trong các file DVrouter.py và LSrouter.py để chúng triển khai các thuật toán định tuyến distance-vector hoặc link-state tương ứng. Trình mô phỏng sẽ chạy các phiên bản độc lập của các lớp này trong các luồng riêng biệt, mô phỏng các router độc lập trong một mạng.

Bạn sẽ nhận thấy rằng các lớp DVrouter và LSrouter chứa một số phương thức chưa hoàn thành được đánh dấu với TODO. Chúng bao gồm:

__init__
handle_packet
handle_new_link
handle_remove_link
handle_time
__repr__ (tùy chọn, dành cho việc gỡ lỗi của bạn)
Các phương thức này ghi đè các phương thức trong lớp cơ sở Router (trong router.py) và được trình mô phỏng gọi khi một sự kiện tương ứng xảy ra (ví dụ: handle_packet sẽ được gọi khi một phiên bản router nhận được một gói tin).

Lưu ý:
Kiểm tra docstring của các phương thức tương ứng trong lớp cơ sở Router trong router.py để biết mô tả chi tiết.

Ngoài việc hoàn thành từng phương thức này, bạn có thể thêm các trường (biến instance) hoặc phương thức trợ giúp vào các lớp DVrouter và LSrouter.

Bạn sẽ được chấm điểm dựa trên việc liệu các giải pháp của bạn có tìm được các đường đi có chi phí thấp nhất trong trường hợp lỗi và thêm liên kết hay không.

Chạy và kiểm tra
Bạn nên kiểm tra DVrouter và LSrouter của mình bằng trình mô phỏng mạng được cung cấp. Có nhiều file JSON định nghĩa các kiến trúc mạng khác nhau và các thay đổi liên kết. Các file JSON không có _events trong tên file không có thay đổi liên kết và phù hợp để kiểm tra ban đầu.

Để chạy mô phỏng với giao diện đồ họa:

usage: visualize_network.py [-h] net_json_path [{DV,LS}]

Visualize a network simulation.

positional arguments:
  net_json_path  Path to the network simulation configuration file (JSON).
  {DV,LS}        DV for DVrouter and LS for LSrouter. If not provided, Router is used.

options:
  -h, --help     show this help message and exit

Tham số thứ hai có thể là DV hoặc LS, chỉ định chạy DVrouter hoặc LSrouter tương ứng.

Để chạy mô phỏng mà không có giao diện đồ họa:
usage: network.py [-h] net_json_path [{DV,LS}]

Run a network simulation.

positional arguments:
  net_json_path  Path to the network simulation configuration file (JSON).
  {DV,LS}        DV for DVrouter and LS for LSrouter. If not provided, Router is used.

options:
  -h, --help     show this help message and exit

Các tuyến đường đến và từ mỗi client ở cuối mô phỏng sẽ được in ra, cùng với việc liệu chúng có khớp với các tuyến đường tham chiếu có chi phí thấp nhất hay không. Nếu các tuyến đường khớp, triển khai của bạn đã vượt qua bài kiểm tra cho mô phỏng đó. Nếu không, hãy tiếp tục gỡ lỗi (sử dụng các câu lệnh print và phương thức __repr__ trong các lớp router của bạn).

Script bash test_dv_ls.sh sẽ chạy tất cả các mạng được cung cấp với các triển khai router của bạn. Bạn cũng có thể truyền LS hoặc DV làm tham số cho test_dv_ls.sh (ví dụ: .[test_dv_ls.sh](http://_vscodecontentref_/6) DV) để chỉ kiểm tra một trong hai triển khai.

Nộp bài và chấm điểm
Nộp bài
Bạn cần gắn thẻ phiên bản mà bạn muốn chúng tôi chấm điểm bằng các lệnh sau và đẩy nó lên repository của bạn. Bạn có thể học cách sử dụng lệnh gắn thẻ git từ hướng dẫn này. Lệnh này sẽ ghi lại thời gian nộp bài của bạn để chúng tôi chấm điểm.

git tag -a submission -m "Final Submission"
git push --tags

Những gì cần nộp
Bạn cần nộp các tài liệu sau:

Mã nguồn cho DVrouter.py hoặc LSrouter.py.
Điểm thưởng: Nếu bạn nộp cả DVrouter.py và LSrouter.py và chúng vượt qua tất cả các bài kiểm tra, bạn sẽ nhận được 20 điểm thưởng.
Chúng tôi sẽ chạy mô phỏng mạng bằng các file JSON được cung cấp. Điểm của bạn sẽ dựa trên việc liệu thuật toán của bạn có tìm được các đường đi có chi phí thấp nhất hay không và liệu bạn có vi phạm bất kỳ hạn chế nào được liệt kê ở trên hay không. Chúng tôi cũng sẽ kiểm tra rằng DVrouter thực sự chạy một thuật toán distance-vector và LSrouter thực sự chạy một thuật toán link-state.

