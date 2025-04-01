string = "aaabbbbaae"
string_dict = {}
new_string=''
for letter in string:
    
    if letter in string_dict:
        string_dict[letter] +=1
    else:
        string_dict[letter] = 1

print(string_dict)
for key,value in string_dict.items(): 
    new_string = new_string+str(value)+key
print(new_string)