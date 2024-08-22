#ifndef table_struct_INCLUDED

typedef struct order_t {
    uint64_t customer_id;
    uint64_t product_id;
    uint64_t quantity;
}  order;

typedef struct product_t {
    uint64_t product_id;
    uint64_t brand;
    uint64_t price;
}  product;

typedef struct output_t {
    uint64_t customer_id;
    uint64_t product_id;
    uint64_t quantity;
    double discount;
}  output;
#define table_struct_INCLUDED 
#endif