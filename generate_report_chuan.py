from pathlib import Path
import re
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'Bao_cao_SQA_StayEasy_Ban_Chuan.docx'
LOGO = ROOT / 'Khách hàng' / 'Picture' / 'logo1.png'
d = Document(); s = d.sections[0]
s.top_margin=Inches(.8); s.bottom_margin=Inches(.75); s.left_margin=Inches(.9); s.right_margin=Inches(.75)
s.header_distance=Inches(.3); s.footer_distance=Inches(.35)
st=d.styles
for n,sz,bold in [('Normal',13,False),('Title',20,True),('Heading 1',16,True),('Heading 2',14,True),('Heading 3',13,True)]:
    x=st[n]; x.font.name='Times New Roman'; x._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); x.font.size=Pt(sz); x.font.bold=bold; x.font.color.rgb=RGBColor(0,0,0)
    x.paragraph_format.space_after=Pt(5)
st['Normal'].paragraph_format.line_spacing=1.22
if 'Caption VN' not in st:
    x=st.add_style('Caption VN', WD_STYLE_TYPE.PARAGRAPH); x.font.name='Times New Roman'; x._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); x.font.size=Pt(11); x.font.italic=True; x.paragraph_format.alignment=WD_ALIGN_PARAGRAPH.CENTER

def shade(c, val):
    pr=c._tc.get_or_add_tcPr(); e=pr.find(qn('w:shd'))
    if e is None: e=OxmlElement('w:shd'); pr.append(e)
    e.set(qn('w:fill'),val)
def borders(t):
    pr=t._tbl.tblPr; e=pr.first_child_found_in('w:tblBorders')
    if e is None: e=OxmlElement('w:tblBorders'); pr.append(e)
    for side in ('top','left','bottom','right','insideH','insideV'):
        z=OxmlElement('w:'+side); z.set(qn('w:val'),'single'); z.set(qn('w:sz'),'4'); z.set(qn('w:color'),'D9D9D9'); e.append(z)
def ctext(c, text, bold=False, color=None, size=11.2):
    c.text=''; p=c.paragraphs[0]; p.paragraph_format.space_after=Pt(2); p.paragraph_format.line_spacing=1.05
    r=p.add_run(str(text)); r.bold=bold; r.font.name='Times New Roman'; r._element.rPr.rFonts.set(qn('w:eastAsia'),'Times New Roman'); r.font.size=Pt(size)
    if color: r.font.color.rgb=RGBColor(*color)
    c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
table_counter = 0
def tbl(title, headers, rows):
    global table_counter
    table_counter += 1
    title = re.sub(r'Bảng\s+\d+', f'Bảng {table_counter}', title)
    q=d.add_paragraph(title); q.paragraph_format.space_before=Pt(4); q.paragraph_format.space_after=Pt(3); q.runs[0].bold=True; q.runs[0].italic=True
    t=d.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; borders(t)
    for i,h in enumerate(headers): ctext(t.rows[0].cells[i],h,True,(255,255,255)); shade(t.rows[0].cells[i],'1F4E78')
    tr=t.rows[0]._tr.get_or_add_trPr(); hd=OxmlElement('w:tblHeader'); hd.set(qn('w:val'),'true'); tr.append(hd)
    for ri,row in enumerate(rows):
        cs=t.add_row().cells
        for i,v in enumerate(row): ctext(cs[i],v)
        if ri%2:
            for c in cs: shade(c,'EEF3F8')
    d.add_paragraph().paragraph_format.space_after=Pt(1)
def P(text, lead=None, center=False):
    p=d.add_paragraph(); p.paragraph_format.line_spacing=1.22; p.paragraph_format.space_after=Pt(6)
    if not center: p.paragraph_format.first_line_indent=Inches(.25)
    if center: p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    if lead and text.startswith(lead): p.add_run(lead).bold=True; p.add_run(text[len(lead):])
    else: p.add_run(text)
    return p
def H(text,level=1): d.add_heading(text,level)
def bullets(items):
    for x in items:
        p=d.add_paragraph(style='List Bullet'); p.paragraph_format.left_indent=Inches(.35); p.paragraph_format.space_after=Pt(2); p.add_run(x)
def br(): d.add_page_break()
def field(p, instr):
    r=p.add_run(); b=OxmlElement('w:fldChar'); b.set(qn('w:fldCharType'),'begin'); r._r.append(b)
    r=p.add_run(); i=OxmlElement('w:instrText'); i.set(qn('xml:space'),'preserve'); i.text=instr; r._r.append(i)
    r=p.add_run(); e=OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'),'end'); r._r.append(e)

head=s.header.paragraphs[0]; head.text='STAYEASY HOMESTAY  |  BÁO CÁO ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM'; head.alignment=WD_ALIGN_PARAGRAPH.RIGHT
head.runs[0].font.name='Times New Roman'; head.runs[0].font.size=Pt(9); head.runs[0].font.color.rgb=RGBColor(80,80,80)
foot=s.footer.paragraphs[0]; foot.alignment=WD_ALIGN_PARAGRAPH.CENTER; foot.add_run('Trang '); field(foot,'PAGE')

# Cover
d.add_paragraph('\n\n')
if LOGO.exists():
    d.add_picture(str(LOGO),width=Inches(5.5)); d.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    docpr=d.paragraphs[-1]._p.xpath('.//wp:docPr')[0]; docpr.set('descr','Logo StayEasy Homestay'); docpr.set('title','Logo StayEasy Homestay')
P('TRƯỜNG ĐẠI HỌC ................................................',center=True)
P('KHOA / BỘ MÔN ................................................',center=True)
d.add_paragraph('\nBÁO CÁO ĐẢM BẢO CHẤT LƯỢNG PHẦN MỀM',style='Title').alignment=WD_ALIGN_PARAGRAPH.CENTER
d.add_paragraph('HỆ THỐNG ĐẶT PHÒNG HOMESTAY STAYEASY',style='Heading 1').alignment=WD_ALIGN_PARAGRAPH.CENTER
P('Áp dụng mô hình Waterfall và tiêu chuẩn ISO IEC 25010 2011',center=True)
P('\nSinh viên thực hiện: ........................................................\nLớp: ........................................................\nGiảng viên hướng dẫn: ........................................................',center=True)
P('\nTP. Hồ Chí Minh, tháng 10 năm 2026',center=True); br()

# TOC
H('MỤC LỤC',1); P('Mục lục được cập nhật tự động khi mở tài liệu trong Microsoft Word.',center=True); field(d.add_paragraph(),'TOC \\o "1-3" \\h \\z \\u'); br()

# CH1
H('1. GIỚI THIỆU VỀ DỰ ÁN PHẦN MỀM',1); H('1.1. Tổng quan về dự án',2)
P('StayEasy Homestay là hệ thống web phục vụ hoạt động quản lý đặt phòng và lưu trú homestay. Hệ thống cung cấp cổng dành cho khách hàng và bảng điều khiển dành cho quản trị viên. Khách hàng có thể khám phá loại hình lưu trú, lựa chọn căn, đặt phòng, theo dõi đơn, cập nhật hồ sơ và xem lịch sử lưu trú. Quản trị viên có thể quản lý danh mục, căn phòng, tài khoản, đơn đặt, hồ sơ, lịch sử và các số liệu vận hành.')
P('Mã nguồn hiện có gồm backend Express trên Node.js, MySQL, giao diện HTML CSS JavaScript và chatbot FastAPI tùy chọn. Phạm vi nghiệp vụ được xác định rõ theo các module hiện có, phù hợp với cách tổ chức Waterfall: từng đầu ra được review và phê duyệt trước khi chuyển sang giai đoạn sau.')
tbl('Bảng 1. Thành phần hệ thống StayEasy Homestay',['Thành phần','Chức năng chính','Đối tượng sử dụng'],[['Cổng khách hàng','Đăng ký, đăng nhập, xem và đặt phòng, hồ sơ, lịch sử','Khách hàng'],['Cổng quản trị','Quản lý loại, căn, đơn, hồ sơ, lịch sử, dashboard','Quản trị viên'],['REST API','Xác thực, nghiệp vụ đặt phòng, phân quyền, truy xuất MySQL','Frontend và admin'],['Chatbot tùy chọn','Tư vấn căn, dịch vụ và quy định','Khách hàng']])
H('1.2. Yêu cầu người dùng và phạm vi dự án',2); H('1.2.1. Yêu cầu người dùng',3)
bullets(['Khách hàng đăng ký hoặc đăng nhập bằng số điện thoại và mật khẩu; sau đăng nhập có token phiên làm việc.','Khách hàng tra cứu loại phòng, căn phòng, tiện nghi, giá; chọn ngày giờ và gửi yêu cầu đặt phòng.','Khách hàng chỉ xem, cập nhật hồ sơ và quản lý đơn của chính mình; có thể hủy đơn theo quy định.','Quản trị viên quản lý dữ liệu vận hành và theo dõi dashboard; các API quản trị phải kiểm tra quyền admin.'])
H('1.2.2. Phạm vi dự án',3)
tbl('Bảng 2. Phạm vi chức năng và phi chức năng',['Nhóm','Trong phạm vi','Ngoài phạm vi'],[['Chức năng','Tài khoản, đặt phòng, đơn, hồ sơ, lịch sử, CRUD admin','Thanh toán online, OTA, nhiều chi nhánh'],['Bảo mật','JWT, role, PBKDF2, rate limit, CORS, parameterized query','SSO, MFA, WAF chuyên dụng'],['Triển khai','Node.js, MySQL, cấu hình biến môi trường','Hạ tầng production đa vùng'],['Trợ lý','Chatbot tư vấn thông tin','Đặt phòng hoàn toàn bằng hội thoại']])

H('1.3. Yêu cầu phần mềm',2)
tbl('Bảng 3. Yêu cầu nghiệp vụ',['Mã','Yêu cầu'],[['BR01','Tạo tài khoản và đăng nhập hợp lệ'],['BR02','Tra cứu loại phòng và căn phòng theo dữ liệu hiện có'],['BR03','Đặt phòng trực tuyến có ngày, giờ, căn và ghi chú'],['BR04','Theo dõi, hủy đơn thuộc quyền sở hữu'],['BR05','Cập nhật hồ sơ và đổi mật khẩu'],['BR06','Quản lý loại phòng, căn phòng và tài khoản'],['BR07','Quản trị đơn đặt, hồ sơ và lịch sử lưu trú'],['BR08','Theo dõi dashboard và nhật ký hoạt động']])
tbl('Bảng 4. Yêu cầu hệ thống và phi chức năng',['Mã','Yêu cầu'],[['SR01','API trả response có mã HTTP, dữ liệu hoặc thông báo lỗi rõ ràng'],['SR02','Kiểm tra token, role và quyền sở hữu dữ liệu trước thao tác'],['SR03','Ràng buộc khóa ngoại và dữ liệu ngày giờ được duy trì'],['NFR01','API tra cứu p95 không quá 2,5 giây trong môi trường kiểm thử'],['NFR02','Không truy cập route bảo vệ khi token sai hoặc thiếu'],['NFR03','Giao diện hoạt động trên Chrome, Edge, Firefox và viewport mobile'],['NFR04','Mã nguồn có thể cấu hình qua biến môi trường và tài liệu README']])
H('1.4. Đội dự án và đảm bảo chất lượng',2)
tbl('Bảng 5. Phân công vai trò',['Vai trò','Trách nhiệm chất lượng'],[['Quản lý dự án','Phê duyệt phạm vi, lịch, baseline và cổng chất lượng'],['BA','Lập SRS, acceptance criteria, RTM'],['Kiến trúc/CSDL','Thiết kế API, dữ liệu, bảo mật và review SDD'],['Developer','Code, unit test, sửa lỗi, giải trình review'],['QA/Tester','Lập test plan, test case, defect report, summary'],['Đại diện người dùng','UAT và xác nhận phù hợp nghiệp vụ']])
H('1.5. Kiến trúc hệ thống và dữ liệu',2)
P('Kiến trúc StayEasy được tổ chức theo tầng. Trình duyệt khách hàng và quản trị viên gọi REST API Express. Middleware authenticateToken và requireAdmin tạo ranh giới xác thực và phân quyền. Backend sử dụng connection pool mysql2 để truy cập MySQL; chatbot FastAPI là dịch vụ phụ trợ và không được phép làm gián đoạn luồng đặt phòng nếu không sẵn sàng.')
tbl('Bảng 6. Thành phần kiến trúc và điểm kiểm soát',['Tầng','Thành phần','Điểm QA'],[['Giao diện','HTML CSS JavaScript theo module khách/admin','Validation, responsive, thông báo lỗi, XSS'],['Nghiệp vụ','Express route và middleware','JWT, role, ownership, status code'],['Dữ liệu','MySQL và database.sql','PK, FK, unique, index, integrity'],['Trợ lý','FastAPI chatbot','Timeout, fallback, API contract']])
tbl('Bảng 7. Thực thể dữ liệu trọng yếu',['Thực thể','Ý nghĩa','Ràng buộc chính'],[['KHACHHANG','Tài khoản và thông tin khách','Số điện thoại unique'],['LOAIPHONG/CANPHONG','Danh mục và căn lưu trú','Căn thuộc một loại phòng'],['DATPHONG','Yêu cầu đặt phòng','Liên kết khách, căn, loại và trạng thái'],['HOSOLUUTRU/LICHSULUUTRU','Hồ sơ và lịch sử','Liên kết khách/căn/phòng'],['QUANTRIVIEN/hoatdong','Tài khoản admin và log','Kiểm soát vận hành']])

# CH2
H('2. THIẾT LẬP MỤC TIÊU VÀ YÊU CẦU CHẤT LƯỢNG CHO DỰ ÁN',1); H('2.1. Mục tiêu chất lượng',2)
P('Mục tiêu của StayEasy là cung cấp chức năng đặt phòng đúng nghiệp vụ, phản hồi ổn định, bảo vệ thông tin tài khoản và có thể duy trì khi yêu cầu thay đổi. Mục tiêu được kiểm soát bằng yêu cầu đo được, review độc lập, kiểm thử và bằng chứng trong Test Summary. ISO IEC 25010 2011 là khung chính để xác định chất lượng sản phẩm; IEEE 730 định hướng SQA Plan; IEEE 829 định hướng tài liệu kiểm thử.')
bullets(['Đầy đủ và chính xác: mọi yêu cầu bắt buộc có mã, tiêu chí chấp nhận và test case.','An toàn: không lộ dữ liệu khác người dùng; xác thực, phân quyền và kiểm soát brute force hoạt động.','Dễ dùng: người dùng hoàn tất đặt phòng theo luồng rõ ràng, thông báo lỗi có thể hiểu.','Dễ bảo trì: cấu trúc mã, API, database và hướng dẫn triển khai có thể review.'])
H('2.2. Yêu cầu chất lượng theo ISO IEC 25010 2011',2)
tbl('Bảng 6. Yêu cầu chất lượng ISO IEC 25010 2011',['Đặc tính','Yêu cầu cho StayEasy','Cách xác nhận'],[['Functional suitability','Đăng nhập, đặt phòng, quản lý đơn và admin đúng nghiệp vụ','Functional test, UAT'],['Performance efficiency','Tra cứu, tạo đơn và dashboard phản hồi trong ngưỡng','Load test, log thời gian'],['Compatibility','Hoạt động trên trình duyệt phổ biến, giao diện responsive','Cross browser test'],['Usability','Điều hướng rõ, lỗi bằng tiếng Việt, thao tác ngắn','UI checklist, UAT'],['Reliability','Không mất dữ liệu sau response thành công, lỗi được kiểm soát','Recovery và integrity test'],['Security','JWT, role, PBKDF2, rate limit, CORS, chống IDOR','Negative/security test'],['Maintainability','Module rõ, code review, README và tài liệu kỹ thuật','Review record'],['Portability','Cấu hình qua env, cài bằng Node.js/MySQL chuẩn','Deployment rehearsal']]); br()

H('2.3. Chỉ tiêu chất lượng và ngưỡng chấp nhận',2)
tbl('Bảng 7. Chỉ tiêu chất lượng',['Chỉ tiêu','Mục tiêu','Bằng chứng'],[['Test case pass','Tối thiểu 95%; 100% critical path','Test Summary'],['Lỗi blocker/critical','Không có lỗi mở trước UAT','Defect Report'],['Truy xuất yêu cầu','100% FR/NFR chính có case liên kết','RTM'],['Phân quyền','0 case customer truy cập tài nguyên admin/khách khác','Security test'],['Hiệu năng','p95 nằm trong ngưỡng kế hoạch','Performance log'],['Review','100% thay đổi chính có peer review','Review record'],['Bàn giao','Đủ README, DB script, cấu hình mẫu, checklist','Release checklist']])
P('Các chỉ tiêu trên là mục tiêu kiểm soát cho đồ án. Khi nộp bài, nhóm phải ghi số liệu thực thi thật vào Test Summary; không thay mục tiêu bằng số liệu chưa đo.')
H('2.4. Ma trận truy xuất yêu cầu chất lượng',2)
tbl('Bảng 8. Ví dụ truy xuất',['Yêu cầu','Module','Test case đại diện'],[['BR01','POST /register, POST /login','TC AUTH 01 đến 09'],['BR03','order1.js, POST /api/dat-phong','TC BOOK 01 đến 11'],['BR04','GET /api/don-dat-user, POST /api/huy-dat-phong','TC BOOK 12 đến 15'],['BR06-08','/api/admin/*, dashboard','TC ADM 01 đến 16'],['NFR02','authenticateToken, requireAdmin','TC SEC 01 đến 10'],['NFR03','CSS và các trang khách/admin','TC UI 01 đến 08']])
H('2.5. Phương pháp đánh giá chất lượng',2)
P('Đánh giá được thực hiện theo ba lớp. Lớp thứ nhất là review tĩnh đối với yêu cầu, thiết kế và code. Lớp thứ hai là kiểm thử động với API, cơ sở dữ liệu, giao diện và phân quyền. Lớp thứ ba là đánh giá nghiệp vụ qua UAT. Bằng chứng của từng lớp phải gắn với một phiên bản baseline để kết quả có thể truy vết.')
tbl('Bảng 9. Phương pháp đánh giá',['Lớp đánh giá','Kỹ thuật','Sản phẩm bằng chứng'],[['Tĩnh','Review SRS, SDD, ERD, code checklist','Biên bản review và finding'],['Động','Unit, integration, system, security, compatibility','Test result, log, screenshot'],['Nghiệp vụ','UAT theo luồng đặt phòng và quản trị','Biên bản UAT'],['Quản trị','Audit tài liệu, trace, change log','SQA audit record']])
P('Các kết quả được phân loại thành đạt, không đạt hoặc chấp nhận có điều kiện. Lỗi blocker và critical bắt buộc đóng trước UAT. Lỗi major chỉ được chấp nhận nếu có workaround đã được đại diện người dùng đồng ý và có kế hoạch khắc phục rõ ràng.'); br()

# CH3
H('3. XÁC ĐỊNH MÔ HÌNH PHÁT TRIỂN',1); H('3.1. Lựa chọn mô hình Waterfall',2)
P('Nhóm áp dụng Waterfall vì yêu cầu chính đã được nhìn thấy từ mã nguồn và có thể tách thành các đầu ra tuần tự: SRS, SDD, mã nguồn, test case và hồ sơ nghiệm thu. Cách tiếp cận này phù hợp bài tập đảm bảo chất lượng vì mỗi giai đoạn có cổng kiểm soát cụ thể, giúp chứng minh truy xuất từ yêu cầu đến kiểm thử.')
P('Waterfall không cấm thay đổi. Khi phát hiện thay đổi sau baseline, thay đổi phải đi theo Change Request, được đánh giá ảnh hưởng tới SRS, SDD, database, API và regression test trước khi phê duyệt.')
tbl('Bảng 9. Quy trình Waterfall cho StayEasy',['Giai đoạn','Hoạt động','Đầu ra','Cổng chất lượng'],[['1. Phân tích','Thu thập nghiệp vụ, vai trò, phạm vi','Danh sách yêu cầu','Stakeholder xác nhận'],['2. Đặc tả','Viết BR, FR, NFR, acceptance criteria','SRS, RTM','Review SRS đạt'],['3. Thiết kế','Kiến trúc, API, ERD, UI flow, security','SDD, API contract','Review SDD đạt'],['4. Lập trình','Code theo thiết kế, unit test, peer review','Mã nguồn','Build và review pass'],['5. Kiểm thử','Integration, system, security, UAT','Test/defect report','Không blocker/critical'],['6. Bàn giao','Triển khai, hướng dẫn, backup, nghiệm thu','Release package','UAT sign off']])
P('Hình 1. Luồng Waterfall: Phân tích yêu cầu -> Đặc tả SRS -> Thiết kế SDD -> Lập trình -> Kiểm thử -> Bàn giao',center=True)
H('3.2. Cổng chất lượng và quản lý cấu hình',2)
tbl('Bảng 10. Baseline kiểm soát',['Baseline','Thành phần','Điều kiện thay đổi'],[['Yêu cầu','SRS, RTM, acceptance criteria','CR được phê duyệt'],['Thiết kế','SDD, ERD, API contract','Review thiết kế và impact analysis'],['Mã nguồn','server.js, frontend, chatbot, database.sql','Code review và test pass'],['Kiểm thử','Test plan, cases, defects, summary','QA/PM duyệt'],['Release','README, .env.example, DB script, release note','UAT và deployment checklist']])
H('3.3. Ánh xạ Waterfall với mã nguồn hiện có',2)
tbl('Bảng 11. Liên kết đầu ra Waterfall và hiện thực',['Giai đoạn','Đầu ra dự án','Hiện thực/đối tượng kiểm tra'],[['Yêu cầu','BR, FR, NFR','Luồng khách hàng/admin và README'],['Thiết kế','ERD, API contract, security design','database.sql, server.js, cấu trúc frontend'],['Code','Module đã kiểm tra','server.js, admin-*.js, order1.js, account.js'],['Kiểm thử','Case và kết quả','API auth, booking, IDOR, CRUD admin'],['Bàn giao','Hướng dẫn và dữ liệu mẫu','README.md, package.json, database.sql']])
P('Sự liên kết này giúp reviewer lần theo một yêu cầu từ giao diện, API, database đến test case. Ví dụ, BR03 đặt phòng phải dẫn tới form đặt phòng, POST /api/dat-phong, bảng DATPHONG, kiểm tra trùng lịch và các test case tích cực/tiêu cực.'); br()

# CH4
H('4. THIẾT LẬP CÁC TIÊU CHUẨN, THỦ TỤC VÀ TÀI LIỆU QA',1); H('4.1. Tiêu chuẩn tài liệu',2)
tbl('Bảng 11. Danh mục tài liệu QA',['Tài liệu','Nội dung tối thiểu','Mục đích'],[['SQA Plan','Mục tiêu, chuẩn, vai trò, review, test, báo cáo','Điều hành chất lượng'],['SRS','BR/FR/NFR, tiêu chí chấp nhận','Cơ sở phát triển và test'],['SDD','Kiến trúc, DB, API, bảo mật','Cơ sở thiết kế/code review'],['Test Plan','Phạm vi, môi trường, chiến lược, lịch','Điều hành kiểm thử'],['Test Cases','ID, tiền điều kiện, bước, data, expected','Thực thi kiểm thử'],['Defect Report','Mô tả, severity, evidence, owner, trạng thái','Theo dõi lỗi'],['Test Summary','Pass/fail, rủi ro còn lại, quyết định release','Nghiệm thu']])
bullets(['Font Times New Roman, nội dung 13pt; tiêu đề đánh số 1, 1.1, 1.1.1.','Tên file theo mẫu TenTaiLieu_Version.docx; có tác giả, reviewer, ngày và trạng thái.','Không sửa trực tiếp bản baseline đã phê duyệt; lưu version để truy vết.','Yêu cầu thay đổi tài liệu phải cập nhật đồng bộ RTM, thiết kế và test case liên quan.'])
H('4.2. Thiết lập chuẩn mã nguồn',2)
tbl('Bảng 12. Coding guidelines',['Hạng mục','Quy tắc áp dụng'],[['Đặt tên','camelCase cho biến/hàm, PascalCase cho lớp, hằng số viết hoa'],['Bảo mật','Không commit secret; truy vấn có tham số; không log mật khẩu/token'],['Xử lý lỗi','I/O, DB và API có xử lý lỗi, status code, thông báo an toàn'],['Cấu trúc','Tách module theo domain, hàm có trách nhiệm đơn, tránh lặp code'],['Review','Thay đổi chính phải được peer review trước baseline'],['Kiểm thử','Thêm logic nghiệp vụ phải thêm hoặc cập nhật test liên quan']]); br()

H('4.3. Thiết lập quy trình review',2)
tbl('Bảng 13. Quy trình review',['Bước','Nội dung','Đầu ra'],[['Chuẩn bị','Chọn artifact/version, reviewer độc lập, checklist','Review request'],['Review cá nhân','Kiểm tra đầy đủ, nhất quán, security, khả kiểm thử','Finding có mã'],['Tổng hợp','Phân loại blocker, major, minor, observation','Biên bản review'],['Khắc phục','Tác giả sửa và phản hồi từng finding','Diff + response'],['Xác nhận','Reviewer xác nhận, QA đóng review','Sign off']])
H('4.4. Thiết lập quy trình kiểm thử',2)
tbl('Bảng 14. Quy trình kiểm thử',['Bước','Thực hiện'],[['1. Phân tích','Xác định điều kiện tích cực, tiêu cực, biên và role'],['2. Thiết kế','Viết case có ID, dữ liệu, expected, mapping yêu cầu'],['3. Môi trường','Chuẩn bị database seed, customer/admin, trình duyệt, API'],['4. Thực thi','Unit, integration, system, security, compatibility, UAT'],['5. Defect','Ghi bằng chứng, severity, bước tái hiện, owner'],['6. Kết thúc','Re-test, regression, summary, quyết định release']])
P('Các cấp độ kiểm thử: Unit test do developer thực hiện; integration/system/security do QA thực hiện; UAT do đại diện người dùng xác nhận.')
H('4.4.1. Kế hoạch kiểm thử theo cấp độ',3)
tbl('Bảng 15. Phạm vi kiểm thử',['Cấp độ','Đối tượng','Ví dụ tại StayEasy','Người thực hiện'],[['Unit','Hàm helper và validation','verifyToken, hashPassword, normalizeDateInput','Developer'],['Integration','Kết hợp frontend, API và MySQL','Đăng nhập hoặc đặt phòng ghi DATPHONG','Developer/Tester'],['System','Toàn bộ luồng nghiệp vụ','Đăng nhập -> chọn căn -> đặt -> xem đơn','Tester'],['Security','Ranh giới quyền và dữ liệu','IDOR, role bypass, SQLi, XSS, brute force','QA/Security reviewer'],['Compatibility','Trình duyệt và viewport','Chrome, Edge, Firefox; 390/768/1366px','Tester'],['Acceptance','Mức độ phù hợp với người dùng','Khách đặt phòng, admin xử lý đơn','Đại diện người dùng']])
H('4.4.2. Môi trường, dữ liệu và vòng đời defect',3)
tbl('Bảng 16. Môi trường và dữ liệu kiểm thử',['Hạng mục','Cấu hình kiểm thử'],[['Backend','Node.js 18+, Express, PORT 3000'],['Database','MySQL 8.x, schema từ database.sql, dữ liệu seed'],['Chatbot','Python 3.10+, FastAPI port 8000 nếu kiểm thử chatbot'],['Tài khoản','Admin và tối thiểu hai customer khác nhau'],['Trình duyệt','Chrome, Edge, Firefox; desktop và mobile viewport'],['Dữ liệu biên','Số điện thoại trùng, mật khẩu sai, ngày thiếu, ngày trùng, id không tồn tại']])
tbl('Bảng 17. Vòng đời defect',['Trạng thái','Ý nghĩa','Điều kiện chuyển'],[['New','Tester phát hiện và ghi đủ bằng chứng','QA triage'],['Assigned','Đã giao developer theo owner','Developer nhận'],['In progress','Đang phân tích và sửa','Có branch/commit'],['Fixed','Developer báo đã sửa','Chờ re-test'],['Re-test','QA kiểm tra bản sửa','Pass hoặc Reopen'],['Closed','Không còn lỗi theo phạm vi','QA xác nhận'],['Deferred','Hoãn có phê duyệt và lý do','Ghi vào risk/backlog']])
P('Mỗi defect phải ghi môi trường, version, bước tái hiện, actual result, expected result, severity và bằng chứng. Không đóng lỗi chỉ vì không tái hiện được nếu chưa xác định điều kiện môi trường hoặc dữ liệu gây ra lỗi.')
H('4.5. Thiết lập danh mục kiểm tra',2); br()

H('4.5.1. Checklist review yêu cầu và thiết kế',3)
tbl('Bảng 15. Checklist SRS và SDD',['STT','Nội dung kiểm tra','Kết quả'],[['1','Mỗi yêu cầu có mã duy nhất và tiêu chí chấp nhận','Đạt/Không đạt'],['2','Thuật ngữ StayEasy được dùng nhất quán','Đạt/Không đạt'],['3','Yêu cầu bảo mật và role được chỉ rõ','Đạt/Không đạt'],['4','Mỗi dữ liệu có nguồn, ràng buộc và owner','Đạt/Không đạt'],['5','Database có PK, FK, unique và index phù hợp','Đạt/Không đạt'],['6','API có input, output, lỗi và quyền truy cập','Đạt/Không đạt'],['7','Yêu cầu chính có test case truy xuất','Đạt/Không đạt']])
H('4.5.2. Checklist coding và bảo mật',3)
tbl('Bảng 16. Checklist code review',['STT','Tiêu chí','Ưu tiên'],[['1','Tên biến/hàm rõ nghĩa và đúng convention','Cao'],['2','Không lặp code hoặc để code chết','Trung bình'],['3','Validation đầu vào trước thao tác dữ liệu','Cao'],['4','Parameterized query, không lộ lỗi SQL','Cao'],['5','Route bảo vệ đúng token, role và ownership','Cao'],['6','Không có secret thật/log nhạy cảm','Cao'],['7','Có xử lý lỗi và test cho thay đổi mới','Cao']])
H('4.5.3. Checklist UI UX, triển khai và kết thúc dự án',3)
tbl('Bảng 17. Checklist UI, triển khai, nghiệm thu',['Hạng mục','Tiêu chí'],[['UI UX','Không tràn trên 390, 768, 1366px; thông báo dễ hiểu'],['Compatibility','Chrome, Edge, Firefox chạy chức năng chính'],['Triển khai','DB import được; env hợp lệ; service khởi động; backup sẵn sàng'],['Chất lượng cuối','Pass rate đạt mục tiêu; không blocker/critical mở'],['Nghiệm thu','README, release note, UAT sign off đầy đủ']])
H('4.5.4. Checklist test case và dữ liệu kiểm thử',3)
tbl('Bảng 18. Checklist test case',['STT','Nội dung kiểm tra','Đạt khi'],[['1','Có ID và yêu cầu liên kết','Truy vết được về BR/FR/NFR'],['2','Có tiền điều kiện và dữ liệu','Có tài khoản, role, dữ liệu phòng'],['3','Có bước rõ ràng','Người khác có thể lặp lại'],['4','Có expected result','Bao gồm HTTP, UI và dữ liệu nếu cần'],['5','Có case tiêu cực và biên','Sai token, sai role, trùng lịch, input thiếu'],['6','Có actual result và evidence','Log, screenshot hoặc DB query'],['7','Có quyết định pass/fail','Nhất quán với expected']])
tbl('Bảng 19. Test case đại diện',['ID','Tình huống','Kết quả mong đợi'],[['TC AUTH 01','Đăng ký số điện thoại mới','Tạo tài khoản, không lộ mật khẩu'],['TC AUTH 07','Sai mật khẩu liên tiếp','Rate limit được áp dụng'],['TC BOOK 05','Đặt phòng hợp lệ','Tạo DATPHONG trạng thái chờ xác nhận'],['TC BOOK 08','Đặt trùng căn và ngày','Từ chối, không tạo bản ghi'],['TC SEC 03','Khách A xem đơn khách B','401/403, không trả dữ liệu B'],['TC ADM 01','Customer gọi admin API','403, dữ liệu không thay đổi']]); br()

H('4.6. Thiết lập thủ tục QA',2); H('4.6.1. Thủ tục kiểm tra mã nguồn',3)
P('Developer tự kiểm tra và chạy test liên quan trước review. Reviewer kiểm tra thay đổi theo checklist; QA đối chiếu thay đổi với yêu cầu và test case. Finding được sửa, reviewer xác nhận, sau đó PM hoặc QA cho phép đưa vào baseline.')
P('Hình 2. Luồng code review: Self check -> Peer review -> QA trace -> Fix -> Re review -> Baseline',center=True)
tbl('Bảng 20. Các bước code review',['Bước','Thực hiện','Tiêu chí đóng'],[['1. Tạo review request','Nêu phạm vi, liên kết yêu cầu và test','Có version rõ ràng'],['2. Tự kiểm tra','Developer chạy test và checklist','Không còn lỗi hiển nhiên'],['3. Peer review','Reviewer ghi finding theo mức độ','Finding có owner'],['4. Khắc phục','Developer sửa và phản hồi','Diff đáp ứng finding'],['5. Xác nhận','Reviewer/QA kiểm tra lại','Review approved']])
H('4.6.2. Thủ tục kiểm thử phần mềm',3)
P('QA chốt version, môi trường và dữ liệu test; thực thi theo Test Plan; ghi actual result; mở defect khi có sai khác; thực hiện re-test và regression sau sửa; phát hành Test Summary trước UAT hoặc release.')
P('Hình 3. Luồng kiểm thử: Plan -> Design case -> Execute -> Defect -> Re test -> Summary',center=True)
tbl('Bảng 21. Các bước kiểm thử',['Bước','Thực hiện','Bằng chứng'],[['1. Chuẩn bị','Chốt build, môi trường, seed data','Environment record'],['2. Thực thi','Chạy case theo priority và ghi actual','Test execution'],['3. Báo lỗi','Mở defect có bước tái hiện và evidence','Defect report'],['4. Xác minh','Re-test bản sửa và regression liên quan','Re-test log'],['5. Kết thúc','Tổng hợp pass/fail và rủi ro','Test Summary']])
H('4.6.3. Thủ tục kiểm soát tài liệu',3)
P('Tài liệu mới được lập theo template, review và phê duyệt trước baseline. Khi có thay đổi, người sở hữu cập nhật version, mô tả thay đổi và liên kết các tài liệu bị ảnh hưởng. Bản cũ được lưu để truy xuất.')
tbl('Bảng 22. Kiểm soát tài liệu',['Hoạt động','Yêu cầu'],[['Lập mới','Có mã, phiên bản, tác giả, reviewer, trạng thái'],['Review','Có checklist và finding được đóng'],['Baseline','Chỉ bản approved được dùng làm đầu vào'],['Sửa đổi','Có change log và liên kết impact'],['Lưu trữ','Bản cũ còn truy xuất được']])
H('4.6.4. Thủ tục kiểm soát thay đổi',3)
P('Mỗi Change Request phải có lý do, phạm vi, ưu tiên và đánh giá tác động. BA, kiến trúc và QA phân tích ảnh hưởng tới yêu cầu, thiết kế, API, database, bảo mật và regression test; PM quyết định; thay đổi chỉ đóng sau khi tài liệu, code và test cùng được cập nhật.')
tbl('Bảng 23. Kiểm soát thay đổi',['Bước','Kết quả'],[['Ghi nhận','CR có mục tiêu, lý do và priority'],['Impact analysis','Danh sách SRS, SDD, code, test bị ảnh hưởng'],['Phê duyệt','Quyết định có owner và ngày'],['Thực hiện','Branch, review và test hồi quy'],['Đóng','Baseline/release note được cập nhật']])
H('4.6.5. Thủ tục kiểm thử tự động',3)
P('Tự động hóa ưu tiên helper xác thực, validate ngày, đăng nhập, đặt phòng và phân quyền. Pipeline tối thiểu gồm cài dependency, kiểm tra syntax hoặc lint, chạy unit/integration test và lưu log. Pipeline fail sẽ chặn merge vào nhánh phát hành nếu chưa có ngoại lệ được phê duyệt.')
H('4.6.6. Thủ tục báo cáo và phản hồi',3)
tbl('Bảng 24. Báo cáo QA',['Báo cáo','Nội dung','Thời điểm'],[['Tiến độ test','Case đã chạy, blocker, kế hoạch','Mỗi buổi test'],['Defect report','Mô tả, evidence, severity, owner, status','Ngay khi phát hiện'],['Review report','Finding, quyết định và xác nhận','Sau review'],['Test summary','Pass/fail, defect, residual risk','Trước UAT/release'],['Retrospective','Bài học và cải tiến','Sau bàn giao']])
H('4.7. Ma trận thực hiện thủ tục QA',2)
tbl('Bảng 25. Trách nhiệm thủ tục QA',['Thủ tục','Thực hiện','Kiểm tra/Phê duyệt','Bằng chứng'],[['Code review','Developer và reviewer','QA/PM','Review record'],['Kiểm thử','Tester và developer','QA lead','Test/defect report'],['Kiểm soát tài liệu','Tác giả tài liệu','Reviewer/PM','Version history'],['Kiểm soát thay đổi','BA/Architect/QA','PM/Stakeholder','Change request'],['Tự động hóa','Developer','QA lead','CI log'],['Báo cáo phản hồi','QA','PM/Stakeholder','Summary/meeting note']])
P('Mỗi thủ tục phải có người chịu trách nhiệm, tiêu chí đầu vào/đầu ra và bằng chứng. Nếu bằng chứng không tồn tại, hoạt động được xem là chưa hoàn thành dù nhóm đã trao đổi miệng.')

# CH5
H('5. CÔNG CỤ HỖ TRỢ',1)
tbl('Bảng 26. Công cụ hỗ trợ chất lượng',['Nhóm','Công cụ','Mục đích'],[['Quản lý mã','Git/GitHub','Version, branch, review, tag release'],['API','Postman/Newman','Functional và integration test'],['Database','MySQL Workbench/CLI','Seed, query đối chiếu, backup'],['UI','Browser DevTools/Playwright','Responsive, regression, screenshot'],['Hiệu năng','k6/JMeter','Đo tải, p95, độ ổn định'],['Bảo mật','OWASP checklist, npm audit','Kiểm tra cơ bản và dependency'],['Tài liệu','Word/Markdown/draw.io','SRS, SDD, ERD, test artifacts'],['CI','GitHub Actions','Tự động build, test, lưu artifact']])
H('5.1. Rủi ro và biện pháp giảm thiểu',2)
tbl('Bảng 27. Rủi ro chất lượng',['Rủi ro','Ảnh hưởng','Biện pháp'],[['Database chưa sẵn sàng','Không test end to end','Seed script, health check, backup'],['Secret mặc định','Rủi ro token giả mạo','JWT secret qua env, không commit .env'],['Đồng thời đặt cùng căn','Trùng booking','Transaction/ràng buộc nghiệp vụ, load test'],['Thiếu test tự động','Regression khó phát hiện','Ưu tiên auth, booking, role'],['Chatbot lỗi','Mất tư vấn','Timeout và fallback'],['Thay đổi muộn','Trễ tiến độ','Change request và impact analysis']])
H('5.2. Checklist bàn giao và nghiệm thu',2)
P('Trước khi trình diễn hoặc bàn giao, nhóm thực hiện checklist dưới đây theo đúng thứ tự. Checklist giúp phân biệt một hệ thống đã chạy được với một phiên bản có đủ bằng chứng chất lượng và khả năng khôi phục.')
tbl('Bảng 28. Checklist bàn giao',['STT','Công việc','Tiêu chí hoàn thành','Bằng chứng'],[['1','Đóng băng phiên bản','Tag hoặc commit release được xác định','Version record'],['2','Kiểm tra cấu hình','PORT, DB và JWT secret đọc từ env','Config checklist'],['3','Khởi tạo database','database.sql chạy sạch, FK hoạt động','Import log'],['4','Kiểm tra tài khoản','Customer/admin đăng nhập đúng role','Auth test'],['5','Kiểm tra luồng đặt','Tạo, xem và hủy đơn đúng quyền','Booking test'],['6','Kiểm tra admin','CRUD và dashboard hoạt động','Admin test'],['7','Chạy regression','Case critical path pass','Test Summary'],['8','Backup dữ liệu','Có bản backup và hướng dẫn restore','Backup record'],['9','Hoàn thiện tài liệu','README, SRS, SDD, test docs đủ version','Document checklist'],['10','Nghiệm thu','Người dùng đại diện ký xác nhận','UAT sign off']])
P('Nếu có mục chưa hoàn thành, QA ghi nhận thành residual risk và đề xuất quyết định: sửa trước khi bàn giao, chấp nhận có điều kiện hoặc chuyển thành hạng mục bảo trì. Quyết định phải có người chịu trách nhiệm và thời hạn, không để lại dưới dạng trao đổi miệng.')
H('5.3. Vận hành, sao lưu và khôi phục',2)
P('Sau bàn giao, chất lượng tiếp tục được duy trì bằng kiểm tra sức khỏe dịch vụ, theo dõi log, sao lưu database và diễn tập khôi phục. Người vận hành phải kiểm tra trạng thái Node.js, kết nối MySQL, dung lượng lưu trữ và lỗi API trước khi mở hệ thống cho người dùng.')
tbl('Bảng 29. Kế hoạch vận hành',['Hoạt động','Tần suất','Tiêu chí/đầu ra'],[['Kiểm tra service','Mỗi lần triển khai','API và giao diện phản hồi đúng'],['Sao lưu database','Hàng ngày hoặc trước release','File backup có thời gian và người tạo'],['Kiểm tra log','Hàng ngày','Không có lỗi auth/DB bất thường chưa xử lý'],['Kiểm tra quyền','Mỗi release','Customer không gọi được admin API'],['Diễn tập restore','Theo mốc release','Khôi phục được DB seed/backup'],['Review dependency','Mỗi lần nâng package','Không có lỗ hổng nghiêm trọng chưa đánh giá'],['Xử lý sự cố','Khi có cảnh báo','Incident log, nguyên nhân và hành động khắc phục']])
P('Khi khôi phục, ưu tiên cô lập phiên bản lỗi, lưu log và backup hiện trạng, khôi phục database theo hướng dẫn, chạy smoke test đăng nhập/tra cứu/đặt phòng và ghi quyết định mở lại dịch vụ. Mọi hotfix sau đó vẫn phải quay lại quy trình review và regression test của Waterfall.')
H('5.4. Kết luận',2)
P('Báo cáo thiết lập hệ thống đảm bảo chất lượng cho StayEasy Homestay dựa trên Waterfall và ISO IEC 25010 2011. Các yêu cầu chất lượng đã được chuyển thành chỉ tiêu, tài liệu, review, test case, checklist, thủ tục QA và cổng chấp nhận. Để hoàn tất nộp bài, nhóm chỉ cần điền thông tin cá nhân trên bìa, chạy test thực tế và cập nhật Test Summary bằng số liệu thật.')
H('5.5. Kiến nghị hoàn thiện',2)
tbl('Bảng 30. Kiến nghị sau nghiệm thu',['Ưu tiên','Nội dung','Lợi ích chất lượng'],[['Cao','Bổ sung test tự động cho auth, booking và role','Giảm regression và lỗi phân quyền'],['Cao','Bổ sung transaction hoặc cơ chế chống race condition','Tránh trùng booking khi đồng thời'],['Cao','Đổi secret mặc định và quản lý ngoài repository','Giảm rủi ro token giả mạo'],['Trung bình','Chuẩn hóa response và correlation id','Dễ debug, dễ bảo trì'],['Trung bình','Thiết lập backup/restore rehearsal định kỳ','Tăng reliability'],['Thấp','Bổ sung quan trắc hiệu năng và lỗi','Theo dõi chất lượng sau bàn giao']])
P('Đánh giá cuối: hệ thống đáp ứng được phạm vi chức năng của đồ án và có cơ sở kiểm soát theo ISO IEC 25010. Các kết quả hiệu năng, tỷ lệ test pass và số lỗi còn lại phải được cập nhật sau khi nhóm chạy kiểm thử thật trên môi trường được ghi trong Test Plan.')
H('PHỤ LỤC A. DANH MỤC API VÀ HỒ SƠ BÀN GIAO',1)
tbl('Bảng 29. API trọng yếu',['Nhóm','Endpoint tiêu biểu','Quyền','Mục đích'],[['Xác thực','POST /register, POST /login','Public','Đăng ký và đăng nhập'],['Danh mục','GET /api/loai-phong, GET /api/can-phong/:id','Public/Auth','Tra cứu loại và căn'],['Đặt phòng','POST /api/dat-phong','Customer','Tạo yêu cầu đặt'],['Đơn của tôi','GET /api/don-dat-user/:idKH','Customer','Xem đúng đơn của mình'],['Hủy đơn','POST /api/huy-dat-phong','Customer','Hủy theo ownership'],['Hồ sơ','GET/PUT /api/khachhang/:idKH','Customer','Xem và sửa hồ sơ'],['Admin','/api/admin/*','Admin','CRUD dữ liệu vận hành'],['Dashboard','GET /api/dashboard, /api/hoatdong','Admin','Thống kê và nhật ký']])
tbl('Bảng 30. Hồ sơ bàn giao',['Hồ sơ','Nội dung cần có','Trạng thái'],[['Mã nguồn','server.js, frontend, chatbot, database.sql','Đính kèm repository'],['Cài đặt','README, package.json, requirements.txt, env mẫu','Kiểm tra được'],['Yêu cầu','SRS, BR/FR/NFR, RTM','Review approved'],['Thiết kế','SDD, ERD, API và security notes','Review approved'],['Kiểm thử','Test Plan, Cases, Defect, Summary, UAT','Cập nhật số liệu thật'],['Vận hành','Backup/restore, release note, hướng dẫn triển khai','QA/PM xác nhận']])
H('PHỤ LỤC B. MẪU TEST SUMMARY VÀ NGHIỆM THU',1)
P('Phụ lục này cung cấp biểu mẫu tối thiểu để nhóm hoàn thiện hồ sơ kiểm thử trước khi nộp hoặc trình diễn. Các ô số liệu phải được điền từ kết quả chạy thật, có version, môi trường và người xác nhận; không dùng số liệu ước lượng để thay thế bằng chứng kiểm thử.')
tbl('Bảng 31. Mẫu Test Summary',['Trường thông tin','Nội dung cần ghi','Bằng chứng kèm theo'],[['Phiên bản kiểm thử','Release/build, commit hoặc tag được chạy','Version record'],['Thời gian và môi trường','Ngày giờ, máy, Node.js, MySQL, trình duyệt','Environment record'],['Phạm vi','Module và yêu cầu được kiểm tra','Test Plan/RTM'],['Tổng số test case','Số case đã thiết kế và số case thực thi','Test case list'],['Kết quả','Pass, Fail, Blocked, Not run','Execution log'],['Tỷ lệ đạt','Pass/(Pass + Fail) theo phạm vi đã chốt','Bảng tổng hợp'],['Lỗi còn mở','Mã lỗi, severity, owner, workaround','Defect report'],['Kiểm thử hồi quy','Phạm vi chạy lại sau sửa lỗi','Re-test log'],['Rủi ro tồn đọng','Ảnh hưởng, xác suất, biện pháp theo dõi','Risk register'],['Quyết định','Release, UAT hoặc chấp nhận có điều kiện','PM/QA sign off']])
H('B.1. Mẫu tiêu chí nghiệm thu theo luồng nghiệp vụ',2)
tbl('Bảng 32. Ma trận UAT mẫu',['ID UAT','Luồng người dùng','Điều kiện đạt','Người xác nhận'],[['UAT-01','Khách đăng ký và đăng nhập','Tài khoản hợp lệ đăng nhập được; sai mật khẩu có thông báo an toàn','Đại diện khách hàng'],['UAT-02','Tra cứu loại và căn phòng','Dữ liệu, giá, tiện nghi và trạng thái hiển thị đúng','Đại diện khách hàng'],['UAT-03','Đặt phòng hợp lệ','Đơn được tạo, trạng thái đúng và xuất hiện trong danh sách của khách','Đại diện khách hàng'],['UAT-04','Từ chối đặt trùng','Hệ thống không tạo đơn trùng và thông báo rõ nguyên nhân','QA/Đại diện người dùng'],['UAT-05','Khách xem và hủy đơn','Chỉ thao tác được trên đơn thuộc quyền sở hữu','Đại diện khách hàng'],['UAT-06','Admin xử lý dữ liệu','Admin CRUD đúng quyền; customer không gọi được API admin','Đại diện quản trị'],['UAT-07','Theo dõi dashboard và log','Số liệu phản ánh dữ liệu kiểm thử; hoạt động quan trọng có log','Đại diện quản trị'],['UAT-08','Bàn giao và khôi phục','README, database script và hướng dẫn restore thực hiện được','PM/QA']])
H('B.2. Mẫu biên bản defect và quyết định phát hành',2)
tbl('Bảng 33. Trường thông tin defect bắt buộc',['Trường','Yêu cầu ghi nhận','Ví dụ'],[['Mã và tiêu đề','Mã duy nhất, mô tả ngắn gọn hành vi sai','BOOK-008: tạo đơn trùng'],['Môi trường/version','Build, trình duyệt, database và dữ liệu test','release-1, Chrome, MySQL 8.x'],['Điều kiện và bước tái hiện','Các bước đủ để người khác lặp lại','Đăng nhập -> chọn cùng căn -> gửi hai đơn'],['Kết quả mong đợi/thực tế','Ghi rõ expected và actual, không mô tả chung chung','Expected từ chối; actual tạo hai bản ghi'],['Severity/priority/owner','Mức độ, ưu tiên, người chịu trách nhiệm','Major/High/Developer A'],['Bằng chứng','Screenshot, request/response, log hoặc query','Ảnh UI và log API'],['Kết quả xử lý','Commit sửa, re-test, regression và trạng thái cuối','Fixed -> Re-test -> Closed']])
P('Trước khi phát hành, QA đối chiếu Test Summary với defect report và checklist bàn giao. Nếu còn lỗi major hoặc rủi ro chưa xử lý, quyết định release phải ghi rõ người chấp nhận, phạm vi ảnh hưởng, biện pháp tạm thời và thời hạn khắc phục. Đây là điều kiện để hồ sơ có thể được kiểm tra độc lập sau khi nhóm kết thúc đồ án.')
H('PHỤ LỤC C. PHIẾU TỰ ĐÁNH GIÁ TRƯỚC KHI NỘP',1)
P('Nhóm sử dụng phiếu này để tự kiểm tra lần cuối báo cáo và sản phẩm. Mỗi mục cần có trạng thái Đạt, Chưa đạt hoặc Cần bổ sung; các mục Chưa đạt phải được chuyển thành hành động khắc phục có người phụ trách và thời hạn.')
tbl('Bảng 34. Phiếu tự đánh giá hồ sơ chất lượng',['STT','Nội dung tự đánh giá','Bằng chứng cần kiểm tra','Trạng thái'],[['1','Bìa báo cáo có tên trường, khoa, đề tài, sinh viên, lớp và giảng viên','Trang bìa đã điền đủ thông tin','Đạt/Chưa đạt'],['2','Mục lục và số trang khớp với nội dung thực tế','Mở file bằng Word và kiểm tra lại field','Đạt/Chưa đạt'],['3','Phạm vi, yêu cầu người dùng và yêu cầu phần mềm rõ ràng','Mục 1.2 và 1.3, SRS/RTM','Đạt/Chưa đạt'],['4','Mô hình Waterfall có giai đoạn, đầu ra và cổng chất lượng','Mục 3 và các baseline','Đạt/Chưa đạt'],['5','Tám đặc tính ISO/IEC 25010 được liên hệ với sản phẩm','Bảng yêu cầu và chỉ tiêu chất lượng','Đạt/Chưa đạt'],['6','Có kế hoạch, checklist, test case và vòng đời defect','Mục 4.4 và 4.5','Đạt/Chưa đạt'],['7','Đủ sáu thủ tục QA và ma trận trách nhiệm','Mục 4.6 và 4.7','Đạt/Chưa đạt'],['8','Có công cụ, rủi ro, bàn giao, vận hành và khôi phục','Chương 5 và Phụ lục A','Đạt/Chưa đạt'],['9','Test Summary sử dụng số liệu đo thật, không chỉ ghi mục tiêu','Phụ lục B và log kiểm thử','Đạt/Chưa đạt'],['10','Thông tin tham khảo và mã nguồn được ghi rõ','Tài liệu tham khảo/README','Đạt/Chưa đạt']])
P('Kết luận tự đánh giá: báo cáo chỉ được xem là sẵn sàng nộp khi các mục bắt buộc đạt, không còn lỗi trình bày nghiêm trọng, các số liệu kiểm thử có bằng chứng và thông tin cá nhân trên bìa đã được hoàn thiện.')
H('TÀI LIỆU THAM KHẢO',1)
bullets(['ISO/IEC 25010:2011 - Systems and software engineering - Systems and software Quality Requirements and Evaluation.','IEEE 730 - Software Quality Assurance Plans.','IEEE 829 - Software and System Test Documentation.','Mã nguồn và README của dự án StayEasy Homestay.','Tài liệu mẫu Bài 08 về thiết lập và vận hành hệ thống đảm bảo chất lượng phần mềm.'])
d.core_properties.title='Báo cáo đảm bảo chất lượng phần mềm StayEasy Homestay'; d.core_properties.subject='Waterfall và ISO IEC 25010 2011'; d.core_properties.author=''
d.save(OUT); print(OUT)
