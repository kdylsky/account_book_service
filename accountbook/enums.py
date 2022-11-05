from accountbook_service.enums import BaseEnum

class DeleteStatus(BaseEnum):
    EXIST   = "E"  # 고객이 삭제되지 않은 상태
    DELETE  = "D"  # 고객이 삭제하지만, 데이터베이스 상에는 남아있는 상태

class IncomeType(BaseEnum):
    SALARY = "S" # 월급관련 수입
    ETC = "E" # 그외 수입

class PayType(BaseEnum):
    FIXED_PAY = "F" # 월세,관리비와 같은 고정비
    LIVING_PAY = "L" # 식비,병원비와 같은 생활비
    ACTIVITY_PAY = "A" # 여행,취미,데이트와 같은 활동비
    VECHICLE_PAY = "V" # 지하철, 버스, 주유 같은 교통비
    ETC = "E" # 그외 지출
    
