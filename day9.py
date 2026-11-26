password = input("enter your password:")
alpha =""
digit =""
special =""
for ch in password:
    if ch.isalpha():
        alpha += ch
    elif ch.isdigit():
        digit += ch
    else:
        special += ch
        if len (digit)==2 and len(special)==1 and len (alpha)>=3:
            print("password is valid")
else:
    print("password is invalid")
