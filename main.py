from datetime import date


HOUSE_TYPE = 0             # 양도할 물건 종류 (주택으로 고정)
NUMBER_HOUSES = 0          # 주택 수. 1주택, 2주택, 3주택 이상
BASIC_DEDUCTION_FLAG = 0   # 연간 기본공제 여부 (인당 250만원)
SHARE_FLAG = 0             # 공동명의 여부
SHARE_RATE = 0             # 공동명의일시 지분비율
AREA_FLAG = 0              # 취득시점 조정대상지역 여부. 1주택일시 취득시점, 다주택일시 양도시점에서 판단.
BUY_PRICE = 0              # 취득가액
BUY_DATE = 0               # 취득일자
SELL_PRICE = 0             # 양도가액
SELL_DATE = 0              # 양도일자
PERIOD_RESIDENCE = 0       # 실거주 기간. 연단위 입력
REQUIRED_COST = 0          # 소요경비

TAX_FREE_FLAG = 0          # 비과세 여부
YANDO_GAIN = 0             # 양도차익
HOLD_DISCOUNT_RATE = 0     # 장기보유특별공제율
TAX_RATE = 0               # 세율
TAX_DISCOUNT = 0           # 누진공제


if __name__ == "__main__":
    print("양도소득세 계산기")

    # 계산에 필요한 정보 입력.
    NUMBER_HOUSES = int(input("주택 수 입력 : "))
    BASIC_DEDUCTION_FLAG = int(input("기본공제 여부 : "))
    SHARE_FLAG = int(input("공동명의 여부 : "))
    if SHARE_FLAG:
        SHARE_RATE = float(input("지분 비율 : "))
    if NUMBER_HOUSES == 1:
        AREA_FLAG = int(input("주택 취득시점 조정대상지역 여부 : "))
    elif NUMBER_HOUSES >= 2:
        AREA_FLAG = int(input("주택 양도시점 조정대상지역 여부 : "))
    BUY_PRICE = int(input("취득가액 : "))
    BUY_DATE = date.fromisoformat(input("취득일자 (YYYY-MM-DD) : "))
    SELL_PRICE = int(input("양도가액 : "))
    SELL_DATE = date.fromisoformat(input("양도일자 (YYYY-MM-DD) : "))
    PERIOD_RESIDENCE = int(input("실거주 기간 (연 단위) : "))
    REQUIRED_COST = int(input("소요경비 : "))

    # 0. 비과세 요건 판단 (1주택 한정)
    if NUMBER_HOUSES == 1:  # 1주택이면
        if SELL_PRICE > 900000000:
            print("비과세 대상 아님.")
        else:
            if BUY_DATE < date.fromisoformat("2017-08-02"):  # 2017.08.02 이전 취득이라면
                if (SELL_DATE - BUY_DATE).days >= 730:  # 일반지역, 조정대상지역 상관없이 2년 이상 보유했다면
                    TAX_FREE_FLAG = 1  # 비과세 대상.
                    print("비과세 대상.")
                else:
                    print("비과세 대상 아님.")
            else:  # 2017.08.02 이후 취득이라면
                if AREA_FLAG == 1:  # 조정대상지역이라면
                    if (SELL_DATE - BUY_DATE).days >= 730 and PERIOD_RESIDENCE >= 2:  # 2년 이상 보유 및 2년 이상 거주했다면
                        TAX_FREE_FLAG = 1  # 비과세 대상
                        print("비과세 대상.")
                    else:
                        print("비과세 대상 아님.")
                else:  # 일반지역이라면
                    if (SELL_DATE - BUY_DATE).days >= 730:  # 2년 이상 보유했다면
                        TAX_FREE_FLAG = 1  # 비과세 대상
                        print("비과세 대상.")
    else:
        print("비과세 대상 아님.")

    # 1. 양도차익 산출 (양도가액 - (취득가액 + 필요경비))
    YANDO_GAIN = SELL_PRICE - (BUY_PRICE + REQUIRED_COST)  # 양도차익
    print("양도차익 : " + str(YANDO_GAIN))
    # 공동명의라면 지분만큼
    if SHARE_FLAG == 1:
        YANDO_GAIN *= SHARE_RATE
    # 1주택이면서 양도가액 9억원 초과, 2년 이상 보유했다면
    if AREA_FLAG == 1:  # 조정대상지역이면
        # 1주택이면서 양도가액 9억원 초과, 2년 이상 보유 및 거주했다면
        if BUY_DATE < date.fromisoformat("2017-08-02"):
            if NUMBER_HOUSES == 1 and SELL_PRICE > 900000000 and (SELL_DATE - BUY_DATE).days >= 730:
                YANDO_GAIN = YANDO_GAIN * (SELL_PRICE - 900000000) / SELL_PRICE  # 과세대상 양도차익 적용
        else:
            if NUMBER_HOUSES == 1 and SELL_PRICE > 900000000 and (SELL_DATE - BUY_DATE).days >= 730 and PERIOD_RESIDENCE >= 2:
                YANDO_GAIN = YANDO_GAIN * (SELL_PRICE - 900000000) / SELL_PRICE  # 과세대상 양도차익 적용
    else:  # 조정대상지역이 아니면
        # 1주택이면서 양도가액 9억원 초과, 2년 이상 보유했다면
        if NUMBER_HOUSES == 1 and SELL_PRICE > 900000000 and (SELL_DATE - BUY_DATE).days >= 730:
            YANDO_GAIN = YANDO_GAIN * (SELL_PRICE - 900000000) / SELL_PRICE  # 과세대상 양도차익 적용

    # 2. 장기보유특별공제
    PERIOD_HOLD = (SELL_DATE - BUY_DATE).days // 365

    if SELL_PRICE > 900000000:  # 고가주택 판단. (고가주택 : 양도가액이 9억원을 초과하는 주택)
        if PERIOD_RESIDENCE < 2:  # 2년 미만 거주했다면
            HOLD_DISCOUNT_RATE = 0.02 * PERIOD_HOLD if PERIOD_HOLD >= 3 else 0
        else:  # 2년 이상 거주했다면
            HOLD_DISCOUNT_RATE = 0.04 * min(10, PERIOD_RESIDENCE) + (0.04 * min(10, PERIOD_HOLD) if PERIOD_HOLD >= 3 else 0)
    else:  # 고가주택이 아니라면
        if PERIOD_HOLD >= 3:  # 3년 이상 보유했다면
            HOLD_DISCOUNT_RATE = 0.02 * min(15, PERIOD_HOLD)

    YANDO_GAIN = YANDO_GAIN - (YANDO_GAIN * HOLD_DISCOUNT_RATE)
    if BASIC_DEDUCTION_FLAG == 0:  # 기본공제를 받지 않았다면
        YANDO_GAIN -= 2500000

    print("과세표준 : " + str(YANDO_GAIN))

    # 3. 세율 계산
    if YANDO_GAIN <= 12000000:  # 1,200만원 이하라면
        TAX_RATE = 0.06
        TAX_DISCOUNT = 0
    elif YANDO_GAIN <= 46000000:  # 4,6000만원 이하라면
        TAX_RATE = 0.15
        TAX_DISCOUNT = 1080000
    elif YANDO_GAIN <= 88000000:  # 8,800만원 이하라면
        TAX_RATE = 0.24
        TAX_DISCOUNT = 5220000
    elif YANDO_GAIN <= 150000000:
        TAX_RATE = 0.35
        TAX_DISCOUNT = 14900000
    elif YANDO_GAIN <= 300000000:
        TAX_RATE = 0.38
        TAX_DISCOUNT = 19400000
    elif YANDO_GAIN <= 500000000:
        TAX_RATE = 0.40
        TAX_DISCOUNT = 25400000
    elif YANDO_GAIN <= 1000000000:
        TAX_RATE = 0.42
        TAX_DISCOUNT = 35400000
    else:
        TAX_RATE = 0.45
        TAX_DISCOUNT = 65400000

    YANDO_TAX = YANDO_GAIN * TAX_RATE - TAX_DISCOUNT

    print("양도소득세 : " + str(YANDO_TAX))