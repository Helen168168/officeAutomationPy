'''
实现一个银行账户系统，包含账户余额敏感数据，也希望限制直接修改余额和隐藏内部计算逻辑
'''
class BankAccount:
    def __init__(self, balance=0, pwd='123456'):
        self._balance = balance  # 使用单下划线表示这是一个受保护的属性
        self.__password = pwd
    def __verifyPassword(self, pwd):  # 私有方法
        """密码验证"""
        return self.__password == pwd
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("存款金额必须大于零")
        self._balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("取款金额必须大于零")
        if amount > self._balance:
            raise ValueError("余额不足")
        self._balance -= amount

    def getBalance(self):
        return self._balance
    def _calculateInterest(self, rate):
        """计算利息的内部方法，不应该被外部调用"""
        return self._balance * rate
    def applyInterest(self, rate):
        """应用利息到账户余额"""
        interest = self._calculateInterest(rate)
        self._balance += interest
        return interest

# 测试代码
if __name__ == "__main__":
    account = BankAccount(100)
    print("初始余额:", account.getBalance())
    print(dir(account))
    print(account.__password)

    account.deposit(50)
    print("存款后余额:", account.getBalance())

    try:
        account.withdraw(200)
    except ValueError as e:
        print(e)

    account.withdraw(30)
    print("取款后余额:", account.getBalance())

    interest = account.applyInterest(0.05)
    print("应用利息后余额:", account.getBalance(), "利息:", interest)

    # 尝试直接访问受保护属性
    print("直接访问受保护属性（不推荐）:", account._balance)  # 这不是一个好习惯
