text="python"
print(text[0:4])

text="ram"
for x in text:
    ord_val=ord(x)
    chr_val=chr(ord_val-32)
    print(chr_val)


    val ="rama is going to school"
    vowels="aeiou"
    for x in val:
        if x in vowels:
            print(x)
        else:
            pass