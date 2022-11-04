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