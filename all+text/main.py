PATH='/home/vitaliy/Загрузки/Telegram Desktop/111 all_texts 2/111 all_texts 2/'
file = open(PATH+'a111_7.html','a', encoding="utf-8")
x=0
for i in range(12787, 13363):

    try:
        with open(PATH+str(i)+'.html','r', encoding="utf-8") as htm:
            print(i, x)
            # file.write('\n')
            file.write(htm.read())
            x +=1
    except:
        print('файл не найден')
        continue
    if x==1000:
        break
print(x)
file.close()