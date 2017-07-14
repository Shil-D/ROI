 #include <stdio.h>
#include <unistd.h>
#include <string.h>

enum Op {STAT, DEP};
typedef enum Op Op_t;

void add(FILE* fd, int month, int year, int iOp, int amnt){
    fprintf(fd, "%d.%d,%d,%d\n", month, year, iOp, amnt);
}

int main()
{
    char helloStr[]=
            "______ _____ _____ \n"
            "| ___ \\  _  |_   _|\n"
            "| |_/ / | | | | |  \n"
            "|    /| | | | | |  \n"
            "| |\\ \\\\ \\_/ /_| |_ \n"
            "\\_| \\_|\\___/ \\___/ \n"
                              ;
    char dbStr[256];
    char command[1000];
    char promt[] = "-->";
    FILE* fd;
    int iOp, month, year, amount;


    printf("%s\n\n", helloStr);
    printf("Enter your database filename:\n-->");
    scanf("%s", dbStr);

    if( access( dbStr, F_OK ) == -1 ) {
        printf("File doesn't %s exist. It will be created.\n", dbStr);
    }
    fd = fopen(dbStr, "a+");
    while (1){
        printf("%s", promt);
        scanf("%s", command);

        if (strcmp(command, "add") == 0)
        {
          scanf("%d.%d", &month, &year);
          scanf("%d", &iOp);
          scanf("%d", &amount);

          printf("adding %d.%d %d %d\n", month, year, iOp, amount);
          add(fd, month, year, iOp, amount);
        }
        else if (strcmp(command, "exit") == 0)
        {
          break;
        }
    }
    fclose(fd);
    return 0;
}
