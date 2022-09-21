# Honors ABCs  

![image](https://user-images.githubusercontent.com/74854445/121958232-a6f3a400-cd8d-11eb-92f8-1d799d23ad43.png)

Ta có source C như sau:  

```c
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

char *correct = "abcdefghijklmnopqrstuvwxyz";

int main() {
    int grade = 0;
    char response[50];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to your first class at BCA: Honors-level ABCs.");
    puts("Because we expect all our students to be perfect, I'm not going to teach you anything.");
    sleep(2);
    puts("Instead, we're going to have a quiz!");
    puts("And, of course, I expect all of you to know the material already.");
    sleep(2);
    puts("");
    puts("╔════════════════════════╗");
    puts("║ THE QUIZ               ║");
    puts("║                        ║");
    puts("║ 1) Recite the alphabet ║");
    puts("╚════════════════════════╝");
    puts("");
    printf("Answer for 1: ");
    gets(response);

    for (int i = 0; i < 26; ++i) {
        if (response[i] == 0)
            break;
        if (response[i] != correct[i])
            break;

        grade = i * 4;
    }

    if (grade < 60)
        puts("An F? I'm sorry, but you clearly need to study harder.");
    else if (grade < 70)
        puts ("You didn't fail, but you could do better than a D.");
    else if (grade < 80)
        puts("Not terrible, but a C's nothing to write home about.");
    else if (grade < 90)
        puts("Alright, a B's not bad, I guess.");
    else if (grade < 100)
        puts("Ayyy, nice job on getting an A!");
    else if (grade == 100) {
        puts("Perfect score!");
        puts("You are an model BCA student.");
    } else {
        puts("How did you end up here?");
        sleep(2);
        puts("You must have cheated!");
        sleep(2);
        puts("Let me recite the BCA plagarism policy.");
        sleep(2);

        FILE *fp = fopen("flag.txt", "r");

        if (fp == NULL) {
            puts("Darn, I don't have my student handbook with me.");
            puts("Well, I guess I'll just give you a verbal warning to not cheat again.");
            puts("[If you are seeing this on the remote server, please contact admin].");
            exit(1);
        }

        int c;
        while ((c = getc(fp)) != EOF) {
            putchar(c);
            usleep(20000);
        }

        fclose(fp);
    }

    puts("");
    puts("Alright, class dismissed!");
}

```  
Vì trong chương trình có `gets(response);` mà `mảng response` lại liền kề `biến grade` nên ta có thể dễ dàng thay đổi `biến grade` bằng `buffer overflow` (làm tràn biến)  

Payload đơn giản là một chuỗi ký tự siêu dài trên 58 ký tự  

Như là AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  

Kết quả là... một chính sách dài về việc cheating :)))  

![image](https://user-images.githubusercontent.com/74854445/121960134-e3280400-cd8f-11eb-9b13-8933c21b0707.png)  

Và flag nữa :)))  

![image](https://user-images.githubusercontent.com/74854445/121960312-1d91a100-cd90-11eb-95e0-7441f862ac38.png)

Flag: bcactf{now_i_know_my_A_B_Cs!!_next_time_wont_you_cheat_with_me??}
