#include <string.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <net/if.h>

#include <linux/sockios.h>

/*  struct for ethtool driver   */
struct ethtool_cmd {
    unsigned int cmd;
    unsigned int    supported;  /* Features this interface supports */
    unsigned int    advertising;    /* Features this interface advertises */
    unsigned short  speed;  /* The forced speed, 10Mb, 100Mb, gigabit */
    unsigned char   duplex; /* Duplex, half or full */
    unsigned char   port;   /* Which connector port */
    unsigned char   phy_address;
    unsigned char   transceiver;    /* Which tranceiver to use */
    unsigned char   autoneg;    /* Enable or disable autonegotiation */
    unsigned int    maxtxpkt;   /* Tx pkts before generating tx int */
    unsigned int    maxrxpkt;   /* Rx pkts before generating rx int */
    unsigned int    reserved[4];
};


#define SPEED_10    10
#define SPEED_100   100
#define SPEED_1000  1000
#define SPEED_10000 10000

/* Duplex, half or full. */
#define DUPLEX_HALF 0x00
#define DUPLEX_FULL 0x01

#define ETHTOOL_GSET    0x00000001 /* Get settings command for ethtool */


int GetEthSpeed(unsigned char *ethname)
{
    int returnValue;
    int fd;
    struct ifreq ifr;
    struct ethtool_cmd ecmd;

    /*  this entire function is almost copied from ethtool source code */
    memset(&ifr, 0, sizeof(ifr));
    strcpy(ifr.ifr_name, ethname);  //eth0

    /* Open control socket. */
    fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) 
    {
        fprintf(stdout,"Cannot get control socket");
        return -1;
    }
    /*  Pass the "get info" command to eth tool driver  */
    ecmd.cmd = ETHTOOL_GSET;
    ifr.ifr_data = (caddr_t)&ecmd;
    returnValue = ioctl(fd, SIOCETHTOOL, &ifr);

    /*  ioctl failed:   */
    if (returnValue != 0)
    {
        fprintf(stdout,"Cannot get device settings");
        return -1;
    }

    /*  and a bit of nifty printf-s for the human eye :-) */
    switch (ecmd.speed)
    {
        case SPEED_10:
            {
                fprintf(stdout,"Speed: 10Mbp/s ");
                break;
            }
        case SPEED_100:
            {
                fprintf(stdout,"Speed: 100Mbp/s ");
                break;
            }
        case SPEED_1000:
            {
                fprintf(stdout,"Speed: 1Gbp/s ");
                break;
            }
        case SPEED_10000:
            {
                fprintf(stdout,"Speed: 10Gbp/s ");
                break;
            }
        default:
            {
                fprintf(stdout,"Speed reading faulty ");
                break;
            }
    }


    switch (ecmd.duplex)
    {
        case    DUPLEX_FULL:
            {
                fprintf(stdout," Full Duplex\n");
                break;
            }
        case    DUPLEX_HALF:
            {
                fprintf(stdout," Half Duplex\n");
                break;
            }
        default:
            {
                fprintf(stdout," Duplex reading faulty\n");
                break;
            }
    }

    return 0;

}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Use: %s <interface>\n", argv[0]);
        return -1;
    }
    GetEthSpeed(argv[1]);
}
