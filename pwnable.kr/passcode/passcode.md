# PWNABLE.KR - passcode

## Giới thiệu  

Link: https://pwnable.kr/play.php  
![image](https://user-images.githubusercontent.com/74854445/118870976-51081980-b911-11eb-8557-e4485a6d496c.png)

Write up tham khảo:  

https://jaimelightfoot.com/blog/pwnable-kr-passcode-walkthrough/  

https://dev.to/christalib/pwnable-kr-passcode-write-up-36gj  

## Xem bài  

```c
#include <stdio.h>
#include <stdlib.h>
void login(){
	int passcode1;
	int passcode2;
	printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);
	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);
	printf("checking...\n");
	if(passcode1==338150 && passcode2==13371337){
                printf("Login OK!\n");
                system("/bin/cat flag");
        }
        else{
                printf("Login Failed!\n");
		exit(0);
        }
}
void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}
int main(){
	printf("Toddler's Secure Login System 1.0 beta.\n");
	welcome();
	login();
	// something after login...
	printf("Now I can safely trust you that you have credential :)\n");
	return 0;	
}
```

Xem qua source cood thì ta có thể suy ra được chỉ cần cho passcode1==338150 && passcode2==13371337 là xong  

Tuy nhiên khi chạy chương trình  

![image](https://user-images.githubusercontent.com/74854445/118872513-d6d89480-b912-11eb-99fc-adbfac13ba79.png)

Lại bị lỗi o.O?  

Nhìn kĩ lại thì thấy có chút sai sai :))) 

```c
printf("enter passcode1 : ");
	scanf("%d", passcode1);
	fflush(stdin);
	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
	printf("enter passcode2 : ");
        scanf("%d", passcode2);
```

Đoạn code trên đã bị thiếu **`&`**  

Chính xác phải là  

```c
scanf("%d", &passcode1);
```

Thử compile (biên dịch) source code của chương trình thì thấy  

![image](https://user-images.githubusercontent.com/74854445/118882315-430cc580-b91e-11eb-866a-ca3ead25e71f.png)

Trình biên dịch cũng có cảnh báo chúng ta về lỗi `scanf`  

Giả thuyết là

Do ghi sai cú pháp nên thay vì hàm scanf sẽ hiểu giá trị của passcode1 và passcode2 là địa chỉ

Và sẽ đưa những dữ liệu mà nó đọc được từ stdin và địa chỉ đó

Mà biến passcode1 và passcode2 khi khởi tạo lại không được gán giá trị cụ thể nên sẽ có giá trị ảo (một giá trị nào đó do máy tính tự khởi tạo)

Vì là một giá trị ảo nên rất có thể là địa chỉ không có trong chương trình hoặc là nằm ở một vùng mà chương trình không được đụng tới

Dẫn đến segmentation fault


Trong chương trình vẫn có một chỗ nữa sài `scanf` 

```c
void welcome(){
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Welcome %s!\n", name);
}
```
Ta có thể dùng xem đoạn code asm của chương trình để so sánh thử scanf của 2 hàm

## Debug

Dùng lệnh `objdump -M intel -d passcode` để xem lệnh asm của chương trình  

![image](https://user-images.githubusercontent.com/74854445/118883402-65531300-b91f-11eb-9bfa-b06cf4b94073.png)  

![image](https://user-images.githubusercontent.com/74854445/118888705-312f2080-b926-11eb-9416-e47f1c303f36.png)

Chú ý vào thanh ghi EDX (thanh ghi dữ liệu, thường xử lý các dữ liệu input và output)  

Ở `welcome` thì là lệnh LEA (Load Effective Address) là đưa ***địa chỉ bộ nhớ*** vào thanh ghi đích  

Còn ở `login` thì là lệnh MOV chỉ là copy toán hạng nguồn vào toán hạng đích  

Vậy thì giả thuyết trên là chính xác

## Khai thác 

> Có thể bạn đã biết =)) Một hàm được gọi sẽ kết thúc khi xuất hiện instrucstion `leave` hoặc `mov esp, ebp` tức là chuyển ebp hiện tại thành esp, lấy giá trị của thanh ghi `ebp` lưu vào thanh ghi `esp`  
>
> Hành động đó có thể tạm hiểu là bỏ đi các biến local (cục bộ) của hàm trong quá trình tính toán
>
> Tuy nhiên cần phải lưu ý là các không gian trong stack **KHÔNG HOÀN TOÀN BỊ XÓA**  
> 
> Tức là nếu ta đưa vào vùng stack đó dữ liệu khác thì dữ liệu mới sẽ ghi đè lên dữ liệu cũ và hoạt động bình thường  
> 
> Nếu không đưa dữ liệu mới vào thì các dữ liệu cũ vẫn sẽ nằm yên ở đó
> 
> Bạn có thể tham khảo thêm [ở đây](https://ctf101.org/binary-exploitation/what-is-the-stack/)  

Quay lại bài, ta có thể xem asm của chương trình để xem thử địa chỉ của các biến cục bộ nằm ở đâu trong stack.
