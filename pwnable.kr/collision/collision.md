# PWNABLE.KR -  collision
## Giới thiệu:
Link challenge: https://pwnable.kr/play.php  
Một challenge rất thích hợp để luyện tập các skill debug cho người mới bắt đầu :))

![image](https://user-images.githubusercontent.com/74854445/116359794-6c5b9980-a829-11eb-8f77-41ef749bef72.png)  

Vì MD5 hay hash collision thật ra cũng không quan trọng lắm đến cách chúng ta giải challenge này cho nên mình sẽ không nói gì về chúng ở đây  

## Solving

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

### Debug  

![image](https://user-images.githubusercontent.com/74854445/117552648-e89a7c00-b076-11eb-94ac-505843d53db9.png)

Dùng lệnh `gdb tên_file_cần_debug` nếu đã cài `pwndbg` thì sẽ nhìn giống như trên hình  

Dùng lệnh `b tên_hàm` hoặc `b *địa_chỉ_lệnh` để đặt breakpoint. Để khi chạy đến breakpoint thì chương trình sẽ dừng lại và hiện thị những dữ liệu mà chương trình đang xử lý ngay tại lệnh đấy  

Dùng lệnh `r đối_số_1 đối_số_2` để chạy chương trình. Ở trên thì mình đã chạy chương trình mà không nhập thêm đối số  

![image](https://user-images.githubusercontent.com/74854445/117553234-7d52a900-b07a-11eb-9bae-bd02d998f262.png)
