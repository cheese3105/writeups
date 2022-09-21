# PWNABLE.KR -  collision
## Giới thiệu:
Link challenge: https://pwnable.kr/play.php  
Một challenge rất thích hợp để luyện tập các skill debug cho người mới bắt đầu :))

![image](https://user-images.githubusercontent.com/74854445/116359794-6c5b9980-a829-11eb-8f77-41ef749bef72.png)  

Vì MD5 hay hash collision thật ra cũng không quan trọng lắm đến cách chúng ta giải challenge này cho nên mình sẽ không nói gì về chúng ở đây  

Writeup này có phần hơi dài dòng một xí vì mình đã note lại hết những cái mình mới học được, và note kỹ từng bước  

Những bước nào đã từng được note rồi thì challenge sau mình sẽ lược bớt nhé

## Debug

Ta có soure code C như sau:
```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}

int main(int argc, char* argv[]){
	if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
	if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
	}

	if(hashcode == check_password( argv[1] )){
		system("/bin/cat flag");
		return 0;
	}
	else
		printf("wrong passcode.\n");
	return 0;
}

```
Giống với challenge fd ta cần thêm vào đối số cho chường trình để thoát khỏi `if(argc<2)`  

Sau đó là đảm bảo đối số ta đưa vào đủ 20 bytes để thoát khỏi `if(strlen(argv[1]) != 20)`  

Để có thể khiến chương trình gửi `"/bin/cat flag"` đến cho system, ta cần phải làm cho kết quả của hàm `check_password` bằng với `hashcode` tức là bằng 0x21DD09EC (số hiển dưới dạng hệ thập lục phân)

Để có thể hiểu một cách chính xác và rõ ràng nhất cách thức hoạt động của chương trình, chúng ta sẽ cần phải debug  

Trên server có sẵn trình debug `gdb`, nhưng do dùng không quen lắm nên mình quyết định sẽ tải file trên server về máy của mình, và dùng trình debug `pwndbg`  

### Tải file

> **Link down pwndbg: https://github.com/pwndbg/pwndbg**  
> 
> **Chi tiết cách tải file thông qua giao thức SSH: https://www.namecheap.com/support/knowledgebase/article.aspx/9571/89/how-to-download-a-file-via-ssh/**   

![image](https://user-images.githubusercontent.com/74854445/117548585-eed12e00-b05f-11eb-94c0-4b0cf080b97c.png)
 
Cấu trúc lệnh sẽ là: 

``` scp -Psố_port username@hostname:/đường_dẫn_đến_file_cần_tải/tên_file /đường_dẫn_đến_nơi_file_sẽ_tải_về/tên_file_mới ```  

![image](https://user-images.githubusercontent.com/74854445/117552349-00710080-b075-11eb-9ea0-2ea1be3ca5da.png)

> Một lưu ý nhỏ là không nên đặt tên file là `col` vì nó là một lệnh (command) nên khi tải về sẽ bị lỗi, không mở được.

![image](https://user-images.githubusercontent.com/74854445/117552648-e89a7c00-b076-11eb-94ac-505843d53db9.png)

Dùng lệnh `gdb tên_file_cần_debug` nếu đã cài `pwndbg` thì sẽ nhìn giống như trên hình  

Dùng lệnh `b tên_hàm` hoặc `b *địa_chỉ_lệnh` để đặt breakpoint. Để khi chạy đến breakpoint thì chương trình sẽ dừng lại và hiện thị những dữ liệu mà chương trình đang xử lý ngay tại lệnh đấy  

Dùng lệnh `r đối_số_1 đối_số_2` để chạy chương trình. Ở trên thì mình đã chạy chương trình mà không nhập thêm đối số  

![image](https://user-images.githubusercontent.com/74854445/117553234-7d52a900-b07a-11eb-9bae-bd02d998f262.png)

Trên hình mọi người có thể thấy có 4 phần:  

| Phần | Mục đích |
| :----- | :---------- |
| REGISTERS | Hiện thị giá trị của các thanh ghi mà chương trình sử dụng để tính toán |
| DISASM | Hiện thị lệnh assembly hiện tại và các lệnh tiếp theo |
| STACK | Hiển thị stack |
| BACKSTRACE | *Cái này thì mình chưa dùng tới nên cũng chưa rõ nó là cái gì :)))* |

Dùng lệnh `next` hoặc `n` để chuyển đến lệnh tiếp theo  

Dùng lệnh `continue` hoặc `c` để chuyển đến breakpoint tiếp theo  

> **Một tip dành cho các bạn chưa quen nhìn hợp ngữ ASM**  
> 
> Các bạn chỉ cẩn tập trung vào những lệnh `cmp` (lệnh so sánh), xem nó so sánh cái gì với cái gì, có thể xem thêm link dưới này để hiểu rõ hơn về lệnh `cmp`  
> 
> https://ti-root.blogspot.com/2015/06/tap-lenh-assembly-cua-intel-80888086-p5.html#:~:text=T%C3%A1c%20d%E1%BB%A5ng%3A%20L%E1%BB%87nh%20Cmp%20(Compare,ZF%2C%20OF%2C...
> 
> Rồi dò ngược lại xem cái đó từ đâu mà ra là được  
> 
> Dễ mà phải hum :3  

![image](https://user-images.githubusercontent.com/74854445/117696822-ef96cb00-b1eb-11eb-8fd7-2779ef43342e.png)

Do khi chạy chương trình mà không thêm đối số nên sau khi `n` liên tục thì đến được lệnh gọi hàm `printf` để in ra dòng này `"usage : %s [passcode]\n"`  

Các bạn có thể so sánh thật kỹ 2 dòng phía dưới lệnh `call` trong hình với đoạn code dưới đây để hiểu rõ hơn nhá  

```c
if(argc<2){
		printf("usage : %s [passcode]\n", argv[0]);
		return 0;
	}
```  

Được rồi, nãy giờ là dạo đầu một xí để hiểu sơ về pwndbg, asm với debug thôi. Giờ mới debug thiệt nè :)))  

Theo phân tích từ đoạn source code phía trên thì ta sẽ cần phải nhập vào chương trình 1 đối số dài 20 bytes và vì `mảng argv` là mảng con trỏ kiểu char (kiểu ký tự)  

Nên mình sẽ nhập thử 20byte là AAAABBBBCCCCDDDDEEEE  

![image](https://user-images.githubusercontent.com/74854445/117701563-99c52180-b1f1-11eb-8ce7-f384d98c918a.png)  

`n` liên tục thì sẽ thấy ta không còn bị kẹt ở lệnh `cmp` trước đó nữa mà ta đã tới được một lệnh `cmp` mới :)))  

![image](https://user-images.githubusercontent.com/74854445/117704722-608eb080-b1f5-11eb-886b-0e2e16dfa67e.png)  

Lệnh này so sánh giá trị của thanh ghi EAX với 0x14 kiểu hex tức là 20 theo kiểu decimal (thập phân)  

Theo source code là ta đang ở chỗ này  

```c
if(strlen(argv[1]) != 20){
		printf("passcode length should be 20 bytes\n");
		return 0;
		}
```

Để ý ở thanh ghi EAX ở phần REGISTERS thì cúng có thể thấy EAX = 0x14 nên cũng không phải nói gì nhiều ở đây cả  

`n` tiếp thì tới `hàm check_password`  

```c
unsigned long check_password(const char* p){
	int* ip = (int*)p;
	int i;
	int res=0;
	for(i=0; i<5; i++){
		res += ip[i];
	}
	return res;
}
```
![image](https://user-images.githubusercontent.com/74854445/117706643-c419dd80-b1f7-11eb-982e-9e0f9e522773.png)  

Tiện thể thì mình vừa đặt breakpoint tại lệnh `call` luôn để lúc sau mình không cần phải `n` nữa :)))  

Chú ý vào source code ta sẽ thấy tham số của `hàm check_password` là **1 con trỏ p kiểu char**  

Sau đó hàm ép kiểu của con trỏ `p`, đưa nó từ kiểu char thành kiểu int `(int*)p`, rồi gán vào con trỏ `ip` kiểu int  

Điều này có nghĩa là nó sẽ lấy 4 byte ký tự thành 1 số

> Để giải thích cho sự xoắn vừa rồi thì bạn cần phải hiểu  
> 
> ![image](https://user-images.githubusercontent.com/74854445/118051671-98d7ef80-b3ab-11eb-8539-a8b2a49e4814.png)  
> 
> Kiểu `char` có size (kích thước) là 1 byte. Nghĩa là 1 ký tự "A" có kích thước là 1 byte
> 
> Kiểu `int` có size (kích thước) là 4 bytes. Nghĩa là 1 số bất kỳ nằm trong khoảng từ -2,147,483,648 đến 2,147,483,647 đều có kích thước là 4 bytes  
> 
> Dữ liệu trong chương trình chỉ là một dãy các bit (8 bit = 1 byte)
> 
> Nên nếu ta quy định dữ liệu đó là kiểu char thì nó sẽ hiển thị từng byte một theo theo quy định ký tự trong bảng mã ASCII  
>
> Còn nếu ta quy định dữ liệu đó là kiểu int thì nó sẽ lấy 4 bytes tức là 32 bit rồi chuyển rồi chuyển từ nhị phân (các bit 0,1) thành sô thập phân rồi hiển thị 

Vì chương trình đã quy định con số ta nhập vào phải là 20 bytes nên sau khi bị ép sang kiểu int sẽ thành 5 số  

```c
for(i=0; i<5; i++){
		res += ip[i];
	}
```
Sau đó chương trình sẽ tiến hành cộng 5 số đó cho `res`   

> Nếu vẫn còn thấy rối về đoạn code trên thì bạn nên xem kỹ lại về con trỏ và mảng
> 
> https://nguyenvanhieu.vn/moi-quan-he-giua-con-tro-va-mang/

![image](https://user-images.githubusercontent.com/74854445/118054998-7d6fe300-b3b1-11eb-887a-5984015e0407.png)

`n` tới đây thì thấy chương trình đang so sánh EAX với EDX, EDX = 0x21dd09ec chính là giá trị của `hashcode`  

Còn EAX chính là 0x41414141 (AAAA) + 0x42424242 (BBBB) + ... + 0x45454545 (EEEE) = 0x5050504f  

Và tất nhiên là vì khi so sánh không bằng nhau nên chương trình sẽ in ***"wrong passcode"***

Vậy hướng giải quyết sẽ là tìm 5 số khi cộng lại với nhau bằng 0x21dd09ec

## Solving

Cách đầu tiên mà mình nghĩ tới là  

```py
print("\x21\xdd\x09\xec" + "\x00"*16)
```
Tuy nhiên cách này sẽ SAI vì \x00 là một Null Byte (ký tự rỗng)  

![image](https://user-images.githubusercontent.com/74854445/118072107-64782980-b3d3-11eb-8ec4-1252b2023ccf.png)

Sau đó mình thử chia 0x21dd09ec thành 5 phần sẽ được là   

```py
print("\x06\xc5\xce\xc8" * 4 + "\x06\xc5\xce\xcc")
```

Nhưng cái này cũng sai luôn nhé :))))  

Cách viết đúng là phải viết theo kiểu ***little endian*** tức là phải đảo ngược thứ tự byte lại  

Link đọc thêm: https://viblo.asia/p/little-endian-vs-big-endian-E375z0pWZGW  

Cách viết đúng sẽ là

```py
print("\xc8\xce\xc5\x06" * 4 + "\xcc\xce\xc5\x06")
```

![image](https://user-images.githubusercontent.com/74854445/118074518-43660780-b3d8-11eb-8cb4-eb1d8b01be0a.png)  

> Lưu ý nhỏ là khi viết payload từ python thì nên in bằng python2 nhé, python3 nó không ra đâu  
> 
> Còn tại sao thì mình chưa biết :)))

![image](https://user-images.githubusercontent.com/74854445/118074769-d606a680-b3d8-11eb-968b-1b53b507dcec.png)  

Đoạn này là vô đầu `hàm check_password` nè, sẽ thấy nó truyền đúng số mình muốn vào EAX  

![image](https://user-images.githubusercontent.com/74854445/118074871-16febb00-b3d9-11eb-8e13-cc255099257e.png)

Còn đây là lệnh `cmp` so sánh `hashcode` nè, lúc này EAX = EDX = 0x21dd09ec

![image](https://user-images.githubusercontent.com/74854445/118075049-765ccb00-b3d9-11eb-97d1-b6de69f63fe3.png)  

Sau đó chương trình sẽ `call` system để chạy command /bin/cat flag  

Tuy nhiên, đây là mình đang debug trên máy, không có file flag, nên sau đó chương trình sẽ báo lỗi  

Kết nối với server và nhập payload tương tự  
![image](https://user-images.githubusercontent.com/74854445/118075881-27b03080-b3db-11eb-8381-7fff3fbd25ff.png)

## HẾT
