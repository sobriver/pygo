
class Human:
    def __init__(self, name, age):
        print('human init')
        self.name = name
        self.age = age

    def say(self):
        print('human say hello')


class Man(Human):

    def __init__(self, name, age):
        super().__init__(name, age)
        print('man init')

    def dog(self):
        print('man dog')


if __name__ == '__main__':
    man = Man('sdsd', 12)
    print(man.name)