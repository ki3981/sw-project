<div align="center">

# 🌊 UUV 1D Depth Control Simulator

### *pylab 기반 UUV 깊이 제어 시뮬레이터 (PID 제어)*

**2021114316 기계공학부 곽유성**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![pylab](https://img.shields.io/badge/pylab-matplotlib-11557C?style=flat-square&logo=plotly&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-CLI-4EAA25?style=flat-square&logo=gnubash&logoColor=white)
![Domain](https://img.shields.io/badge/Domain-Underwater%20Robotics-1E88E5?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)

</div>

---

## 📌 한 문장 설명

> PID 게인(Kp, Ki, Kd)과 목표 깊이를 입력하면 UUV가 해당 깊이로 수렴하는 과정을 1D로 시뮬레이션하고, 깊이 vs 시간 그래프를 출력하는 Python 시뮬레이터.

---

## 🎯 무엇을 하는 프로그램인가요?

수중 무인 잠수정(UUV)이 **목표 깊이(z_target)** 에 정확히 수렴하도록 **PID 피드백 제어**를 적용하는 것이 핵심이다. PID 제어기는 현재 오차(비례), 누적 오차(적분), 오차 변화율(미분)을 합산해 추력을 계산하고, 추진기의 물리적 한계를 넘지 않도록 추력을 제한한 뒤 UUV 동역학에 입력한다.

이 프로그램은 사용자가 입력한 UUV 파라미터(질량·항력), PID 게인(Kp, Ki, Kd), 추력 제한(u_min, u_max), 목표 깊이, 시뮬레이션 시간을 받아 **1D 깊이 운동 방정식**으로 시간별 깊이를 계산하고, 결과를 깊이 vs 시간 그래프로 출력한다.

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
==================================
   UUV Depth Control Sim  (PID)
==================================
1. UUV 파라미터 설정  (mass, drag)
2. PID 게인 설정      (Kp, Ki, Kd + 목표 깊이)
3. 시뮬레이션 시간 설정
4. 시뮬레이션 실행 + 그래프 출력
5. 종료
----------------------------------
>> 2

--- PID 게인 설정 ---
  ┌──────────────────────────────────────────┐
  │  u = Kp·e + Ki·∫e·dt + Kd·(de/dt)        │
  │  e = z_target − z  (목표 깊이 - 현재 깊이) │
  └──────────────────────────────────────────┘
비례 게인 Kp             [기본값  5.0] : 5.0
적분 게인 Ki             [기본값  0.5] : 0.5
미분 게인 Kd             [기본값  2.0] : 2.0
최소 추력 u_min (N)      [기본값 -50.0] : -50
최대 추력 u_max (N)      [기본값 +50.0] : 50
목표 깊이 z_target (m)   [기본값  10.0] : 10
설정 완료: Kp=5.0, Ki=0.5, Kd=2.0 / u=[-50.0, +50.0] N / 목표=10.0 m
```

---

## ✨ 핵심 기능 2가지

<table>
<tr>
<td align="center" width="50%">

### 📝
**PID 게인 설정**

UUV 파라미터(질량·항력), 비례·적분·미분 게인(Kp, Ki, Kd), 추력 제한, 목표 깊이를 입력하여 시뮬 조건 설정

</td>
<td align="center" width="50%">

### 📉
**1D 동역학 + 그래프 출력**

뉴턴 운동 방정식으로 시간별 깊이 계산 후 깊이 vs 시간 그래프 출력 (목표 깊이 기준선 포함)

</td>
</tr>
</table>

---

## 👤 예상 사용자

- 🌊 UUV / AUV 같은 **수중 로봇 제어**에 관심 있는 학생
- 🎛️ **PID 게인이 깊이 응답에 어떤 영향**을 미치는지 직관적으로 확인하고 싶은 사람
- 🙋 **본인** — 자율주행·제어 백그라운드를 살려 피드백 제어 시뮬레이터를 직접 구현해보기 위해

---

## 💻 결과물 형태

```
CLI 프로그램 + pylab 그래프 출력
```

| 출력 채널 | 내용 |
| :---: | --- |
| 🖥️ **터미널** | PID 게인 입력 인터페이스 |
| 📊 **그래프** | 깊이 z(t) vs 시간 (목표 깊이 빨간 점선 포함) |

---

## 🐍 사용된 Python 개념

| 개념 | 사용 내용 |
| :---: | --- |
| 🔹 **변수** | mass, drag, Kp, Ki, Kd, u_min, u_max, z_target, T, dt 저장 |
| 🔹 **리스트** | `depth_list`에 시간별 깊이 결과 저장 |
| 🔹 **딕셔너리** | `uuv = {"mass", "drag"}`로 파라미터 그룹화 |
| 🔹 **조건문** | `if/elif/else`로 메뉴 선택 분기 처리 |
| 🔹 **반복문** | `while True`로 메뉴 루프, `for _ in time:`로 시뮬레이션 진행 |
| 🔹 **함수** | 입력·PID 계산·동역학 업데이트·그래프를 기능별로 분리 |
| 🔹 **배열 연산** | `pl.arange()`로 시간축 생성, `pl.clip()`으로 추력 제한 |
| 🔹 **그래프 출력** | `pl.plot()`, `pl.axhline()`, `pl.gca().invert_yaxis()`로 깊이 그래프 출력 |

---

## 📦 왜 pylab인가?

pylab은 **numpy 배열 계산** + **matplotlib 그래프 출력**을 한 번에 제공한다. 시간 배열을 만들고 → PID로 추력을 계산하고 → 깊이 그래프로 그리는 흐름에 딱 맞는다.

| 역할 | 코드 |
| :---: | :---: |
| 📐 시간 배열 생성 | `pl.arange(0, T, dt)` |
| 📏 추력 클리핑 | `pl.clip(u_raw, u_min, u_max)` |
| 📈 그래프 출력 | `pl.plot(time, depth_list)` |

> 💡 `import pylab as pl` 방식 사용 — `pl.arange()`, `pl.clip()`, `pl.plot()`, `pl.show()`처럼 함수 출처가 명확해서 코드 설명이 쉬움.

---

## 🧮 핵심 계산 공식

### ① PID 제어 공식

<div align="center">

> **u = Kp·e + Ki·∫e·dt + Kd·(de/dt)**

</div>

- `e = z_target − z` : 현재 오차 (목표 깊이 - 현재 깊이)
- `Kp` : 비례 게인 — 오차에 즉각 반응
- `Ki` : 적분 게인 — 누적 오차 제거 (잔류 오차 억제)
- `Kd` : 미분 게인 — 오차 변화율에 반응 (오버슈트 억제)

### ② 추력 제한 (Thrust Clipping)

```
u = clip(u_raw, u_min, u_max)
```

- 추진기의 물리적 최대·최소 출력을 넘지 못하도록 제한
- 기본값: `u_min = −50 N`, `u_max = +50 N`

### ③ UUV 1D 운동 방정식 (뉴턴 제2법칙)

<div align="center">

> **m · a = u − c · v**

</div>

- `m`: UUV 질량 (kg)
- `c`: 항력 계수 (N·s/m)
- `v`: 수직 속도 (m/s)
- `u`: 추력 (N) — PID 출력

### ④ Euler 이산화

```
a[k]   = (u[k] − c·v[k]) / m
v[k+1] = v[k] + a[k]·dt
z[k+1] = z[k] + v[k+1]·dt
```

### 가정 (단순화)
- 중성부력(buoyancy ≈ weight)으로 부력·중력 항 상쇄
- 항력은 속도에 선형 비례 (저속 가정)
- 외란(해류·파도) 없음

---

## 🛠️ 함수 설계

| 함수 | 역할 |
| --- | --- |
| `set_uuv_params()` | UUV 질량·항력 계수 입력받아 딕셔너리로 반환 |
| `input_pid_params()` | Kp, Ki, Kd, 추력 제한, 목표 깊이 입력받아 반환 |
| `input_scenario()` | 시뮬 총 시간 T, 시간 간격 dt 입력받아 반환 |
| `update_uuv()` | 1D 운동 방정식으로 다음 깊이·속도 계산 |
| `run_simulation()` | PID 제어 시뮬레이션 루프 실행 + 깊이 리스트 반환 |
| `plot_results()` | pylab으로 깊이 vs 시간 그래프 출력 |

---

## 🔄 프로그램 실행 흐름

```text
[1] UUV 파라미터 / PID 게인 / 시간 설정
    - mass, drag, Kp, Ki, Kd, u_min, u_max, z_target, T, dt

            ↓

[2] pylab으로 시간 배열 생성
    - time = pl.arange(0, T, dt)

            ↓

[3] 시뮬레이션 루프 (for _ in time)
    - e = z_target - z
    - integral += e * dt
    - derivative = (e - e_prev) / dt
    - u_raw = Kp*e + Ki*integral + Kd*derivative
    - u = clip(u_raw, u_min, u_max)
    - 1D 동역학으로 깊이 z, 속도 v 업데이트
    - 깊이 결과 리스트에 저장

            ↓

[4] 결과 출력
    - 깊이 z(t) vs 시간 (파란 실선)
    - 목표 깊이 z_target (빨간 점선)
```

---

## 🔁 제어 블록 다이어그램

```text
              z_target
                 │
                 ▼
          ┌─────────────┐
          │   Error     │      ← e = z_target - z
          └──────┬──────┘
                 │ e
                 ▼
   ┌─────────────────────────────┐
   │        PID Controller       │  ← u = Kp·e + Ki·∫e·dt + Kd·(de/dt)
   └──────────────┬──────────────┘
                  │ u_raw
                  ▼
        ┌──────────────────┐
        │  Thrust Limit    │      ← u_min ≤ u ≤ u_max
        └────────┬─────────┘
                 │ u
                 ▼
        ┌──────────────────┐
        │    UUV Plant     │      ← m·a = u − c·v
        │  v = v + a·dt    │
        │  z = z + v·dt    │
        └────────┬─────────┘
                 │ z(t)
                 └──── feedback ────► 현재 깊이 z
```

---

## 💡 예시 코드

```python
import pylab as pl

# 1. 파라미터 설정
dt       = 0.1
T        = 30.0
Kp, Ki, Kd = 5.0, 0.5, 2.0
u_min, u_max = -50.0, 50.0
z_target = 10.0
time     = pl.arange(0, T, dt)

uuv = {"mass": 10.0, "drag": 5.0}

# 2. 초기 상태
z, v = 0.0, 0.0
integral = 0.0
e_prev   = z_target
depth_list = []

# 3. 시뮬레이션 루프 (PID 제어)
for _ in time:
    e = z_target - z
    integral += e * dt
    derivative = (e - e_prev) / dt
    u_raw = Kp * e + Ki * integral + Kd * derivative
    u = float(pl.clip(u_raw, u_min, u_max))

    # 1D 동역학
    a = (u - uuv["drag"] * v) / uuv["mass"]
    v = v + a * dt
    z = z + v * dt

    e_prev = e
    depth_list.append(z)

# 4. 그래프 출력
pl.figure(figsize=(8, 5))
pl.title("UUV 1D Depth Control (PID)", fontsize=14)
pl.plot(time, depth_list, color='blue', label='Depth z(t)')
pl.axhline(y=z_target, color='red', linestyle='--', label=f'Target {z_target} m')
pl.xlabel("Time (s)")
pl.ylabel("Depth (m)")
pl.legend()
pl.grid(True)
pl.gca().invert_yaxis()
pl.tight_layout()
pl.show()
```

---

## 🤖 AI 도구 사용 내역

<table>
<tr>
<td>

**🔧 Claude (Anthropic)**


- **💬 받은 도움**: PID 제어 루프 구조 검토, `pl.clip()` 추력 제한 적용, 제어 블록 다이어그램 아스키아트 구성
- **✅ 내 판단**: 1D + 중성부력 가정으로 범위 한정, 외란 제외, 기본 게인값(Kp=5, Ki=0.5, Kd=2)과 추력 제한(±50 N)은 내가 결정 (목표 깊이 10 m로 안정 수렴 확인 기준)

</td>
</tr>
</table>

---

## 🚧 한계와 다음 단계

### ✅ 구현 완료
- **PID 피드백 제어** — 비례·적분·미분 게인으로 목표 깊이 정밀 추종
- **추력 제한(Clipping)** — 추진기 물리 한계 반영
- **깊이 vs 시간 그래프** 출력 (목표 깊이 기준선 포함)

### ⚠️ 현재의 한계
- **1D 깊이 제어만 지원** (2D 평면·3D 위치 미지원)
- **중성부력 가정** — 실제 부력·중력 변동 미반영
- **항력 모델이 선형** (실제로는 |v|·v 같은 2차항이 더 정확)
- **외란(해류·파도) 없음** — 이상적 환경 가정
- **CLI만 지원** (GUI 없음)

### 🔮 다음 단계
- **Step reference** 지원 (목표 깊이가 시간에 따라 5m → 15m → 8m처럼 변화)
- **게인 자동 튜닝** (Ziegler-Nichols 등)
- **2D/3D 확장** — 수평 위치 제어 추가

---

<div align="center">

*곽유성*

</div>
