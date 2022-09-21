# PWNABLE.KR - fd
## Giới thiệu
Link challenge: https://pwnable.kr/play.php  
  
Đây là một challenge khá đơn giản sẽ giúp ta tìm hiểu thêm về file descriptor
## Thế nào là một file descriptor?
Để hiểu chi tiết hơn thì bạn có thể đọc bài viết dưới đây

https://vsudo.net/blog/file-descriptor-la-gi.html

Trong bài này ta chỉ cần nhớ, trên hệ điều hành như UNIX, theo mặc định, 3 file descriptor đầu tiên là STDIN (standard input), STDOUT (standard output) và STDERR (standard error)  
  
| Tên | File descriptor | Mô tả | Tên viết tắt |
| --- | --- | --- | --- |
| Standard input | 0 | Luồng dữ liệu mặc định cho input, ví dụ trong lệnh pipeline. Trong terminal, mặc định bàn phím là input từ người dùng | stdin |
| Standard output | 1 | Luồng dữ liệu mặc định cho output, ví dụ khi sử dụng lệnh in lên màn hình. Trong terminal, mặc định tới màn hình người dùng | stdout |
| Standard error | 2 | Luồng dữ liệu mặc định cho output liên quan đến lỗi. Trong terminal, mặc định tới màn hình người dùng | stderr |

## Solving

Quay lại với challenge, vì đây là challenge đầu tiên nên mình sẽ note lại chi tiết các bước research nên có khi mới bắt đầu challenge. Các challenge sau thì mình sẽ skip bước này nhé  

Đầu tiên, sau khi kết nối với server, mình dùng lệnh `ls` để xem những tập tin trong thư mục hiện tại  

Nhưng mình khuyến khích dùng lệnh `ls -la` để xem tất cả các tập tin bao gồm cả tập tin ẩn và thông tin phân quyền của từng tập tin  

![image-2](https://user-images.githubusercontent.com/74854445/115533284-cbb52900-a2c0-11eb-826d-50642e31d9d0.png)  

Nếu chưa rõ về cách xem phân quyền trên linux thì bạn có thể xem qua link dưới đây  

https://quantrimang.com/phan-quyen-truy-cap-file-bang-lenh-chmod-59672  

Có thể thấy owner (chủ sở hữu) của tập tin flag là fd_pwn, group (nhóm) của tập tin là root, còn chúng ta là user (người dùng) fd   
=> chúng ta thuộc nhóm other (những người còn lại)  

Và những người còn lại thì không có quyền gì với tập tin này cả. Nên khi cat tập tin flag thì sẽ bị báo Permission denied  

Tương tự như 2 tập tin còn lại thì với user là fd ta có thể execute (thực thi) tập tin fd và read (đọc) được tập tin fd.c  

`cat fd.c` ta sẽ được source code như sau:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
    if(argc<2){
        printf("pass argv[1] a number\n");
        return 0;
    }
    int fd = atoi( argv[1] ) - 0x1234;
    int len = 0;
    len = read(fd, buf, 32);
    if(!strcmp("LETMEWIN\n", buf)){
        printf("good job :)\n");
        system("/bin/cat flag");
        exit(0);
    }
    printf("learn about Linux file IO\n");
    return 0;
 
}
```

Trong challenge này, chúng ta sẽ học cách để điều khiển (control) được `argc` và `argv`. Nếu bạn chưa biết gì về chúng thì có thể xem qua link dưới đây  

http://crasseux.com/books/ctutorial/argc-and-argv.html  

Tạm hiểu `argc` và `argv` là những tham số của hàm main  
`argc` là số lượng các tham số được đưa vào  
`argv` là một mảng chứa các tham số đó bắt đầu từ *argv[0]*  

> Lưu ý: Vì *argv[0]* thường trỏ tới chuỗi là đại diện cho tên chương trình (tạm hiểu là *argv[0]* chứa tên chương trình). Nên các ***argument*** (đối số) được đưa vào lúc bắt đầu chạy chương trình sẽ được tính từ *argv[1]*  

```c
if(argc<2){
        printf("pass argv[1] a number\n");
        return 0;
    }
```

Như vậy nếu chỉ chạy chương trình mà không thêm bất kỳ tham số nào thì kết quả mà ta nhận được sẽ là ***“pass argv[1] a number\n”***, do `argc` lúc này bằng 1. Nên chỉ cần thêm vào ít nhất 1 đối số thì `argc` lúc này sẽ lớn hơn hoặc bằng 2   
=> thoát khỏi `if(argc<2)`  

![image](https://user-images.githubusercontent.com/74854445/115540296-256d2180-a2c8-11eb-9e97-100e89806564.png)  

Cái chúng ta cần là chương trình có thể chạy tới câu lệnh `system(“/bin/cat flag”);` để *"/bin/cat flag"* được gửi tới hệ thống và hệ thống sẽ in ra nội dung của tập tin flag  

> P/s: Có thể bạn sẽ thắc mắc “Tại sao bên ngoài chương trình thì không có quyền cat flag nhưng trong chương trình thì lại được?”. Có thể nói là ta đang mượn danh tính của chương trình để cat flag. Ta thì không có quyền nhưng chương trình thì lại có :)))  

```c
int fd = atoi( argv[1] ) - 0x1234;
int len = 0;
len = read(fd, buf, 32);
if(!strcmp("LETMEWIN\n", buf)){
    printf("good job :)\n");
    system("/bin/cat flag");
    exit(0);
```

Return value (Giá trị trả về) của hàm `strcmp(s1,s2)` ***là một số nguyên <0 nếu s1 ngắn hơn s2, >0 nếu s1>s2, =0 nếu s1 bằng s2***  

```
If(!tên_biến) trong C.

If(!a) tương đương với if(a == 0)

If(a) tương đương với if (a != 0)
```

> Trông có vẻ khó chịu nhỉ. Nhưng tin mình đi, đây là cái mà bạn cần phải học thuộc ngay từ bây giờ vì các chương trình sau này bạn gặp, sẽ thường được viết theo cách này. Nếu không nhớ được thì bạn sẽ phải google nó rất nhiều lần như mình đấy :))  

Vì vậy để vào được trong `if(!strcmp(“LETMEWIN\n”, buf))` thì ta cần phải đảm bảo chuỗi `buf` phải bằng với chuỗi `“LETMEWIN\n”`  

Có thể thấy từ đầu chương trình tới giờ, thứ duy nhất mà chúng ta có thể control (điều khiển) được là `argc` và `argv`. Nhưng điều đó thì làm sao giúp ta biến chuỗi `buf` thành `“LETMEWIN\n”` được???  

Giờ thì ta sẽ chú ý đến những lệnh sau
```c
int fd = atoi( argv[1] ) - 0x1234;
int len = 0;
len = read(fd, buf, 32);
```

Hàm `atoi(const char *str)` sẽ chuyển đổi chuỗi được con trỏ `str` trỏ tới thành kiểu số nguyên. Vì biến `fd` là kiểu int (số nguyên).
Nên hàm này dùng để đảm bảo dù bạn nhập gì cho `argv[1]` thì chương trình vẫn có thể thực hiện câu lệnh này một cách bình thường mà không xảy ra lỗi.  

![image-1](https://user-images.githubusercontent.com/74854445/115553054-2c4f6080-a2d7-11eb-9aad-ac3d72e77a47.png)

Hàm `read()` sẽ đọc cnt byte từ tệp được chỉ định bởi file descriptor và đưa cnt byte đọc được vào buf  

Như đã nói ở trên thì file descriptor là một số nguyên định danh duy nhất của tập tin. 
Hơi giống như CMND vậy, mỗi người sẽ có một số và khi nhắc đến số đấy thì ta sẽ biết được đấy là người nào.  

Và theo mặc định, 3 file descriptor đầu tiên là STDIN (standard input), STDOUT (standard output) và STDERR (standard error). Tương ứng với các số là 0, 1, 2.  

=> Nếu fd = 0 thì hàm `read()` sẽ đọc 32 byte từ STDIN (tức là từ bàn phím). Lúc đó ta có thể dễ dàng nhập ký tự mình muốn vào `buf`  

Như vậy đối số mà ta sẽ nhập vào chương trình sẽ là 4660 (hệ thập phân của số 0x1234)  

![image-2 (1)](https://user-images.githubusercontent.com/74854445/115553565-be576900-a2d7-11eb-886a-44d11641def1.png)  

Nếu bạn thắc mắc vì sao lại là 4660 mà không phải là 0x1234 hay 1 0010 0011 0100 (hệ nhị phân của 0x1234) 
thì có thể hiểu đơn giản là vì hàm `atoi()` sẽ chuyển đổi dữ liệu chuỗi trong `argv[1]` thành kiểu số nguyên.  
Nếu nhập 0x1234 thì ký tự "x" vừa nhập sẽ bị chuyển đổi thành số nguyên nên khi trừ với 0x1234 sẽ không thể =0 được.  
Tương tự như thế máy tính cũng sẽ hiểu 1 0010 0011 0100 là một số nguyên nên khi trừ cho 0x1234 cũng không thể =0 được.

# HẾT
