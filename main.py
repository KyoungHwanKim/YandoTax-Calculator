from datetime import date
from after_20210101 import cal_2021_after

# 양도할 물건 종류 (주택으로 고정)
HOUSE_TYPE = 0
# 주택 수. 1주택, 2주택, 3주택 이상
NUMBER_HOUSES = 1
# 연간 기본공제 여부 (인당 250만원)
BASIC_DEDUCTION_FLAG = 0
# 공동명의 여부
SHARE_FLAG = 0
# 공동명의일시 지분비율
SHARE_RATE = 0
# 조정대상지역 여부. 1주택일시 취득시점, 다주택일시 양도시점에서 판단.
AREA_FLAG = 0
# 취득가액
BUY_PRICE = 100000000
# 취득일자
BUY_DATE = date.fromisoformat("2020-05-07")
# 양도가액
SELL_PRICE = 300000000
# 양도일자
SELL_DATE = date.fromisoformat("2021-06-07")
# 실거주 기간. 연단위 입력
PERIOD_RESIDENCE = 0
# 소요경비
REQUIRED_COST = 30000000


if __name__ == "__main__":
    print("양도소득세 계산기")

    # 계산에 필요한 정보 입력.
    '''
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
    '''

    if SELL_DATE >= date.fromisoformat("2021-01-01"):
        cal_2021_after(
            NUMBER_HOUSES=NUMBER_HOUSES,
            BASIC_DEDUCTION_FLAG=BASIC_DEDUCTION_FLAG,
            SHARE_FLAG=SHARE_FLAG,
            SHARE_RATE=SHARE_RATE,
            AREA_FLAG=AREA_FLAG,
            BUY_PRICE=BUY_PRICE,
            BUY_DATE=BUY_DATE,
            SELL_PRICE=SELL_PRICE,
            SELL_DATE=SELL_DATE,
            PERIOD_RESIDENCE=PERIOD_RESIDENCE,
            REQUIRED_COST=REQUIRED_COST
        )

