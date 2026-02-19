

def attempt(n=5):

    def decorator(func):
        def wrapper(*args, **kwargs):
            print("___________")
            print(n)
            func(*args, **kwargs)
            print("___________")
            return
        return wrapper
    return decorator

@attempt(n=5)
def my_print(name):
    print(f"Hello, {name} !")

@attempt(n=5)
def my_print1(age):
    print(f"Hello, {age} 1!")

@attempt(n=5)
def my_print2(name):
    print(f"Hello, {name} 2!")

@attempt(n=5)
def my_print3(name):
    print(f"Hello, {name} 3!")

my_print(name ='Вася')
my_print1(age ='100')
my_print2(name ='Macha')
my_print3(name ='Даша')