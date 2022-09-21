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

Xem qua source code thì ta có thể suy ra được chỉ cần cho passcode1==338150 && passcode2==13371337 là xong  

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

Và sẽ đưa những dữ liệu mà nó đọc được từ stdin vào địa chỉ đó

Mà biến passcode1 và passcode2 khi khởi tạo lại không được gán giá trị cụ thể nên sẽ có giá trị ảo (1 lát chúng ta sẽ nói đến giá trị ảo này sau)

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
Ta có thể xem đoạn code asm của chương trình để so sánh thử scanf của 2 hàm

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

Quay lại bài, ta có thể `objdump` xem asm của chương trình để xem thử địa chỉ của các biến cục bộ nằm ở đâu trong stack  

![image](https://user-images.githubusercontent.com/74854445/131057737-98b716d6-cc00-45b5-968f-381196bc73ab.png)

Ở đây ta có thể thấy, trước khi gọi hàm `scanf`để lấy dữ liệu đưa vào mảng `name[100]` chương trình có sử dụng lệnh `lea edx, [ebp - 0x70]`  

Ta có thể tạm hiểu là chương trình tạo một khoảng `0x70` từ `ebp` để chứa dữ liệu của mảng `name[100]` nằm trong stack  

Vì mảng `name[100]` là biến cục bộ nên sau khi kết thúc hàm `welcome` phần dữ liệu của hàm này sẽ bị loại bỏ nhưng **KHÔNG HOÀN TOÀN**  

> Ghi chú:  
> 
> Các phần dữ liệu được lưu trong stack sẽ được ghi dưới dạng `ebp - (1 số nào đó)` hoặc `esp + (1 số nào đó)`  
> 
> Lý do là `ebp -` chứ không phải là `ebp +` vì stack phát triển ngược, stack phát triển từ vị trí có địa chỉ cao đến vị trí có địa chỉ thấp  
> 
> Nên các dữ liệu được lưu trữ trong stack sẽ luôn có địa chỉ thấp hơn địa chỉ của `ebp`  
> 
> ![image](https://user-images.githubusercontent.com/74854445/131058659-3f769a24-ce80-4098-b9ae-85191f245921.png)
 
Còn giá trị`passcode1` thì nằm ở vị trí `ebp - 0x10`
![image](https://user-images.githubusercontent.com/74854445/118888705-312f2080-b926-11eb-9416-e47f1c303f36.png)  

Ta lấy `0x70 - 0x10 = 0x60` tức là bằng `96 bytes`  

Như đã nói ở trên là phần dữ liệu trong stack sẽ **KHÔNG HOÀN TOÀN BỊ LOẠI BỎ** + biến `passcode1` không hề được gán giá trị ngay lúc khởi tạo  

=> Giá trị của `passcode1` sẽ bằng `4 bytes` dữ liệu cuối của mảng `name[100]`

### Kiểm tra giả thuyết

Mình sẽ nhập vào mảng `name` đoạn payload như sau  

![image](https://user-images.githubusercontent.com/74854445/131500685-066356be-194e-473d-9caf-548f2c3b3b66.png)  

Sau đó `n` đến `scanf` trong hàm `login`, thì thấy chương trình bảo ta nhập dữ liệu vào địa chỉ `0x42424242`  

=> Giả thuyết trên là đúng  

![image](https://user-images.githubusercontent.com/74854445/131501329-9680e41c-9e99-4aa2-8219-83e1d9f6a452.png)

Thông qua việc điều khiển `passcode1` ta có thể chọn được một địa chỉ bất kỳ và quyết định được giá trị của địa chỉ đó  

Vậy câu hỏi được đặt ra là ***Ghi đè ở đâu và ghi đè cái gì ??***  

> Ý tưởng chính để giải bài này là dùng Got Overwrite nếu chưa rõ về Got Overwrite thì bạn có thể tham khảo [bài viết này](https://github.com/cheese3105/research/blob/main/GOT%20OVERWRITE/GOT%20OVERWRITE.md) của mình  

Ta để ý ngay sau khi gọi hàm `scanf` thì kế tiếp là đến hàm `fflush`  

![image](https://user-images.githubusercontent.com/74854445/131642719-3d99a6e3-6814-4fe5-b250-bf32e9f52568.png)

`0x08048430` là địa chỉ của hàm `fflush` trong section `PLT`  

![image](https://user-images.githubusercontent.com/74854445/131643332-ee1b5f99-24ce-465b-892d-2659b638131e.png)

Các instrution của hàm `fflush` trong section `PLT` có instruction `jmp    DWORD PTR ds:0x804a004`  

Để cho rõ thì `jmp    DWORD PTR ds:0x804a004` = `jmp    *0x804a004`  

Nghĩa là nhảy tới địa chỉ mà con trỏ `0x804a004` trỏ tới  

Bình thường thì con trỏ sẽ trỏ tới địa chỉ của hàm `fflush` trong `GOT`

Địa chỉ của hàm `fflush` trong `GOT` chính là địa chỉ mà chúng ta sẽ ghi đè  

### Bình thường

Khi hàm `fflush` được gọi nó sẽ gọi đến địa chỉ hàm `fflush` trong `PLT`  

Sau đó hàm `fflush` trong `PLT` sẽ `jmp` đến của hàm `fflush` trong `GOT` và bắt đầu thực thi các instruction từ địa đó trở đi  

Sau khi thực xong các instruction của hàm `fflush` trong `GOT` thì nó trở lại thực hiện nốt các intruction trong `PLT`  

Rồi trở lại hàm `login`...

### Tấn công  

Do ta có thể chọn một địa chỉ và ghi đè nội dung của địa chỉ đó thông qua biến `passcode1`  

Nên ta sẽ chọn địa chỉ bắt đầu các instruction của hàm`jmp` trong GOT  

Cúng chính là nội dung/giá trị của con trỏ `0x804a004`

Ta sẽ thay nội dung/giá trị của con trỏ `0x804a004` thành địa chỉ của instruction `puts` hoặc intrustion `system` (mình đề xuất dùng địa chỉ của instruction `puts`)  

Tức là khi hàm `fflush` được gọi nó sẽ nhảy đến địa chỉ mà con trỏ `0x804a004` trỏ tới  

Lúc này nó sẽ trỏ tới instuction `puts` và thực thi các instruction từ instruction `puts` trở đi  

### Payload

Vậy Payload sẽ gồm:  

- 96 bytes "A"
- 4 bytes "\x04\xa0\x04\x08"  
- Cái mà ta muốn ghi đè được viết dưới dạng số nguyên (int): "134514147"  

```
python2 -c 'print("A"*96 + "\x04\xa0\x04\x08" + "134514147")' | ./passcode
```  

Kết quả:  

![image](https://user-images.githubusercontent.com/74854445/131665872-12a95200-f84c-4943-a15f-e13a96e98460.png)

**Flag: Sorry mom.. I got confused about scanf usage :(**  

## HẾT
