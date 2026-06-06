# ============================================================
#  UUV 1D Depth Control Simulator  ─  PID Control
#  수중 무인 잠수정(UUV) 깊이 응답 시뮬레이터
#  2021114316 기계공학부 곽유성
# ============================================================
#
#  PID 제어 블록 다이어그램
#
#               z_target
#                  │
#                  ▼
#           ┌─────────────┐
#           │   Error     │      ← e = z_target - z
#           └──────┬──────┘
#                  │ e
#                  ▼
#    ┌─────────────────────────────┐
#    │        PID Controller        │  ← u = Kp·e + Ki·∫e·dt + Kd·(de/dt)
#    └──────────────┬──────────────┘
#                   │ u_raw
#                   ▼
#         ┌──────────────────┐
#         │  Thrust Limit    │      ← u_min ≤ u ≤ u_max
#         └────────┬─────────┘
#                  │ u
#                  ▼
#         ┌──────────────────┐
#         │    UUV Plant     │      ← m·a = u − c·v
#         │  v = v + a·dt    │        v = v + a·dt
#         │  z = z + v·dt    │        z = z + v·dt
#         └────────┬─────────┘
#                  │ z(t)
#                  └──── feedback ────► 현재 깊이 z
# ============================================================

# [개념 7 - pylab/numpy 배열 연산]
# pylab은 numpy(수치 계산)와 matplotlib(그래프)를 한 번에 제공하는 패키지다.
# "import pylab as pl" 로 불러오면 pl.arange(), pl.plot() 처럼 사용한다.
import pylab as pl


# ==============================================================
# 함수 1: UUV 파라미터 입력
# ==============================================================
# [개념 6 - 함수(def)]
# def 키워드로 함수를 정의한다.
# 함수는 관련 코드를 묶어 이름을 붙여두고, 필요할 때마다 호출해 재사용한다.
def set_uuv_params():
    """UUV의 질량(mass)과 항력 계수(drag)를 입력받아 딕셔너리로 반환한다."""
    print("\n--- UUV 파라미터 설정 ---")

    # [개념 1 - 변수]
    # 변수는 데이터를 담아두는 이름표다.
    # input()으로 문자열을 받고, float()으로 실수(소수점 숫자)로 변환해 저장한다.
    mass = float(input("UUV 질량 mass (kg)     [기본값 10.0] : "))
    drag = float(input("항력 계수 drag (N·s/m)  [기본값  5.0] : "))

    # [개념 3 - 딕셔너리]
    # 딕셔너리는 "키: 값" 쌍으로 데이터를 묶는 자료구조다.
    # uuv["mass"] 처럼 키 이름으로 값을 꺼낸다.
    uuv = {"mass": mass, "drag": drag}

    print(f"설정 완료: mass={uuv['mass']} kg, drag={uuv['drag']} N·s/m")
    return uuv  # 딕셔너리를 반환해 호출한 쪽에서 사용하게 한다


# ==============================================================
# 함수 2: PID 게인 및 목표 깊이 입력
# ==============================================================
def input_pid_params():
    """Kp, Ki, Kd, 추력 제한, 목표 깊이를 입력받아 반환한다."""
    print("\n--- PID 게인 설정 ---")
    print("  ┌──────────────────────────────────────────┐")
    print("  │  u = Kp·e + Ki·∫e·dt + Kd·(de/dt)        │")
    print("  │  e = z_target − z  (목표 깊이 - 현재 깊이) │")
    print("  └──────────────────────────────────────────┘")

    # [개념 1 - 변수]
    # Kp: 오차에 즉각 반응하는 비례 게인
    # Ki: 오차가 쌓일수록 커지는 적분 게인 (잔류 오차 제거)
    # Kd: 오차 변화 속도에 반응하는 미분 게인 (오버슈트 억제)
    Kp       = float(input("비례 게인 Kp             [기본값  5.0] : "))
    Ki       = float(input("적분 게인 Ki             [기본값  0.5] : "))
    Kd       = float(input("미분 게인 Kd             [기본값  2.0] : "))
    u_min    = float(input("최소 추력 u_min (N)      [기본값 -50.0] : "))
    u_max    = float(input("최대 추력 u_max (N)      [기본값 +50.0] : "))
    z_target = float(input("목표 깊이 z_target (m)   [기본값  10.0] : "))

    print(f"설정 완료: Kp={Kp}, Ki={Ki}, Kd={Kd} / "
          f"u=[{u_min:+.1f}, {u_max:+.1f}] N / 목표={z_target} m")

    # 여러 값을 한꺼번에 반환할 때는 쉼표로 나열한다 → 튜플로 묶여 반환됨
    return Kp, Ki, Kd, u_min, u_max, z_target


# ==============================================================
# 함수 3: 시뮬레이션 시간 설정
# ==============================================================
def input_scenario():
    """시뮬레이션 총 시간 T와 시간 간격 dt를 입력받아 반환한다."""
    print("\n--- 시뮬레이션 시간 설정 ---")

    # [개념 1 - 변수]
    T  = float(input("시뮬레이션 총 시간 T (s)  [기본값 30.0] : "))
    dt = float(input("시간 간격 dt (s)           [기본값  0.1] : "))

    print(f"설정 완료: 총 시간={T}s, dt={dt}s")
    return T, dt


# ==============================================================
# 함수 4: UUV Plant — 1D 운동 방정식으로 깊이·속도 업데이트
# ==============================================================
def update_uuv(uuv, z, v, u, dt):
    """
    뉴턴 제2법칙 m·a = u − c·v 으로 다음 스텝의 속도와 깊이를 계산한다.

    매개변수:
      uuv : {"mass", "drag"} 딕셔너리
      z   : 현재 깊이 (m)
      v   : 현재 속도 (m/s)
      u   : 이번 스텝의 추력 (N)
      dt  : 시간 간격 (s)
    반환값:
      z_new, v_new : 다음 스텝의 깊이·속도
    """
    # [개념 3 - 딕셔너리]
    # uuv["mass"], uuv["drag"] 로 딕셔너리에서 값을 꺼낸다.
    #
    # 1단계: 가속도 계산
    #   a = (추력 - 항력) / 질량
    #   항력 = drag × 현재속도  (속도에 비례하는 저항력)
    a = (u - uuv["drag"] * v) / uuv["mass"]

    # 2단계: Euler 이산화 — 미분방정식을 한 스텝씩 근사 계산
    #   v[k+1] = v[k] + a[k] · dt
    v_new = v + a * dt

    #   z[k+1] = z[k] + v[k+1] · dt
    z_new = z + v_new * dt

    return z_new, v_new


# ==============================================================
# 함수 5: 시뮬레이션 루프 (PID 제어 + UUV Plant 반복)
# ==============================================================
def run_simulation(uuv, Kp, Ki, Kd, u_min, u_max, z_target, T, dt):
    """
    매 시간 스텝마다 블록 다이어그램 순서대로 계산을 반복한다.
      1. Error     : e = z_target - z
      2. PID       : u_raw = Kp·e + Ki·∫e·dt + Kd·(de/dt)
      3. Thrust Limit : u = clip(u_raw, u_min, u_max)
      4. UUV Plant : z, v 업데이트
    """
    # [개념 7 - pylab 배열 연산]
    # pl.arange(시작, 끝, 간격) → 시작부터 끝 직전까지 간격 크기로 나눈 배열 생성
    # 예) pl.arange(0, 3, 1) → [0, 1, 2]
    time = pl.arange(0, T, dt)

    # [개념 1 - 변수] 초기 상태 설정
    z        = 0.0          # 초기 깊이: 0m (수면)
    v        = 0.0          # 초기 속도: 0m/s (정지)
    integral = 0.0          # 적분 항 누적값 초기화 (∫e dt)
    e_prev   = z_target     # 첫 스텝 이전 오차 = z_target - 0 = z_target

    # [개념 2 - 리스트]
    # 빈 리스트를 만들어 매 스텝 결과를 append()로 하나씩 추가한다.
    depth_list = []         # 시간별 깊이 z 저장 (그래프용)

    # [개념 5 - 반복문(for)]
    # time 배열의 원소 수만큼 반복한다. (_는 t값이 필요없어 관례상 _로 받음)
    for _ in time:

        # ── [블록 1] Error ─────────────────────────────────────
        # 오차 = 목표 깊이 - 현재 깊이
        # e > 0 : 아직 목표보다 얕음 → 더 내려가야 함 (양(+) 추력 필요)
        # e < 0 : 목표를 지나침    → 올라가야 함 (음(-) 추력 필요)
        e = z_target - z

        # ── [블록 2] PID Controller ────────────────────────────
        # 적분(I): 오차를 시간에 걸쳐 누적 → 잔류 오차(steady-state error) 제거
        integral += e * dt

        # 미분(D): 오차의 변화율 → 오버슈트를 미리 감지해 억제
        derivative = (e - e_prev) / dt

        # PID 합산: 비례 + 적분 + 미분
        u_raw = Kp * e + Ki * integral + Kd * derivative

        # ── [블록 3] Thrust Limit ──────────────────────────────
        # pl.clip(값, 최솟값, 최댓값): 값이 범위를 벗어나면 경계값으로 자른다
        # 추진기의 물리적 최대·최소 출력을 넘지 못하도록 제한한다
        u = float(pl.clip(u_raw, u_min, u_max))

        # ── [블록 4] UUV Plant ─────────────────────────────────
        # [개념 6 - 함수 호출]
        # update_uuv() 를 호출해 z, v 를 다음 스텝 값으로 갱신한다
        z, v = update_uuv(uuv, z, v, u, dt)

        # 다음 스텝의 미분 항 계산을 위해 현재 오차를 저장해둔다
        e_prev = e

        # [개념 2 - 리스트 .append()]
        # 이번 스텝의 깊이를 리스트 맨 뒤에 추가한다
        depth_list.append(z)

    # 시간 배열과 깊이 리스트를 반환해 그래프에서 사용한다
    return time, depth_list


# ==============================================================
# 함수 6: 그래프 출력 (깊이 vs 시간)
# ==============================================================
def plot_results(time, depth_list, z_target):
    """깊이 z(t) vs 시간 그래프를 출력한다."""

    # [개념 8 - pylab 그래프 출력]
    pl.figure(figsize=(8, 5))                         # 그래프 창 크기 설정
    pl.title("UUV 1D Depth Control (PID)", fontsize=14)

    # pl.plot(x축, y축): 시간-깊이 곡선을 파란 실선으로 그린다
    pl.plot(time, depth_list, color='blue', label='Depth z(t)')

    # pl.axhline: 수평 기준선 — 목표 깊이를 빨간 점선으로 표시한다
    pl.axhline(y=z_target, color='red', linestyle='--',
               label=f'Target {z_target} m')

    pl.xlabel("Time (s)")           # x축 레이블
    pl.ylabel("Depth (m)")          # y축 레이블
    pl.legend()                     # 범례 표시
    pl.grid(True)                   # 격자 표시
    pl.gca().invert_yaxis()         # 깊이는 아래로 갈수록 증가 → y축 뒤집기

    pl.tight_layout()               # 레이블이 잘리지 않도록 여백 자동 조정
    pl.show()                       # 그래프 창 열기


# ==============================================================
# 메인 프로그램: 메뉴 루프
# ==============================================================

# [개념 1 - 변수] 기본값으로 초기화 — 사용자가 메뉴를 건너뛰어도 바로 실행 가능
uuv      = {"mass": 10.0, "drag": 5.0}
Kp       =  5.0     # 비례 게인
Ki       =  0.5     # 적분 게인
Kd       =  2.0     # 미분 게인
u_min    = -50.0    # 최소 추력 (N)
u_max    =  50.0    # 최대 추력 (N)
z_target =  10.0    # 목표 깊이 (m)
T        =  30.0    # 시뮬레이션 총 시간 (s)
dt       =   0.1    # 시간 간격 (s)

# [개념 5 - 반복문(while True)]
# 조건이 항상 True이므로 무한 반복 → 사용자가 '5. 종료'를 선택해야 break로 탈출
while True:
    print("\n" + "=" * 34)
    print("   UUV Depth Control Sim  (PID)")
    print("=" * 34)
    print("1. UUV 파라미터 설정  (mass, drag)")
    print("2. PID 게인 설정      (Kp, Ki, Kd + 목표 깊이)")
    print("3. 시뮬레이션 시간 설정")
    print("4. 시뮬레이션 실행 + 그래프 출력")
    print("5. 종료")
    print("-" * 34)

    choice = input(">> ")

    # [개념 4 - 조건문(if / elif / else)]
    # 사용자 입력값에 따라 해당 함수를 호출한다
    if choice == "1":
        # [개념 6 - 함수 호출]
        # set_uuv_params()가 반환한 딕셔너리를 uuv 변수에 저장한다
        uuv = set_uuv_params()

    elif choice == "2":
        # 반환된 여러 값을 각각의 변수에 동시에 저장한다 (언패킹)
        Kp, Ki, Kd, u_min, u_max, z_target = input_pid_params()

    elif choice == "3":
        T, dt = input_scenario()

    elif choice == "4":
        print("\n시뮬레이션 실행 중...")

        # run_simulation()을 호출해 시간 배열과 깊이 결과를 받는다
        time, depth_list = run_simulation(
            uuv, Kp, Ki, Kd, u_min, u_max, z_target, T, dt
        )

        # 깊이 vs 시간 그래프를 출력한다
        plot_results(time, depth_list, z_target)

    elif choice == "5":
        print("프로그램을 종료합니다.")
        break   # while True 루프를 탈출해 프로그램 종료

    else:
        # 1~5 이외의 값 입력 시 안내 메시지 출력
        print("1~5 중에서 선택하세요.")
