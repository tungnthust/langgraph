*Filename*: Public_584
*TITLE*: HƯỚNG DẪN KHAI BÁO QOS CHO THIẾT BỊ TRUYỀN DẪN VIBA

# Các nhóm nhiệm vụ, giải pháp chủ yếu

## Nhóm 1: Xây dựng Kiến trúc ICT cho đô thị thông minh tỉnh Bắc Giang Các nguyên tắc của kiến trúc ICT cho đô thị thông minh:

Kiến trúc ICT cho đô thị thông minh của tỉnh Bắc Giang được xây dựng theo những

nguyên tắc của Kiến trúc ICT cho đô thị thông minh tại Công văn số 58/BTTTT-KHCN

ngày 11/1/2018 của Bộ Thông tin và Truyền thông về Hướng dẫn các nguyên tắc định

hướng về công nghệ thông tin và truyền thông trong xây dựng đô thị thông minh ở Việt

Nam.

Kiến trúc phục vụ hướng đến các đối tượng ở các khu vực khác nhau: khu vực

công, khu vực tư nhân, khu vực cộng đồng, khu vực của tổ chức thứ ba (các doanh

nghiệp xã hội, tổ chức phi lợi nhuận, tổ chức từ thiện...); có tầm nhìn dài hạn. Kiến trúc

đảm bảo các nguyên tắc sau:

- Phân tầng: Kiến trúc được thiết kế phân tầng (Layered structure), nhóm các chức

năng liên quan đến nhau trong từng tầng. Các chức năng ở một tầng khi làm nhiệm vụ

của mình có thể sử dụng các chức năng mà tầng bên dưới cung cấp.

- Hướng dịch vụ: Kiến trúc dựa trên mô hình hướng dịch vụ (SOA-Service

Oriented Architecture), nghĩa là được phát triển và tích hợp các thành phần chức năng

xoay quanh các quy trình nghiệp vụ.

- Liên thông: Giao diện của mỗi thành phần trong kiến trúc phải được mô tả tường

minh để sẵn sàng tương tác với các thành phần khác trong kiến trúc vào thời điểm hiện

tại và tương lai.

- Khả năng mở rộng: Kiến trúc có thể mở rộng hoặc thu hẹp tùy theo quy mô đô

thị, nhu cầu đối với các dịch vụ và sự thay đổi của các nghiệp vụ trong mỗi đô thị.

- Linh hoạt: Dễ dàng thích ứng với các công nghệ mới để có thể cung cấp nhanh

chóng, linh hoạt các dịch vụ của đô thị thông minh.

- Tính sẵn sàng: Đáp ứng được một cách kịp thời, chính xác và tin cậy các yêu cầu

sử dụng của người dân.

- Đo lường được: Kiến trúc phải được thiết kế thành phần hiển thị thông tin trên

cơ sở phân tích dữ liệu lịch sử, dữ liệu lớn, cho phép các bên liên quan quan sát, theo

dõi được hoạt động của các thành phần cũng như toàn bộ kiến trúc và dự báo được các

hoạt động của các thành phần kiến trúc trong tương lai.

- Phản hồi: Có thành phần chức năng tiếp nhận phản hồi từ người dân - đối tượng

phục vụ của đô thị thông minh.

- Chia sẻ: Các thành phần dữ liệu trong kiến trúc được mô tả tường minh để sẵn

sàng cho việc chia sẻ và khai thác chung.

- An toàn: Kiến trúc có phương án đảm bảo an toàn thông tin cho từng thành phần,

tầng, cũng như toàn bộ kiến trúc.

- Trung lập: Không phụ thuộc nhà cung cấp các sản phẩm, công nghệ ICT, không

thiên vị cũng không hạn chế bất kỳ một công nghệ, sản phẩm nào.

**Xây dựng và sử dụng kiến trúc ICT:**

Trên cơ sở kế thừa và mở rộng từ sơ đồ Kiến trúc Chính quyền điện tử tỉnh Bắc

Giang theo Quyết định số 503/QĐ-UBND ngày 30/03/2017 của Ủy ban nhân dân tỉnh

Bắc Giang về việc phê duyệt Kiến trúc Chính quyền điện tử tỉnh Bắc Giang, phiên bản

1.0. Kiến trúc ICT cho đô thị thông minh tỉnh Bắc Giang được mô tả như sau:

|<image_1>|

**Hình 1: Kiến trúc ICT cho đô thị thông minh tỉnh Bắc Giang**

Sự khác nhau giữa hai mô hình kiến trúc là sự mở rộng lĩnh vực, trong đó Chính

quyền điện tử chỉ là một trong các lĩnh vực ứng dụng thông minh. Trên thực tế nó là

thành phần cốt lõi vì đã và đang được đầu tư triển khai. Mô hình kiến trúc ICT cho đô

thị thông minh tỉnh Bắc Giang được mở rộng công nghệ hiện đại để giúp cho thành phố

thông minh hơn. Đó là Big Data, các hệ thống thiết bị cảm biến ứng dụng công nghệ

IoT, M2M…

Chức năng chính của các thành phần trong kiến trúc ICT cho đô thị thông minh

tỉnh Bắc Giang như sau:

_Người sử dụng:_ Người sử dụng thông qua các kênh giao tiếp để trao đổi và tiếp

nhận kết quả từ các dịch vụ thông minh. Bao gồm người dân, tổ chức, doanh nghiệp,

cán bộ, công chức, viên chức, các cơ quan nhà nước.

_Kênh giao tiếp:_

Kênh giao tiếp là các hình thức, phương tiện qua đó người sử dụng truy cập thông

tin, dịch vụ mà thành phố thông minh cung cấp.

Các kênh giao tiếp chính bao gồm: Trung tâm Hành chính công tỉnh; các

trang/cổng thông tin điện tử; kiosk; điện thoại (cố định hoặc di động), trung tâm hỗ trợ...

_Ứng dụng:_ Là các ứng dụng cung cấp dịch vụ thuộc các lĩnh vực của đời sống xã

hội, trong đó có hệ thống chính quyền điện tử, giáo dục thông minh, y tế thông minh,

giao thông thông minh, nông nghiệp thông minh, năng lượng thông minh, cấp nước

thông minh, thoát nước thông minh, an toàn công cộng… Các ứng dụng này có thể được

xây dựng hoặc phát triển trên nền tảng các ứng dụng lõi có sẵn như các ứng dụng ERP,

bản đồ GIS...

_Nền tảng tích hợp:_ Là dịch vụ nền tảng hay còn gọi là nền tảng tích hợp, cung cấp

các công cụ, dịch vụ dùng chung để phát triển và tích hợp, liên thông các hệ thống dịch

vụ. Trong kiến trúc ICT cho đô thị thông minh đây là tầng trung gian phân tách giữa

tầng ứng dụng, dịch vụ là lớp bên trên xử lý các nghiệp vụ trong các lĩnh vực chuyên

ngành cụ thể, lớp phía dưới được xem là các nguồn thông tin, dữ liệu số chia sẻ để phát

triển các ứng dụng bên trên.

_Dữ liệu:_ Là nguồn tài nguyên số của thành phố thông minh đặc trưng là dữ liệu

lớn (Big Data), được hình thành từ các cơ sở dữ liệu cốt lõi phục vụ công tác quản lý

điều hành của chính quyền, đặc biệt là nguồn dữ liệu phản ánh trạng thái của các hệ

thống kiểm soát, giám sát các hoạt động đô thị, môi trường như giao thông, an toàn, an

ninh… trong kiến trúc ICT cho đô thị thông minh, thông tin sẽ từ các hệ thống cảm biến

(IoT), từ mạng xã hội…

_Hạ tầng trung tâm dữ liệu:_ Hệ thống hạ tầng trung tâm dữ liệu để đảm bảo hoạt

động toàn bộ thành phố thông minh. Về mặt vật lý đây là trung tâm dữ liệu cho thành

phố thông minh. Về mặt công nghệ đây là tầng đám mây cho thành phố thông minh đảm

bảo phục vụ cho các hoạt động của các ứng dụng thành phố thông minh trên các ngành,

lĩnh vực.

_Hạ tầng truyền dẫn:_ Với đặc trưng của mạng viễn thông băng rộng đa dịch vụ

(mạng WAN, 3G/4G, Wifi đô thị...) đảm bảo sự kết nối toàn bộ các hệ thống công nghệ

thông tin cũng như kết nối đến các hệ thống IoT của các ứng dụng thông minh.

_Hệ thống sensor/thiết bị đo, cảm biến:_

Là lớp các thiết bị sensor vật lý để giúp tỉnh nhìn, nghe, đo đếm được các đối tượng

quan sát. Hệ thống các sensor này giống như đầu dây thần kinh để cảm nhận được sự

thay đổi để truyền về trung tâm qua tầng kết nối. Nó có thể là các hệ thống camera giám

sát, các bộ cảm biến, đầu đo của các hệ thống kiểm soát, giám sát các hoạt động đô thị,

môi trường như giao thông, an ninh công cộng, nước thải... Thông tin từ các thiết bị cảm

nhận sẽ được truyền theo công nghệ IoT để xử lý và truyền về đám mây thành phố thông

minh qua mạng kết nối.

Hệ thống Internet of Things (IoT **-** kết nối Internet vạn vật): Đơn giản hóa kết nối,

quản lý các thiết bị đo, cảm biến và cung cấp khả năng giám sát, quản lý, kiểm soát thiết

bị đo, cảm biến và chuyển về hạ tầng đám mây.

Xét về cấu trúc, kiến trúc ICT cho đô thị thông minh tỉnh Bắc Giang cũng bao gồm

các tầng như Kiến trúc chính quyền điện tử (thực chất Chính quyền điện tử là một thành

phần trong mô hình thành phố thông minh). Xây dựng thành phố thông minh sẽ là quá

trình phát triển các thành phần Kiến trúc theo lộ trình và bước đi cụ thể, trên cơ sở ưu

tiên từng lĩnh vực, dịch vụ trong từng giai đoạn.

**Thời gian triển khai:** Giai đoạn 2019 – 2020.

**Nguồn lực đầu tư:** Ngân sách tỉnh.

## Nhóm 2: Đẩy mạnh xây dựng hạ tầng thành phố thông minh

### Xây dựng Trung tâm điều hành thành phố thông minh

Trung tâm điều hành thành phố thông minh tỉnh Bắc Giang xây dựng trên nền tảng

kết cấu hạ tầng điện toán đám mây và trở thành một thành phần cốt lõi của kết cấu hạ

tầng thông minh. Các thông tin được thu thập, lưu trữ từ các hệ thống, thiết bị kỹ thuật,

các ứng dụng của từng ngành, lĩnh vực, địa phương trong tỉnh được truyền về trung tâm

thành kho dữ liệu dùng chung lớn của tỉnh, được tích hợp với các hệ thống phân tích và

xử lý chuyên ngành để đưa ra các báo cáo, dự báo, cảnh báo, giúp ứng cứu, xử lý sự cố

khẩn cấp; hỗ trợ lãnh đạo các cấp ra quyết định điều hành một cách tổng thể, phù hợp

và chính xác.

Trung tâm điều hành thành phố thông minh hoạt động giống như bộ não trung tâm,

kết nối với các lĩnh vực thành phần như giao thông, giáo dục, y tế, nông nghiệp, môi

trường, xây dựng, an ninh, năng lượng… cho một cái nhìn toàn diện, phân tích, xử lý

trên cơ sở dữ liệu thu thập được từ các lĩnh vực và từ các nguồn dữ liệu khác, cho phép

lãnh đạo tỉnh đưa ra quyết định điều hành với thông tin đầy đủ nhất.

Trung tâm điều hành thông minh được xây dựng dựa trên các nguyên tắc chủ yếu:

Khai thác thông tin để ra các quyết định tốt hơn; Dự đoán các vấn đề để chủ động giải

quyết; Phối hợp các tài nguyên và quy trình để hoạt động hiệu quả; Cho phép các nhà

lãnh đạo phục vụ công dân và doanh nghiệp tốt hơn.

**Các yêu cầu cơ bản về Trung tâm điều hành thành phố thông minh:**

Xây dựng Trung tâm điều hành đảm bảo kết cấu hạ tầng và các phương tiện kỹ

thuật công nghệ hiện đại, phù hợp với yêu cầu chức năng, nhiệm vụ của một Trung tâm

điều hành cấp tỉnh đáp ứng một số nội dung cơ bản:

- Cung cấp bức tranh toàn cảnh của tỉnh trên cơ sở tập hợp thông tin, dữ liệu của

tất cả các hệ thống thông minh và các nguồn dữ liệu khác, đồng thời đưa ra các chỉ số

đo lường hoạt động của từng hệ thống (KPI).

- Truy nhập thời gian thực đến các hệ thống ứng dụng thông minh của tỉnh.

- Tích hợp công cụ tương tác và hỗ trợ ra quyết định kịp thời.

- Cung cấp cho công dân điểm truy cập vào các dịch vụ của tỉnh.

- Tối ưu hóa các dịch vụ của tỉnh bằng cách cải thiện hiệu suất và giảm chi phí.

- Quản lý và khắc phục sự cố bằng việc tổ chức phản ứng xử lý nhanh.

- Phân tích và đưa ra các dự báo về các sự kiện tương lai.

**Cấu trúc của hệ thống Trung tâm điều hành thành phố thông minh:**

Cấu trúc của hệ thống Trung tâm điều hành thành phố thông minh được mô tả như

sau:

|<image_2>|

**Hình 2: Cấu trúc của hệ thống Trung tâm điều hành thành phố thông**

**minh**

Hệ thống của Trung tâm điều hành thành phố thông minh thường được chia ra làm

3 cấp:

- Cấp chiến lược: Trung tâm điều hành của thành phố thông minh, phục vụ cho

hoạt động quản lý, chỉ đạo và điều hành của tỉnh.

- Cấp chiến thuật là các Trung tâm điều hành chuyên ngành của các đơn vị cấp

dưới như: giao thông, giáo dục, y tế, nông nghiệp, môi trường, xây dựng…

- Cấp tác nghiệp là các đơn vị hoạt động như bệnh viện, trường học, khu vực giao

thông trọng điểm...

**Các chức năng của Trung tâm điều hành thành phố thông minh:**

Mặc dù có thể ở các cấp điều hành khác nhau nhưng chức năng chung của Trung

tâm điều hành thành phố thông minh phải được kết nối, tích hợp trong một nền tảng

chung để trao đổi và chia sẻ thông tin theo phân cấp và thẩm quyền và phải cung cấp

các chức năng nghiệp vụ sau:

- Giám sát và quản lý các nguồn tài nguyên, các sự kiện và sự cố thông qua thông

tin tiếp nhận phản ánh các tình huống.

- Tối ưu hóa các hoạt động của tỉnh thông qua phân tích sâu sắc về môi trường và

các nguồn lực tỉnh.

- Thực hiện kết nối với các công dân và giải quyết các mối quan tâm của họ thông

qua các công cụ và dịch vụ tương tác với công dân.

- Đảm bảo an toàn trật tự xã hội thông qua phân tích các điểm nóng nguy cơ tội

phạm.

- Tích hợp dữ liệu từ các cơ quan khác nhau thông qua một nền tảng chung (nền

tảng tích hợp).

**Thời gian triển khai:**

Giai đoạn đến 2020:

Xây dựng Trung tâm điều hành thành phố thông minh trên nền tảng kết cấu hạ tầng

điện toán đám mây, với công nghệ hiện đại, đảm bảo kết nối và tích hợp dữ liệu các

ngành, lĩnh vực thành kho dữ liệu lớn (big data) và ứng dụng phần mềm trí tuệ nhân tạo

để phân tích, tổng hợp số liệu, hỗ trợ lãnh đạo các cấp ra quyết định điều hành một cách

tổng thể, phù hợp và chính xác.

Kiện toàn, tổ chức bộ máy vận hành Trung tâm điều hành thành phố thông minh

của tỉnh đáp ứng yêu cầu theo dõi, báo cáo, ứng cứu, xử lý sự cố khẩn cấp, vận hành hạ

tầng kỹ thuật, hỗ trợ ra các quyết định điều phối, cung cấp, trao đổi và chia sẻ thông tin.

Trong giai đoạn thí điểm, Trung tâm điều hành được đặt tại Trung tâm dữ liệu của

tỉnh (do Sở Thông tin và Truyền thông quản lý) để đảm bảo tích hợp với Trung tâm dữ

liệu của tỉnh. Kết thúc giai đoạn thử nghiệm sẽ có đánh giá và đề xuất tổ chức cho phù

hợp với tình hình thực tế.

**Nguồn lực đầu tư:** Ngân sách tỉnh, tỉnh đầu tư xây dựng.

### Xây dựng Trung tâm dữ liệu thành phố thông minh

Xây dựng Trung tâm dữ liệu thành phố thông minh theo tiêu chuẩn hiện đại, đáp

ứng các tiêu chuẩn, quy chuẩn kỹ thuật theo Thông tư số 03/2013/TT-BTTTT ngày

22/01/2013 của Bộ Thông tin và Truyền thông và các tiêu chuẩn quốc tế; đáp ứng mô

hình thành phố thông minh. Đảm bảo xây dựng hệ thống hạ tầng thiết bị và phần mềm,

cơ sở dữ liệu tập trung, thống nhất, phục vụ nhu cầu quản lý và khai thác dữ liệu trong

tỉnh. Bao gồm:

- Xây dựng cơ bản hệ thống phòng máy chủ, hệ thống điện, hệ thống an ninh và

giám sát tường vách, hệ thống báo và chữa cháy tự động; hệ thống cắt - lọc sét và tiếp

địa; hệ thống tủ rack; hệ thống cáp cấu trúc; hệ thống quản trị tập trung, giám sát môi

trường phù hợp theo chuẩn Trung tâm dữ liệu.

- Các hệ thống mạng LAN, WAN, MAN, Internet đảm bảo vận hành ổn định cho

thành phố thông minh.

- Xây dựng hệ thống phần mềm nền tảng trục liên thông kết nối (ESB) nhằm cho

phép các ứng dụng, dịch vụ phần mềm khác nhau; với nhiều kiến trúc, nền tảng và chuẩn

giao tiếp khác nhau trên các hệ điều hành khác nhau có thể liên kết trao đổi thông tin

với nhau.

- Hệ thống phần cứng, phần mềm đảm bảo an toàn bảo mật cho toàn bộ hệ thống

hạ tầng công nghệ thông tin của thành phố thông minh, bao gồm các trang thiết bị cho

hệ thống chuyển mạch trung tâm và quản trị hệ thống mạng, hệ thống kết nối Internet

tốc độ cao nhằm cung cấp các dịch vụ hành chính công cho người dân, cung cấp thông

tin, hệ thống bảo mật như tường lửa, diệt virus, dò quét lỗ hổng… nhằm đảm bảo khả

năng an ninh vào bảo mật cho các hệ thống hoạt động an toàn và hiệu quả.

- Hệ thống lưu trữ và sao lưu: sử dụng công nghệ SAN giúp dễ dàng trong việc

tích hợp, mở rộng, nâng cấp hệ thống. Với các hệ thống lớn, công nghệ mạng SAN hiện

vẫn là công nghệ lưu trữ hàng đầu với những ưu điểm vượt trội như sau:

+ Có khả năng sao lưu dữ liệu với dung lượng lớn và thường xuyên mà không làm

ảnh hưởng đến lưu lượng thông tin trên mạng.

+ SAN đặc biệt thích hợp với các ứng dụng cần tốc độ và độ trễ nhỏ.

+ Dữ liệu luôn ở mức độ sẵn sàng cao.

+ Dữ liệu được lưu trữ thống nhất, tập trung và có khả năng quản lý cao. Có

khả năng khôi phục dữ liệu nếu có xảy ra sự cố.

+ Có khả năng mở rộng tốt trên cả phương diện số lượng thiết bị, dung lượng

hệ thống cũng như khoảng cách vật lý.

+ Mức độ an toàn cao do thực hiện quản lý tập trung cũng như sử dụng các công

cụ hỗ trợ quản lý SAN.

- Đẩy mạnh đầu tư mua sắm phần mềm thương mại (như phần mềm hệ điều hành,

quản trị cơ sở dữ liệu, phần mềm giám sát và quản lý hệ thống, phần mềm bảo mật máy

tính, phần mềm sao lưu/phục hồi số liệu, phần mềm ảo hóa, phần mềm đám mây, phần

mềm trục tích hợp, phần mềm quản lý sự kiện và thông tin bảo mật) phục vụ xây dựng

nền tảng tích hợp, đảm bảo kết nối được dễ dàng và an toàn tất cả các ứng dụng thông

minh của các ngành, lĩnh vực.

- Xây dựng hạ tầng đám mây trung tâm bao gồm phần cứng, phần mềm đảm bảo

cho việc sử dụng, khai thác kết nối của toàn bộ hệ thống công nghệ thông tin của tỉnh.

_Mô hình tổng quan triển khai Trung tâm dữ liệu:_

Trung tâm dữ liệu sẽ triển khai theo mô hình công nghệ trung tâm dữ liệu “xanh”,

trong đó tiêu chí tiết kiệm chi phí điện năng được là một trong những tiêu chí được quan

tâm hàng đầu.

|<image_3>|

**Hình 3: Mô hình tổng quan hệ thống Trung tâm dữ liệu**

Mô hình hệ thống bao gồm các Module:

(a) Module Internet: Là phân hệ cung cấp kết nối Internet cho người dùng và cung

cấp các dịch vụ public ra Internet.

(b) Module WAN: Là phân hệ kết nối các lĩnh vực của thành phố thông minh về

Trung tâm dữ liệu để khai thác và sử dụng các ứng dụng thông minh trong các lĩnh vực

trong Trung tâm dữ liệu.

(c) Chuyển mạch lõi (Core Switch) gồm các thiết bị mạng chuyên dụng (Switch,

Router, Link…) cho phép chuyển dữ liệu lớn, tốc độ cao.

(d) Module máy chủ Server Farm: Gồm hệ thống máy chủ phục vụ cài đặt hệ thống

ứng dụng của Tỉnh.

(e) Module Trung tâm Điều hành là phân hệ tập trung các máy chủ giám sát, quản

trị toàn bộ hệ  thống mạng và bảo mật, cũng như hệ thống máy chủ ứng dụng và database,

SAN trong Trung tâm dữ liệu.

(f) Hạ tầng đám mây trung tâm được ứng dụng công nghệ ảo hóa trên nền tảng hạ

tầng phần cứng tại Trung tâm tích hợp dữ liệu.

(g) Có hai Module Internet và Module WAN, các trang thiết bị mạng, cáp, bao gồm

các thiết bị tường lửa Router kết nối Internet và WAN.

# Các nhóm nhiệm vụ ưu tiên thực hiện

_Đơn vị tính: Tỷ đồng_

<table>
<colgroup>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
<col/>
</colgroup>
<thead>
<tr>
<th rowspan="2">TT</th>
<th rowspan="2">Nhóm
nhiệm
vụ ưu
tiên và
nội dung
chính</th>
<th rowspan="2">Đơn vị
chủ trì</th>
<th rowspan="2">Đơn vị
phối
hợp</th>
<th rowspan="2">Mục
tiêu,
quy mô</th>
<th rowspan="2">Thời
gian
thực
hiện</th>
<th colspan="3">Phân bổ nguồn vốn đầu
tư (dự kiến)</th>
<th rowspan="2">Tổng
đầu
tư</th>
<th rowspan="2">Hình thức
đầu tư</th>
</tr>
<tr>
<th>Ngân
sách
Trung
ương</th>
<th>Ngân
sách
địa
phương</th>
<th>Doanh
nghiệp,
Xã hội
hóa</th>
</tr>
</thead>
<tbody>
<tr>
<td>I</td>
<td colspan="10">Đẩy mạnh xây dựng Chính quyền điện tử và hạ tầng thành phố thông minh</td>
</tr>
<tr>
<td>1</td>
<td>Xây
dựng hệ
thống
thông tin
tương tác
với người
dân trong
thành
phố
thông
minh tích
hợp với
chính
quyền
điện tử
của tỉnh</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Văn
phòng
Ủy ban
nhân
dân
tỉnh;
Các sở,
ban,
ngành,
địa
phương</td>
<td rowspan="2">Mở
rộng
nhiều
kênh
tương
tác giữa
cán bộ
với
người
dân,
doanh
nghiệp
nhằm
tăng
hiệu
quả,
hiệu
suất
trong xử
lý công
việc
góp
phần
hiện đại
hóa báo
cáo,
thống
kê, các
dữ liệu
được
cập nhật
trực
tuyến</td>
<td>2019-
2022</td>
<td></td>
<td>2,00</td>
<td></td>
<td>2,00</td>
<td>Thuê hạ
tầng, dịch
vụ công
nghệ
thông tin
từ các
doanh
nghiệp</td>
</tr>
<tr>
<td>2</td>
<td>Xây
dựng hệ
thống
giám sát,
tự động
phân tích
và cảnh
báo
những
phản ánh
của
người
dân về
chính
quyền
trên</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Văn
phòng
Ủy ban
nhân
dân
tỉnh;
Các sở,
ban,
ngành,
địa
phương</td>
<td>2019-
2022</td>
<td></td>
<td>2,00</td>
<td></td>
<td>2,00</td>
<td>Thuê hạ
tầng, dịch
vụ công
nghệ
thông tin
từ các
doanh
nghiệp</td>
</tr>
<tr>
<td rowspan="2">TT</td>
<td rowspan="2">Nhóm
nhiệm
vụ ưu
tiên và
nội dung
chính</td>
<td rowspan="2">Đơn vị
chủ trì</td>
<td rowspan="2">Đơn vị
phối
hợp</td>
<td rowspan="3">Mục
tiêu,
quy mô
trên
nhiều
lĩnh
vực.
Triển
khai hệ
thống
tại
100%
các sở,
ban,
ngành,
địa
phương
trong
tỉnh.</td>
<td rowspan="2">Thời
gian
thực
hiện</td>
<td colspan="3">Phân bổ nguồn vốn đầu
tư (dự kiến)</td>
<td rowspan="2">Tổng
đầu
tư</td>
<td rowspan="2">Hình thức
đầu tư</td>
</tr>
<tr>
<td>Ngân
sách
Trung
ương</td>
<td>Ngân
sách
địa
phương</td>
<td>Doanh
nghiệp,
Xã hội
hóa</td>
</tr>
<tr>
<td></td>
<td>mạng xã
hội</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>3</td>
<td>Xây
dựng
Kiến trúc
ICT cho
đô thị
thông
minh tỉnh
Bắc
Giang</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Các sở,
ban,
ngành,
địa
phương</td>
<td>Tạo nền
tảng
tổng thể
làm căn
cứ xây
dựng
các
thành
phần,
chức
năng,
giải
pháp và
dịch vụ
ứng
dụng
ICT
trong
việc xây
dựng
thành
phố</td>
<td>2019-
2020</td>
<td></td>
<td>0,50</td>
<td></td>
<td>0,50</td>
<td>Ngân sách
nhà nước</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td>thông
minh</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>4</td>
<td>Xây
dựng
Trung
tâm điều
hành
thành
phố
thông
minh</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Các sở,
ban,
ngành,
địa
phương</td>
<td>Kết nối
dữ liệu
các
ngành,
lĩnh vực
thành
phần
như
giao
thông,
giáo
dục, y
tế, nông
nghiệp,
môi
trường,
xây
dựng,
an ninh,
năng
lượng…
hỗ trợ
lãnh
đạo các
cấp ra
quyết
định
điều
hành
một
cách
tổng
thể, phù
hợp và</td>
<td>2019-
2020</td>
<td></td>
<td>15,00</td>
<td></td>
<td>15,00</td>
<td>Ngân sách
nhà nước</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td>chính
xác</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>5</td>
<td>Xây
dựng
Trung
tâm dữ
liệu
thành
phố
thông
minh</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Các sở,
ban,
ngành,
địa
phương</td>
<td>- Xây
dựng hạ
tầng
thiết bị
tập
trung,
thống
nhất
(máy
chủ,
máy
trạm,
thiết bị
sao lưu,
lưu
trữ…)
làm nền
tảng
cho việc
xây
dựng
thành
phố
thông
minh.
- Hệ
thống
đám
mây
cho
thành</td>
<td>2019-
2021</td>
<td></td>
<td>35,00</td>
<td></td>
<td>35,00</td>
<td>Ngân sách
nhà nước</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td>phố
thông
minh.
- Hệ
thống
mạng
và hệ
thống
an ninh
mạng.
- Hệ
thống
phần
mềm
nền
tảng
cho cơ
sở hạ
tầng
thành
phố
thông
minh,
đảm
bảo kết
nối
được dễ
dàng và
an toàn
tất cả
các ứng
dụng
thông
minh
của các
lĩnh vực</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>6</td>
<td>Xây
dựng
Nền tảng
tích hợp
dữ liệu
thành
phố
thông
minh</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Các sở,
ban,
ngành,
địa
phương</td>
<td>Cung
cấp các
dịch vụ
kết nối,
tích
hợp,
cho
phép
kết nối,
chia sẻ
giữa các
ứng
dụng,
hệ
thống
thông
tin
trong
nội bộ
tỉnh Bắc
Giang,
cũng
như kết
nối với
các hệ
thống
thông
tin, cơ
sở dữ
liệu
quốc
gia của
Chính
phủ, các
Bộ,
ngành
trung
ương và</td>
<td>2019-
2020</td>
<td></td>
<td>10,00</td>
<td></td>
<td>10,00</td>
<td>Ngân sách
nhà nước</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td>với các
địa
phương
khác</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>7</td>
<td>Xây
dựng
Trung
tâm an
toàn
thông tin</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Các sở,
ban,
ngành,
địa
phương</td>
<td>Đảm
bảo an
toàn, an
ninh
mạng,
giám
sát, phát
hiện tấn
công,
cảnh
báo
sớm,
ngăn
chặn
kịp thời
và ứng
cứu các
sự cố
liên
quan
cho các
hệ
thống
thông
tin và
các hệ
thống tự
động
hóa
trong</td>
<td>2020-
2022</td>
<td></td>
<td>18,00</td>
<td></td>
<td>18,00</td>
<td>Ngân sách
nhà nước</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td>các cơ
sở hạ
tầng, dữ
liệu
trọng
yếu của
tỉnh</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>8</td>
<td>Mở rộng
hệ thống
trạm thu
phát sóng
mạng
Wifi</td>
<td>Sở
Thông
tin và
Truyền
thông</td>
<td>Các sở,
ban,
ngành,
địa
phương;
doanh
nghiệp
viễn
thông</td>
<td>Phủ
sóng
Wifi tại
các khu
vực cơ
quan
nhà
nước,
khu vực
di tích,
dịch vụ
công
cộng,
bến xe,
trạm đợi
xe
buýt…
với
khoảng
40
điểm,
nhằm
đảm
bảo lưu
lượng
đường
truyền
mạng
phục vụ
cho hệ
thống</td>
<td>2019-
2022</td>
<td></td>
<td></td>
<td>4,00</td>
<td>4,00</td>
<td>Xã hội hóa</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td>chính
quyền
điện tử,
thành
phố
thông
minh</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>II</td>
<td>Giáo dục
thông
minh</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>1</td>
<td>Xây
dựng lớp
học
tương tác
thông
minh</td>
<td>Sở
Giáo
dục và
Đào
tạo</td>
<td>Phòng
giáo
dục và
đào tạo
các
huyện,
thành
phố;
các
trường
phổ
thông
thuộc
tỉnh</td>
<td>Triển
khai thí
điểm
mô hình
lớp học
thông
minh tại
100
trường
phổ
thông
có điều
kiện
thuận
lợi về
công
nghệ
thông
tin</td>
<td>2019-
2025</td>
<td></td>
<td>1,00</td>
<td>13,00</td>
<td>14,00</td>
<td>Thuê hạ
tầng, dịch
vụ công
nghệ
thông tin
từ các
doanh
nghiệp;
Xã hội hóa</td>
</tr>
<tr>
<td>2</td>
<td>Xây
dựng môi
trường
học tập
trực
tuyến
hiện đại
(e-
learning);</td>
<td>Sở
Giáo
dục và
Đào
tạo</td>
<td>Phòng
giáo
dục và
đào tạo
các
huyện,
thành
phố;
các</td>
<td>Triển
khai thí
điểm tại
5
trường
đại học,
cao
đẳng</td>
<td>2019-
2025</td>
<td></td>
<td></td>
<td>5,00</td>
<td>5,00</td>
<td>Xã hội hóa</td>
</tr>
<tr>
<td></td>
<td>hệ thống
luyện thi
trực
tuyến</td>
<td></td>
<td>trường
đại học,
cao
đẳng
thuộc
tỉnh</td>
<td>trên địa
bàn tỉnh</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>3</td>
<td>Xây
dựng hệ
thống
tuyển
sinh trực
tuyến đầu
cấp</td>
<td>Sở
Giáo
dục và
Đào
tạo</td>
<td>Phòng
giáo
dục và
đào tạo
các
huyện,
thành
phố;
các
trường
học
trong
toàn
tỉnh</td>
<td>Thí
điểm
triển
khai tại
các
trường
học
trong
thành
phố Bắc
Giang;
tiến tới
triển
khai tại
tất cả
các
trường
học
trong
tỉnh
(khoảng
trên 800
trường)</td>
<td>2019-
2025</td>
<td></td>
<td>8,00</td>
<td></td>
<td>8,00</td>
<td>Thuê hạ
tầng, dịch
vụ công
nghệ
thông tin
từ các
doanh
nghiệp</td>
</tr>
<tr>
<td>4</td>
<td>Thẻ học
sinh
thông
minh</td>
<td>Sở
Giáo
dục và
Đào
tạo</td>
<td>Phòng
giáo
dục và
đào tạo
các
huyện,
thành
phố;
các</td>
<td>Triển
khai thí
điểm
thẻ học
sinh
thông
minh
cho 100
trường</td>
<td>2019-
2025</td>
<td></td>
<td></td>
<td>2,50</td>
<td>2,50</td>
<td>Xã hội
hóa; thu
phí người
sử dụng</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td>trường
phổ
thông
thuộc
tỉnh</td>
<td>phổ
thông
có điều
kiện
thuận
lợi về
công
nghệ
thông
tin, với
khoảng
50.000
thẻ</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td>5</td>
<td>Xây
dựng hệ
thống cơ
sở dữ liệu
ngành
giáo dục
và triển
khai tích
hợp các
hệ thống
quản lý
nhà
trường
vào hệ
thống cơ
sở dữ liệu
ngành</td>
<td>Sở
Giáo
dục và
Đào
tạo</td>
<td>Phòng
giáo
dục và
đào tạo
các
huyện,
thành
phố;
các
trường
học
trong
toàn
tỉnh</td>
<td>Toàn
ngành
giáo
dục và
đào tạo
trên địa
bàn
tỉnh,
gồm
khoảng
trên 800
trường</td>
<td>2019-
2025</td>
<td></td>
<td>5,60</td>
<td></td>
<td>5,60</td>
<td>Thuê hạ
tầng, dịch
vụ công
nghệ
thông tin
từ các
doanh
nghiệp</td>
</tr>
</tbody>
</table>