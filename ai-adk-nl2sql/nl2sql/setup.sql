
BEGIN
    ##### Change the name of dataset as required for the project demo #####
    DECLARE dataset string default "ecommerce_ds_demo";
    #######################################################################

    execute immediate "create schema if not exists " || dataset;
    execute immediate "create or replace table `"|| dataset || """.users`
      (
        id INTEGER	OPTIONS (description = 'user id'),
        first_name STRING	OPTIONS (description = 'first name of the user'), 
        last_name		STRING	OPTIONS (description = 'last name of the user'),
        email		STRING OPTIONS (description = 'email address of the user'),
        age		INTEGER OPTIONS (description = '	age of the user'),
        gender STRING OPTIONS (description = 'gender of user'),
        state		STRING OPTIONS (description = 'state to which the user belongs'),
        street_address STRING OPTIONS (description = 'residential address'),
        postal_code	STRING OPTIONS (description = 'postal zip code'),
        city	STRING OPTIONS (description = 'city'),
        country	STRING OPTIONS (description = 'country of the user'),
        latitude	FLOAT64 OPTIONS (description = 'latitude coordinates of the user address'),
        longitude	FLOAT64 OPTIONS (description = 'longitude coordinates of the user address'),
        traffic_source STRING OPTIONS (description = 'traffic source'),
        created_at TIMESTAMP	OPTIONS (description = 'user created date'),
        user_geom	GEOGRAPHY	OPTIONS (description = 'geometry coordinates')
      )
    """;

    execute immediate "create or replace table `"|| dataset || """.products`
      (
        id	INTEGER	OPTIONS (description = 'product id'),
        cost	FLOAT64 OPTIONS (description = 'cost of the product'),	
        category	STRING OPTIONS (description = 'category of the product'),	
        name	STRING OPTIONS (description = 'name of the product'),	
        brand	STRING OPTIONS (description = 'brand of the product'),	
        retail_price 	FLOAT64 OPTIONS (description = 'retail price of the product'),	
        department	STRING OPTIONS (description = 'department of the product'),	
        sku	STRING OPTIONS (description = 'sku of the product'),
        distribution_center_id INTEGER OPTIONS (description = 'distribution center id, points to id in distribution_centers dimension')
      )
    """;
  
  execute immediate "create or replace table `"|| dataset || """.orders`
    (
      order_id	INTEGER OPTIONS (description = 'id of the order'),
      user_id	INTEGER OPTIONS (description = 'user id, points to id in the users table'),
      status	STRING OPTIONS (description = '	status of the order'),
      gender	STRING OPTIONS (description = 'gender details'),
      created_at	TIMESTAMP OPTIONS (description = '	order created date'),
      returned_at	TIMESTAMP	 OPTIONS (description = 'order returned date'),
      shipped_at	TIMESTAMP	 OPTIONS (description = 'order shipped date'),
      delivered_at	TIMESTAMP OPTIONS (description = 'order delivered date'),
      num_of_item	INTEGER	OPTIONS (description = ' Number of items in the current order')
    )
  """;

  execute immediate "create or replace table `"|| dataset || """.order_items`
    (
      id	INTEGER	OPTIONS (description = 'Order Item Id'),
      order_id	INTEGER	 OPTIONS (description = 'Order Id pointing to the orders in orders table'),
      user_id	INTEGER OPTIONS (description = 'user id who placed the order, pointing to user in user table'),	
      product_id INTEGER OPTIONS (description = 'id of the product, points to product in the products table'),	
      inventory_item_id	INTEGER OPTIONS (description = 'inventory item id, points to id of inventory in the inventory table'),	
      status	STRING OPTIONS (description = 'status of the order item'),	
      created_at	TIMESTAMP OPTIONS (description = 'order item created date'),	
      shipped_at	TIMESTAMP OPTIONS (description = 'order item shipped date'),	
      delivered_at	TIMESTAMP OPTIONS (description = 'order item delivered date'),	
      returned_at	TIMESTAMP OPTIONS (description = 'order item returned date'),	
      sale_price FLOAT64 OPTIONS (description = 'sales price of the item')
    )
  """;

  execute immediate "create or replace table `"|| dataset || """.inventory_items`
    (
      id	INTEGER	OPTIONS (description = 'Inventory id'),
      product_id	INTEGER OPTIONS (description = 'product id corresponding to the product dimension'),
      created_at	TIMESTAMP OPTIONS (description = 'inventory creation timestamp'),
      sold_at	TIMESTAMP OPTIONS (description = '	inventory sold timestamp'),
      cost	FLOAT64	 OPTIONS (description = 'cost of the inventory'),
      product_category STRING OPTIONS (description = 'category of the product'),
      product_name	STRING OPTIONS (description = 'name of the product'),
      product_brand	STRING OPTIONS (description = 'brand of the product'),
      product_retail_price FLOAT64 OPTIONS (description = 'retail price of the product'),	
      product_department	STRING OPTIONS (description = 'department of the product'),
      product_sku	STRING OPTIONS (description = 'sku of product'),
      product_distribution_center_id	INTEGER OPTIONS (description = 'distribution center id pointing to distribution center dimension')
    )
  """;

  execute immediate "create or replace table `"|| dataset || """.distribution_centers`
    (
      id INTEGER OPTIONS (description = 'distribution center id'),	
      name	STRING OPTIONS (description = 'distribution center name'),	
      latitude FLOAT64 OPTIONS (description = 'Latitude of the distribution center'),	
      longitude	FLOAT64	OPTIONS (description = 'Longitude of the distribution center'), 
      distribution_center_geom GEOGRAPHY	OPTIONS (description = 'Geography coordinate of the distribution center')
    )
  """;

  execute immediate "insert into `" || dataset || ".users` select * from `bigquery-public-data.thelook_ecommerce.users`";
  execute immediate "insert into `" || dataset || ".products` select * from `bigquery-public-data.thelook_ecommerce.products`";
  execute immediate "insert into `" || dataset || ".orders` select * from `bigquery-public-data.thelook_ecommerce.orders`";
  execute immediate "insert into `" || dataset || ".order_items` select * from `bigquery-public-data.thelook_ecommerce.order_items`";
  execute immediate "insert into `" || dataset || ".inventory_items` select * from `bigquery-public-data.thelook_ecommerce.inventory_items`";
  execute immediate "insert into `" || dataset || ".distribution_centers` select * from `bigquery-public-data.thelook_ecommerce.distribution_centers`";


END