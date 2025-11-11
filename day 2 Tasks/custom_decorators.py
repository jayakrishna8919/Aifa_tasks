#decorator without arguments

def decorator1(func):
    def inner():
        return func().upper()
    return inner
@decorator1
def fun():
    return "hello"
print(fun())


#decorator with arguments

def decorator2(func):
    def inner(*args,**kwargs):
        print("start of function")
        result = func(*args,**kwargs)
        print("End of function")
        return result
    return inner

@decorator2
def add(a,b):
    return a+b
print(add(10,20))




