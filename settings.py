BOT_NAME = 'bookscraper'

SPIDER_MODULES = ['bookscraper.spiders']
NEWSPIDER_MODULE = 'bookscraper.spiders'

# obey robots.txt rule
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'bookscraper.pipelines.BookscraperPipeline': 300,
}
