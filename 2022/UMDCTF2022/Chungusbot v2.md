# Chungusbot v2

> Check out my code!
>
> NOTE: Browser Discord might be finicky with this challenge.
>
>Author: itsecgary

## 1. Tìm kiếm thông tin

Tìm được `Chungusbot v2` trên kênh discord của giải  

Tìm được code của bot trong github của giải 

https://github.com/UMD-CSEC/ChungusBot_v2/tree/79b9d00e53fedf9dd587440a95a4bf6fd0b47822

Có 4 file:
- `chungus.py`
- `help_info.py`
- `jokes.txt`
- `tellmy.py `

## 2. Phân tích source code

Vì mình không chuyên lắm về python cũng như chưa biết về cách code bot bằng discord bot  

Nên mình giải bài này bằng cách đoán mò là chính =)))  

### chungus.py

```py
commands = ["help", "tellme ajoke", "tellme", "tellme theflag"]
start = 'Oh Lord Chungus please '
if str(ctx.channel.type) == "private" and start in str(ctx.content) and str(ctx.content).split(start)[1] in commands:
    print("here")
    first_check, msg = check1(str(ctx.author.avatar_url))
    print(f'\n{first_check}\n{msg}\n')
    if first_check:
        if check2(str(ctx.created_at)):
            await ctx.channel.send(f'`{flag}`')
        else:
            await ctx.channel.send("not the right time my friend")
```
Để vào được `check1` ta cần:
- nhắn riêng với bot trong DM
- có `start` trong tin nhắn
- từ cuối trong tin nhắn nằm là 1 trong các từ nằm trong `commands`  

Nếu `check1` trả ra True thì ta sẽ vào được `check2`  

Nếu `check2` trả ra True thì ta sẽ nhận được flag
### Check1:
```py
def check1(av):
    r = requests.get(str(av), stream = True)
    if r.status_code == 200:
        r.raw.decode_content = True
        filename = str(str(av).split("/")[-1].split('?')[0])
        path = f'./downloaded_files/{filename}'
        with open(path,'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        return False, "Could not grab your pfp for some reason"
```

Đoạn trên là code để lấy avatar của người đang nhắn với bot  

Nếu không lấy được thì sẽ trả ra `False`, báo lỗi, thoát khỏi `check1`  

```py
img1 = list(Image.open('chungus_changed.jpg').convert("1").getdata())
img2 = list(Image.open(path).convert("1").getdata())

os.system(f"rm {path}")

bigger = len(img1)
if bigger > len(img2):
    bigger = len(img2)

try:
    count = 0
    for i in range(bigger):
        if img1[i] == img2[i]:
            count += 1
except:
    return False, "Image size not the same"
```

`img1` là 1 cái ảnh nào của con bot  

`img2` là avatar của mình  

So sánh 2 ảnh nếu ảnh `len(img1)` < `len(img2)` của mình thì trả ra False  

```py
message = "Percentage of pixels correct: " + str(count / len(img1))
if count / len(img1) > 0.92:
    return True, message
elif count / len(img1) > 0.6:
    return False, message
else:
    return False, f"Images are not the same ({100 * count / len(img1)}%)"
```

Nếu không nhỏ hơn thì sẽ tính toán tỉ lệ phần trăm các pixels giống nhau  

Nếu tỉ lệ hơn `0.92` thì sẽ pass được `check1`  

Ban đầu mình thử với một hình toàn đen thì tỉ lệ lên tới 0.85

![unknown](https://user-images.githubusercontent.com/74854445/156973219-3fafabef-f815-4f8b-b5fe-e883faef476a.png)

```py
@tellme.command()
@in_dms()
async def avatar(self,ctx):
    with open(f'chunga_diff.jpg', 'rb') as f:
        await ctx.channel.send(file=File(f, 'chunga_diff.jpg'))
```
Trong `tellme.py` là code để thực hiện chức năng của các `commands`  

Trong này có thêm một command nữa được code là command `avatar`  

Chức năng của command này là sẽ gửi cho ta 1 bức hình  

Mình thay thử sang bức hình vừa được bot gửi lên thì cũng chỉ mới lên được `0.88`

![image](https://user-images.githubusercontent.com/74854445/156973370-3f6e194d-0f13-480e-8b90-a401d769cb15.png)

Mình dự đoán bức hình được đem so chính là avatar của bot  

Nên đã kiếm trên mạng 1 bức hình rõ nét, tương tự sau đó resize thành `894 x 894` giống size của bức hình được bot gửi lên

![image](https://user-images.githubusercontent.com/74854445/156973453-c8c00ede-6478-4641-bda7-4f325582ed60.png)

Thành công pass được `check1`

## Check2: 

```py
def check2(hmm):
    something = int(hmm.split(':')[-1].split('.')[0])
    if (something > 45 and something < 50) or (something > 14 and something < 19):
        return True
    return False
```
`check2` sẽ nhận vào thời gian ta gửi tin nhắn cho bot  

`something` = số giây  

=> Chỉ cần canh thời gian gửi tin nhắn hợp lý rồi gửi tin nhắn cho bot là được như 12:28:15

**Flag: UMDCTF{Chungus_15_wh0_w3_str1v3_t0_b3c0m3}**
