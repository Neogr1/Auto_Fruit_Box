# Auto_Fruit_Box

https://www.gamesaien.com/game/fruit_box_a/

이 게임을 자동화

## Execution
- 조건: `alt+tab`을 누르면 브라우저로 이동하도록 세팅
- 실행: 터미널에 `python main.py` 입력 혹은 유사한 파이썬 코드 실행 방식 사용

## How?
1. pyautogui로 게임 플레이 자동화
    selenium으로 하고 싶었지만, 광고도 많고 java script가 난독화 되어 있어 제어의 어려움 있음.
2. AWS의 textract로 OCR하여 숫자 검사
    java script 난독화 때문에 OCR 돌림.
    pyautogui의 locateOnScreen도 사용해봤지만 부정확함.
3. 무작위 탐색으로 최적 점수 찾기
    본 게임의 최고점을 얻는 문제는 NP-hard 추측됨.
    때문에 무작위 탐색 + 유사 유전 알고리즘으로 최적 점수를 찾음.

## Dependencies
- Python=3.11.5
- boto3=1.35.22
- pillow=9.5.0
- PyAutoGUI=0.9.54

## 환경
- OS: Windows 11
- 해상도: 2560*1600
- 배율: 125%
- 브라우저: Microsoft Edge (130.0.2849.80)

다른 환경(특히 해상도)에서 사용할 경우 (당연히) 잘 안 될 것임.

## TODO
- 환경 상관 없이 범용적으로
- box 찾기 알고리즘 개선
- 드래그 속도 개선
- java script 난독화 풀어서 OCR 없이 숫자 알아내기