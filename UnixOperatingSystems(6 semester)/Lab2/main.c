#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include <time.h>

#define N 100
#define LEFT (i + N - 1) % N
#define RIGHT (i + 1) % N
#define THINKING 0
#define HUNGRY 1
#define EATING 2

int state[N];
pthread_mutex_t mutex_;
sem_t s[N];
pthread_mutex_t mo;

int myrand(int min, int max) {
    return rand() % (max - min + 1) + min;
}

void test(int i) {
    if (state[i] == HUNGRY && state[LEFT] != EATING && state[RIGHT] != EATING) {
        state[i] = EATING;
        sem_post(&s[i]);
    }
}

void think(int i) {
    int duration = myrand(400, 800);
    pthread_mutex_lock(&mo);
    printf("%d thinks for %dms\n", i, duration);
    pthread_mutex_unlock(&mo);
    usleep(duration * 1000);
}

void take_forks(int i) {
    pthread_mutex_lock(&mutex_);
    state[i] = HUNGRY;
    pthread_mutex_lock(&mo);
    printf("%d is hungry\n", i);
    pthread_mutex_unlock(&mo);
    test(i);
    pthread_mutex_unlock(&mutex_);
    sem_wait(&s[i]);
    pthread_mutex_lock(&mo); // Logging picking up forks
    printf("    %d picked up forks %d (left) and %d (right)\n", i, LEFT, RIGHT);
    pthread_mutex_unlock(&mo);
}

void eat(int i) {
    int duration = myrand(400, 800);
    pthread_mutex_lock(&mo);
    printf("    %d eats for %dms\n", i, duration);
    pthread_mutex_unlock(&mo);
    usleep(duration * 1000);
}

void put_forks(int i) {
    pthread_mutex_lock(&mutex_);
    state[i] = THINKING;
    pthread_mutex_lock(&mo); // Logging putting down forks
    printf("    %d put down forks %d (left) and %d (right)\n", i, LEFT, RIGHT);
    pthread_mutex_unlock(&mo);
    test(LEFT); // See if left neighbor can now eat
    test(RIGHT); // See if right neighbor can now eat
    pthread_mutex_unlock(&mutex_);
}

void* philosopher(void* num) {
    int i = *(int*)num;
    while (1) {
        think(i);
        take_forks(i);
        eat(i);
        put_forks(i);
    }
}

int main() {
    int i;
    int philosophers[N];
    pthread_t thread_id[N];

    printf("Dining Philosophers Problem\n");

    srand(time(NULL));
    pthread_mutex_init(&mutex_, NULL);
    pthread_mutex_init(&mo, NULL);

    for (i = 0; i < N; i++)
        sem_init(&s[i], 0, 0);


    for (i = 0; i < N; i++) {
        philosophers[i] = i;
        pthread_create(&thread_id[i], NULL, philosopher, &philosophers[i]);
    }

    for (i = 0; i < N; i++) {
        pthread_join(thread_id[i], NULL);
    }

    return 0;
}
