# PWNABLE.KR -  collision
## Giới thiệu:
Link challenge: https://pwnable.kr/play.php  
Một challenge rất thích hợp để luyện tập các skill debug cho người mới bắt đầu :))

![image](https://user-images.githubusercontent.com/74854445/116359794-6c5b9980-a829-11eb-8f77-41ef749bef72.png)  

Vì MD5 hay hash collision thật ra cũng không quan trọng lắm đến cách chúng ta giải challenge này cho nên mình sẽ không nói gì về chúng ở đây  
Nhưng thông qua challenge mình cũng có học được khá nhiều thứ mới nên mình sẽ note lại chúng ở phía dưới nhé

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


