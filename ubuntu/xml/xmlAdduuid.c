#include <stdio.h>
#include <libxml/parser.h>
#include <libxml/tree.h>
#include <string.h>

xmlDoc *xml_tree_doc = NULL; 

typedef int t_std_error;
#define STD_ERR_OK (0)
#define EINVAL (-1)
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

t_std_error modify_xml_config(char *cfg_file, char *fru_tag, char *field_tag, char *value)
{
    size_t len = 0;
    FILE *fname = NULL;
    char *linebuf = NULL;
    xmlNode *root_element = NULL;
    xmlNode *cur = NULL;
    xmlNode *cur_entry = NULL;
    xmlNode *cur_entry_data = NULL;
    xmlNode *cur_field_entry = NULL;
    xmlNode *cur_field_entry_data = NULL;
    xmlNode *node = NULL;
    xmlNode *newnode = NULL;
    int flag_find_field_tag = 0;
    printf("%s %s %s\n", fru_tag, field_tag, value);

    /* Check if this is an xml config and if so call the common parser library function */
    if(strstr(cfg_file, "xml") != NULL) {
        xmlKeepBlanksDefault(0);
        xmlIndentTreeOutput = 1;
        
        /* Read in the XML config and perform validation*/
        xml_tree_doc = xmlReadFile(cfg_file, NULL, 0);
        if(xml_tree_doc == NULL) {
            return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, EINVAL);
        }
        /* Debug - Dump the read tree to the console */
        /*Get the root element node */
        root_element = xmlDocGetRootElement(xml_tree_doc);
        if(root_element == NULL) {
            printf("Empty XML Tree\n");
            return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, EINVAL);
        }

        if(xmlStrcmp(root_element->name, (const xmlChar *) "config")) {
            printf("Invalid xml config file (%s)\n", root_element->name);
            return STD_ERR_MK(e_std_err_DIAG, e_std_err_code_FAIL, EINVAL);
        }

        node = root_element;
        // Get the first child of the root node, which shoudl be a device
        cur = node->children;
        // the child will be the TEXT Node for the config entry, discard that
        while ((cur != NULL) && (cur->type == XML_TEXT_NODE)) {
            cur = cur->next;
        }


        while (cur != NULL) {
            if(!xmlStrcmp(cur->name, (const xmlChar *)fru_tag)) {
                for(cur_entry = cur->children; cur_entry != NULL; cur_entry=cur_entry->next) {
                    if(cur_entry->type == XML_ELEMENT_NODE) {
                        if (!xmlStrcmp(cur_entry->name, (const xmlChar *)"mac")){
                            for(cur_field_entry = cur_entry->children; cur_field_entry != NULL; cur_field_entry = cur_field_entry->next ){
                                if (!xmlStrcmp(cur_field_entry->name, (const xmlChar *)field_tag)){
                                    flag_find_field_tag = 1;
                                    cur_field_entry_data = cur_field_entry->children;
                                    if(cur_field_entry_data->type == XML_TEXT_NODE) {
                                        printf("%s changed to %s\n", cur_field_entry_data->content, value);
                                        if(strlen(value) <= xmlStrlen(cur_field_entry_data->content)){
                                            memset((char *)cur_field_entry_data->content, ' ', xmlStrlen(cur_field_entry_data->content));
                                            memcpy((char *)cur_field_entry_data->content, value, strlen(value));
                                        }else{
                                            printf("tag str beyoned the length range!\n");
                                        }

                                    }
                                }
                            }
                        }
                        if (!xmlStrcmp(cur_entry->name, (const xmlChar *)"iua")){
                            for(cur_field_entry = cur_entry->children; cur_field_entry != NULL; cur_field_entry = cur_field_entry->next ){
                                if (!xmlStrcmp(cur_field_entry->name, (const xmlChar *)field_tag)){
                                    flag_find_field_tag = 1;
                                    cur_field_entry_data = cur_field_entry->children;
                                    if(cur_field_entry_data->type == XML_TEXT_NODE) {
                                        printf("%s changed to %s\n", cur_field_entry_data->content, value);
                                        if(strlen(value) <= xmlStrlen(cur_field_entry_data->content)){
                                            memset((char *)cur_field_entry_data->content, ' ', xmlStrlen(cur_field_entry_data->content));
                                            memcpy((char *)cur_field_entry_data->content, value, strlen(value));
                                        }else{
                                            printf("tag str beyoned the length range!\n");
                                        }

                                    }
                                }
                            }
                        }
                        if (!xmlStrcmp(cur_entry->name, (const xmlChar *)"bia")){
                            for(cur_field_entry = cur_entry->children; cur_field_entry != NULL; cur_field_entry = cur_field_entry->next ){
                                if (!xmlStrcmp(cur_field_entry->name, (const xmlChar *)field_tag)){
                                    flag_find_field_tag = 1;
                                    cur_field_entry_data = cur_field_entry->children;
                                    if(cur_field_entry_data->type == XML_TEXT_NODE) {
                                        printf("%s changed to %s\n", cur_field_entry_data->content, value);
                                        if(strlen(value) <= xmlStrlen(cur_field_entry_data->content)){
                                            memset((char *)cur_field_entry_data->content, ' ', xmlStrlen(cur_field_entry_data->content));
                                            memcpy((char *)cur_field_entry_data->content, value, strlen(value));
                                        }else{
                                            printf("tag str beyoned the length range!\n");
                                        }
                                    }
                                }
                            }
                        }
                        if (!xmlStrcmp(cur_entry->name, (const xmlChar *)"pia")){
                            for(cur_field_entry = cur_entry->children; cur_field_entry != NULL; cur_field_entry = cur_field_entry->next ){
                                if (!xmlStrcmp(cur_field_entry->name, (const xmlChar *)field_tag)){
                                    flag_find_field_tag = 1;
                                    cur_field_entry_data = cur_field_entry->children;
                                    if(cur_field_entry_data->type == XML_TEXT_NODE) {
                                        printf("%s changed to %s\n", cur_field_entry_data->content, value);
                                        if(strlen(value) <= xmlStrlen(cur_field_entry_data->content)){
                                            memset((char *)cur_field_entry_data->content, ' ', xmlStrlen(cur_field_entry_data->content));
                                            memcpy((char *)cur_field_entry_data->content, value, strlen(value));
                                        }else{
                                            printf("tag str beyoned the length range!\n");
                                        }
                                    }
                                }
                            }
                        }
                        if (!xmlStrcmp(cur_entry->name, (const xmlChar *)"fan")){
                            for(cur_field_entry = cur_entry->children; cur_field_entry != NULL; cur_field_entry = cur_field_entry->next ){
                                if (!xmlStrcmp(cur_field_entry->name, (const xmlChar *)field_tag)){
                                    flag_find_field_tag = 1;
                                    cur_field_entry_data = cur_field_entry->children;
                                    if(cur_field_entry_data->type == XML_TEXT_NODE) {
                                        printf("%s changed to %s\n", cur_field_entry_data->content, value);
                                        if(strlen(value) <= xmlStrlen(cur_field_entry_data->content)){
                                            memset((char *)cur_field_entry_data->content, ' ', xmlStrlen(cur_field_entry_data->content));
                                            memcpy((char *)cur_field_entry_data->content, value, strlen(value));
                                        }else{
                                            printf("tag str beyoned the length range!\n");
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                if(flag_find_field_tag == 0) {
                    printf("Unsupport the modify tag: %s\n", field_tag);
                    printf("cur->name = %s\n", cur->name);
                    if(strcmp(cur->name, "sys_fru") == 0){ 
                        if(strcmp(field_tag, "uuid_tag") == 0){
                            newnode = xmlNewNode(NULL, BAD_CAST "uuid");
                            xmlAddChild(cur, newnode);
                            xmlNewTextChild(newnode, NULL, (const xmlChar *)field_tag, (const xmlChar *)value);
                        }
                    }
                }
            }
            cur = cur->next;
            /* After the device is the text node which is the carriage return */
            while ((cur != NULL) && (cur->type == XML_TEXT_NODE)) {
                cur = cur->next;
            }
        }

        xmlSaveFormatFile(cfg_file, xml_tree_doc, 1);
        xmlFreeDoc(xml_tree_doc);
    }
}

#define FRU_CONTEXT_FILENAME  "fru_context.xml"
int main(void)
{
    char pfrustr[] = "sys_fru";
    char pmodstr[] = "uuid_tag";
    char pvalstr[] = "9f1c45ab-ff00-4bf2-8e34-4cad10b881d3";
    if(modify_xml_config(FRU_CONTEXT_FILENAME, pfrustr, pmodstr, pvalstr) != STD_ERR_OK) {
        return -1;
    }
    return 0;
}
