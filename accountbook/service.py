from accountbook.repository import BookRepo, PayRepo

class BookService:
    def __init__(self)-> None:
        self.repo =  BookRepo()

    def create_book(self, user: object, day: str, money: int, title: str, memo: str) -> dict:
        """
        가계부 생성은 두 단계로 이루어진다.
        phase1 : 날짜에 해당하는 가계부 만들기 create_book
        phase2 : 해당 날짜에 지출내역 연결하기 create_pay
        """
        accountbook = self.repo.create_book(
                        user=user,
                        day=day)
        created = self.repo.create_pay(
                        accountbook=accountbook,
                        money=money,
                        title=title,
                        memo=memo)
        return created
    
    def get_list(self, request) -> list:
        """
        가계부를 디폴트로 현재 날짜로 부터 1달 전 까지의 데이터를 가지고 온다.
        offset에 숫자를 입력시 이전 기록까지 가지고 온다. 
        delete_status가 False에 해당하는 값만 가지고 온다.
        예)offset=3 -> 3달 전까지 표기
        """
        return self.repo.get_list(request)
    
    def delete_book(self, request)->bool:
        """
        accountbook객체를 삭제하면, 날짜에 해당하는 모든 pay객체도 삭제해주어야 한다.
        예)11월1일(객체) - 교통비(객체), 생활비(객체) 등
        """
        return self.repo.delete_book(request)

    def deleted_booklist(self, request)->dict:
        """
        삭제한 객체의 delete_status=True가된다.(데이터베이스상에서는 1이다.)
        Ture에 해당하는 accountbook객체를 가지고 와서 리스트로 보여준다.
        """
        return self.repo.deletd_booklist(request)
    
    def recovey_booklist(self, request):
        """
        삭제한 accountbook객체 들 중 리스트로 골라서 복구시킨다.
        삭제 후에는 다시 일일 총 금액에 더해주어야 한다.
        """
        return self.repo.recovey_booklist(request)


class PayService:
    def __init__(self)-> None:
        self.repo = PayRepo()
    
    def get_pay_day(self, request, day: str)-> list:
        return self.repo.get_list_pay(request, day)
    
    def delete_pay_day(self, request, day: str)-> bool:
        return self.repo.delete_day_pay(request,day)
    
    def patch_pay_day(self, request, day: str)-> bool:
        return self.repo.patch_day_pay(request, day)