# Auto_Fruit_Box

https://www.gamesaien.com/game/fruit_box_a/

위 게임을 자동화

## Execution
- 조건: `alt+tab`을 누르면 브라우저로 이동하도록 세팅. 브라우저 배율은 100%로 창을 최대화.
- 실행: 터미널에 `python main.py` 입력하거나 비슷한 방식으로 Python 코드 실행

## How It Works
- **PyAutoGUI로 게임 플레이 자동화**

    selenium으로 하고 싶었지만, 광고도 많고 JavaScript 코드가 난독화되어 있어 제어의 어려움 있음.
- **AWS의 Textract를 통한 OCR**

    JavaScript 난독화 때문에 OCR 사용.
    PyAutoGUI의 `locateOnScreen`도 사용해봤지만 부정확함.

- **무작위 탐색으로 최적 점수 찾기**
  
    본 게임의 최고점을 얻는 문제는 NP-hard 추측됨.
    때문에 무작위 탐색과 유사 유전 알고리즘을 결합하여 최적 점수를 찾음.

## Dependencies
- Python=3.11.5
- boto3=1.35.22
- pillow=9.5.0
- PyAutoGUI=0.9.54

## Environment
- OS: Windows 11
- 해상도: 2560*1600
- 화면배율: 125%
- 브라우저: Microsoft Edge (130.0.2849.80)

다른 환경(특히 해상도)에서 사용할 경우 (당연히) 잘 안 될 것임.

## TODO
- 다양한 GUI 환경에서도 범용적으로 작동하도록 개선
- box 찾기 알고리즘 개선
- 드래그 속도 최적화
- JavaScript 난독화를 풀어서 OCR 사용하지 않고 숫자 알아내기
