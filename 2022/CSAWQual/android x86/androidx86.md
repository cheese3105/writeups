# Android x86
> There are some secrets on this phone image. Please find the flag!

Đính kèm với bài là 1 file image `android_forensics_easy.dd`  

Đầu tiên ta sẽ mở file bằng AutoSpy và tiến hành dò tìm từng folder một trong file này  

![](./Pics/Screenshot%202022-09-15%20164734.png)

Sau đấy ta sẽ tìm thấy file `note_pad.db-wal` có nói gì đó về secret note và một đoạn mã base64

![](./Pics/Screenshot%202022-09-15%20171633.png)

Đem đoạn mã đi decode base64 thì thấy flag

**Flag: flag{ev1dence_n0t_del3ted}**