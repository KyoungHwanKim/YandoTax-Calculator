from datetime import date

def cal_2021_after(NUMBER_HOUSES,
                   BASIC_DEDUCTION_FLAG,
                   SHARE_FLAG,
                   SHARE_RATE,
                   AREA_FLAG,
                   BUY_PRICE,
                   BUY_DATE,
                   SELL_PRICE,
                   SELL_DATE,
                   PERIOD_RESIDENCE,
                   REQUIRED_COST):

    # 기본 변수들.
    TAX_FREE_FLAG = 0  # 비과세 여부
    YANDO_GAIN = 0  # 양도차익
    HOLD_DISCOUNT_RATE = 0  # 장기보유특별공제율
    TAX_RATE = 0  # 세율
    TAX_DISCOUNT = 0  # 누진공제

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
    # 공동명의라면 지분만큼
    if SHARE_FLAG == 1:
        YANDO_GAIN *= SHARE_RATE
    # 1주택이면서 양도가액 9억원 초과, 2년 이상 보유했다면
    if BUY_DATE < date.fromisoformat("2017-08-02"):
        # 1주택이면서 양도가액 9억원 초과, 2년 이상 보유했다면
        if NUMBER_HOUSES == 1 and SELL_PRICE > 900000000 and (SELL_DATE - BUY_DATE).days >= 730:
            YANDO_GAIN = YANDO_GAIN * (SELL_PRICE - 900000000) / SELL_PRICE  # 과세대상 양도차익 적용
    else:
        if AREA_FLAG == 1:
            if NUMBER_HOUSES == 1 and SELL_PRICE > 900000000 and (
                    SELL_DATE - BUY_DATE).days >= 730 and PERIOD_RESIDENCE >= 2:
                YANDO_GAIN = YANDO_GAIN * (SELL_PRICE - 900000000) / SELL_PRICE  # 과세대상 양도차익 적용
        else:
            if NUMBER_HOUSES == 1 and SELL_PRICE > 900000000 and (SELL_DATE - BUY_DATE).days >= 730:
                YANDO_GAIN = YANDO_GAIN * (SELL_PRICE - 900000000) / SELL_PRICE  # 과세대상 양도차익 적용

    print("양도차익 : " + str(YANDO_GAIN))

    # 2. 장기보유특별공제
    PERIOD_HOLD = (SELL_DATE - BUY_DATE).days // 365

    if SELL_PRICE > 900000000:  # 고가주택 판단. (고가주택 : 양도가액이 9억원을 초과하는 주택)
        if PERIOD_RESIDENCE < 2:  # 2년 미만 거주했다면
            HOLD_DISCOUNT_RATE = 0.02 * PERIOD_HOLD if PERIOD_HOLD >= 3 else 0
        else:  # 2년 이상 거주했다면
            HOLD_DISCOUNT_RATE = 0.04 * min(10, PERIOD_RESIDENCE) + (
                0.04 * min(10, PERIOD_HOLD) if PERIOD_HOLD >= 3 else 0)
    else:  # 고가주택이 아니라면
        if PERIOD_HOLD >= 3:  # 3년 이상 보유했다면
            HOLD_DISCOUNT_RATE = 0.02 * min(15, PERIOD_HOLD)

    YANDO_GAIN = YANDO_GAIN - (YANDO_GAIN * HOLD_DISCOUNT_RATE)

    print("과세표준 : " + str(YANDO_GAIN))

    if BASIC_DEDUCTION_FLAG == 0:  # 기본공제를 받지 않았다면
        YANDO_GAIN -= 2500000

    # 3. 세율 계산
    if PERIOD_HOLD < 1:  # 보유 기간이 1년 미만이면
        TAX_RATE = 0.7
        TAX_DISCOUNT = 0
    elif PERIOD_HOLD < 2:
        TAX_RATE = 0.6
        TAX_DISCOUNT = 0
    else:
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