# Web Basic

## 1. Sause

> Trình duyệt đang rất vất vả để chuyển đổi các đoạn mã thành hình ảnh và màu sắc. Hãy trải nghiệm góc nhìn của trình duyệt nhé!
>
> http://chal1.web.letspentest.org/

Bài này ta chỉ cần kiểm tra mã nguồn của trang web (Page source code) là nhìn thấy flag  

![image](https://user-images.githubusercontent.com/74854445/140925029-aa152cc7-efc9-41f9-b32a-c81164dc49ad.png)

**Flag: Flag{Web_Sause_Delicious}**  

## 2. I am not a robot

> Nếu là người thì cho xem tai, còn nếu là robot thì đứng ở ngoài. Bạn đã bị chặn
>
> http://chal2.web.letspentest.org/

Để giải được bài này ta cần tìm hiểu về [robots.txt](https://carly.com.vn/blog/file-robots-txt-la-gi/)  

Tạm hiểu `robots.txt` là một tập tin txt quy định những phần nào trên trang web mà các công cụ tìm kiếm (SE) được đi vào và thu thập dữ liệu  

Tập tin `robots.txt` được cấu tạo gồm các phần như sau:  

- User-agent: tên loại bot 

- Disallow: Không cho bot có tên trong User-agent ở trên truy cập  

- Allow: Cho bot có tên trong User-agent ở trên truy cập  

`User-agent: *` là tất cả các loại bot, `Disallow:/` là chặn với toàn bộ trang web  

Để xem file `robots.txt` của một trang web, ta chỉ cần thêm `/robots.txt` vào sau tên miền của trang web như này  

![image](https://user-images.githubusercontent.com/74854445/140974837-df223187-f838-4d75-bc34-60ad7dd46de3.png)

Qua nội dung của tập tin `robots.txt` ta biết được mình có thể truy cập vào phần `/fl@g1337_d240c789f29416e11a3084a7b50fade5.txt` của trang web  

![image](https://user-images.githubusercontent.com/74854445/140975700-6bcdab15-e873-4207-b6a9-3630638c268e.png)

**Flag: Flag{N0_B0T_@ll0w}**  

## 3. Header 401  

> Để nhiều loại Trình duyệt và Web Server có thể nói chuyện và hiểu được nhau thì họ phải sử dụng chung một giao thức có tên gọi là HTTP Protocol. Khi người dùng bắt đầu truy cập Web, trình duyệt sẽ chuyển những hành động của họ thành yêu cầu (Request) tới Web Server. Còn Web Server sẽ trả lời (Response) xem có thể đáp ứng hay từ chối cung cấp thông tin cho trình duyệt.
>
>Ví dụ, bạn Gà muốn LẤY danh sách các thử thách trong cookiearena<chấm>org, ở đường dẫn /challenges bằng TRÌNH DUYỆT Chrome. Trình duyệt của Gà sẽ phải điền vào một cái form mẫu có tên gọi là HTTP Header và gửi đi. Mỗi yêu cầu sẽ được viết trên một dòng, và nội dung của mỗi yêu cầu sẽ phải viết đằng sau dấu hai chấm.
>
>Hãy đoán xem trong thử thách này có những Header thú vị nào nha
>
>http://chal3.web.letspentest.org/

Đây là bài mà ta sẽ cần phải sử dụng công cụ `Burp Suite` mới có thể giải ra được  

Hướng dẫn cách cài đặt, setup và sử dụng Burp Suite đã được `cookiehanhoan` hướng dẫn vô cùng chi tiết [tại đây](https://www.youtube.com/watch?v=4mpszXedKeQ)  

Khi truy cập vào 1 trang web là ta đang thực hiện việc gửi một `GET request` đến Web Server và sẽ nhận được `response` của trang web như sau  

![image](https://user-images.githubusercontent.com/74854445/140978392-ec4116e9-e042-490d-8c68-f5a3f49c83b0.png)

Để ý thấy có một đoạn comment trong response nói về `Basic Authentication Credential`  

Sau khi tìm hiểu về [Basic Authentication](https://viblo.asia/p/basic-authentication-Qbq5QmJL5D8) thì mình nghĩ bài này đang muốn mình gửi request có kèm theo thông tin đăng nhập  

Để làm được việc đó thì mình sẽ thêm phần `Authorization: Basic <Base 64 encode {username:password}>` vào cấu trúc của header như sau  

- Base 64 encode {gaconlonton:cookiehanhoan} -> `Z2Fjb25sb250b246Y29va2llaGFuaG9hbg==`  

- Thêm `Authorization: Basic Z2Fjb25sb250b246Y29va2llaGFuaG9hbg==` vào header  

- Vì đây là đang gửi thông tin đến Web server nên mình sẽ đổi thành phương thức `POST`  

![image](https://user-images.githubusercontent.com/74854445/140987236-4aadf846-71b5-4cfb-a038-1e13d369513c.png)

**Flag: Flag{m4g1c@l_h34d3r_xD}**

## 4. JS B\*\*p B\*\*p  

> Sau nhiều đêm suy nghĩ về việc làm thế nào để bảo vệ mã nguồn. Cố gắng thoát khỏi ánh mắt soi mói của Mèo Yang Hồ.
>
> Gà chẹp miệng rồi nói: "Đã tới lúc phải cho nó phải thốt lên rằng! WTF!!!"
>
> http://chal4.web.letspentest.org/  

![image](https://user-images.githubusercontent.com/74854445/141047368-207b8855-456d-436a-9286-e948b1c65a7b.png)

Kiểm tra source code của trang web thì thấy có 4 file `JavaScript`  

![image](https://user-images.githubusercontent.com/74854445/140988881-d293979d-64f4-41ea-a545-c78162613604.png)

Mở lên thử thì thấy cái này @@  

![image](https://user-images.githubusercontent.com/74854445/140988996-784e18f9-4de9-4108-8bd4-72a708dd9fcc.png)

Google thử thì mình biết được đây là `JSFuck`  

Một style lập trình rất khó hiểu dựa trên những thành phần cốt lõi của javascript  

Nó chỉ sử dụng 6 ký tự để viết và chạy code là  \[ , ] , ( , ) , ! , và +  

May mắn thay là có rất nhiều trang web hỗ trợ decode JSFuck  

Giúp mình không cần phải học cách code JSFuck mới có thể hiểu được đoạn code đó nói gì  

Ví dụ như trang này: https://enkhee-osiris.github.io/Decoder-JSFuck/  

Decode xong thì mình sẽ có được đoạn code sau  

```js 
//js 1: 
function verifyUsername(username) {
  if (username != "cookiehanhoan") {
    return false     
  }     
  return true   
}
// => username = cookiehanhoan
//js 2: 
function reverseString(str) {
  if (str === "") { 
    return "" 
  }
  else {
    return reverseString(str.substr(1)) + str.charAt(0)
  }
}
// => Đây là hàm dùng để để đảo ngược thứ tự chữ cái trong câu
//js 3: 
function verifyPassword(password) {
  if (reverseString(password) != "dr0Wss@p3rucreSr3pus") {
    return false     
  }     
  return true   
}
// => password = sup3rSercur3p@ssW0rd
//js 4: 
function verifyRole(role) {
  if (role.charCodeAt(0) != 64) {
    return false;       
  }       
  if ((role.charCodeAt(1) + role.charCodeAt(2) != 209) && (role.charCodeAt(2) - role.charCodeAt(1) != 9)) {
    return false       
  }       
  if ((role.charCodeAt(3).toString() + role.charCodeAt(4).toString() != "10578") && (role.charCodeAt(3) - role.charCodeAt(4) != 27)) {
    return false       
  }     
  return true   
}
// => role = @mdiN

```  

Từ đoạn code suy ra được những cái cần điền  

![image](https://user-images.githubusercontent.com/74854445/141047534-e7003dea-741d-418d-ba74-871a21cfafcd.png)

Submit và get flag thui  

![image](https://user-images.githubusercontent.com/74854445/141047574-a4cf76dc-da78-4919-bf3f-e94aa9c7af56.png)

**Flag: Flag{JAV-ascript_F*ck}**  

## 5. Hân Hoan 

> Mô tả: Thấy hộp bánh quy của chú Hazy để hớ hênh trên bàn. Với bản tính nghịch ngợm, Mèo Yang Hồ nhanh tay thêm chút gia vị để biến cuộc đời trở nên hài hước và hân hoan hơn.
>
> http://chal5.web.letspentest.org/  

Thông qua đề bài thì mình có tìm hiểu một xíu về `cookie` của một trang web là gì.  
  
Và đã đúc kết được những cái sau:

*Cookie là một đoạn văn bản mà một Web server có thể lưu trên ổ cứng của người dùng.*  

*Cookie cho phép một website lưu các thông tin trên máy tính của người dùng và sau đó lấy lại nó.*  

*Các mẩu thông tin sẽ được lưu dưới dạng cặp tên – giá trị (name-value)...*  [Đọc thêm](https://quantrimang.com/internet-cookies-lam-viec-nhu-the-nao-70733)  

Vì Cookie được lưu trên ổ cứng của người dùng (hay còn gọi là client)  

=> Phía client có thể dễ dàng thay đổi cookie  

Phía server nếu đọc cookie ko phân biệt ip, đặc điểm trình duyệt người dùng,... thì ta có thể dựa vào đó để khai thác. 

![image](https://user-images.githubusercontent.com/74854445/140918669-ad426e80-b32e-45e7-be71-36e9d71b7b06.png)  

Mình thử nhập đại `username` và `password` rồi ấn submit thì được kết quả như sau  

![image](https://user-images.githubusercontent.com/74854445/140923959-9fc2a3e0-859a-4db1-8ff1-c2c7dda32081.png)  

Server báo lại là mình không phải `CookieHanHoan`

Chuột phải vào trang web chọn `Inspect` để xem mọi thông tin về trang web mà ta có thể xem được như source code, hình ảnh, css, cookies,...  

Vào tab `Application` chọn vào phần `Cookies` để xem về cookie của trang web

![image](https://user-images.githubusercontent.com/74854445/140919642-91981a7d-0709-480f-b107-c5a0da91becb.png)  

Có thể thấy `value` của cookie hiện tại đang là `Guest`  

Mình thử double click vào, sửa `Guest` lại thành `CookieHanHoan` rồi tải lại trang web bằng cách `F5`  

![image](https://user-images.githubusercontent.com/74854445/140924486-d6fda835-3d2e-4d09-8cca-e131f9045d12.png)

**Flag: Flag{Cookies_Yummy_Cookies_Yammy!}**  

## 6. Infinite Loop  

> Cuộc đời luôn là vậy. Một giây trước tưởng đã cùng đường, một giây sau có lại đầy hy vọng. Các chiến binh đã có công cụ mạnh mẽ trong tay, hãy dùng nó để can thiệp dòng chảy.
>
> http://chal6.web.letspentest.org/  




