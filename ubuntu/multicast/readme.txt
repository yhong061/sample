
multi_udp_server:

�ļ����룺gcc -Wall multi_udp_server.c -o server 

���У�./server 230.1.1.1 7838

================================================================

multi_udp_clinet:

���룺gcc -Wall multi_udp_clinet.c -o clinet

���У�./clinet 230.1.1.1 7838 192.168.1.121 5500