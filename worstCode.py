class SmartLock:
    def __init__(self):
        self.__password = "123456"
        self.__is_locked = True
        self.__attempts = 0

    def unlock(self, password):
        if self.__attempts >= 3:
            print("尝试次数过多，已锁定")
            return

        if password == self.__password:
            self.__is_locked = False
            self.__attempts = 0
            print("门已开锁")
        else:
            self.__attempts += 1
            print(f"密码错误，剩余尝试次数：{3 - self.__attempts}")

    def changePassword(self, old_pass, new_pass):
        if old_pass == self.__password:
            self.__password = new_pass
            print("密码修改成功")
        else:
            print("原密码错误")
smartLock = SmartLock()
smartLock.unlock("123456")  # 正确密码，门已开锁
smartLock.changePassword("123456", "654321")  # 修改密码