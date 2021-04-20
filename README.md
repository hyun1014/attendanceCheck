# 출석체크 스샷 이름 추출

일일이 노가다로 스크린샷에 있는 이름들을 하나하나 세고 앞출석, 뒤출석과 비교하는게 빡쳐서<br/>
카카오 developer open api중에 OCR api를 한번 써보기로 했습니다.<br/>
쉽게 보면 이미지에서 문자 영역을 감지하고 추출하는건데 스샷 있는것들 전부 api 요청해서<br/>
앞출석에만 있는 이름들 / 뒤출석에만 있는 이름들 / 전부 있는 이름들 <br/>
이렇게 구별해서 json으로 내보내는 방식으로 진행해봤습니다.

### 환경 세팅

가상환경 만들던가 하고 필요한 패키지들 설치하세요.
```shell script
pip install -r requirements.txt
```
### 사용 방법
```shell script
python main.py 앞출석스샷폴더 뒤출석스샷폴더 apikey
```
apikey는 보안상 github에 올리지 않았습니다

### 사용해본 결과
문자 인식률이 그래도 괜찮습니다. 일부 요상하게 뜨는 이름들(전현국 -> 전헌국)이 있기는 한데<br/>
그런 경우는 뭐... 어쩔수 없습니다. 다른 방법 생각해보면 있을것 같긴 한데 일단은 이정도입니다.<br/>
-> 출석부랑 비교해서 한 글자정도 틀린거는 출석부에 맞게 수정한다던가...<br/>
분명히 양쪽 다 있는데 한 쪽에만 출석된 걸로 인식되는 경우가 좀 있습니다. 이 경우는 한쪽에서는 글자를 제대로 인식한건데 다른 쪽에는 약간 잘못 인식했다거나 하는 경우입니다.<br/>
(앞출석에는 전현국, 뒤출석에는 전헌국 이런 식으로)<br/>

출처: https://developers.kakao.com/docs/latest/ko/vision/dev-guide#ocr <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://developers.kakao.com/
