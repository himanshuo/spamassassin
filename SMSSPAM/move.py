__author__ = 'himanshu'
#this script is meant to take the SMSSPamCOllection and split it up to make independent files in ham and spam folders

def convert_to_string(mylist):
    out = ""
    for i in mylist:
        out += i+ " "
    return out+"\n"

i=0
for line in open('SMSSpamCollection').readlines():
    i+=1

    first_word = line.split()[0]
    text = convert_to_string(line.split()[1:])
    if first_word=="ham":
        f= open("./ham/"+"smsham"+str(i), 'w')
        print text
        f.write(text)
        f.close()
    else:
        f= open("./spam/"+"smsspam"+str(i), 'w')
        f.write(text)
        f.close()




