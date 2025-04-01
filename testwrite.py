lines = ['Potato', 'Lots of potatoers']
for line in lines:
    with open('test.txt', 'a') as f:
        f.write(line)
    
        f.write('\n')
        input('wait')