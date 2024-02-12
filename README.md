# GUI tool for Pothole Detection

## Requirements
This project requires the following development environment:
- Ubuntu 20.04 LTS
- Python 3.8.10
- PyQt5 5.14.1
- OpenCV2 4.9.0

## Guide
- `GUI.py` : Main Script for GUI. 
- `scripts/segnet-camera-excel.py` : Python Script to detect pothole and save data file. DO NOT RUN WITHOUT SETTING DEPENDENCY.
- `test/file_down_test.py` : Example Script for testing scenario. If you run `GUI.py`, this script will also be executed.
- `test/from_path/` : Directory for test (Data Save Path).
- `test/to_path/` : Directory fro test (Data Copy Path).

## Run
Run these commands in bash shell (Ubuntu 20.04) :
```
$ pip install pyqt5
$ pip install opencv-python
$ python3 GUI.py
```
---
## GUI 화면 구성

### 메인창 - 좌측
* 카메라 미리보기(1280*720) & ROI 박스(1024*512)
    * 웹캠 화면(1920*1080)을 resize된 크기로 미리 보여주며, 터치로 ROI 영역 지정 가능함.
    * ROI 영역의 초기 좌표는 중앙 하단이며, 어디를 터치해도 카메라 미리보기 영역을 벗어나지 않음.
 
### 메인창 - 우측
* ROI 박스 좌표 표시 영역
    * 메인창 좌측에서 터치로 ROI 영역의 좌표를 바꿀 때마다 웹캠 해상도(1920*1080)를 기준으로 한 ROI 영역의 좌표를 업데이트함.
    * 이 표시 영역에 보이는 두 정수(x, y)가 매개변수가 되어 자식 프로세스의 스크립트로 넘어감.
* `HORIZONTAL FLIP(상하반전)` 버튼
    * 클릭 시 메인창 좌측에 보이는 카메라 미리보기가 상하반전됨.
    * 상하반전 여부에 관련된 이진 변수의 값이 변경되는 방식이며, 이 또한 매개변수로 넘어감.
* `START(자식 프로세스 시작)` 버튼
    * 클릭 시 메인창 좌측의 카메라 미리보기와 ROI 박스가 사라지고, GUI 프로그램의 위에 실제 웹캠 화면과 ROI 영역이 새 창으로 뜨게 됨.
* `STOP(자식 프로세스 종료)` 버튼
    * 클릭 시 메인창 좌측의 카메라 미리보기와 ROI 박스가 원상복구되고, 실제 웹캠 화면과 ROI 영역이 포함된 새 창이 종료됨.
* 경로 표시 영역 & `SELECT PATH(경로 선택)` 버튼
    * 저장된 데이터를 복사(혹은 이동)할 경로로, 기본값은 ".."(상대경로)로 지정되어 있으나 경로 표시 영역에는 절대경로로만 표시됨. 버튼 클릭 시 파일선택창이 새로 열리며, 해당 창에서 디렉토리 경로 선택 가능함. 경로 선택 완료 시 경로 표시 영역도 업데이트됨.
* `DOWNLOAD` 버튼
    * 클릭 시 ./Result/Excel/ 경로(코드 내에 리터럴로 정의되어 있음. GUI 상에서 수정 불가)의 엑셀 파일(.xls)을 체크 가능한 리스트 형태로 새 창에 띄워줌 (-> 파일관리창).
    * 각 엑셀 파일들은 ./Result/full_frame_detect/ 경로 내에 존재하는 동일 이름의 디렉토리(이미지 데이터를 포함)와 연동되어 있으며, 리스트에서 엑셀 파일을 체크하면 해당 파일과 연동된 디렉토리까지 처리됨.
    * OS의 파일관리시스템 기능 중 일부 기능을 구현했으며, 실 환경에서 OS의 파일관리시스템의 역할을 일부 대체하는 것을 목표로 함.
* `SHUTDOWN` 버튼
    * 실행 중인 자식 프로세스를 안전하게 종료한 후 컴퓨터의 전원을 끔.
 
#### 파일관리창
* `Select All` 버튼
    * 리스트에 표시된 모든 엑셀 파일을 체크함.
* `REFRESH` 버튼
    * 리스트를 새로고침함.
* `COPY` 버튼
    * 체크된 엑셀 파일들과 각 엑셀 파일에 해당하는 디렉토리를 전부 메인창 우측의 경로 표시 영역에 표시된 경로로 복사함.
    * 복사 도중에는 모든 버튼이 클릭 불가능하게 바뀌며, 복사가 완료되면 메세지창으로 완료되었다고 알려줌.
* `MOVE` 버튼
    * 체크된 엑셀 파일들과 각 엑셀 파일에 해당하는 디렉토리를 전부 메인창 우측의 경로 표시 영역에 표시된 경로로 이동함.
    * 이동 도중에는 모든 버튼이 클릭 불가능하게 바뀌며, 이동이 완료되면 메세지창으로 완료되었다고 알려줌.
    * 사용자가 따로 새로고침하지 않아도 이동 작업이 완료되면 리스트가 자동으로 업데이트됨.
* `DELETE` 버튼
    * 체크된 엑셀 파일들과 각 엑셀 파일에 해당하는 디렉토리를 전부 삭제함.
    * 삭제 도중에는 모든 버튼이 클릭 불가능하게 바뀌며, 삭제가 완료되면 메세지창으로 완료되었다고 알려줌.
    * 사용자가 따로 새로고침하지 않아도 삭제가 완료되면 리스트가 자동으로 업데이트됨.
* `FINISH` 버튼
    * 현재 창을 안전하게 종료한 후 메인창으로 돌아감.
 

