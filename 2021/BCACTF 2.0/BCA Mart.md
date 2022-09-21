# BCA Mart
![image](https://user-images.githubusercontent.com/74854445/121952362-5298f600-cd86-11eb-99de-806733cd6dc8.png)  

Ta có source C mà đề cho như sau:

```c 
#include <stdio.h>
#include <stdlib.h>

int money = 15;

int purchase(char *item, int cost) {
    int amount;
    printf("How many %s would you like to buy?\n", item);
    printf("> ");
    scanf("%d", &amount);

    if (amount > 0) {
        cost *= amount;
        printf("That'll cost $%d.\n", cost);
        if (cost <= money) {
            puts("Thanks for your purchse!");
            money -= cost;
        } else {
            puts("Sorry, but you don't have enough money.");
            puts("Sucks to be you I guess.");
            amount = 0;
        }
    } else {
        puts("I'm sorry, but we don't put up with pranksters.");
        puts("Please buy something or leave.");
    }

    return amount;
}

int main() {
    int input;

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);

    puts("Welcome to BCA MART!");
    puts("We have tons of snacks available for purchase.");
    puts("(Please ignore the fact we charge a markup on everything)");

    while (1) {
        puts("");
        puts("1) Hichew™: $2.00");
        puts("2) Lays® Potato Chips: $2.00");
        puts("3) Water in a Bottle: $1.00");
        puts("4) Not Water© in a Bottle: $2.00");
        puts("5) BCA© school merch: $20.00");
        puts("6) Flag: $100.00");
        puts("0) Leave");
        puts("");
        printf("You currently have $%d.\n", money);
        puts("What would you like to buy?");

        printf("> ");
        scanf("%d", &input);

        switch (input) {
            case 0:
                puts("Goodbye!");
                puts("Come back soon!");
                puts("Obviously, to spend more money :)");
                return 0;
            case 1:
                purchase("fruity pieces of goodness", 2);
                break;
            case 2:
                purchase("b̶a̶g̶s̶ ̶o̶f̶ ̶a̶i̶r̶ potato chips", 2);
                break;
            case 3:
                purchase("bottles of tap water", 1);
                break;
            case 4:
                purchase("generic carbonated beverages", 2);
                break;
            case 5:
                purchase("wonderfully-designed t-shirts", 20);
                break;
            case 6:
                if (purchase("super-cool ctf flags", 100) > 0) {
                    FILE *fp = fopen("flag.txt", "r");
                    char flag[100];

                    if (fp == NULL) {
                        puts("Hmm, I can't open our flag.txt file.");
                        puts("Sorry, but looks like we're all out of flags.");
                        puts("Out of luck, we just sold our last one a couple mintues ago.");
                        puts("[If you are seeing this on the remote server, please contact admin].");
                        exit(1);
                    }

                    fgets(flag, sizeof(flag), fp);
                    puts(flag);
                }
                break;
            default:
                puts("Sorry, please select a valid option.");
        }
    }
}

```  

Dựa trên đoạn code thì số tiền mà ta có là **money = 15**, flag thì có giá là **100$**  

Nhập vào số lượng cần mua rồi **hàm purchase** sẽ tính tổng giá tiền cần phải trả  

```c
int purchase(char *item, int cost) {
    int amount;
    printf("How many %s would you like to buy?\n", item);
    printf("> ");
    scanf("%d", &amount);

    if (amount > 0) {
        cost *= amount;
        printf("That'll cost $%d.\n", cost);
        if (cost <= money) {
            puts("Thanks for your purchse!");
            money -= cost;
        } else {
            puts("Sorry, but you don't have enough money.");
            puts("Sucks to be you I guess.");
            amount = 0;
        }
    } else {
        puts("I'm sorry, but we don't put up with pranksters.");
        puts("Please buy something or leave.");
    }

    return amount;
}
```  

Bình thường thì sẽ chẳng có cách nào để ta có thể mua một món đồ có giá 100 với số tiền là 15 được cả  

Nhưng trong chương trình này, có một lỗ hổng có thể khai thác để khiến `cost` (số tiến cần phải trả) nhỏ hơn `money` (số tiền mà ta có)  

Bằng cách `int overflow` với Payload là `2147483647`, số nguyên dương lớn nhất mà biến kiểu int có thể lưu trữ  

Nếu nhập vào một số lớn hơn số này thì số đấy sẽ trở thành số âm  

Thế nên sau khi **cost** nhân với một số âm thì nó sẽ trở thành số âm, nhỏ hơn số tiển 15$ mà ta đang có

`100 * 2147483647 = 100 * (2^31 - 1) = 50 * (2^32 - 2) = 50 * (-2) = 100 * -1`

Hoặc chỉ cần nhập 

`21474837, sau khi nhân với 100 sẽ thành 2147483700 > 2147483647 => trở thành số âm`

![image](https://user-images.githubusercontent.com/74854445/121955083-b375fd80-cd89-11eb-835f-3d49d34ce879.png)  

Flag: bcactf{bca_store??_wdym_ive_never_heard_of_that_one_before}



