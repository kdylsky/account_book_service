from accountbook.repository import BookRepo

class BookService:
    def __init__(self):
        self.repo =  BookRepo()

    def book_create(self, user: object, day: str, money: int, title: str, memo: str) -> dict:
        """
        가계부 생성은 두 단계로 이루어진다.
        phase1 : 날짜에 해당하는 가계부 만들기 create_book
        phase2 : 해당 날짜에 지출내역 연결하기 create_pay
        """
        accountbook = self.repo.create_book(
                        user=user,
                        day=day
                    )
        created = self.repo.create_pay(
                accountbook=accountbook,
                money=money,
                title=title,
                memo=memo
        )
        return created
    
    def get_list(self, request) -> list:
        """
        가계부를 디폴트로 현재 날짜로 부터 1달 전 까지의 데이터를 가지고 온다.
        offset에 숫자를 입력시 이전 기록까지 가지고 온다. 
        예)offset=3 -> 3달 전까지 표기
        """
        return self.repo.get_list(request)