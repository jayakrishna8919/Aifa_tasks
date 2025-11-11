try:
    with open("data.txt",'r') as f:
        data = f.readlines()
    
        gen_data=(line for line in data)
        gen_data = [line for line in data if len(line)>20]
        print(type(gen_data))
    

    print(next(gen_data))
    print(next(gen_data))
    print(next(gen_data))
    print(next(gen_data))
    print(next(gen_data))
    print(next(gen_data))
    print(next(gen_data))

except Exception as e:
    print(e)
