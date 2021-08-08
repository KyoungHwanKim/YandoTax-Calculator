from datetime import date

def getLongTermHoldingDiscount(SELL_PRICE, SELL_DATE, HOLD_PERIOD, RESIDENCE_PERIOD):
    DISCOUNT_RATE = 0

    if date.fromisoformat("2019-01-01") <= SELL_DATE <= date.fromisoformat("2019-12-31"):
        print("2019-01-01 ~ 2019-12-31 양도분")
        DISCOUNT_RATE = min(HOLD_PERIOD, 10) * 0.08 if HOLD_PERIOD >= 3 else 0

    elif date.fromisoformat("2020-01-01") <= SELL_DATE <= date.fromisoformat("2020-12-31"):
        print("2020-01-01 ~ 2020-12-31 양도분")
        if RESIDENCE_PERIOD >= 2:
            DISCOUNT_RATE = min(HOLD_PERIOD, 10) * 0.08 if HOLD_PERIOD >= 3 else 0
        else:
            DISCOUNT_RATE = min(HOLD_PERIOD, 15) * 0.02 if HOLD_PERIOD >= 3 else 0

    elif date.fromisoformat("2021-01-01") <= SELL_DATE:
        print("2021-01-01 이후 양도분")
        if SELL_PRICE > 900000000:  # 고가주택 판단. (고가주택 : 양도가액이 9억원을 초과하는 주택)
            if RESIDENCE_PERIOD < 2:  # 2년 미만 거주했다면
                DISCOUNT_RATE = HOLD_PERIOD * 0.02 if HOLD_PERIOD >= 3 else 0
            else:  # 2년 이상 거주했다면
                DISCOUNT_RATE = (min(10, RESIDENCE_PERIOD) + min(10, HOLD_PERIOD)) * 0.04 if HOLD_PERIOD >= 3 else 0
        else:  # 고가주택이 아니라면
            if HOLD_PERIOD >= 3:  # 3년 이상 보유했다면
                DISCOUNT_RATE = min(15, HOLD_PERIOD) * 0.02

    return DISCOUNT_RATE

print("장기보유특별공제율 :", getLongTermHoldingDiscount(910000000, date.fromisoformat("2021-10-30"), 10, 5))