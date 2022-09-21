# Python Wrangling  

![image](https://user-images.githubusercontent.com/74854445/123783426-8a647980-d900-11eb-943d-68312f2af299.png)  

Challenge này siêu dễ luôn mọi người.  

Thực ra challenge này nhằm mục đích muốn giới thiệu về cách dùng terminal để chạy các lệnh python thôi.  

Nên cách giải vô cùng đơn giản, chỉ cần tải 3 file script python, password, flag về máy như này 

![image](https://user-images.githubusercontent.com/74854445/123784250-6f463980-d901-11eb-8744-09800877395f.png)

Nội dung của flag.txt.en và pw.txt như sau:  

![image](https://user-images.githubusercontent.com/74854445/123811010-1389a980-d91d-11eb-8fe4-1405e4f8564e.png)


Mở terminal lên, vì mình đang dùng Window nên có thể nói là mở cmd (command promt) lên.  

Sau đó đi đến thư mục có file script python lên và chạy thử file như này.  

> Ở đây các bạn cần phải có cài python vào máy thì mới chạy được file script này nhé  

![image](https://user-images.githubusercontent.com/74854445/123785377-a9640b00-d902-11eb-8316-f413e4c96310.png)

Ở đây bị báo lỗi là không có module cryptography nên mình google một xí và mò được cách tải về là dùng lệnh `pip` của python để tải module này về rồi thử lại  

![image](https://user-images.githubusercontent.com/74854445/123785766-1d061800-d903-11eb-8fad-bea37484dc63.png)  

Hmmmm... Giờ mở thử `ende.py` lên xem có gì trong đấy  

> Trong thư mục mà cứ double click vô file `ende.py` thì tới mai cũng không xem được đâu nhé =))
> Chuột phải vào file rồi chọn Open with, chọn Notepad thì mới đọc được nhé  

Script python như sau:  
```py

import sys
import base64
from cryptography.fernet import Fernet



usage_msg = "Usage: "+ sys.argv[0] +" (-e/-d) [file]"
help_msg = usage_msg + "\n" +\
        "Examples:\n" +\
        "  To decrypt a file named 'pole.txt', do: " +\
        "'$ python "+ sys.argv[0] +" -d pole.txt'\n"



if len(sys.argv) < 2 or len(sys.argv) > 4:
    print(usage_msg)
    sys.exit(1)



if sys.argv[1] == "-e":
    if len(sys.argv) < 4:
        sim_sala_bim = input("Please enter the password:")
    else:
        sim_sala_bim = sys.argv[3]

    ssb_b64 = base64.b64encode(sim_sala_bim.encode())
    c = Fernet(ssb_b64)

    with open(sys.argv[2], "rb") as f:
        data = f.read()
        data_c = c.encrypt(data)
        sys.stdout.write(data_c.decode())


elif sys.argv[1] == "-d":
    if len(sys.argv) < 4:
        sim_sala_bim = input("Please enter the password:")
    else:
        sim_sala_bim = sys.argv[3]

    ssb_b64 = base64.b64encode(sim_sala_bim.encode())
    c = Fernet(ssb_b64)

    with open(sys.argv[2], "r") as f:
        data = f.read()
        data_c = c.decrypt(data.encode())
        sys.stdout.buffer.write(data_c)


elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print(help_msg)
    sys.exit(1)


else:
    print("Unrecognized first argument: "+ sys.argv[1])
    print("Please use '-e', '-d', or '-h'.")


```

`sys.argv[1]` là tham số đầu vào của chương trình, được đưa vào bằng cách nhập ngay sau dòng lệnh  

Đối số mình đưa vào ở đây là `-h` để chương trình in ra `help_msg`  

![image](https://user-images.githubusercontent.com/74854445/123791641-e67fcb80-d909-11eb-84a2-4fe7c2be1e2a.png)  

`help_msg` đã ghi hướng dẫn cách để derypt file flag, nên ta chỉ cần làm theo thôi  

![image](https://user-images.githubusercontent.com/74854445/123809975-40898c80-d91c-11eb-85b6-85c75ed8dbf9.png)  

Tương tự trên terminal của Linux/Ubuntu cũng thế nhé  

## Cách tà đạo =)))  

Như đã nói ở trên thì mục đích của bài này là giúp bạn tìm hiểu cách chạy script python trên terminal  

Mà muốn chạy được script trên terminal thì máy đó, hệ điều hành đó phải có cài python mới được  

Cách tà đạo chính là ta sẽ giải bài này mà không cần sử dụng terminal hay phải cài python vào máy =)))  

Đầu tiên thì mình sẽ tìm một trang web giúp biên dịch python online  

Sau đó copy các script python bỏ vào và chạy thử, nếu bị báo lỗi thiếu module thì kiếm trang khác nhé =)))  

Đây là một trang mà khi chạy script sẽ không bị báo lỗi thiếu module: https://www.tutorialspoint.com/execute_python_online.php  

![image](https://user-images.githubusercontent.com/74854445/123813408-138aa900-d91f-11eb-96cf-3fb798eb0d87.png)

Sau đó mình tiến hành thay đổi script một xí như sau:  
```py
import sys
import base64
from cryptography.fernet import Fernet

#them doi so "-d" ngay trong chuong trinh
(sys.argv).append("-d")

usage_msg = "Usage: "+ sys.argv[0] +" (-e/-d) [file]"
help_msg = usage_msg + "\n" +\
        "Examples:\n" +\
        "  To decrypt a file named 'pole.txt', do: " +\
        "'$ python "+ sys.argv[0] +" -d pole.txt'\n"



if len(sys.argv) < 2 or len(sys.argv) > 4:
    print(usage_msg)
    sys.exit(1)



if sys.argv[1] == "-e":
    if len(sys.argv) < 4:
        # sim_sala_bim = input("Please enter the password:")
        sim_sala_bim = "6008014f6008014f6008014f6008014f"
    else:
        sim_sala_bim = sys.argv[3]

    ssb_b64 = base64.b64encode(sim_sala_bim.encode())
    c = Fernet(ssb_b64)

    with open(sys.argv[2], "rb") as f:
        data = f.read()
        data_c = c.encrypt(data)
        sys.stdout.write(data_c.decode())


elif sys.argv[1] == "-d":
    if len(sys.argv) < 4:
        # sim_sala_bim = input("Please enter the password:")
        sim_sala_bim = "6008014f6008014f6008014f6008014f"
    else:
        sim_sala_bim = sys.argv[3]

    ssb_b64 = base64.b64encode(sim_sala_bim.encode())
    c = Fernet(ssb_b64)
    
    #Bo doan nay
    '''
    with open(sys.argv[2], "r") as f:
        data = f.read()
        data_c = c.decrypt(data.encode())
        sys.stdout.buffer.write(data_c)
    '''
    #data la flag chua decrypt
    data = "gAAAAABgUAIVI-r3OTKrDSgUJ8i3N9OzjacXZ1w4Hua00I_-Bg7gZu9Fld-TFYRiUiZlkLkChceqqpL9XnGOMO-W2-lRXpFhTkrqk9fHAvDfNkZHuZcjGPpG4xaR4mPnagzSNIrtL9tK"
    data_c = c.decrypt(data.encode())
    
    #in ra flag da decrypt
    print(data_c)

elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print(help_msg)
    sys.exit(1)


else:
    print("Unrecognized first argument: "+ sys.argv[1])
    print("Please use '-e', '-d', or '-h'.")
```
Kết quả được như này hihi =)))
![image](https://user-images.githubusercontent.com/74854445/123820433-c9a4c180-d924-11eb-8ffd-db95e75d54e5.png)  

**Flag:** picoCTF{4p0110_1n_7h3_h0us3_6008014f}
