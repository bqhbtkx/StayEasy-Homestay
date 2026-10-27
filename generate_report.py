from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "Bao_cao_SQA_StayEasy_Waterfall_ISO25010.docx"
IMG = ROOT / "Khách hàng" / "Picture"

doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.8); sec.bottom_margin = Inches(0.75)
sec.left_margin = Inches(0.9); sec.right_margin = Inches(0.75)
sec.header_distance = Inches(0.35); sec.footer_distance = Inches(0.35)

styles = doc.styles
styles['Normal'].font.name = 'Times New Roman'; styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman'); styles['Normal'].font.size = Pt(13); styles['Normal'].font.color.rgb = RGBColor(0,0,0)
styles['Normal'].paragraph_format.line_spacing = 1.15; styles['Normal'].paragraph_format.space_after = Pt(5)
for name, size, color in [('Title', 20, RGBColor(0,0,0)), ('Heading 1', 16, RGBColor(0,0,0)), ('Heading 2', 14, RGBColor(0,0,0)), ('Heading 3', 13, RGBColor(0,0,0))]:
    st=styles[name]; st.font.name='Times New Roman'; st._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); st.font.size=Pt(size); st.font.bold=True; st.font.color.rgb=color
    st.paragraph_format.space_before=Pt(10); st.paragraph_format.space_after=Pt(5)
if 'Caption VN' not in styles:
    st=styles.add_style('Caption VN', WD_STYLE_TYPE.PARAGRAPH); st.font.name='Times New Roman'; st._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); st.font.size=Pt(11); st.font.italic=True; st.font.color.rgb=RGBColor(70,70,70); st.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER; st.paragraph_format.space_after=Pt(7)

def shade(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = tcPr.find(qn('w:shd'))
    if shd is None: shd = OxmlElement('w:shd'); tcPr.append(shd)
    shd.set(qn('w:fill'), fill)
def borders(table, color='D9D9D9'):
    tblPr=table._tbl.tblPr; bd=tblPr.first_child_found_in('w:tblBorders')
    if bd is None: bd=OxmlElement('w:tblBorders'); tblPr.append(bd)
    for edge in ('top','left','bottom','right','insideH','insideV'):
        tag='w:'+edge; el=bd.find(qn(tag))
        if el is None: el=OxmlElement(tag); bd.append(el)
        el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:space'),'0'); el.set(qn('w:color'),color)
def repeat_header(row):
    trPr=row._tr.get_or_add_trPr(); el=OxmlElement('w:tblHeader'); el.set(qn('w:val'),'true'); trPr.append(el)
def cell_text(cell, text, bold=False, size=10.5, color=None):
    cell.text=''; p=cell.paragraphs[0]; p.paragraph_format.space_after=Pt(2); p.paragraph_format.line_spacing=1.0
    r=p.add_run(str(text)); r.bold=bold; r.font.name='Times New Roman'; r._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); r.font.size=Pt(size)
    if color: r.font.color.rgb=RGBColor(*color)
    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
def table(headers, rows, widths=None, size=10.5):
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.autofit=True; borders(t)
    for i,h in enumerate(headers): cell_text(t.rows[0].cells[i], h, True, size, (255,255,255)); shade(t.rows[0].cells[i], '1F4E78')
    repeat_header(t.rows[0])
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for i,val in enumerate(row): cell_text(cells[i], val, False, size)
        if ri%2==1:
            for c in cells: shade(c,'EEF3F8')
    if widths:
        for row in t.rows:
            for i,w in enumerate(widths): row.cells[i].width=Inches(w)
    doc.add_paragraph().paragraph_format.space_after=Pt(1)
    return t
def p(text='', bold_lead=None, align=None):
    para=doc.add_paragraph(); para.paragraph_format.first_line_indent=Inches(0.25); para.paragraph_format.line_spacing=1.15; para.paragraph_format.space_after=Pt(5)
    if align: para.alignment=align
    if bold_lead and text.startswith(bold_lead):
        r=para.add_run(bold_lead); r.bold=True; para.add_run(text[len(bold_lead):])
    else: para.add_run(text)
    return para
def bullets(items):
    for x in items:
        para=doc.add_paragraph(style='List Bullet'); para.paragraph_format.left_indent=Inches(0.35); para.paragraph_format.space_after=Pt(3); para.add_run(x)
def heading(text, level=1):
    doc.add_heading(text, level=level)
def page(): doc.add_page_break()
def caption(text): doc.add_paragraph(text, style='Caption VN')
def add_page_number(paragraph):
    paragraph.alignment=WD_ALIGN_PARAGRAPH.CENTER; run=paragraph.add_run('Trang '); fld=OxmlElement('w:fldSimple'); fld.set(qn('w:instr'),'PAGE'); paragraph._p.append(fld)

# Header/footer
header=sec.header.paragraphs[0]; header.text='STAYEASY HOMESTAY | BÁO CÁO ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM'; header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
header.runs[0].font.name='Times New Roman'; header.runs[0].font.size=Pt(9); header.runs[0].font.color.rgb=RGBColor(90,90,90)
add_page_number(sec.footer.paragraphs[0])

# Bìa
doc.add_paragraph('\n\n\n', style='Normal')
if (IMG/'logo1.png').exists():
    doc.add_picture(str(IMG/'logo1.png'), width=Inches(5.8)); doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    # Alt text for accessibility and screen readers.
    inline = doc.paragraphs[-1]._p.xpath('.//wp:docPr')
    if inline:
        inline[0].set('descr', 'Logo StayEasy Homestay')
        inline[0].set('title', 'Logo StayEasy Homestay')
doc.add_paragraph('TRƯỜNG ĐẠI HỌC ................................................', style='Normal').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('KHOA / BỘ MÔN ................................................', style='Normal').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('\nBÁO CÁO ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM', style='Title').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('HỆ THỐNG ĐẶT PHÒNG HOMESTAY STAYEASY', style='Heading 1').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('Mô hình phát triển Waterfall và tiêu chuẩn ISO/IEC 25010:2011', style='Normal').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('\n\nSinh viên thực hiện: ................................................\nLớp: ................................................\nGiảng viên hướng dẫn: ................................................', style='Normal').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('\nTP. Hồ Chí Minh, tháng 10 năm 2026', style='Normal').alignment=WD_ALIGN_PARAGRAPH.CENTER
page()

# Mục lục
heading('MỤC LỤC',1)
toc=[('1','Giới thiệu dự án StayEasy Homestay'),('1.1','Tổng quan hệ thống'),('1.2','Đối tượng sử dụng và phạm vi'),('1.3','Kiến trúc công nghệ và mã nguồn hiện có'),('1.4','Đội dự án và trách nhiệm chất lượng'),('2','Yêu cầu phần mềm và yêu cầu chất lượng'),('2.1','Yêu cầu nghiệp vụ'),('2.2','Yêu cầu chức năng'),('2.3','Yêu cầu phi chức năng'),('2.4','Ánh xạ yêu cầu với ISO/IEC 25010:2011'),('3','Thiết kế hệ thống và dữ liệu'),('3.1','Kiến trúc tổng thể'),('3.2','Thiết kế cơ sở dữ liệu'),('3.3','Các luồng nghiệp vụ chính'),('4','Mục tiêu chất lượng theo ISO/IEC 25010:2011'),('4.1','Functional suitability'),('4.2','Performance efficiency và Compatibility'),('4.3','Usability và Reliability'),('4.4','Security, Maintainability và Portability'),('5','Quy trình phát triển Waterfall và kế hoạch SQA'),('5.1','Các giai đoạn và cổng chất lượng'),('5.2','Kế hoạch QA, QC và QE'),('5.3','Quản lý cấu hình và thay đổi'),('6','Tiêu chuẩn, thủ tục và tài liệu QA'),('6.1','Chuẩn tài liệu và mã nguồn'),('6.2','Review và kiểm thử'),('6.3','Báo cáo lỗi và cải tiến'),('7','Kế hoạch kiểm thử và test case đại diện'),('7.1','Chiến lược kiểm thử'),('7.2','Ma trận truy xuất yêu cầu'),('7.3','Test case'),('8','Checklist, chỉ số và tiêu chí nghiệm thu'),('9','Công cụ, rủi ro, kết luận và kiến nghị'),('Phụ lục','Danh mục API, tài liệu bàn giao và tài liệu tham khảo')]
for num, title in toc: doc.add_paragraph(f'{num}. {title}', style='Normal')
p('Báo cáo được tổ chức theo cách tiếp cận của tài liệu mẫu: mô tả dự án, xác lập yêu cầu, lựa chọn Waterfall, thiết lập kế hoạch SQA, chuẩn hóa review - testing - tài liệu và kết luận theo các đặc tính chất lượng của ISO/IEC 25010:2011. Nội dung được đối chiếu với mã nguồn StayEasy hiện có trong thư mục dự án.')
page()

# Chương 1
heading('1. GIỚI THIỆU DỰ ÁN STAYEASY HOMESTAY',1)
heading('1.1. Tổng quan hệ thống',2)
p('StayEasy Homestay là ứng dụng web hỗ trợ quản lý hoạt động đặt phòng homestay và lưu trú. Hệ thống phục vụ hai nhóm người dùng chính là khách hàng và quản trị viên. Khách hàng có thể xem các loại hình homestay, chọn căn phòng, kiểm tra tình trạng đã đặt, gửi yêu cầu đặt phòng, theo dõi đơn đặt, cập nhật hồ sơ và xem lịch sử lưu trú. Quản trị viên có thể quản lý danh mục loại phòng, căn phòng, tài khoản khách hàng, đơn đặt, hồ sơ lưu trú, hóa đơn và các chỉ số trên bảng điều khiển.')
p('Mã nguồn hiện thực gồm backend Express chạy trên Node.js, cơ sở dữ liệu MySQL, giao diện HTML/CSS/JavaScript và một dịch vụ chatbot FastAPI tùy chọn. Đây là nền tảng phù hợp để áp dụng quy trình Waterfall vì phạm vi chức năng đã được xác định tương đối rõ, các đầu ra của từng giai đoạn có thể được phê duyệt trước khi chuyển sang giai đoạn kế tiếp.')
table(['Thành phần','Mô tả thực tế trong dự án','Đầu ra kiểm soát chất lượng'],[
['Cổng khách hàng','Trang chủ, đăng nhập/đăng ký, đặt phòng, đơn đã đặt, hồ sơ và lịch sử lưu trú','SRS, UI checklist, system test'],
['Cổng quản trị','Dashboard, quản lý loại phòng, căn phòng, tài khoản, đơn đặt, hồ sơ và lịch sử','Role matrix, admin test cases'],
['Backend API','Express 5, MySQL2, CORS, body-parser, xác thực token và API REST','API checklist, integration test'],
['Chatbot tùy chọn','FastAPI và chatbot tư vấn thông tin homestay','Interface test, availability check'],
['Cơ sở dữ liệu','Các bảng QUANTRIVIEN, KHACHHANG, LOAIPHONG, CANPHONG, DATPHONG, HOSOLUUTRU, LICHSULUUTRU, hoatdong','DB design review, data integrity test']], [1.25,3.1,2.0])
heading('1.2. Đối tượng sử dụng và phạm vi',2)
bullets(['Khách hàng chưa đăng nhập: xem thông tin homestay, tiện nghi và nội dung giới thiệu; có thể chuyển tới chức năng đăng ký hoặc đăng nhập.','Khách hàng đã đăng nhập: đặt phòng, xem đơn, hủy đơn theo điều kiện, cập nhật hồ sơ, đổi mật khẩu và xem lịch sử lưu trú.','Quản trị viên: quản lý dữ liệu vận hành, duyệt/cập nhật trạng thái đơn, quản lý tài khoản và theo dõi dashboard.','Quản lý hệ thống: triển khai Node.js, MySQL và dịch vụ chatbot; kiểm soát cấu hình môi trường, sao lưu và nhật ký hoạt động.'])
heading('1.3. Phạm vi chức năng',2)
table(['Nhóm phạm vi','Bao gồm','Không bao gồm trong phiên bản hiện tại'],[
['Khách hàng','Đăng ký, đăng nhập, xem phòng, đặt phòng, hủy đơn, hồ sơ, lịch sử','Thanh toán trực tuyến, tích hợp OTA'],
['Quản trị','CRUD loại phòng/căn phòng, tài khoản, đơn đặt, hồ sơ, lịch sử, dashboard','Quản lý nhiều chi nhánh độc lập'],
['An toàn','JWT tự cài đặt HS256, PBKDF2-SHA256, rate limit, CORS whitelist, chống IDOR','SSO, MFA, WAF chuyên dụng'],
['Trợ lý','Chatbot cung cấp thông tin dịch vụ và chính sách','Đặt phòng hoàn toàn bằng hội thoại']], [1.2,3.1,2.05])
page()

heading('1.3. Kiến trúc công nghệ và mã nguồn hiện có',2)
p('Frontend được tổ chức theo các thư mục Khách hàng và Quản trị viên. Mỗi nhóm chức năng có HTML, CSS và JavaScript riêng, giúp việc kiểm thử theo module rõ ràng. Backend server.js phục vụ tài nguyên tĩnh, định nghĩa API, kết nối MySQL và áp dụng các middleware xác thực. database.sql khởi tạo schema, khóa ngoại, chỉ mục, view tương thích và dữ liệu mẫu.')
table(['Công nghệ','Vai trò','Điểm cần QA'],[
['Node.js 18+ / Express 5','HTTP server, REST API, static server','HTTP status, validation, error handling, route authorization'],
['MySQL 5.7+/8.x','Lưu trữ người dùng, phòng, booking, lịch sử','Khóa ngoại, unique, index, transaction boundary'],
['HTML/CSS/JavaScript','Giao diện khách và admin','Responsive, thông báo lỗi, XSS ở DOM, tương thích trình duyệt'],
['Python FastAPI','Dịch vụ chatbot tùy chọn','API contract, timeout, graceful degradation'],
['Crypto module','JWT HS256, PBKDF2-SHA256 và so sánh timing-safe','Secret từ môi trường, TTL, không ghi log mật khẩu']], [1.35,2.3,2.7])
p('Các điểm tích hợp quan trọng được lấy từ mã nguồn: POST /register và /login; nhóm API /api/loai-phong, /api/can-phong, /api/dat-phong; nhóm /api/admin/* dành cho quản trị; /api/dashboard và /api/hoatdong phục vụ dashboard và nhật ký. Các route thay đổi dữ liệu đều phải được bao phủ bởi kiểm thử xác thực, phân quyền, dữ liệu hợp lệ và dữ liệu lỗi.')
heading('1.4. Đội dự án và trách nhiệm chất lượng',2)
table(['Vai trò','Trách nhiệm chính','Sản phẩm bàn giao'],[
['Quản lý dự án','Phê duyệt phạm vi, lịch và cổng chất lượng','Baseline, biên bản nghiệm thu'],
['BA/Đặc tả','Chuyển nghiệp vụ đặt phòng thành SRS, tiêu chí chấp nhận','SRS, use case, RTM'],
['Kiến trúc/CSDL','Thiết kế API, luồng, bảng và ràng buộc dữ liệu','SDD, ERD, API contract'],
['Developer','Lập trình theo thiết kế, unit test, sửa lỗi','Mã nguồn, build, unit result'],
['QA/Tester','Review độc lập, viết và thực thi test, báo cáo lỗi','Test plan, test case, defect report'],
['Đại diện người dùng','UAT và xác nhận mức độ phù hợp nghiệp vụ','UAT sign-off']], [1.25,3.0,2.1])
page()

# Ch 2
heading('2. YÊU CẦU PHẦN MỀM VÀ YÊU CẦU CHẤT LƯỢNG',1)
heading('2.1. Yêu cầu nghiệp vụ',2)
table(['Mã','Yêu cầu nghiệp vụ','Tiêu chí chấp nhận'],[
['BR-01','Khách hàng tạo tài khoản và đăng nhập','Số điện thoại duy nhất; đăng nhập đúng trả token; sai trả thông báo an toàn'],
['BR-02','Khách hàng xem loại phòng và căn phòng','Danh sách lọc được theo loại; dữ liệu khớp database'],
['BR-03','Khách hàng đặt phòng trực tuyến','Chọn căn, ngày, giờ, ghi chú; kiểm tra lịch đã đặt trước khi tạo'],
['BR-04','Theo dõi và hủy đơn','Chỉ chủ đơn được xem/hủy; trạng thái cập nhật đúng'],
['BR-05','Quản lý hồ sơ và mật khẩu','Đọc/sửa đúng tài khoản; mật khẩu mới đạt quy tắc'],
['BR-06','Quản trị viên quản lý danh mục và căn','CRUD có kiểm tra khóa ngoại và quyền admin'],
['BR-07','Quản trị viên quản lý đơn đặt','Xem, tạo, cập nhật, xóa theo quy trình và ghi hoạt động'],
['BR-08','Quản lý hồ sơ, lịch sử và dashboard','Số liệu tổng hợp đúng; không lộ dữ liệu trái quyền'],
['BR-09','Chatbot tư vấn homestay','Trả lời đúng dữ liệu cẩm nang; lỗi dịch vụ không làm hỏng cổng web']], [0.7,2.6,3.05])
heading('2.2. Yêu cầu chức năng',2)
table(['Mã','Chức năng','Đầu vào / đầu ra chính'],[
['FR-01','Đăng ký','hoTen, sdt, matKhau -> tài khoản mới hoặc lỗi trùng'],
['FR-02','Đăng nhập','sdt, matKhau -> JWT role, id, iat, exp'],
['FR-03','Tra cứu phòng','id loại hoặc ngày -> danh sách phòng và tiện nghi/giá'],
['FR-04','Đặt phòng','id khách, id căn, loại, ngày/giờ, ghi chú -> DATPHONG'],
['FR-05','Đơn của tôi','JWT và id -> chỉ các đơn của khách hiện tại'],
['FR-06','Hủy đơn','JWT, id đơn -> trạng thái hủy nếu thuộc quyền'],
['FR-07','Hồ sơ/lịch sử','JWT, id khách -> hồ sơ và LICHSULUUTRU'],
['FR-08','Admin CRUD','JWT admin -> loại, căn, tài khoản, đặt, hồ sơ, lịch sử'],
['FR-09','Dashboard','JWT admin -> số liệu tổng quan, đặt theo ngày, activity log']], [0.7,1.65,4.0])
heading('2.3. Yêu cầu phi chức năng',2)
table(['Mã','Đặc tính','Mục tiêu đo lường / tiêu chí'],[
['NFR-01','Hiệu năng','API tra cứu và dashboard p95 <= 2.5 giây trong tải mục tiêu'],
['NFR-02','Bảo mật','Không truy cập được route bảo vệ nếu thiếu/sai token; admin route không cho customer'],
['NFR-03','Tin cậy','Không mất bản ghi sau phản hồi thành công; lỗi DB trả response có kiểm soát'],
['NFR-04','Dễ sử dụng','Luồng đặt phòng hoàn tất trong tối đa 5 bước; lỗi hiển thị rõ bằng tiếng Việt'],
['NFR-05','Tương thích','Chrome, Edge, Firefox bản hiện hành; viewport desktop và mobile'],
['NFR-06','Bảo trì','Module tách theo domain; tên biến camelCase; log và lỗi nhất quán'],
['NFR-07','Di động','Có thể chạy với cấu hình Node/MySQL chuẩn trên môi trường triển khai mới']], [0.8,1.6,3.95])
page()

heading('2.4. Ánh xạ yêu cầu với ISO/IEC 25010:2011',2)
table(['Đặc tính ISO/IEC 25010','Yêu cầu StayEasy','Bằng chứng kiểm tra'],[
['Functional suitability','Đăng nhập, đặt phòng, CRUD admin, chatbot đúng nghiệp vụ','Functional test, UAT, RTM'],
['Performance efficiency','Phản hồi API, tải giao diện, truy vấn index','Load test, timing log, SQL review'],
['Compatibility','Trình duyệt phổ biến, responsive','Cross-browser và viewport test'],
['Usability','Điều hướng rõ, lỗi dễ hiểu, thao tác đặt ngắn','Usability checklist, UAT'],
['Reliability','Xử lý lỗi, trạng thái nhất quán, backup','Recovery test, DB integrity test'],
['Security','JWT, role, PBKDF2, rate limit, CORS, XSS/SQLi','Security checklist, negative test'],
['Maintainability','Cấu trúc file rõ, API nhất quán, code review','Review checklist, static inspection'],
['Portability','Cấu hình qua biến môi trường, triển khai Node/MySQL','Deployment rehearsal, install guide']], [1.45,2.65,2.25])
p('ISO/IEC 25010:2011 được dùng như mô hình chất lượng sản phẩm. IEEE 730 được dùng làm định hướng cho SQA Plan; IEEE 829 được dùng làm định hướng cho test plan, test case, defect report và test summary. Báo cáo không coi các tiêu chuẩn này là thủ tục thay thế cho việc đo kiểm; mỗi mục tiêu đều phải gắn với chỉ số hoặc bằng chứng kiểm thử.')
heading('3. THIẾT KẾ HỆ THỐNG VÀ DỮ LIỆU',1)
heading('3.1. Kiến trúc tổng thể',2)
p('Kiến trúc triển khai gồm trình duyệt của khách/admin, Express API và MySQL. Chatbot chạy độc lập trên FastAPI ở cổng 8000 và được gọi từ giao diện khi người dùng yêu cầu tư vấn. Ranh giới tin cậy được đặt tại middleware authenticateToken và requireAdmin. Dữ liệu chỉ được ghi qua API đã kiểm tra đầu vào, không cho frontend truy cập trực tiếp database.')
table(['Tầng','Thành phần','Trách nhiệm','Điểm kiểm soát'],[
['Presentation','HTML, CSS, JS','Nhập dữ liệu, gọi API, hiển thị trạng thái','Validation UI, XSS-safe rendering, responsive'],
['Application','Express routes/middleware','Xác thực, phân quyền, nghiệp vụ, response','JWT, IDOR, status code, rate limit'],
['Data access','mysql2 pool','Truy vấn parameterized, CRUD','SQL injection, connection error, indexes'],
['Data','MySQL schema','Ràng buộc quan hệ, log hoạt động','FK, unique, not null, backup'],
['External assistant','FastAPI/chatbot','Tư vấn nội dung cẩm nang','Timeout, fallback, API contract']], [1.15,1.45,2.45,1.3])
caption('Hình 1. Mô hình triển khai logic của StayEasy Homestay')
doc.add_paragraph('Trình duyệt khách hàng / quản trị viên  ->  Express API  ->  MySQL\n                                      \\->  FastAPI Chatbot (tùy chọn)', style='Normal').alignment=WD_ALIGN_PARAGRAPH.CENTER
heading('3.2. Thiết kế cơ sở dữ liệu',2)
table(['Bảng','Khóa chính','Quan hệ và mục đích'],[
['QUANTRIVIEN','idQTV','Tài khoản quản trị, số điện thoại unique'],
['KHACHHANG','idKH','Thông tin người dùng, sdt unique'],
['LOAIPHONG','idLoaiPhong','Danh mục loại hình homestay'],
['CANPHONG','idCanPhong','Căn/phòng, FK tới LOAIPHONG'],
['HOSOLUUTRU','idHoSoLuuTru','Hồ sơ lưu trú, FK tới KHACHHANG'],
['DATPHONG','idDatPhong','Đơn đặt; FK tới khách, căn, loại'],
['LICHSULUUTRU','idLichSu','Lịch sử, đánh giá, chi tiết hóa đơn'],
['hoatdong','id','Nhật ký hành động và thời gian']], [1.55,1.1,3.7])
page()

heading('3.3. Các luồng nghiệp vụ chính',2)
heading('Luồng đặt phòng của khách hàng',3)
bullets(['Khách hàng mở trang đặt phòng; frontend tải loại phòng và danh sách căn.','Người dùng chọn ngày/giờ; frontend kiểm tra các căn đã có lịch và hiển thị khả dụng.','Người dùng gửi form; backend xác minh JWT, quyền sở hữu, dữ liệu ngày giờ và trạng thái trùng.','API ghi DATPHONG với trạng thái chờ xác nhận và trả kết quả cho frontend.','Khách hàng xem lại đơn trong trang đơn đã đặt; nếu hủy, backend kiểm tra quyền và cập nhật trạng thái.'])
heading('Luồng xử lý của quản trị viên',3)
bullets(['Admin đăng nhập và nhận token role=admin.','Giao diện dashboard gọi các API tổng hợp; các module quản lý gọi endpoint riêng.','Middleware xác thực token trước, requireAdmin sau; mọi thao tác thay đổi dữ liệu được kiểm tra tham số.','Sau thao tác thành công, hệ thống có thể ghi nhật ký hoatdong và giao diện tải lại dữ liệu.'])
heading('Các ràng buộc dữ liệu cần kiểm thử',3)
bullets(['Không cho tạo khách hàng có số điện thoại đã tồn tại.','Không cho tạo căn phòng với loại phòng không tồn tại.','Không cho xóa loại phòng/căn phòng khi còn bản ghi phụ thuộc nếu không xử lý force theo chính sách.','Khách hàng không được đọc hoặc sửa đơn của người khác dù thay đổi id trên URL.','Token hết hạn, sai chữ ký hoặc role không hợp lệ phải bị từ chối.'])
heading('4. MỤC TIÊU CHẤT LƯỢNG THEO ISO/IEC 25010:2011',1)
heading('4.1. Functional suitability',2)
p('Mục tiêu là các chức năng chính phải đầy đủ, chính xác và phù hợp với quy trình đặt phòng thực tế. Độ phù hợp không chỉ đánh giá việc API trả HTTP 200 mà còn đánh giá trạng thái dữ liệu sau giao dịch, quyền của người thực hiện và thông báo hiển thị trên giao diện.')
table(['Tiêu chí','Mục tiêu','Phương pháp đo','Mức đạt'],[
['Tính đầy đủ','100% BR-01 đến BR-09 có test case','Review RTM và test execution','Không bỏ yêu cầu bắt buộc'],
['Tính chính xác','Kết quả API và DB nhất quán','Functional/integration test','100% case nghiệp vụ chính pass'],
['Tính phù hợp','Luồng người dùng không có bước thừa','UAT và usability test','Đại diện người dùng chấp nhận'],
['Phân quyền nghiệp vụ','Customer/admin đúng phạm vi','Negative test theo role','0 lỗi truy cập trái quyền']], [1.25,2.0,2.35,1.1])
page()

heading('4.2. Performance efficiency và Compatibility',2)
p('Hiệu năng của phiên bản này tập trung vào thời gian phản hồi của API, số lượng truy vấn và khả năng phục vụ các thao tác đồng thời trong phạm vi đồ án. Chỉ số được đo trên môi trường có cấu hình ghi rõ trong Test Summary; không dùng số liệu giả như kết quả triển khai production.')
table(['Chỉ số','Cách đo','Mục tiêu đề xuất'],[
['API tra cứu phòng','100 lần gọi, lấy p50/p95','p95 <= 2.5 giây'],
['API đặt phòng','Tải tuần tự và đồng thời 20 request hợp lệ','Không tạo bản ghi trùng; p95 <= 3 giây'],
['Dashboard admin','Tải 20 lần sau khi seed dữ liệu','p95 <= 3 giây'],
['Tài nguyên server','Theo dõi CPU/RAM trong test','CPU <= 80%, RAM ổn định'],
['Tương thích trình duyệt','Chrome, Edge, Firefox; desktop/mobile','Không lỗi chức năng chính'],
['Responsive','Viewport 390, 768, 1366 px','Không tràn ngang, nút chính nhìn thấy']], [1.5,3.0,1.2])
heading('4.3. Usability và Reliability',2)
p('Tính dễ sử dụng được kiểm tra bằng các luồng hoàn chỉnh: đăng ký, đăng nhập, tìm phòng, đặt phòng, xem đơn và quản trị đơn. Giao diện phải dùng thuật ngữ thống nhất, hiển thị thông báo khi thành công/thất bại và không làm mất dữ liệu nhập khi API lỗi. Tính tin cậy được đánh giá qua khả năng xử lý lỗi kết nối database, token hết hạn, dữ liệu thiếu và thao tác lặp.')
table(['Kịch bản','Kết quả mong đợi','Bằng chứng'],[
['API trả lỗi validation','Frontend hiển thị nguyên nhân có thể sửa','Screenshot/test log'],
['DB tạm thời không khả dụng','Server không crash; trả lỗi kiểm soát','Server log và API response'],
['Refresh sau đặt phòng','Đơn đã tạo chỉ xuất hiện một lần','DB query và UI test'],
['Token hết hạn','Chuyển về đăng nhập hoặc báo phiên hết hạn','Negative test'],
['Màn hình nhỏ','Menu, form và bảng không bị cắt','Viewport screenshots']], [1.7,3.0,1.0])
heading('4.4. Security, Maintainability và Portability',2)
bullets(['Security: JWT ký HS256, TTL, kiểm tra role; PBKDF2-SHA256 100.000 vòng với salt; so sánh timing-safe; rate limit đăng nhập 5 lần/phút/IP; CORS whitelist; parameterized queries; security headers và escapeHtml.','Maintainability: mỗi miền nghiệp vụ có file frontend riêng; server chia helper xác thực, validate và route; tên file phản ánh chức năng; README mô tả khởi chạy và tài khoản mẫu.','Portability: cấu hình port, database và JWT secret qua biến môi trường; có thể cài trên môi trường Node.js/MySQL mới bằng package.json và database.sql.'])
page()

# Ch 5
heading('5. QUY TRÌNH PHÁT TRIỂN WATERFALL VÀ KẾ HOẠCH SQA',1)
heading('5.1. Các giai đoạn và cổng chất lượng',2)
p('Waterfall được áp dụng theo trình tự tuyến tính có kiểm soát. Mỗi giai đoạn có đầu vào, hoạt động, đầu ra và điều kiện phê duyệt. Khi có thay đổi sau baseline, thay đổi phải đi qua quy trình change control; không tự ý sửa yêu cầu trong lúc kiểm thử mà không cập nhật truy xuất.')
table(['Giai đoạn','Hoạt động','Đầu ra','Cổng chất lượng'],[
['1. Phân tích','Thu thập nghiệp vụ, vai trò, phạm vi, rủi ro','Biên bản yêu cầu, scope','Đủ stakeholder và phạm vi'],
['2. Đặc tả','Viết SRS, FR/NFR, acceptance criteria','SRS, RTM bản đầu','Review SRS, không mơ hồ'],
['3. Thiết kế','Kiến trúc, DB, API, UI flow, security design','SDD, ERD, API contract','Review độc lập và trace'],
['4. Lập trình','Code theo SDD, unit test, peer review','Mã nguồn, unit result','Build chạy, checklist đạt'],
['5. Kiểm thử','Integration, system, security, UAT','Test report, defect report','Không còn lỗi blocker/critical'],
['6. Bàn giao','Triển khai, hướng dẫn, backup, nghiệm thu','Release package, manual','UAT sign-off và deployment checklist'],
['7. Bảo trì','Theo dõi lỗi, thay đổi, backup, review sau phát hành','Change log, maintenance report','Mỗi thay đổi có impact review']], [1.05,2.25,1.6,1.85])
caption('Hình 2. Luồng Waterfall: Yêu cầu -> SRS -> Thiết kế -> Code -> Test -> Bàn giao và bảo trì')
heading('5.2. Kế hoạch QA, QC và QE',2)
table(['Hoạt động','QA/QC/QE','Thời điểm','Người chịu trách nhiệm'],[
['Review SRS/SDD','QA phòng ngừa + QC phát hiện lỗi','Sau đặc tả/thiết kế','BA, Architect, QA'],
['Code review','QC và cải tiến maintainability','Trước merge/baseline','Developer, reviewer'],
['Unit/integration test','QC xác nhận từng module và tích hợp','Trong coding','Developer/Tester'],
['System/security test','QC theo yêu cầu ISO','Sau coding hoàn tất','Tester/QA'],
['UAT','QE xác nhận phù hợp người dùng','Trước bàn giao','Đại diện khách hàng'],
['Audit tài liệu','QA bảo đảm quy trình và truy xuất','Mỗi cổng','QA leader']], [1.7,1.8,1.55,1.7])
page()

heading('5.3. Quản lý cấu hình và thay đổi',2)
p('Baseline gồm mã nguồn, database.sql, README, file cấu hình mẫu, tài liệu SRS/SDD/Test Plan và kết quả kiểm thử. Mỗi thay đổi phải ghi mã, lý do, người yêu cầu, ảnh hưởng, quyết định và test hồi quy. Secret thật không được commit; sử dụng .env ở môi trường chạy và giá trị mẫu không nhạy cảm trong tài liệu.')
table(['Bước','Nội dung bắt buộc','Điều kiện đóng'],[
['CR-01','Tạo yêu cầu thay đổi và phân loại khẩn cấp','Có người yêu cầu và mục tiêu rõ'],
['CR-02','Phân tích ảnh hưởng tới SRS, DB, API, test','Có danh sách tài liệu/test cần cập nhật'],
['CR-03','Phê duyệt hoặc từ chối','Có người quyết định và ngày'],
['CR-04','Thực hiện thay đổi trên nhánh riêng','Code review đạt'],
['CR-05','Test chức năng và hồi quy','Case liên quan pass, defect được xử lý'],
['CR-06','Cập nhật baseline và release note','Tài liệu, version và checksum ghi nhận']], [1.0,3.5,2.0])
heading('6. TIÊU CHUẨN, THỦ TỤC VÀ TÀI LIỆU QA',1)
heading('6.1. Chuẩn tài liệu và mã nguồn',2)
bullets(['Tài liệu dùng Times New Roman, cỡ 13 cho nội dung; tiêu đề đánh số 1, 1.1, 1.1.1; bảng có tên, nguồn hoặc phạm vi dữ liệu.','Tên file theo mẫu TenTaiLieu_Version.docx; tài liệu có mã, phiên bản, ngày, tác giả, người review và trạng thái phê duyệt.','JavaScript dùng camelCase cho biến/hàm, PascalCase cho class; hằng số viết hoa; không để code thử nghiệm hoặc mật khẩu thật trong nhánh phát hành.','Mỗi hàm nghiệp vụ nên ngắn, có trách nhiệm rõ; thao tác I/O có xử lý lỗi; truy vấn database dùng tham số; logic xác thực không lặp tùy tiện.','Commit mô tả được mục đích; thay đổi lớn phải có review và test liên quan.'])
table(['Tài liệu','Nội dung tối thiểu','Mã/phiên bản đề xuất'],[
['SQA Plan','Mục tiêu, chuẩn, vai trò, review, test, báo cáo','SQA_Plan_v1.0'],['SRS','BR/FR/NFR, acceptance criteria, trace','SRS_v1.0'],['SDD','Kiến trúc, DB, API, bảo mật, deployment','SDD_v1.0'],['Test Plan','Phạm vi, chiến lược, môi trường, lịch','Test_Plan_v1.0'],['Test Cases','ID, precondition, steps, data, expected, result','Test_Cases_v1.0'],['Defect Report','Mô tả, severity, evidence, owner, status','Defect_Report_v1.0'],['Test Summary','Tổng hợp pass/fail, coverage, residual risk','Test_Summary_v1.0']], [1.45,3.9,1.15])
page()

heading('6.2. Quy trình review',2)
table(['Bước','Thực hiện','Bằng chứng'],[
['1. Chuẩn bị','Xác định artifact, version, reviewer độc lập và checklist','Review request'],
['2. Đọc cá nhân','Reviewer kiểm tra đầy đủ, nhất quán, khả kiểm thử, bảo mật','Comment có mã'],
['3. Tổng hợp','Phân loại finding: blocker, major, minor, observation','Biên bản review'],
['4. Sửa và phản hồi','Tác giả sửa, trả lời từng finding, cập nhật version','Diff và response'],
['5. Xác nhận','Reviewer kiểm tra lại; QA ghi trạng thái đóng','Review sign-off']], [1.2,3.8,1.5])
heading('6.3. Quy trình kiểm thử',2)
bullets(['Phân tích yêu cầu để xác định điều kiện tích cực, tiêu cực và biên.','Thiết kế test case có ID liên kết FR/NFR và tiêu chí pass/fail rõ.','Chuẩn bị database seed, tài khoản customer/admin, trình duyệt và cấu hình API.','Thực thi theo thứ tự unit -> integration -> system -> security -> UAT; ghi kết quả thực tế.','Mở defect có bằng chứng, severity, bước tái hiện và môi trường; sau khi sửa phải re-test và regression test.','Tổng hợp Test Summary, đánh giá residual risk và quyết định release.'])
heading('6.4. Phân loại lỗi và quy tắc đóng',2)
table(['Mức độ','Định nghĩa','Quy tắc xử lý'],[
['Blocker','Không thể khởi động, mất dữ liệu, lộ quyền nghiêm trọng','Không release; xử lý ngay'],['Critical','Sai nghiệp vụ lõi hoặc bypass bảo mật','Phải fix và regression trước UAT'],['Major','Chức năng quan trọng lỗi nhưng có workaround','Không còn lỗi mở khi nghiệm thu'],['Minor','Ảnh hưởng nhỏ, giao diện hoặc thông báo','Có thể ghi kế hoạch bảo trì'],['Observation','Đề xuất cải tiến không chặn release','Theo dõi trong change backlog']], [1.0,3.3,2.2])
heading('6.5. Thủ tục kiểm tra mã nguồn',2)
p('Thủ tục code review áp dụng cho server.js, các module JavaScript frontend và chatbot Python. Reviewer không phải là người duy nhất viết phần thay đổi. Mục tiêu là phát hiện sớm lỗi logic, lỗ hổng quyền, truy vấn không an toàn và vi phạm quy ước trước khi đưa mã vào baseline.')
table(['Bước','Nội dung thực hiện','Bằng chứng'],[
['1','Developer tự kiểm tra, chạy test liên quan và mô tả thay đổi','Commit/PR description'],['2','Reviewer kiểm tra naming, validation, auth, SQL, lỗi và khả năng bảo trì','Code review checklist'],['3','QA đối chiếu thay đổi với yêu cầu và test case','RTM + test link'],['4','Developer sửa finding; reviewer xác nhận từng điểm','Comment resolved + diff'],['5','PM/QA chấp thuận merge vào baseline','Review sign-off']], [0.8,4.1,1.6])
heading('6.6. Thủ tục kiểm thử phần mềm',2)
table(['Bước','Nội dung','Điều kiện hoàn thành'],[
['Chuẩn bị','Chốt version, database seed, tài khoản và môi trường','Environment record đầy đủ'],['Thiết kế','Viết case tích cực, tiêu cực, biên và phân quyền','Case có expected rõ'],['Thực thi','Chạy unit, integration, system, security và UAT','Kết quả actual được ghi'],['Xử lý lỗi','Mở defect, fix, re-test và regression','Defect có trạng thái'],['Kết thúc','Tổng hợp pass rate, lỗi tồn và residual risk','Test Summary được duyệt']], [1.0,3.8,1.7])
heading('6.7. Thủ tục kiểm soát tài liệu',2)
bullets(['Mỗi tài liệu có mã, phiên bản, ngày lập, người soạn, reviewer và trạng thái.','Tài liệu được lưu cùng baseline mã nguồn; không sửa trực tiếp bản đã phê duyệt.','Khi thay đổi yêu cầu hoặc thiết kế, cập nhật SRS/SDD/RTM/test case đồng bộ.','Bản cũ được lưu để truy vết; bản phát hành ghi trong release note.'])
heading('6.8. Thủ tục kiểm soát thay đổi',2)
table(['Giai đoạn','Nội dung','Người chịu trách nhiệm'],[
['Yêu cầu','Ghi lý do, phạm vi, mức ưu tiên và người đề xuất','Requester/BA'],['Phân tích ảnh hưởng','Đánh giá API, DB, UI, bảo mật, test và lịch','BA/Architect/QA'],['Phê duyệt','Chấp thuận, từ chối hoặc hoãn; ghi quyết định','PM/Stakeholder'],['Thực hiện','Tạo branch, code review, test hồi quy','Developer/QA'],['Đóng','Cập nhật baseline, tài liệu và release note','QA/PM']], [1.35,3.75,1.4])
heading('6.9. Thủ tục kiểm thử tự động',2)
p('Các kiểm thử tự động ưu tiên helper xác thực, validate ngày, route đăng nhập, route đặt phòng và các trường hợp phân quyền. Pipeline tối thiểu gồm cài dependency, kiểm tra syntax/lint, chạy unit/integration test và lưu log. Nếu pipeline fail, không merge vào nhánh phát hành cho tới khi có kết quả re-run đạt hoặc được PM phê duyệt ngoại lệ có lý do.')
heading('6.10. Thủ tục báo cáo và phản hồi',2)
table(['Loại báo cáo','Nội dung','Chu kỳ/điểm gửi'],[
['Daily/Progress','Case đã chạy, blocker, rủi ro, kế hoạch','Mỗi buổi kiểm thử'],['Defect report','Mã lỗi, môi trường, bước tái hiện, severity, owner','Ngay khi phát hiện'],['Review report','Finding, quyết định, người xác nhận','Sau mỗi review'],['Test summary','Pass/fail, coverage, defect, rủi ro còn lại','Trước UAT/release'],['Retrospective','Điều làm tốt, chưa tốt, cải tiến','Sau giai đoạn/bàn giao']], [1.3,3.8,1.4])
heading('7. KẾ HOẠCH KIỂM THỬ VÀ TEST CASE ĐẠI DIỆN',1)
heading('7.1. Chiến lược kiểm thử',2)
p('Chiến lược kiểm thử ưu tiên các giao dịch làm thay đổi dữ liệu, ranh giới xác thực và các chức năng có nhiều vai trò. Kiểm thử hộp đen xác nhận hành vi theo SRS; kiểm thử hộp trắng ở mức review tập trung vào nhánh xác thực, validate, truy vấn và xử lý lỗi.')
page()

table(['Cấp độ','Đối tượng','Ví dụ trong StayEasy','Exit criteria'],[
['Unit','Helper và hàm nghiệp vụ','verifyToken, hashPassword, normalizeDateInput','Case helper chính pass'],['Integration','Frontend/API/DB','Đặt phòng ghi DATPHONG và kiểm tra trùng','Không lỗi contract/FK'],['System','Toàn hệ thống','Đăng nhập -> đặt -> xem đơn -> hủy','100% critical path pass'],['Security','Route và dữ liệu','IDOR, role bypass, SQLi, XSS, brute force','0 critical/high mở'],['Compatibility','Trình duyệt/viewport','Customer/admin trên desktop/mobile','Không lỗi chức năng chính'],['UAT','Người dùng đại diện','Đặt một căn, admin xác nhận','Có biên bản chấp nhận']], [1.0,1.45,2.75,1.3])
heading('7.2. Ma trận truy xuất yêu cầu',2)
table(['Yêu cầu','Module/code area','Test case','Bằng chứng'],[
['BR-01 / FR-01','/register, trangchupre','TC-AUTH-01..04','API log + screenshot'],['BR-01 / FR-02','/login, JWT helper','TC-AUTH-05..09','Token/negative result'],['BR-03 / FR-03','order1.js, /api/loai-phong','TC-BOOK-01..04','UI + response'],['BR-03 / FR-04','/api/dat-phong, DATPHONG','TC-BOOK-05..11','DB record + response'],['BR-04 / FR-05/06','donDatUser.js, /api/huy-dat-phong','TC-BOOK-12..15','Ownership test'],['BR-06/07','admin-*.js, /api/admin/*','TC-ADM-01..16','CRUD + role test'],['NFR-02','auth middleware, security headers','TC-SEC-01..10','Security checklist'],['NFR-04/05/06','CSS, UI modules, README','TC-UI-01..08','Viewport screenshots']], [1.25,2.2,1.5,1.55])
heading('7.3. Test case đại diện',2)
table(['ID','Tiền điều kiện / bước chính','Kết quả mong đợi'],[
['TC-AUTH-01','POST /register với sdt mới, mật khẩu hợp lệ','201/200; KHACHHANG tạo; không lộ mật khẩu'],
['TC-AUTH-02','Đăng ký lại cùng sdt','4xx; thông báo trùng; DB không tạo thêm'],
['TC-AUTH-05','POST /login đúng tài khoản customer','Token có role customer và exp hợp lệ'],
['TC-AUTH-07','Sai mật khẩu 5 lần trong 1 phút','Lần tiếp theo bị rate limit; sau thời gian cho phép thử lại'],
['TC-BOOK-03','Truy vấn căn theo loại không tồn tại','Response lỗi/empty có kiểm soát; không crash'],
['TC-BOOK-05','Đặt phòng với token customer hợp lệ','DATPHONG được tạo ở trạng thái chờ xác nhận'],
['TC-BOOK-08','Đặt cùng căn và ngày đã có lịch','Từ chối trùng; không ghi bản ghi mới'],
['TC-BOOK-12','Customer A gọi đơn của Customer B','401/403; không trả dữ liệu của B'],
['TC-ADM-01','Customer gọi POST /api/admin/canphong','403; dữ liệu không thay đổi'],
['TC-ADM-08','Admin cập nhật trạng thái đơn hợp lệ','Dữ liệu đổi đúng và giao diện hiển thị đúng'],
['TC-SEC-04','Nhập ký tự SQL vào trường tìm kiếm','Không thay đổi schema; không trả lỗi SQL nội bộ'],
['TC-UI-03','Mở trang đặt phòng ở 390px','Không tràn ngang; form và nút submit nhìn thấy']], [1.0,3.7,1.8])
page()

heading('8. CHECKLIST, CHỈ SỐ VÀ TIÊU CHÍ NGHIỆM THU',1)
heading('8.1. Checklist review SRS/SDD',2)
table(['STT','Hạng mục kiểm tra','Đạt khi'],[
['1','Mỗi yêu cầu có mã duy nhất','Không trùng/mất mã'],['2','Câu chữ khả kiểm thử','Có điều kiện và kết quả đo'],['3','Phạm vi và out-of-scope rõ','Không lẫn chức năng tương lai'],['4','API có auth/role','Mỗi route bảo vệ được ghi rõ'],['5','Thiết kế DB có FK/index','Quan hệ và ràng buộc khớp database.sql'],['6','Có trace tới test case','Mỗi FR/NFR quan trọng có case'],['7','Rủi ro được đánh giá','Có owner và biện pháp giảm thiểu']], [0.6,3.2,2.7])
heading('8.2. Checklist code và bảo mật',2)
table(['STT','Tiêu chí','Kết quả cần ghi'],[
['1','Tên biến/hàm rõ nghĩa, camelCase','Pass/Findings'],['2','Không có mật khẩu/secret thật trong code','Pass/Findings'],['3','Truy vấn dùng tham số','Pass/Findings'],['4','Route bảo vệ đúng middleware','Pass/Findings'],['5','Kiểm soát IDOR theo user id','Pass/Findings'],['6','Xử lý lỗi DB/API và status code','Pass/Findings'],['7','Không render dữ liệu người dùng không an toàn','Pass/Findings'],['8','Có test cho thay đổi nghiệp vụ','Pass/Findings'],['9','Không để console log nhạy cảm','Pass/Findings']], [0.6,4.4,1.5])
heading('8.3. Chỉ số chất lượng và tiêu chí release',2)
table(['Chỉ số','Mục tiêu','Cách đánh giá'],[
['Tỷ lệ test pass','>= 95% tổng case; 100% critical path','Test Summary'],['Lỗi blocker/critical','0 lỗi mở','Defect report'],['Traceability','100% FR/NFR quan trọng có test','RTM review'],['Bảo mật','0 lỗi high/critical','Security checklist'],['Hiệu năng','p95 trong ngưỡng ở Test Plan','Performance log'],['Code review','100% thay đổi chính đã review','Review record'],['UAT','Đại diện người dùng ký xác nhận','Biên bản UAT'],['Tài liệu release','Đủ README, config mẫu, backup/restore','Deployment checklist']], [1.8,2.0,2.55])
page()

heading('9. CÔNG CỤ, RỦI RO, KẾT LUẬN VÀ KIẾN NGHỊ',1)
heading('9.1. Công cụ hỗ trợ',2)
table(['Nhóm','Công cụ đề xuất','Mục đích'],[
['Quản lý mã','Git/GitHub','Branch, review, tag release, history'],['Backend test','Node test/được cấu hình bổ sung, Postman hoặc Newman','API functional/integration'],['Database','MySQL Workbench hoặc CLI','Seed, query kiểm chứng, backup'],['UI test','Browser DevTools, Playwright/Selenium','Responsive, regression, screenshot'],['Load test','k6/JMeter','p95, concurrent request, stability'],['Security','OWASP checklist, npm audit','Kiểm tra cơ bản và dependency'],['Tài liệu','Word/Markdown, draw.io','SRS, SDD, ERD, test docs'],['CI/CD','GitHub Actions','Build, lint, test, artifact']], [1.25,2.9,2.2])
heading('9.2. Rủi ro và biện pháp giảm thiểu',2)
table(['Rủi ro','Ảnh hưởng','Biện pháp'],[
['DB không chạy hoặc sai schema','Không thể test end-to-end','README setup, health check, seed/backup'],['Secret mặc định','Rủi ro giả mạo token','Bắt buộc JWT_SECRET ở production, không commit .env'],['Trùng booking khi đồng thời','Sai trạng thái phòng','Transaction/lock hoặc unique business rule và test concurrency'],['Thiếu test tự động','Regression khó phát hiện','Bổ sung test cho helper và API lõi'],['Chatbot không sẵn sàng','Mất chức năng tư vấn','Timeout, thông báo fallback, kiểm thử độc lập'],['Thay đổi yêu cầu muộn','Trễ Waterfall','Change request và phân tích impact']], [1.7,2.0,2.65])
heading('9.3. Kết luận',2)
p('StayEasy Homestay có nền tảng chức năng phù hợp để hoàn thiện thành hệ thống đặt phòng homestay trong phạm vi đồ án. Việc áp dụng Waterfall giúp nhóm kiểm soát tài liệu và cổng phê duyệt; ISO/IEC 25010:2011 cung cấp khung đánh giá chất lượng sản phẩm theo tám đặc tính. Báo cáo đã chuyển các đặc tính này thành yêu cầu, chỉ số, test case, checklist và tiêu chí release có thể kiểm chứng.')
p('Để đạt trạng thái sẵn sàng nộp và có thể trình diễn, nhóm cần chạy đầy đủ test case với database thực tế, lưu bằng chứng kết quả, hoàn thiện thông tin sinh viên/giảng viên trên bìa và cập nhật Test Summary theo số liệu thực thi. Các mục tiêu hiệu năng trong báo cáo là ngưỡng kiểm soát đề xuất; không được ghi là kết quả đo nếu chưa thực hiện đo.')
heading('9.4. Kiến nghị hoàn thiện',2)
bullets(['Bổ sung test tự động cho các helper xác thực, validate ngày và route đặt phòng.','Áp dụng transaction hoặc cơ chế chống race condition cho kiểm tra trùng lịch khi nhiều request đồng thời.','Thay JWT secret mặc định bằng secret quản lý ngoài môi trường và bổ sung rotation policy.','Bổ sung backup/restore rehearsal, logging có correlation id và giám sát lỗi.','Chuẩn hóa API response và thông báo frontend để giảm lỗi tích hợp giữa các module.'])
page()

heading('PHỤ LỤC A. DANH MỤC API VÀ TÀI LIỆU BÀN GIAO',1)
heading('A.1. Danh mục API trọng yếu',2)
table(['Nhóm','Endpoint tiêu biểu','Quyền','Mục đích'],[
['Auth','POST /register, POST /login','Public','Đăng ký và đăng nhập'],['Catalog','GET /api/loai-phong, GET /api/can-phong/:id','Public/Auth','Tra cứu danh mục/căn'],['Booking','POST /api/dat-phong, GET /api/don-dat-user/:idKH','Customer','Tạo/xem đơn'],['Booking','POST /api/huy-dat-phong','Customer','Hủy đơn thuộc quyền'],['Profile','GET/PUT /api/khachhang/:idKH','Customer','Xem/sửa hồ sơ'],['Admin','/api/admin/canphong, /api/admin/datphong','Admin','Quản lý vận hành'],['History','/api/admin/hosoluutru, /api/admin/lichsuluutru','Admin','Hồ sơ và lịch sử'],['Dashboard','GET /api/dashboard, /api/hoatdong','Admin','Thống kê và nhật ký']], [1.2,2.65,1.05,1.45])
heading('A.2. Danh mục bàn giao',2)
bullets(['Mã nguồn frontend và backend đã được tổ chức trong thư mục dự án StayEasy-Homestay.','database.sql với schema, khóa ngoại, chỉ mục, view tương thích và dữ liệu mẫu.','README.md hướng dẫn cài đặt Node.js, MySQL, chatbot và tài khoản trải nghiệm.','SQA Plan, SRS, SDD, Test Plan, Test Cases, Defect Report, Test Summary và biên bản UAT cần được lưu cùng phiên bản release.','File .env.example không chứa secret thật; quy trình backup và restore được ghi trong tài liệu triển khai.'])
heading('A.3. Tài liệu tham khảo',2)
table(['Tài liệu','Cách sử dụng trong báo cáo'],[
['ISO/IEC 25010:2011','Mô hình đặc tính chất lượng sản phẩm phần mềm'],['IEEE 730','Định hướng cấu trúc kế hoạch đảm bảo chất lượng phần mềm'],['IEEE 829','Định hướng cấu trúc tài liệu kiểm thử và báo cáo kiểm thử'],['Mã nguồn StayEasy Homestay','Căn cứ mô tả chức năng, API, bảo mật và cơ sở dữ liệu'],['Bài 08. Thiết lập và vận hành hệ thống đảm bảo chất lượng phần mềm','Căn cứ cấu trúc báo cáo mẫu và cách trình bày các hoạt động QA']], [2.5,3.85])
p('Ngày lập báo cáo: 18/10/2026. Phiên bản tài liệu: 1.0. Trạng thái: Dự thảo hoàn thiện để rà soát thông tin cá nhân và bổ sung kết quả chạy kiểm thử thực tế.')

doc.core_properties.title='Báo cáo đảm bảo chất lượng phần mềm StayEasy Homestay'
doc.core_properties.subject='Waterfall và ISO/IEC 25010:2011'
doc.core_properties.author=''
doc.save(OUT)
print(OUT)
