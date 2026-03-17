from itemadapter import ItemAdapter

# useful for handling different item types with a single interface
class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # strip all whitespace from strings
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                if isinstance(value, str):
                    adapter[field_name] = value.strip()

        # category & product type -> switch to lowercase
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            if isinstance(value, str):
                adapter[lowercase_key] = value.lower()

        # price => convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            if value is not None:
                value = value.replace('£', '')
                adapter[price_key] = float(value)

        # availability -> extract number of books in stock
        availability_string = adapter.get('availability')
        if availability_string:
            split_string_array = availability_string.split('(')
            if len(split_string_array) < 2:
                adapter['availability'] = 0
            else:
                availability_array = split_string_array[1].split(' ')
                adapter['availability'] = int(availability_array[0])

        # reviews -> convert string to number
        num_reviews_string = adapter.get('num_reviews')
        if num_reviews_string:
            adapter['num_reviews'] = int(num_reviews_string)

        # stars -> convert text to number
        stars_string = adapter.get('stars')
        if stars_string:
            split_stars_array = stars_string.split(' ')
            stars_text_value = split_stars_array[1].lower()
            if stars_text_value == 'zero':
                adapter['stars'] = 0
            elif stars_text_value == 'one':
                adapter['stars'] = 1
            elif stars_text_value == 'two':
                adapter['stars'] = 2
            elif stars_text_value == 'three':
                adapter['stars'] = 3
            elif stars_text_value == 'four':
                adapter['stars'] = 4
            elif stars_text_value == 'five':
                adapter['stars'] = 5

        return item
import mysql.connector

class SaveToMysqlPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Oolongtoker1!',
            database='books'
        )

        # create cursor, used to execute commands
        self.cur = self.conn.cursor()

        # create books table if none exists
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS `books` (
            id int NOT NULL AUTO_INCREMENT,
            url varchar(255),
            title text,
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):
        self.cur.execute(
            """INSERT INTO `books` (
            url, 
            title, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) VALUES (
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s, 
            %s,
            %s
            )""", (
                item['url'],
                item['title'],
                item['product_type'],
                item['price_excl_tax'],
                item['price_incl_tax'],
                item['tax'],
                item['price'],
                item['availability'],
                item['num_reviews'],
                item['stars'],
                item['category'],
                item['description'][0])
            )

        # execute insert of data into database
        self.conn.commit()
        return item

    def close_spider(self, spider):
        # close cursor & connection to database
        self.cur.close()
        self.conn.close()
