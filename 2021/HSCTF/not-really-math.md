# not-really-math

Đây là lần đầu tiên mình giải được một challenge loại algorithm (thuật toán) hay code, hay programing kiểu kiểu thế  

Nên mình quyết định sẽ ghi lại write up dù mình biết nó rất dễ =)))

![image](https://user-images.githubusercontent.com/74854445/122644503-bc771e00-d13f-11eb-9d8a-3f139853b26b.png)  

File pdf thì giải thích đề bài, input như thế nào và output ra làm sao  

![image](https://user-images.githubusercontent.com/74854445/122644574-0829c780-d140-11eb-8d4a-2df5fd16877d.png)  

Hiểu đơn giản là chữ `a` thì cộng 2 số lại, chữ `m` thì nhân 2 số lại  

Theo nguyên tắc `cộng trước nhân sau`, *not-really-math mà =))))*  

Tiếp theo thì kết nối với server để xem thử đề sẽ hiển thị như thế nào  

![image](https://user-images.githubusercontent.com/74854445/122644707-db29e480-d140-11eb-928e-2d544b8da703.png)  

Và đây là thuật toán để giải bài này của mình được viết bằng python3  

```py
from pwn import *

context.log_level = 'debug'

host, port = 'not-really-math.hsc.tf', 1337

s = remote(host,port)

title = s.recvline()
problem = s.recvline()
a = 0
mod = 2**32-1

while (a == 0):	

	print (problem)
	problem = problem.decode("utf-8")
	problem = problem.replace(": ","")
	problem = problem.replace("a","+")
	problem = problem.split("m")
	print(problem)
	
	result = 1
	for i in problem:
		result = result*eval(i)
	result = result%mod

	print (result)
	s.send((str(result) + '\n').encode())
	problem = s.recvline_contains(b'a' or b'm')

s.close
```  
> Lúc làm bài này thì mình có một vài phát hiện mới  
> 
> - `recvline()` là lấy thông tin được gửi từ server theo từng dòng (tức là nhận tới `\n` thì ngưng) và lấy tới đâu thì lần sau lấy tiếp từ chỗ đó  
> - Thông tin lấy về từ server thường là byte nên sau đó sẽ phải `decode()` về kiểu string cho dễ làm tính toán  
> - Tương tự khi gửi cũng phải chuyển những cái mình cần gửi thành kiểu string rồi `encode()` thành kiểu byte thì mới gửi lại cho server được  
> - `eval()` một hàm của python giúp ta có thể tính toán một chuỗi biểu thức kiểu string  
> - `mod = 2\*\*32-1`, cái này là do giới hạn lưu trữ của kiểu int là từ -2147483648 đến 2147483647, nếu kết quả tính toán lớn hơn 2147483647 thì sẽ bị đổi thành số âm 
> để nó vẫn nằm trong khoảng giới hạn. Nên đối với những số lớn hơn 2147483647 thì tác giả bảo là gửi phần dư là được. Nên mình chỉ cần lấy kết quả chia cho `mod` rồi lấy phần 
> dư gửi đi là được

Kết quả khi chạy:  

![image](https://user-images.githubusercontent.com/74854445/122644858-820e8080-d141-11eb-9119-b9be5bae145c.png)  

Flag: flag{yknow_wh4t_3ls3_is_n0t_real1y_math?_c00l_m4th_games.com}

