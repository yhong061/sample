#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <inttypes.h>
//#include <libxml/parser.h>
//#include <libxml/tree.h>

//xmlDoc *xml_tree_doc = NULL; 

typedef int t_std_error;
#define STD_ERR_OK (0)
#define EINVAL (-1)
#define ENOMEM (-2)

#define PRINTERR(frmt, ...)       {printf("%s[%d]: ", __FUNCTION__, __LINE__);printf(frmt, ## __VA_ARGS__);}
#define PRINT(verb, frmt, ...)     printf(verb, frmt, ## __VA_ARGS__)
#define D_VERB0                    0
#define D_VERB1                    1
#define D_VERB2                    2
#define D_VERB3                    3


enum e_std_error_subsystems {
    e_std_err_NULL=0,
    e_std_err_NPU=1,
    e_std_err_BOARD=2,
    e_std_err_TEST=3,
    e_std_err_INTERFACE=4,
    e_std_err_DIAG=5,
    e_std_err_COM=6,
    e_std_err_HALCOM=7,
    e_std_err_QOS=8,
    e_std_err_ROUTE=9,
    e_std_err_ACL=10,
};

enum e_std_error_codes {
    e_std_err_code_FAIL=1,
    e_std_err_code_CFG=2,
    e_std_err_code_PARAM=3,
    e_std_err_code_TOOBIG=4,
    e_std_err_code_CLOSED=5,
    e_std_err_code_NOMEM=6,
};

#define STD_BIT_MASK_MAKE(type, bits) \
        (~((((type)~0) << ((bits)) & ((type)~0))))

#define STD_BIT_MASK(type, bits, bit_offset) \
        (STD_BIT_MASK_MAKE(type,bits) << (bit_offset))


#define STD_MK_ERR_FLAG_POS (31)
#define STD_MK_ERR_FLAG (1 << (STD_MK_ERR_FLAG_POS))

#define STD_MK_ERR_SUB_POS  (25)
#define STD_MK_ERR_SUB_MASK (STD_BIT_MASK(unsigned int,\
                                        STD_MK_ERR_FLAG_POS-STD_MK_ERR_SUB_POS,0))

#define STD_MK_ERR_ERRID_POS  (15)
#define STD_MK_ERR_ERRID_MASK (STD_BIT_MASK(unsigned int,\
                                        STD_MK_ERR_SUB_POS-STD_MK_ERR_ERRID_POS,0))

#define STD_MK_ERR_PRIV_POS  (0)
#define STD_MK_ERR_PRIV_MASK (STD_BIT_MASK(unsigned int,\
                                        STD_MK_ERR_ERRID_POS-STD_MK_ERR_PRIV_POS,0))


#define STD_ERR_MK(SUB, ERRID, PRIV) \
        ((1 << STD_MK_ERR_FLAG_POS ) | \
             (((SUB) & STD_MK_ERR_SUB_MASK) << STD_MK_ERR_SUB_POS )| \
             (((ERRID) & STD_MK_ERR_ERRID_MASK) << STD_MK_ERR_ERRID_POS ) | \
             (((PRIV) & STD_MK_ERR_PRIV_MASK) << STD_MK_ERR_PRIV_POS ))

/* FRU type/length, inspired from Linux kernel's include/linux/ipmi-fru.h */
struct fru_type_length {
    uint8_t     type_length;
    uint8_t     data[];
};

/* 8. Common Header Format */
struct fru_common_header {
    uint8_t     format_version;
    uint8_t     internal_use_offset;
    uint8_t     chassis_info_offset;
    uint8_t     board_info_offset;
    uint8_t     product_info_offset;
    uint8_t     multirecord_info_offset;
    uint8_t     pad;
    uint8_t     checksum;
};

/* 9. Internal Use Area Format */
struct internal_use_area {
    uint8_t     format_version;
    uint8_t     data[];
};

/* 10. Chassis Info Area Format
 * tl - Type/Length
 */
struct __attribute__ ((__packed__)) chassis_info_area {
    uint8_t     format_version;
    uint8_t     area_length;
    uint8_t     chassis_type;
    struct fru_type_length tl[];
};

/* 11. Board Info Area Format */
struct __attribute__ ((__packed__)) board_info_area {
    uint8_t     format_version;
    uint8_t     area_length;
    uint8_t     language_code;
    uint8_t     mfg_date[3];
    struct fru_type_length tl[];
};

/* 12. Product Info Area Format */
struct __attribute__ ((__packed__)) product_info_area {
    uint8_t     format_version;
    uint8_t     area_length;
    uint8_t     language_code;
    struct fru_type_length tl[];
};

struct __attribute__ ((__packed__)) element_hdr{
    uint8_t     type;
    uint16_t    offset;
};

/* 13. Internal Use Info Area Format */
struct __attribute__ ((__packed__)) internal_area_hdr {
    uint8_t     format_version;
    char        format_type[4];
    uint8_t     reserve[3];
    uint8_t     header_rev_flag;
    uint8_t     feature_flag;
    uint8_t     unit;
    uint16_t    max_fru_size;
    uint8_t     hdr_len;
    uint8_t     hdr_sum;
    uint8_t     element_cnt;
};

/*sperate two struct, according to element_cnt form the complete struct*/
struct __attribute__ ((__packed__)) internal_info_area{
    struct internal_area_hdr hdr;
    struct element_hdr el_hdr[];
};

/* 16. MultiRecord area format */
struct __attribute__ ((__packed__)) multirecord_area_hdr {
    uint8_t     record_type_id;
    uint8_t     record_format_version;
    uint8_t     record_length;
    uint8_t     record_checksum;
    uint8_t     header_checksum;
};

#define UUID_LEN (16)
#define UUID_STR_LEN (36)
/* 18.4. Management Access Record */
struct __attribute__ ((__packed__)) management_access_uuid {
    uint8_t     subrecord_type;
    uint8_t     uuid[UUID_LEN];
};

struct __attribute__ ((__packed__)) element_info_fru_type{
    uint8_t ele_type;
    uint16_t ele_len;
    uint8_t ele_cksum;
    uint8_t ele_rev;
    uint8_t fru_card_type_id;
    uint8_t reserve[2];
};

struct __attribute__ ((__packed__)) element_info_mac{
    uint8_t ele_type;
    uint16_t ele_len;
    uint8_t ele_cksum;
    uint8_t ele_rev;
    uint8_t mac_cnt;
    uint8_t mac_b[6];
};

struct __attribute__ ((__packed__)) element_info_power{
    uint8_t ele_type;
    uint16_t ele_len;
    uint8_t ele_cksum;
    uint8_t ele_rev;
    uint16_t max_sustained_s0;
    uint16_t max_peak_s0;
    uint16_t max_throttled_s0;
    uint16_t max_sustained_s5;
    uint16_t max_peak_s5;
};

struct __attribute__ ((__packed__)) element_info_fan{
    uint8_t ele_type;
    uint16_t ele_len;
    uint8_t ele_cksum;
    uint8_t ele_rev;
    uint8_t fan_dir;
    uint8_t no_of_fan;
    uint16_t max_speed;
};

struct __attribute__ ((__packed__)) element_list{
    uint8_t list_type;
    uint16_t list_addr;
    uint8_t list_entry_cnt;

};

struct __attribute__ ((__packed__)) element_sensor_list{
    uint8_t sensor_type;
    uint16_t sensor_target;
    uint8_t sensor_offset;
    uint16_t sensor_crit_limit;
    uint8_t reserve;
};

/* Mezzanine Card*/
struct __attribute__ ((__packed__)) element_info_mc{
    uint8_t ele_type;
    uint16_t ele_len;
    uint8_t ele_cksum;
    uint8_t list_number;
    struct element_list list[2];
    uint8_t form_factor;
    uint8_t self_protect;
    uint8_t operation_thermal_tier;
    uint8_t standby_thermal_tier;
    uint16_t min_inlet_temp;
    uint16_t max_inlet_temp;
    uint8_t min_fan_speed_pwm;
    uint8_t op_cool_tier_fan_failure;
    uint8_t extend_temp_tier;
    struct element_sensor_list sensor_list[3];
};


/*fru config, read from xml*/
typedef struct __attribute__ ((__packed__)){
    uint8_t fan_cnt; /*for sys eeprom only*/
    uint16_t max_fru_size;
    uint8_t iua_ele_cnt;
    struct element_hdr el_hdr[3]; /*sys eeprom 2, fan eeprom 3 element*/
}iua_conf_t;


#define MAC_STR_LEN 18
typedef struct{
    uint8_t mac_cnt;
    uint8_t mac_addr[MAC_STR_LEN];
}mac_conf_t;

#define MANUF_STR_LEN 7
#define PROD_STR_LEN 32
#define SERIAL_STR_LEN 14
#define PARTNUMB_STR_LEN 9
#define SYSTEM_ID_STR_LEN 2
#define BOARD_REV_ID_STR_LEN 2
#define SYS_SER_TAG_STR_LEN 32
#define ASSET_TAG_STR_LEN 63
typedef struct __attribute__ ((__packed__)){
    uint8_t manufacturer[MANUF_STR_LEN+1];
    uint8_t product_name[PROD_STR_LEN+1];
    uint8_t serial_number[SERIAL_STR_LEN+1];
    uint8_t part_number[PARTNUMB_STR_LEN+1];
}bia_conf_t;

typedef struct __attribute__ ((__packed__)){
    uint8_t manufacturer[MANUF_STR_LEN+1];
    uint8_t product_name[PROD_STR_LEN+1];
    uint8_t system_id[SYSTEM_ID_STR_LEN+1];
    uint8_t board_rev_id[BOARD_REV_ID_STR_LEN+1];
    uint8_t sys_ser_tag[SYS_SER_TAG_STR_LEN+1];
    uint8_t asset_tag[ASSET_TAG_STR_LEN+1];
}pia_conf_t;

typedef struct __attribute__ ((__packed__))
{
    uint16_t max_sustained_s0;
    uint16_t max_peak_s0;
    uint16_t max_throttled_s0;
    uint16_t max_sustained_s5;
    uint16_t max_peak_s5;
}power_conf_t;

typedef struct __attribute__ ((__packed__))
{
    uint8_t fan_dir;
    uint8_t no_of_fan;
    uint16_t max_speed;
}fan_conf_t;



typedef struct __attribute__ ((__packed__))
{
    iua_conf_t iua;
    uint8_t fru_type;
    mac_conf_t mac;
    bia_conf_t bia;
    pia_conf_t pia;
}sys_fru_conf_t;

typedef struct __attribute__ ((__packed__))
{
    iua_conf_t iua;
    uint8_t fru_type;
    power_conf_t power;
    fan_conf_t fan;
    bia_conf_t bia;
}fan_fru_conf_t;

typedef struct __attribute__ ((__packed__)) {
    uint8_t list_type;
    uint16_t list_addr;
    uint8_t list_entry_cnt;
}list_conf_t;

typedef struct __attribute__ ((__packed__)) {
    uint8_t sensor_type;
    uint16_t sensor_target;
    uint8_t sensor_offset;
    uint16_t sensor_crit_limit;
    uint8_t reserve;
}sensor_conf_t;

typedef struct __attribute__ ((__packed__))
{
    uint8_t list_number;
    list_conf_t *plist;
    uint8_t operation_thermal_tier;
    uint8_t standby_thermal_tier;
    uint16_t min_inlet_temp;
    uint16_t max_inlet_temp;
    uint8_t min_fan_speed_pwm;
    uint8_t operating_cooling_tier_fan_failure;
    uint8_t extend_temp_tier;
    sensor_conf_t sensor[3];
}mc_conf_t;


typedef struct __attribute__ ((__packed__))
{
    iua_conf_t iua;
    uint8_t fru_type;
    power_conf_t power;
    mc_conf_t mc;
    bia_conf_t bia;
    pia_conf_t pia;
}mc_fru_conf_t;


void dump_hex(const char *key, const void *buf, int off, int len)
{
    char *ptr = (char *)buf;
    int i;

    printf("dump %s, off=0x%x: ", key, off);
    for(i=0; i<len; i++){
        printf(" %02x", ptr[i]&0xff);
    }
    printf("\n");
}

t_std_error sys_fru_read_data(const char *filename, char *buf, int offset, int len)
{
    FILE *fp = NULL;
    int size;

    fp = fopen(filename, "rb");
    if(fp) {
        fseek(fp, offset, SEEK_SET);
        size = fread(buf, 1, len, fp);
        fclose(fp);
        if(size != len) {
            PRINTERR("Failed to get right len %d, expect %d\n", size, len);
            return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, EINVAL);
        }
        PRINTERR("expect %d\n", len);
    }
    else {
        PRINTERR("Failed to open %s\n", filename);
        return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, EINVAL);
    }
    return STD_ERR_OK;
}

t_std_error sys_fru_parse_iua(const char *filename, int offset, sys_fru_conf_t *pconf)
{
    t_std_error ret = STD_ERR_OK;
    int size;
    char *data = NULL;
    struct internal_info_area *iua = NULL;

    size = sizeof(struct internal_info_area);
    data = (char *)calloc(size, 1);
    if(data == NULL) {
        PRINTERR("Could not allocate memory\n");
        return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, ENOMEM);
    }

    ret = sys_fru_read_data(filename, data, offset, size);
    if(ret != STD_ERR_OK) {
        free(data);
        PRINTERR("Failed to get fru_common_header\n");
        return ret;
    }

    iua = (struct internal_info_area *)data;
    dump_hex("iua", iua, offset, size);

    free(data);
    return STD_ERR_OK;
}

t_std_error sys_fru_parse_bia(const char *filename, int offset, sys_fru_conf_t *pconf)
{
    return STD_ERR_OK;
}

t_std_error sys_fru_parse_pia(const char *filename, int offset, sys_fru_conf_t *pconf)
{
    return STD_ERR_OK;
}

t_std_error sys_fru_parse_mia(const char *filename, int offset, sys_fru_conf_t *pconf)
{
    return STD_ERR_OK;
}

t_std_error sys_fru_parse(const char *filename, sys_fru_conf_t *pconf)
{
    t_std_error ret = STD_ERR_OK;
    int size;
    int offset;
    char *data = NULL;
    struct fru_common_header *header = NULL;

    size = sizeof(struct fru_common_header);
    data = (char *)calloc(size, 1);
    if(data == NULL) {
        PRINTERR("Could not allocate memory\n");
        return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, ENOMEM);
    }

    ret = sys_fru_read_data(filename, data, 0, size);
    if(ret != STD_ERR_OK) {
        free(data);
        PRINTERR("Failed to get fru_common_header\n");
        return ret;
    }

    header = (struct fru_common_header *)data;
    dump_hex("header", header, 0, size);
    if(header->format_version != 1) {
        free(data);
        PRINTERR("Unknown FRU header version 0x%02x\n", header->format_version);
        return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, EINVAL);
    }

    offset = header->internal_use_offset * 8;
    if(offset >= size) {
        sys_fru_parse_iua(filename, offset, pconf);
    }

    offset = header->board_info_offset * 8;
    if(offset >= size) {
        sys_fru_parse_bia(filename, offset, pconf);
    }

    offset = header->product_info_offset * 8;
    if(offset >= size) {
        sys_fru_parse_pia(filename, offset, pconf);
    }

    offset = header->multirecord_info_offset * 8;
    if(offset >= size) {
        sys_fru_parse_mia(filename, offset, pconf);
    }

    free(data);
    return STD_ERR_OK;
}

#define FRU_CONTEXT_FILENAME  "fru_context.xml"
#define FRU_READ_FILENAME  "read.bin"

int main(void)
{
    sys_fru_conf_t sys_fru_conf;
    memset(&sys_fru_conf, 0, sizeof(sys_fru_conf));
    sys_fru_parse(FRU_READ_FILENAME, &sys_fru_conf);
    return 0;
}
