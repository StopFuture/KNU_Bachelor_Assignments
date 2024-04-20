#include <sys/ptrace.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#ifdef __x86_64__
#define PC_REGISTER REG_RIP
    #define SYSCALL_ARG_REG0 REG_RDI
    #define SYSCALL_ARG_REG1 REG_RSI
    #define SYSCALL_ARG_REG2 REG_RDX
#elif __arm64__
#include <mach/arm/thread_status.h>
#define PC_REGISTER ((arm_thread_state64_t *)&state)->__pc
#define SYSCALL_ARG_REG0 ((arm_thread_state64_t *)&state)->__x[0]
#define SYSCALL_ARG_REG1 ((arm_thread_state64_t *)&state)->__x[1]
#define SYSCALL_ARG_REG2 ((arm_thread_state64_t *)&state)->__x[2]
#endif

const int long_size = sizeof(long);

void reverse(char *str)
{
    int i, j;
    char temp;
    for (i = 0, j = strlen(str) - 2; i <= j; ++i, --j) {
        temp = str[i];
        str[i] = str[j];
        str[j] = temp;
    }
}

void getdata(pid_t child, long addr, char *str, int len)
{
    int i, j = 0;
    long data = 0;
    char *tmp = str;
    for (i = 0, j = 0; i < len; i += long_size, j++) {
        data = ptrace(PT_READ_D, child, (caddr_t)(addr + (j * long_size)), NULL);
        memcpy((void *)tmp, (void *)&data, long_size);
        tmp = tmp + long_size;
    }
    str[len] = '\0';
}

void putdata(pid_t child, long addr, char *str, int len)
{
    int i, j = 0;
    char *tmp = str;
    for (i = 0, j = 0; i < len; i += long_size, j++) {
        long val;
        memcpy(&val, tmp, long_size);
        ptrace(PT_WRITE_D, child, (caddr_t)(addr + (j * long_size)), val);
        tmp = tmp + long_size;
    }
}

int main()
{
    pid_t child;
    long orig_rax;
    long params[3];
    int status;
    int toggle = 0;
    char *str = 0;
    arm_thread_state64_t state; // For ARM64 architecture


    child = fork();

    if (child == 0) {
        ptrace(PT_TRACE_ME, 0, NULL, NULL);
        execl("/bin/echo", "echo", "Hello, World!", NULL);
    } else {
        while (1) {
            waitpid(child, &status, 0);
            if (WIFEXITED(status)) {
                break;
            }

            orig_rax = ptrace(PT_READ_D, child, (caddr_t)(long_size * PC_REGISTER), NULL);
            if (orig_rax == SYS_write) {
                toggle = 1;
                params[0] = ptrace(PT_READ_D, child, (caddr_t)(long_size * SYSCALL_ARG_REG0), NULL);
                params[1] = ptrace(PT_READ_D, child, (caddr_t)(long_size * SYSCALL_ARG_REG1), NULL);
                params[2] = ptrace(PT_READ_D, child, (caddr_t)(long_size * SYSCALL_ARG_REG2), NULL);

                printf("Before reversing:\n");
                printf("File descriptor: %ld\n", params[0]);
                printf("Output buffer address: %ld\n", params[1]);
                printf("Output buffer length: %ld\n", params[2]);

                int malloc_len = params[2] + params[2] % long_size + 1;
                str = (char *)malloc(malloc_len);
                getdata(child, params[1], str, params[2]);
                printf("Original string: %s\n", str);
                reverse(str);
                printf("Reversed string: %s\n", str);
                putdata(child, params[1], str, params[2]);

                printf("After reversing:\n");
                printf("File descriptor: %ld\n", params[0]);
                printf("Output buffer address: %ld\n", params[1]);
                printf("Output buffer length: %ld\n", params[2]);
            }

            ptrace(PT_CONTINUE, child, NULL, NULL);
        }
    }

    return 0;
}

// gcc -o demo main.cpp
// sudo ./demo