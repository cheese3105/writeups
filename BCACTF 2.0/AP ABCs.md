# AP ABCs  

![image](https://user-images.githubusercontent.com/74854445/121961316-7c0b4f00-cd91-11eb-9051-9a34ac6caed9.png)  

Ta có source code như sau:  

```c
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

char *correct = "abcdefghijklmnopqrstuvwxyz";

int main() {
    int score = 1;
    char response[50];

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to AP ABCs!");
    puts("Unlike the non-AP class, you get the privilege of taking the AP test.");
    puts("Wow, I know, so exciting right\?\?!1");
    puts("Anyways, good luck!");
    sleep(2);
    puts("");
    puts("╔══════════════════════════════════════════╗");
    puts("║ 2021              AP® | 🌰 College Board ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║  ───────────────────────                 ║");
    puts("║  AP Alphabet                             ║");
    puts("║  Free-Response Questions                 ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║ Something about trademarks               ║");
    puts("╚══════════════════════════════════════════╝");
    sleep(2);
    puts("");
    puts("╔══════════════════════════════════════════╗");
    puts("║          2021 AP® Alphabet FRQs          ║");
    puts("║                                          ║");
    puts("║                 ALPHABET                 ║");
    puts("║                Section II                ║");
    puts("║             Total Time—1 hour            ║");
    puts("║           Number of Questions—1          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║ 1. Recite the alphabet                   ║");
    puts("║                                          ║");
    puts("║ ──────────────────────────────────────── ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                                          ║");
    puts("║                   STOP                   ║");
    puts("║                END OF EXAM               ║");
    puts("║                                          ║");
    puts("║                    -2-                   ║");
    puts("╚══════════════════════════════════════════╝");
    sleep(1);
    puts("");
    printf("Answer for 1: ");
    gets(response);

    for (int i = 0; i < 26; ++i) {
        if (response[i] == 0)
            break;
        if (response[i] != correct[i])
            break;

        if (i == 0)
            score = 1;
        if (i == 7 || i == 14 || i == 20 || i == 24)
            ++score;
    }

    puts("");
    printf("You got a %d on your APs.\n", score);

    if (score == 1)
        puts("Ouch. That hurts.");
    else if (score == 2)
        puts("At least that's not a 1...");
    else if (score == 3)
        puts("You are \"qualified\".");
    else if (score == 4)
        puts("You are \"very well qualified\".");
    else if (score == 5)
        puts("Nice job!");
    else if (score == 0x73434241) {
        puts("Tsk tsk tsk.");
        sleep(2);
        puts("Cheating on the AP® tests is really bad!");
        sleep(2);
        puts("Let me read you the College Board policies:");
        sleep(2);
        
        FILE *fp = fopen("flag.txt", "r");

        if (fp == NULL) {
            puts("AAAA, I lost my notes!");
            puts("You stay here while I go look for them.");
            puts("And don't move, you're still in trouble!");
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
}
```  

Ý tưởng của bài này cũng là `buffer overflow`  

Vì cần làm tràn chính xác `0x73434241` vào `score` nên mình sẽ lấy file thực thi về để debug hoặc có thể biên dịch source code trên để debug cũng được  




