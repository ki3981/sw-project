<div align="center">

# ☕ Caffeine Sleep Simulator

### *pylab 기반 카페인 잔량 및 수면 방해 위험도 시뮬레이터*

**2021114316 기계공학부 곽유성**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![pylab](https://img.shields.io/badge/pylab-matplotlib-11557C?style=flat-square&logo=plotly&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-CLI-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)

</div>

---

## 📌 한 문장 설명

> 카페인 음료 섭취 정보를 입력하면 시간별 카페인 잔량을 계산하고, 취침 시간 기준 수면 방해 위험도를 알려주는 Python 시뮬레이터.

---

## 🎯 무엇을 하는 프로그램인가요?

커피, 에너지 드링크, 커피믹스 같은 카페인 음료는 일상에서 자주 마시지만, 시간이 지나도 몸속에 어느 정도 남아 있는지 쉽게 알기 어렵다. 특히 늦은 시간에 섭취한 카페인은 잠들기 전까지 몸속에 남아 수면을 방해할 수 있다.

이 프로그램은 사용자가 마신 카페인 음료의 정보(이름·섭취 시간·카페인 양)를 입력받아 **카페인 반감기 공식**으로 0시부터 24시까지 시간별 카페인 잔량을 계산한다. 그리고 사용자가 입력한 취침 시간에 남아 있는 카페인 양을 기준으로 **수면 방해 위험도(높음 / 주의 / 낮음)** 를 판정하고, 결과를 텍스트 리포트와 pylab 그래프로 출력한다.

---

## 🚀 실행 방법

### 1️⃣ 필요 환경
- Python **3.10+**
- `matplotlib`, `numpy` (pylab은 matplotlib에 포함)

### 2️⃣ 설치
```bash
pip install matplotlib numpy
```

### 3️⃣ 실행
```bash
python main.py
```

### 4️⃣ 실행 예시
```text
==============================
     Caffeine Simulator
==============================
1. 음료 추가
2. 섭취 기록 보기
3. 분석 리포트 + 그래프
4. 종료
------------------------------
>> 1
음료 이름   : 아메리카노
섭취 시간   : 10
카페인 양   : 150 mg
등록 완료!
```

---

## ✨ 핵심 기능 3가지

<table>
<tr>
<td align="center" width="33%">

### 📝
**카페인 음료 정보 입력**

음료 이름, 섭취 시간, 카페인 양을 입력하여 섭취 기록 생성

</td>
<td align="center" width="33%">

### 📉
**시간별 카페인 잔량 계산**

카페인 반감기 공식으로 0시~24시 잔량을 한 번에 계산

</td>
<td align="center" width="33%">

### 🚨
**수면 방해 위험도 판단**

취침 시간 잔량 기준으로 위험도를 판단하고 pylab 그래프 출력

</td>
</tr>
</table>

---

## 👤 예상 사용자

- ☕ 커피·에너지 드링크를 자주 마시는 **학생** / **직장인**
- 😴 자신의 카페인 섭취가 **수면에 어떤 영향**을 주는지 확인하고 싶은 사람
- 🙋 **본인** — 하루 동안 마신 카페인이 밤에 얼마나 남는지 직접 확인하기 위해

---

## 💻 결과물 형태

```
CLI 프로그램 + pylab 그래프 출력
```

| 출력 채널 | 내용 |
| :---: | --- |
| 🖥️ **터미널** | 음료 입력 인터페이스, 분석 리포트 텍스트 |
| 📊 **그래프** | 시간별 카페인 잔량 변화 선 그래프 |

---

## 🐍 사용된 Python 개념

| 개념 | 사용 내용 |
| :---: | --- |
| 🔹 **변수** | 음료 이름, 섭취 시간, 카페인 양, 반감기, 취침 시간 저장 |
| 🔹 **리스트** | 여러 카페인 음료 섭취 기록 저장 |
| 🔹 **딕셔너리** | 음료 하나의 이름·시간·카페인 양을 묶어서 저장 |
| 🔹 **조건문** | 카페인 잔량에 따라 위험도(높음/주의/낮음) 판단 |
| 🔹 **반복문** | 입력된 여러 음료를 하나씩 확인하며 잔량 계산 |
| 🔹 **함수** | 음료 추가, 잔량 계산, 위험도 판단, 그래프 출력, 리포트 출력 분리 |
| 🔹 **배열 연산** | pylab 배열로 시간별 잔량을 한 번에 계산 |
| 🔹 **그래프 출력** | `pl.plot()`으로 카페인 변화 시각화 |

---

## 📦 왜 pylab인가?

pylab은 **numpy 배열 계산** + **matplotlib 그래프 출력**을 한 번에 제공한다. 시간 배열을 만들고 → 시간별 잔량을 계산하고 → 결과를 그래프로 그리는 흐름에 딱 맞는다.

| 역할 | 코드 |
| :---: | :---: |
| 📐 배열 계산 | `pl.arange(0, 25)` |
| 📈 그래프 출력 | `pl.plot(hours, remain)` |

> 💡 `import pylab as pl` 방식 사용 — `pl.arange()`, `pl.plot()`, `pl.show()`처럼 함수 출처가 명확해서 코드 설명이 쉬움.

---

## 🧮 핵심 계산 공식

<div align="center">

### 카페인 반감기 공식

> **남은 카페인 = 섭취량 × 0.5 ^ (지난 시간 / 반감기)**

</div>

> ⏰ 섭취 이전 시간에는 잔량을 **0**으로 처리 (아직 몸에 들어오지 않았으므로)

---

## 🛠️ 함수 설계

| 함수 | 역할 |
| --- | --- |
| `add_drink()` | 음료 이름·섭취 시간·카페인 양을 입력받아 저장 |
| `show_drinks()` | 입력된 카페인 음료 목록 출력 |
| `calculate_remaining_caffeine()` | 한 음료의 시간별 카페인 잔량 계산 |
| `calculate_total_caffeine()` | 여러 음료의 카페인 잔량 합산 |
| `check_sleep_risk()` | 취침 시간 기준 수면 방해 위험도 판정 |
| `plot_caffeine_graph()` | pylab으로 시간별 카페인 잔량 그래프 출력 |
| `print_report()` | 총 섭취량, 취침 시간 잔량, 위험도 결과 출력 |

---

## 🔄 프로그램 실행 흐름

```text
[1] 카페인 음료 정보 입력
    - 음료 이름, 섭취 시간, 카페인 양 입력

            ↓

[2] 섭취 기록 저장
    - 입력한 음료 정보를 리스트에 저장

            ↓

[3] 시간별 카페인 잔량 계산
    - pylab으로 0시부터 24시까지 시간 배열 생성
    - 카페인 반감기 공식 적용

            ↓

[4] 취침 시간 기준 분석
    - 취침 시간에 남아 있는 총 카페인 양 확인
    - 수면 방해 위험도 판정

            ↓

[5] 결과 출력
    - 하루 분석 리포트 출력
    - pylab 그래프로 잔량 변화 시각화
```

---

## 💡 예시 코드

```python
import pylab as pl

half_life = 5
hours = pl.arange(0, 25)

drink = {
    "name": "아메리카노",
    "time": 10,
    "caffeine": 150
}

elapsed = hours - drink["time"]
remain = drink["caffeine"] * (0.5 ** (elapsed / half_life))

# 음료를 마시기 전 시간에는 카페인이 없으므로 0으로 바꾼다.
# 예: 10시에 마셨다면 0시~9시는 0mg으로 처리
for i in range(len(hours)):
    if elapsed[i] < 0:
        remain[i] = 0

pl.plot(hours, remain, label=drink["name"])
pl.xlabel("Time")
pl.ylabel("Caffeine Remaining (mg)")
pl.title("Caffeine Remaining Simulation")
pl.legend()
pl.grid(True)
pl.show()
```

---

## 🤖 AI 도구 사용 내역

<table>
<tr>
<td>

**🔧 Claude (Anthropic)**

- **📍 어디에 사용**: README 항목 점검 — 가이드북에서 요구하는 README 항목이 모두 들어 있는지 확인 요청
- **💬 받은 도움**: 누락 항목(실행 방법, AI 사용 내역, 한계와 다음 단계) 지적 + 통합본 초안 작성
- **✅ 내 판단**: 누락 항목은 채우되, 핵심 기능·함수 설계·계산 공식 등은 내가 직접 설계한 부분이라 그대로 유지

</td>
</tr>
</table>

---

## 🚧 한계와 다음 단계

### ⚠️ 현재의 한계
- 카페인 반감기를 **모두 5시간으로 고정** (실제로는 개인차가 크다 — 1.5~9시간까지 변동)
- 음료 섭취 시간을 **1시간 단위 정수**로만 입력 (분 단위 미지원)
- 입력 데이터가 **프로그램 종료 시 사라짐** (저장 기능 없음)
- 위험도 임계값(50mg / 100mg)이 **고정값** — 개인 민감도 미반영
- **CLI만 지원** (GUI 없음)

### 🔮 다음 단계
- 사용자 프로필 입력(나이·체중·카페인 민감도)으로 **반감기 개인화**
- **분 단위 입력 지원** 및 24시간을 넘는 누적 분석(전날 섭취량 영향 반영)

---

<div align="center">

*곽유성*

</div>
