BOT_NAME = 'bookscraper'

SPIDER_MODULES = ['bookscraper.spiders']
NEWSPIDER_MODULE = 'bookscraper.spiders'

# FEEDS = {
#     'booksdata.csv': {'format': 'csv'}
# }



# obey robots.txt rule
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'bookscraper.pipelines.BookscraperPipeline': 300,
    # 'bookscraper.pipelines.SaveToMysqlPipeline': 400,
}
