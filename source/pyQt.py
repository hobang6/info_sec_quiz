import os
import sys

# 반드시 PyQt5 import 전에 실행되어야함
if getattr(sys, 'frozen', False):
    pathlist = []
    pathlist.append(sys._MEIPASS)
    _main_app_path = os.path.dirname(sys.executable)
    pathlist.append(_main_app_path)
    os.environ["PATH"] += os.pathsep + os.pathsep.join(pathlist)

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import CUHA_logo
import font

from design_1 import quiz_main
from design_2 import quiz_result
from design_3 import quiz_solution

# 전역변수
Sel_Status = 0
current_stage = 0
max_stage = 20
user_answer = [0 for i in range(max_stage)]
quiz_list = """
문제 1. 다음 중 가장 안전하게 비밀번호를 설정한 사람은?#
문제 2. 다음 중 가장 안전하게 공용 컴퓨터를 사용한 사람은?#
문제 3. 유튜브 링크가 적힌 광고성 문자를 받았다. 가장 현명하게 대처한 사람은?#
문제 4. 친한 친구가 메신저로 온라인 게임의 이벤트 보상을 대신 받아준다며\n아이디와 비밀번호를 요구했다. 가장 현명하게 대처한 사람은?#
문제 5. 나의 SNS 계정이 해킹당해 내가 작성하지 않은 게시글들이 업로드되었다.\n가장 현명하게 대처한 사람은?#
문제 6. 최근에 상영된 영화를 무료로 볼 수 있는 불법 사이트를 발견했다.\n다음 중 옳은 행동은?#
문제 7. 새로운 S/W 업데이트 알림이 울렸다. 다음 중 옳은 행동은?#
문제 8. 다음 중 가장 안전하게 개인 PC를 보호하는 사람은?#
문제 9. 은행에서 수상한 거래내역이 있다며 문자로 링크를 보내왔다.\n가장 현명하게 대처한 사람은?#
문제 10. 유명 유튜버의 구독자 이벤트 당첨 메일이 왔다. 메일에서는\n본인확인을 위한 개인 정보를 입력을 요구했다. 가장 현명하게 대처한 사람은?#
문제 11. 마스크를 무료로 제공한다는 메일을 받았다. 다음 중 옳은 행동은?#
문제 12. 설문 조사에 참여하면 무료로 기프티콘을 준다며 링크를 보내왔다.\n다음 중 옳은 행동은?#
문제 13. 평소에 갖고 싶었던 무선 이어폰이 저렴한 가격에 중고장터에 올라왔다.\n연락을 해보니 안전거래를 제안하며 링크를 보내온다. 가장 현명하게 대처한 사람은?#
문제 14. 가족 혹은 친한 지인이 갑자기 돈을 빌려달라며 문자로 계좌를 보내왔다.\n가장 현명하게 대처한 사람은?#
문제 15. 자신이 속해있는 집단(학교, 회사 등)에서 메일을 보내\n첨부파일을 확인해달라고 한다. 가장 현명하게 대처한 사람은?#
문제 16. 다음 중 랜섬웨어의 예방법으로 옳지 않은 것은?#
문제 17. 다음 중 피싱 사이트와 정상 사이트를 구분하기 위한 방법으로 옳은 것은?#
문제 18. 다음 중 본인의 계정이 해킹 당했을 때\n예상할 수 있는 피해로 옳지 않은 것은?#
문제 19. 다음 중 본인의 계정이 해킹 당했다는 사실을 알았을 때\n대처로 옳지 않은 것은?#
문제 20. 다음 중 자신의 개인 정보를 보호하기 위한 방법으로 옳지 않은 것은?
""".split('#')
sel_1_list = """
쉽게 기억할 수 있도록 모든 사이트의 비밀번호를 동일하게 설정한 나연#
컴퓨터를 사용한 뒤 모든 페이지에서 로그아웃하고, 다운로드했던 문서들을 삭제한 나연#
인터넷에 해당 유튜브 링크를 검색한 후, 피해 사례가 없는 것을 확인 후 링크를 클릭한 나연#
아이디와 비밀번호를 알려주어 아이템을 받아낸 후, 친구와의 연락을 끊고 잠적한 나연#
해커가 올린 게시글을 삭제한 후 계정을 탈퇴한 나연#
불법 사이트의 주소를 공유하는 것은 범죄이기 때문에 혼자서만 이용한 나연#
기존에 유료 백신을 사용하고 있었기 때문에 업데이트를 하지 않은 나연#
유료 백신 프로그램을 구매해 사용하는 나연#
계좌가 도용당해 더 큰 사건에 휘말리기 전에 링크를 클릭하여 확인한 나연#
이벤트에 당첨되었다는 소식에 바로 개인 정보를 입력한 나연#
본인보다 마스크 구매가 힘든 상황의 사람들에게 메일을 전달해 도우려 한 나연#
친구에게 생일 선물이라며 링크를 전달한 나연#
해당 링크 주소를 인터넷에 검색해본 뒤 별다른 피해 사례가 없는 것을 확인하고
 링크를 클릭한 나연#
문자로 자초지종을 묻고 안타까운 마음에 돈을 보낸 나연#
학교 메일의 주소가 맞는지 확인해본 뒤 첨부파일을 확인한 나연#
의심스러운 파일은 다운로드하지 않기#
정상 사이트와 유사하지만 미세하게 다른 부분이 있기 때문에 그 점을 이용한다.#
주변 지인들에게 보내며 돈을 빌리려는 메시지가 발송될 수 있다.#
비밀번호를 변경하고 2차 비밀번호를 설정하여 보안을 강화한다.#
비밀번호를 주기적으로 변경한다.
""".replace('\n', '').split('#')
sel_2_list = """
쉽게 기억할 수 있도록 본인의 이름과 생년월일로 비밀번호를 설정한 정연#
자주 이용하던 웹사이트에서 자동 로그인 기능을 활성화하여 편리하게 사용한 정연#
자신의 컴퓨터를 보호하기 위해 공용 컴퓨터에서 링크를 클릭한 정연#
친구를 믿지 못해 아이디와 비밀번호를 알려주지 않은 정연#
해커가 올린 게시글을 삭제한 후 비밀번호를 변경하고 2차 비밀번호를 추가로 설정한 정연#
좋은 사이트를 발견했다며 친구들과 사이트의 주소를 공유한 정연#
S/W 업데이트 알림이 불편해 알림을 꺼놓은 정연#
무료 백신을 사용하며 의심스러운 파일은 다운로드하지 않는 정연#
본인이 자주 사용하는 은행인 것을 확인하고 링크를 클릭한 정연#
유튜버 본인의 메일인지 확인하기 위해 메일의 주소를 확인하고 정보를 입력한 정연#
마스크를 구하기 위해 메일을 바로 확인한 정연#
무료로 기프티콘을 준다고 하자 바로 설문 조사 링크를 누른 정연#
링크를 클릭하니 수상한 사이트가 아닌 안전한 네이버 로그인 화면이 나와 
로그인을 시도한 정연#
전화를 걸어 확인해보려 했지만 받지 않는 것을 보아 급한 일이라 생각하여 돈을 보낸 정연#
평소에 비슷한 메일을 자주 받았었기에 첨부파일을 확인한 정연#
유료 프로그램의 불법 복제판을 사용하기#
사이트의 URL을 공식 사이트와 비교한다.#
나는 주변 지인이 없는 외톨이기 때문에 아무런 피해가 없다.#
해커에게 고소하겠다며 협박한다.#
SNS에서 친구로 추가된 사람만 내 개인 정보를 확인할 수 있게 한다.
""".replace('\n', '').split('#')
sel_3_list = """
남들이 쉽게 유추할 수 없는 비밀번호를 설정하고 
모든 사이트의 비밀번호를 다르게 설정한 다현#
업무 관련 문서 열람 후 다른 사람이 보지 못하도록 컴퓨터를 종료시킨 다현#
의심스러운 링크를 클릭하지 않은 다현#
아이디와 비밀번호를 알려주어 아이템을 받아낸 후, 비밀번호를 재설정한 다현#
해커가 올린 게시글을 삭제한 후 같은 비밀번호를 사용하는 모든 사이트의 비밀번호를 변경한 다현#
불법 사이트에 바이러스가 있을지 모르니 접속하지 않은 다현#
매번 알림이 울리도록 설정하며 S/W를 업데이트한 다현#
백신을 사용하지는 않지만 주기적으로 S/W 업데이트를 하는 다현#
의심스러운 링크를 클릭하지 않은 다현#
개인 정보를 입력하는 것이 불안해 메일을 삭제하고 답장을 하지 않은 다현#
마스크를 나눔 하는 제공자를 확인해본 뒤, 정부 기관이라면 
메일을 확인하려는 다현#
거짓된 설문 조사인지 검색 후 안전하지 않다는 것을 알고 
링크를 누르지 않은 다현#
의심스러운 링크를 클릭하지 않은 다현#
다른 친한 지인에게도 같은 내용의 문자가 왔다는 것을 확인 후 
돈을 보내지 않고 기다린 다현#
같은 집단 구성원에게도 같은 메일이 왔는지 확인한 후 
안심하고 첨부파일을 열어본 다현#
PC의 운영체제와 백신을 항상 최신 버전으로 유지하기#
웹 브라우저에 자물쇠 아이콘이 있고, https 연결이 이루어지는 
사이트라면 정상 사이트이다.#
본인의 계정이 중고장터 등에서 범죄 수단으로 이용될 수 있다.#
2차 피해자가 있는지 확인한다.#
공용 컴퓨터 사용을 자제한다.
""".replace('\n', '').split('#')
sol_list = """
비밀번호를 자신의 개인 정보와 연관 지어 생성하면 해킹 당할 가능성이 더 높아진다. 또한 기억하기 쉽게 하기 위해
모든 사이트의 비밀번호를 동일하게 설정하면 하나의 사이트라도 해킹당하면 해커가 모든 사이트에 접근할 수 있어 
추가 피해가 더욱더 커질 수 있다. 남들이 쉽게 유추할 수 없는 비밀번호를 설정하고, 모든 사이트의 비밀번호를 
다르게 설정한다면 이러한 피해를 예방할 수 있다.#
공용 컴퓨터를 사용하고 나선 항상 자기가 로그인했던 모든 페이지에서 로그아웃하고 다운로드했던 문서들을 확실하게 
삭제하는 것이 안전하다. 또한 자동 로그인 기능을 공용 컴퓨터에서 활성화하여 사용한다면 타인이 내 계정에 
접속할 수 있기 때문에 공용 컴퓨터 사용시 주의해야 한다.#
자신이 피해 사례의 첫 번째가 될 수도 있기 때문에 모르는 링크는 항상 조심하는 게 좋다. 가장 현명하게 대처한 
사람이기 때문에 공용 컴퓨터에서 링크를 클릭한 정연보다는 의심스러운 링크를 클릭하지 않은 다현이 
가장 현명한 대처 방법이다.#
자신의 개인 정보는 아무리 친한 지인이더라도 알려주지 않는 것이 바람직하다. 또한 친한 친구의 계정이 
해킹 당했을 가능성이 있기 때문에 개인 정보는 더더욱 알려주지 않는 것이 좋다. 따라서 아이디와 비밀번호를 
알려주지 않은 정연이 제일 현명하게 대처했다고 볼 수 있다.#
계정을 해킹당하고 각자 대처는 나쁘지 않았지만, 나연이와 정연이는 2차 피해를 생각하지 못하고 SNS 
계정에 대한 것만 생각했다. 다현이처럼 2차 피해도 고려해 같은 비밀번호를 사용하는 모든 사이트의 비밀번호를 
변경해서 추가적인 피해를 막는 것이 가장 현명하다.#
불법 사이트 자체가 이름에서도 알 수 있듯이 범법행위이다. 불법 사이트는 사용하지 않는 것이 바람직하다. 
또한 불법 사이트를 공유하는 것도 범법 행위이다. 특히 불법 사이트에는 바이러스가 포함되어 있을 가능성이 높기 
때문에 사이트에 접속하지 않은 다현이가 가장 옳은 행동을 했다고 볼 수 있다.#
S/W에는 항상 보안 결함이 존재한다. 이러한 결함들을 보완해 새로운 업데이트를 하기 때문에 꾸준히 
S/W 업데이트를 하는 것이 바람직하다. 또한 백신 프로그램을 사용하고 있더라도 S/W 업데이트를 하지 않으면 
안전하다고 할 수 없다.#
개인 PC를 안전하게 보호하기 위해서는 주기적으로 S/W 업데이트를 진행하고, 백신 프로그램을 설치하는것이 
바람직하다. 또한 백신프로그램을 사용하더라도 모든 바이러스를 방지하지는 못하기 때문에 의심스러운 
파일을 다운로드 하지 않는 것이 바람직하다.#
본인이 평소 사용하던 은행에서 온 문자로 하더라도 사칭의 위험성이 있기 때문에 링크룰 클릭하지 않는 것이 
바람직하다. 만약 이러한 상황이 발생한다면 링크를 클릭하지 않고 은행에 전화해 사실 여부를 확인해야 한다.#
유튜버 본인의 메일 주소가 맞다고 하더라도 해커가 유명 유튜버의 계정을 해킹해 이벤트를 빌미로 개인 정보를 
요구하는 메일을 다량으로 전송해 큰 피해가 발생한 사례가 있기 때문에 개인 정보 처리 방침을 명시한 신뢰할 수 
있는 기관이 아니라면 절대 개인 정보를 입력하지 않는 것이 바람직하다.#
메일의 발신자를 확인하지 않으면 바이러스에 감염되거나 개인정보를 탈취 당할 수 있다. 신뢰할 수 있는 발신자인지 
확인 후 메일을 열어보는 것이 현명하다. 또한 검증되지 않은 메일을 다른 사람들에게 전송하면 
추가 피해가 발생할 수 있다.#
링크의 발신자를 확인하지 않으면 바이러스에 감염되거나 개인정보를 탈취 당할 수 있다. 신뢰할 수 있는 발신자인지 
확인 후 링크를 확인하는것이 현명하다. 또한 설문조사에 응할때는 개인정보를 기입하지 않도록 하고 
만약 기입해야 한다면 개인정보 처리 방침이 있는지 확인해야 한다.#
확인되지 않은 링크를 클릭하면 바이러스에 감염되거나 개인정보를 탈취 당할 수 있다. 또한 링크 주소를 인터넷에 
검색해본 뒤 별다른 피해 사례가 없다고 하더라도, 본인이 첫 피해자일 수 있으니 안심할 수 없다. 
의심스러운 링크는 클릭하지 않는 것이 가장 현명하다.#
금전을 요구하는 문자를 수신했을시에는 반드시 당사자가 보낸 문자가 맞는지 확인을 해야한다. 특히 
위와 같은 사례는 휴대전화를 분실한 경우가 대다수이기 때문에 전화를 받지 않는 경우가 많다. 따라서 본인확인이 
어려울 경우에는 절대 돈을 보내지 않고 침착하게 기다리는것이 바람직하다.#
메일을 확인할 때에는 반드시 발신자를 확인해야 한다. 이는 바이러스를 방지하는 가장 좋은 습관이기도 하다. 
또한 대량의 스팸 메일 또는 바이러스를 포함한 메일이 다수에게 동시다발적으로 발송된 것일 수 있기 때문에 같은 
집단 구성원에게 동일한 메일이 왔다고 하더라도 반드시 메일의 발신자를 확인 해야한다.#
랜섬웨어 뿐만 아니라 컴퓨터 바이러스를 예방하기 위해서는 불법 복제판 등의 프로그램 사용을 지양하고
PC의 운영체제와 백신을 항상 최신 버전으로 유지하는 것이 바람직하다. 또한 값비싼 유료 백신을 사용하기 보다는 
무료 백신을 사용하면서 의심스러운 파일을 다운로드하지 않는 것이 더욱 효과적이다.#
피싱 사이트는 육안으로 확인할 수 없을 정도로 정상 사이트와 유사한 경우가 많다. 따라서 반드시 공식 사이트와 
URL을 비교한 후 이용해야 한다. 또한 최근에는 무료 인증서 발급 절차가 간소화되어 피싱 사이트도 웹 브라우저에 
자물쇠가 표시되고, https 접속이 가능해졌기 때문에 정상 사이트와 주소야 정확히 일치해야 신뢰할 수 있다.#
개인정보 해킹 피해가 발생하면 다음과 같은 피해가 예상된다. 
1. 피해자의 메신저 등을 통해 주변 지인들에게 금전 요구 
2. 피해자의 온라인 게임 아이템 혹은 인터넷 쇼핑몰 포인트 탈취 
3. 피해자의 계정을 중고장터 사기 등 각종 범죄 수단으로 이용함#
본인의 계정이 해킹 당했을 때에는 다음과 같이 행동해야 한다. 
1. 비밀번호 변경과 OTP, 2차 비밀번호등을 설정하여 보안 수준을 높여 해킹 피해를 예방. 
2. 2차 피해자가 있는지 확인하여 추가 피해를 예방. 또한 해커를 자극하게 되면 더 큰 피해를 야기할 수 있으며
현 상황에서의 이점이 없다고 볼 수 있다.#
개인정보를 보호하기 위해서는 다음과 같이 행동해야 한다. 
1. 백신프로그램 설치하고 바이러스 검사하기		
2. 비밀번호 설정하고 주기적으로 변경하기		
3. 신뢰할 수 없는 웹사이트 및 파일 주의하기 또한 친구의 SNS 계정이 해킹 당했을 시에 본인의 개인 정보까지 
유출될 가능성이 있기 때문에 온라인 상에서는 개인정보를 공개하지 않는 것이 안전하다.#
""".split('#')
answer_list = "3/1/3/2/3/3/3/2/3/3/3/3/3/3/1/2/2/2/2/2".split('/')


class MyMainWindow(QtWidgets.QMainWindow, quiz_main):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.quiz_main_setupUi(self)

        self.Btn_1.clicked.connect(self.Btn_1_clicked)
        self.Btn_2.clicked.connect(self.Btn_2_clicked)
        self.Btn_3.clicked.connect(self.Btn_3_clicked)

        self.Btn_Next.clicked.connect(self.Btn_Next_clicked)
        self.Btn_Prev.clicked.connect(self.Btn_Prev_clicked)

    def Btn_1_clicked(self):
        global Sel_Status
        self.reset_btn()
        self.Btn_1.setText("V")
        self.Btn_1.setStyleSheet("Color : green")
        Sel_Status = 1

    def Btn_2_clicked(self):
        global Sel_Status
        self.reset_btn()
        self.Btn_2.setText("V")
        self.Btn_2.setStyleSheet("Color : green")
        Sel_Status = 2

    def Btn_3_clicked(self):
        global Sel_Status
        self.reset_btn()
        self.Btn_3.setText("V")
        self.Btn_3.setStyleSheet("Color : green")
        Sel_Status = 3

    def Btn_Next_clicked(self):
        global user_answer
        global current_stage
        if Sel_Status != 0:
            user_answer[current_stage] = Sel_Status
            if current_stage != 19:
                current_stage += 1
                self.reset_btn()
                self.Current_num.setText(str(current_stage + 1))
                self.Quiz_Label.setText(quiz_list[current_stage])
                self.Sel_1.setText(sel_1_list[current_stage])
                self.Sel_2.setText(sel_2_list[current_stage])
                self.Sel_3.setText(sel_3_list[current_stage])
            else:
                self.switch_window.emit()

    def Btn_Prev_clicked(self):
        global user_answer
        global current_stage
        if current_stage != 0:
            current_stage -= 1
            self.reset_btn()
            self.Current_num.setText(str(current_stage + 1))
            self.Quiz_Label.setText(quiz_list[current_stage])
            self.Sel_1.setText(sel_1_list[current_stage])
            self.Sel_2.setText(sel_2_list[current_stage])
            self.Sel_3.setText(sel_3_list[current_stage])
            if user_answer[current_stage] == 1:
                self.Btn_1_clicked()
            if user_answer[current_stage] == 2:
                self.Btn_2_clicked()
            if user_answer[current_stage] == 3:
                self.Btn_3_clicked()

    def reset_btn(self):
        global Sel_Status

        Sel_Status = 0

        self.Btn_1.setEnabled(True)
        self.Btn_1.setText("1")
        self.Btn_1.setStyleSheet("Color : black")

        self.Btn_2.setEnabled(True)
        self.Btn_2.setText("2")
        self.Btn_2.setStyleSheet("Color : black")

        self.Btn_3.setEnabled(True)
        self.Btn_3.setText("3")
        self.Btn_3.setStyleSheet("Color : black")

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_1:
            self.Btn_1_clicked()
        if key == QtCore.Qt.Key_2:
            self.Btn_2_clicked()
        if key == QtCore.Qt.Key_3:
            self.Btn_3_clicked()
        if key == QtCore.Qt.Key_Return:
            self.Btn_Next_clicked()
        if key == QtCore.Qt.Key_Backspace:
            self.Btn_Prev_clicked()
        if key == QtCore.Qt.Key_Escape:
            self.close()


class ShowResult(QtWidgets.QMainWindow, quiz_result):
    switch_window = QtCore.pyqtSignal(int)

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.quiz_result_setupUi(self)
        btn_list = [self.q_1_btn, self.q_1_btn_2, self.q_1_btn_3, self.q_1_btn_4, self.q_1_btn_5, self.q_1_btn_6,
                    self.q_1_btn_7, self.q_1_btn_8, self.q_1_btn_9, self.q_1_btn_10, self.q_1_btn_11, self.q_1_btn_12,
                    self.q_1_btn_13, self.q_1_btn_14, self.q_1_btn_15, self.q_1_btn_16, self.q_1_btn_17,
                    self.q_1_btn_18, self.q_1_btn_19, self.q_1_btn_20]
        score = 0
        i = 0

        while i != 20:
            if user_answer[i] == int(answer_list[i]):
                btn_list[i].setText('O')
                btn_list[i].setStyleSheet("Color : green")
                score += 1
            else:
                btn_list[i].setText('X')
                btn_list[i].setStyleSheet("Color : red")
            btn_list[i].clicked.connect(partial(self.switch, i))
            i += 1

        self.score_label.setText(str(score))

    def switch(self, arg):
        self.switch_window.emit(arg)

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()


class ShowSolution(QtWidgets.QMainWindow, quiz_solution):

    def __init__(self, q_num):
        QtWidgets.QMainWindow.__init__(self)
        self.quiz_solution_setupUi(self)
        self.sol_q.setText(quiz_list[q_num])
        self.my_answer.setText(str(user_answer[q_num]))
        self.real_answer.setText(answer_list[q_num])
        self.question_1.setText(sel_1_list[q_num])
        self.question_2.setText(sel_2_list[q_num])
        self.question_3.setText(sel_3_list[q_num])
        self.question_4.setText(sol_list[q_num])  # 문제 해설

        if answer_list[q_num] == '1':
            self.question_1.setStyleSheet("Color : green")
            self.question_2.setStyleSheet("Color : red")
            self.question_3.setStyleSheet("Color : red")
        elif answer_list[q_num] == '2':
            self.question_1.setStyleSheet("Color : red")
            self.question_2.setStyleSheet("Color : green")
            self.question_3.setStyleSheet("Color : red")
        else:
            self.question_1.setStyleSheet("Color : red")
            self.question_2.setStyleSheet("Color : red")
            self.question_3.setStyleSheet("Color : green")

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Escape:
            self.close()


class Controller:

    def __init__(self):
        pass

    def show_main(self):
        self.window = MyMainWindow()
        self.window.switch_window.connect(self.show_result)
        self.window.show()

    def show_result(self):
        self.window_two = ShowResult()
        self.window_two.switch_window.connect(self.show_solution)
        self.window.close()
        self.window_two.show()

    def show_solution(self, q_num):
        self.window_three = ShowSolution(q_num)
        self.window_three.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())
