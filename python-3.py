

class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    ## стоковые представления 
    def __str__(self):
        return f"{self.amount} {self.currency}"

    def __repr__(self):
        return f"{self.amount} {self.currency}"
    
    ## Операторы сравнения 
    def __eq__(self, other): ##  == 
        return self.amount == other.amount

    def __lt__(self, other): ##  сравнение  < 
        return self.amount < other.amount

    def __gt__(self, other): ##  сравнение  > 
            return self.amount > other.amount

    ## Арифметические операции 

    def __add__(self, other):
        return Money(self.amount + other.amount, self.currency)
    
    def __sub__(self, other):
        return Money(self.amount - other.amount, self.currency)
    
    def __mul__(self, other):
        return Money(self.amount * other.amount, self.currency)
    

 ## Создаем несколько экземпляров класса Money с разными значениями

wallet1 = Money(500, "KGS")
wallet2 = Money(300, "KGS")
wallet3 = Money(500, "USD")

## Проверяем работу строкового представления

print("Кошелек 1:", wallet1)
print("Кошелек 2:", wallet2)

## Проверяем операторы сравнения
print("wallet1 == wallet2:", wallet1 == wallet2)
print("wallet1 == wallet3:", wallet1 == wallet3)
print("wallet1 > wallet2:", wallet1 > wallet2)
print("wallet2 < wallet1:", wallet2 < wallet1)

## Проверяем арифметические операции
sum_wallets = wallet1 + wallet2
print("Сложение (500 + 300):", sum_wallets)

sub_wallets = wallet1 - wallet2
print("Вычитание (500 - 300):", sub_wallets)

mul_wallet = wallet2 * 2
print("Умножение (300 * 2):", mul_wallet)
