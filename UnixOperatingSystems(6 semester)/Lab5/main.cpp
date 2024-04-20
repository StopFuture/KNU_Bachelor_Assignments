//
// Created by Fedorych Andriy on 20/4/24.
//

#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <unistd.h>
#include <sys/wait.h>
#include <csignal>
#include <sys/ipc.h>
#include <sys/msg.h>

bool f(int x);
bool g(int x);

// Structure for message queue
struct MessageBuffer {
    long messageType;
    int value;
};

int getFirstQueueKey() {
    return ftok("progfile", 65);
}

int getSecondQueueKey() {
    return ftok("progfile", 66);
}

int getMessageQueue(int key, int flags) {
    int messageQueueId = msgget(key, flags);
    if (messageQueueId == -1) {
        perror("Failed to create or access message queue");
        exit(EXIT_FAILURE);
    }
    return messageQueueId;
}

void sendMessage(int queueId, const MessageBuffer& message) {
    if (msgsnd(queueId, &message, sizeof(MessageBuffer), 0) == -1) {
        perror("Failed to send message");
        exit(EXIT_FAILURE);
    }
}

MessageBuffer receiveMessage(int queueId, long messageType) {
    MessageBuffer message;
    if (msgrcv(queueId, &message, sizeof(MessageBuffer), messageType, 0) == -1) {
        perror("Failed to receive message");
        exit(EXIT_FAILURE);
    }
    return message;
}

void handleChildProcesses(pid_t firstChild, pid_t secondChild, int firstQueue, int secondQueue) {
    int status1, status2;
    bool firstComplete = false, secondComplete = false;
    MessageBuffer resp1, resp2;
    int time = 1;

    while (true) {
        // WNOHANG - immediately returns control if no child process has terminated
        pid_t firstCheck = waitpid(firstChild, &status1, WNOHANG);
        pid_t secondCheck = waitpid(secondChild, &status2, WNOHANG);

        std::cout << "Statuses: " << std::endl
                  << "First: " << firstCheck << ' '
                  << "Second: " << secondCheck << std::endl;

        if (firstCheck > 0) firstComplete = true;
        if (secondCheck > 0) secondComplete = true;

        if (firstComplete && secondComplete) {
            break;
        }

        if (firstComplete && resp1.value == -1) {
            std::cout << "Getting f result" << std::endl;
            resp1 = receiveMessage(firstQueue, 2);
            std::cout << "Received f value: " << resp1.value << std::endl;
            if (resp1.value == 1) {
                std::cout << "f(x)=1 and g(x)=undefined" << std::endl;
                std::cout << "Result: 1 || undefined = 1" << std::endl;
                msgctl(firstQueue, IPC_RMID, nullptr);
                msgctl(secondQueue, IPC_RMID, nullptr);
                std::cout << "Killing second child" << std::endl;
                kill(secondChild, SIGKILL);
                exit(0);
            }
        }

        if (secondComplete && resp2.value == -1) {
            std::cout << "Getting g result" << std::endl;
            resp2 = receiveMessage(secondQueue, 2);
            std::cout << "Received g value: " << resp2.value << std::endl;
            if (resp2.value == 1) {
                std::cout << "f(x)=undefined and g(x)=1" << std::endl;
                std::cout << "Result: undefined || 1 = 1" << std::endl;
                msgctl(firstQueue, IPC_RMID, nullptr);
                msgctl(secondQueue, IPC_RMID, nullptr);
                std::cout << "Killing first child" << std::endl;
                kill(firstChild, SIGKILL);
                exit(0);
            }
        }

        if (time % 5 == 0) {
            std::cout << "Do you want to continue calculations: y/n?" << std::endl;
            char response;
            std::cin >> response;
            if (response != 'y') {
                std::cout << "Killing everything" << std::endl;
                msgctl(firstQueue, IPC_RMID, nullptr);
                msgctl(secondQueue, IPC_RMID, nullptr);
                kill(firstChild, SIGKILL);
                kill(secondChild, SIGKILL);
                exit(0);
            }
        }

        sleep(1);
        time++;
    }

    if (resp1.value == -1) {
        resp1 = receiveMessage(firstQueue, 2);
    }
    if (resp2.value == -1) {
        resp2 = receiveMessage(secondQueue, 2);
    }

    msgctl(firstQueue, IPC_RMID, nullptr);
    msgctl(secondQueue, IPC_RMID, nullptr);

    std::cout << "f(x)=" << resp1.value << " and g(x)=" << resp2.value << std::endl;
    std::cout << "Result: " << resp1.value << " || " << resp2.value << " = " << (resp1.value || resp2.value) << std::endl;
}

int main() {
    int x;
    std::cout << "Enter data:" << std::endl;
    std::cin >> x;

    pid_t firstChild, secondChild;

    MessageBuffer msg1 = {1, x}, msg2 = {1, x};

    int firstQueue = getMessageQueue(getFirstQueueKey(), 0666 | IPC_CREAT);
    int secondQueue = getMessageQueue(getSecondQueueKey(), 0666 | IPC_CREAT);

    if ((firstChild = fork()) < 0) {
        perror("Can't fork process");
        exit(EXIT_FAILURE);
    }

    if (firstChild == 0) {
        MessageBuffer message = receiveMessage(firstQueue, 1);
        std::cout << "Child 1 received " << message.value << std::endl;
        int res1 = f(message.value);

        MessageBuffer response = {2, res1};
        sendMessage(firstQueue, response);
        std::cout << "Child 1 send " << res1 << std::endl;

        exit(EXIT_SUCCESS);
    } else {
        sendMessage(firstQueue, msg1);
        sendMessage(secondQueue, msg2);

        if ((secondChild = fork()) < 0) {
            perror("Can't fork process");
            exit(EXIT_FAILURE);
        }

        if (secondChild == 0) {
            MessageBuffer message = receiveMessage(secondQueue, 1);
            std::cout << "Child 2 received " << message.value << std::endl;
            int res2 = g(message.value);

            MessageBuffer response = {2, res2};
            sendMessage(secondQueue, response);
            std::cout << "Child 2 send " << res2 << std::endl;

            exit(EXIT_SUCCESS);
        } else {
            handleChildProcesses(firstChild, secondChild, firstQueue, secondQueue);
        }
    }

    return 0;
}

bool f(int x) {
    if (x < 0) return false;
    if (x == 0) return false;
    if (x > 0) {
        while (true) {
            sleep(1);
        }
    }
    return false; // Unreachable, but added for completeness
}

bool g(int x) {
    if (x < 0) {
        while (true) {
            sleep(1);
        }
    }
    if (x == 0) return true;
    if (x > 0) return true;

    return false; // Unreachable, but added for completeness
}