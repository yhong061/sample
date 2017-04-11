// "/dev/video0": video0�豸��ʹ�þ���
/*
=============================================================
VIDIOC_REQBUFS�������ڴ� 
VIDIOC_QUERYBUF����VIDIOC_REQBUFS�з�������ݻ���ת���������ַ 
VIDIOC_QUERYCAP����ѯ�������� 
VIDIOC_ENUM_FMT����ȡ��ǰ����֧�ֵ���Ƶ��ʽ 
VIDIOC_S_FMT�����õ�ǰ������Ƶ�����ʽ 
VIDIOC_G_FMT����ȡ��ǰ������Ƶ�����ʽ 
VIDIOC_TRY_FMT����֤��ǰ��������ʾ��ʽ 
VIDIOC_CROPCAP����ѯ�������޼����� 
VIDIOC_S_CROP��������Ƶ�źŵı߿� 
VIDIOC_G_CROP����ȡ��Ƶ�źŵı߿� 
VIDIOC_QBUF�������ݷŻػ������ 
VIDIOC_DQBUF�������ݴӻ����ж�ȡ���� 
VIDIOC_STREAMON����ʼ��Ƶ��ʾ 
VIDIOC_STREAMOFF��������Ƶ��ʾ 
VIDIOC_QUERYSTD����鵱ǰ��Ƶ�豸֧�ֵı�׼������PAL��NTSC�� 
=============================================================
*/

#include <stdio.h>

#define CAMERA_DEVICE "/dev/video0"
#define CAPTURE_FILE "frame.jpg"

#define VIDEO_WIDTH 640
#define VIDEO_HEIGHT 480
#define VIDEO_FORMAT V4L2_PIX_FMT_YUYV
#define BUFFER_COUNT 4

typedef long unsigned int size_t;
typedef unsigned short __u16;
typedef unsigned int	__u32;
typedef unsigned char __u8;
typedef unsigned long long	__u64;	

typedef struct VideoBuffer {
    void   *start;
    size_t  length;
} VideoBuffer;


struct v4l2_capability {
	__u8	driver[16];
	__u8	card[32];
	__u8	bus_info[32];
	__u32   version;
	__u32	capabilities;
	__u32	device_caps;
	__u32	reserved[3];
};




struct v4l2_pix_format {
	__u32         		width;
	__u32			height;
	__u32			pixelformat;
	__u32			field;		/* enum v4l2_field */
	__u32            	bytesperline;	/* for padding, zero if unused */
	__u32          		sizeimage;
	__u32			colorspace;	/* enum v4l2_colorspace */
	__u32			priv;		/* private data, depends on pixelformat */
};

struct v4l2_plane_pix_format {
	__u32		sizeimage;
	__u16		bytesperline;
	__u16		reserved[7];
} __attribute__ ((packed));

struct v4l2_pix_format_mplane {
	__u32				width;
	__u32				height;
	__u32				pixelformat;
	__u32				field;
	__u32				colorspace;

	struct v4l2_plane_pix_format	plane_fmt[VIDEO_MAX_PLANES];
	__u8				num_planes;
	__u8				reserved[11];
} __attribute__ ((packed));

struct v4l2_rect {
	__s32   left;
	__s32   top;
	__s32   width;
	__s32   height;
};

struct v4l2_clip {
	struct v4l2_rect        c;
	struct v4l2_clip	__user *next;
};

struct v4l2_window {
	struct v4l2_rect        w;
	__u32			field;	 /* enum v4l2_field */
	__u32			chromakey;
	struct v4l2_clip	__user *clips;
	__u32			clipcount;
	void			__user *bitmap;
	__u8                    global_alpha;
};

struct v4l2_vbi_format {
	__u32	sampling_rate;		/* in 1 Hz */
	__u32	offset;
	__u32	samples_per_line;
	__u32	sample_format;		/* V4L2_PIX_FMT_* */
	__s32	start[2];
	__u32	count[2];
	__u32	flags;			/* V4L2_VBI_* */
	__u32	reserved[2];		/* must be zero */
};

struct v4l2_sliced_vbi_format {
	__u16   service_set;
	/* service_lines[0][...] specifies lines 0-23 (1-23 used) of the first field
	   service_lines[1][...] specifies lines 0-23 (1-23 used) of the second field
				 (equals frame lines 313-336 for 625 line video
				  standards, 263-286 for 525 line standards) */
	__u16   service_lines[2][24];
	__u32   io_size;
	__u32   reserved[2];            /* must be zero */
};

struct v4l2_format {
	__u32	 type;
	union {
		struct v4l2_pix_format		pix;     /* V4L2_BUF_TYPE_VIDEO_CAPTURE */
		struct v4l2_pix_format_mplane	pix_mp;  /* V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE */
		struct v4l2_window		win;     /* V4L2_BUF_TYPE_VIDEO_OVERLAY */
		struct v4l2_vbi_format		vbi;     /* V4L2_BUF_TYPE_VBI_CAPTURE */
		struct v4l2_sliced_vbi_format	sliced;  /* V4L2_BUF_TYPE_SLICED_VBI_CAPTURE */
		__u8	raw_data[200];                   /* user-defined */
	} fmt;
};

struct v4l2_requestbuffers {
	__u32			count;
	__u32			type;		/* enum v4l2_buf_type */
	__u32			memory;		/* enum v4l2_memory */
	__u32			reserved[2];
};

enum v4l2_buf_type {
	V4L2_BUF_TYPE_VIDEO_CAPTURE        = 1,
	V4L2_BUF_TYPE_VIDEO_OUTPUT         = 2,
	V4L2_BUF_TYPE_VIDEO_OVERLAY        = 3,
	V4L2_BUF_TYPE_VBI_CAPTURE          = 4,
	V4L2_BUF_TYPE_VBI_OUTPUT           = 5,
	V4L2_BUF_TYPE_SLICED_VBI_CAPTURE   = 6,
	V4L2_BUF_TYPE_SLICED_VBI_OUTPUT    = 7,
#if 1
	/* Experimental */
	V4L2_BUF_TYPE_VIDEO_OUTPUT_OVERLAY = 8,
#endif
	V4L2_BUF_TYPE_VIDEO_CAPTURE_MPLANE = 9,
	V4L2_BUF_TYPE_VIDEO_OUTPUT_MPLANE  = 10,
	/* Deprecated, do not use */
	V4L2_BUF_TYPE_PRIVATE              = 0x80,
};

enum v4l2_memory {
	V4L2_MEMORY_MMAP             = 1,
	V4L2_MEMORY_USERPTR          = 2,
	V4L2_MEMORY_OVERLAY          = 3,
	V4L2_MEMORY_DMABUF           = 4,
};


int main()
{
    int i, ret;

    // ���豸
    int fd = open(CAMERA_DEVICE, O_RDWR, 0);

    // ��ȡ������Ϣ
    struct v4l2_capability cap;
    ret = ioctl(fd, VIDIOC_QUERYCAP, &cap);
    // Print capability infomations
    printf("Capability Informations:\n");
    printf(" driver: %s\n", cap.driver);
    printf(" card: %s\n", cap.card);
    printf(" bus_info: %s\n", cap.bus_info);
    printf(" version: %08X\n", cap.version);
    printf(" capabilities: %08X\n", cap.capabilities);

    // ������Ƶ��ʽ
    struct v4l2_format fmt;
    memset(&fmt, 0, sizeof(fmt));
    fmt.type                = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt.fmt.pix.width       = VIDEO_WIDTH;
    fmt.fmt.pix.height      = VIDEO_HEIGHT;
    fmt.fmt.pix.pixelformat = V4L2_PIX_FMT_YUYV;
    fmt.fmt.pix.field       = V4L2_FIELD_INTERLACED;
    ret = ioctl(fd, VIDIOC_S_FMT, &fmt);

    // ��ȡ��Ƶ��ʽ
    ret = ioctl(fd, VIDIOC_G_FMT, &fmt);
    // Print Stream Format
    printf("Stream Format Informations:\n");
    printf(" type: %d\n", fmt.type);
    printf(" width: %d\n", fmt.fmt.pix.width);
    printf(" height: %d\n", fmt.fmt.pix.height);
    char fmtstr[8];
    memset(fmtstr, 0, 8);
    memcpy(fmtstr, &fmt.fmt.pix.pixelformat, 4);
    printf(" pixelformat: %s\n", fmtstr);
    printf(" field: %d\n", fmt.fmt.pix.field);
    printf(" bytesperline: %d\n", fmt.fmt.pix.bytesperline);
    printf(" sizeimage: %d\n", fmt.fmt.pix.sizeimage);
    printf(" colorspace: %d\n", fmt.fmt.pix.colorspace);
    printf(" priv: %d\n", fmt.fmt.pix.priv);
    printf(" raw_date: %s\n", fmt.fmt.raw_data);

    // ��������ڴ�:  BUFFER_COUNT * v4l2_buffer
    struct v4l2_requestbuffers reqbuf;
    reqbuf.count = BUFFER_COUNT;
    reqbuf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    reqbuf.memory = V4L2_MEMORY_MMAP; 
    ret = ioctl(fd , VIDIOC_REQBUFS, &reqbuf);

    // ����ȡ�����ڴ湲�����
    //VideoBuffer*  buffers = calloc( reqbuf.count, sizeof(*buffers) );
    struct v4l2_buffer buf;
    for (i = 0; i < reqbuf.count; i++) 
    {
        buf.index = i;
        buf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
        buf.memory = V4L2_MEMORY_MMAP;
        ret = ioctl(fd , VIDIOC_QUERYBUF, &buf);  //����index��ѯbuf

        // mmap buffer
        framebuf[i].length = buf.length;
        framebuf[i].start = (char *) mmap(0, buf.length, PROT_READ|PROT_WRITE, MAP_SHARED, fd, buf.m.offset);
    
        // Queen buffer
        ret = ioctl(fd , VIDIOC_QBUF, &buf); //��buf�ŵ����������

        printf("Frame buffer %d: address=0x%x, length=%d\n", i, (unsigned int)framebuf[i].start, framebuf[i].length);
    }

    // ��ʼ¼��
    enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    ret = ioctl(fd, VIDIOC_STREAMON, &type);

    // Get frame
    ret = ioctl(fd, VIDIOC_DQBUF, &buf);   //��buf�ӻ���������ó���

    // Process the frame
    FILE *fp = fopen(CAPTURE_FILE, "wb");
    fwrite(framebuf[buf.index].start, 1, buf.length, fp);
    fclose(fp);
    printf("Capture one frame saved in %s\n", CAPTURE_FILE);

    // Re-queen buffer
    ret = ioctl(fd, VIDIOC_QBUF, &buf);

    enum v4l2_buf_type type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    ret = ioctl(fd, VIDIOC_STREAMOFF, &type);

    // Release the resource
    for (i=0; i< 4; i++) 
    {
        munmap(framebuf[i].start, framebuf[i].length);
    }

    close(fd);
    printf("Camera test Done.\n");
    return 0;
}
