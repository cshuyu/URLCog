import scrapy
#usage:  
#  scrapy crawl links -a seed_fname=./mozilla-top500-url.txt -o result.json
class LinkSpider(scrapy.Spider):
    name = 'links'
    def __init__(self, seed_fname, *args, **kwargs):
        self.filterSet = set()
        # TODO: what if the size of collectedSet is too large
        #       to be stored in the memory?
        self.collectedSet = set()
        self.threshold = 500000
        self.filename = seed_fname

    # this method must return an iterable of Requests,
    # either a list or a generator function.
    def start_requests(self):
        # TODO: change the hard-coded urls to be a list of
        #       URLs whose file name is given by the program's 
        #       parameter. 
        urls = []
        with open(self.filename) as f:
            for line in f:
                urls.append(line.strip())
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                headers=self.create_header())

    def parse(self, response):
        # extract the href attribute of a tag.
        a_tags = response.css('a::attr(href)')
        if a_tags is not None and len(a_tags) > 0:
            for a_tag in a_tags:
                # rebuild relative URL as full URL.
                url = response.urljoin(a_tag.extract())
                url = url.lower()
                if url in self.filterSet:
                    continue
                if url in self.collectedSet:
                    continue
                self.collectedSet.add(url)
                yield {
                    'url' : url 
                }
                if len(self.collectedSet) < self.threshold:
                    yield scrapy.Request(url, callback=self.parse, 
                        headers=self.create_header())
    
    #TODO: this method is supposed to randomly select and return
    #      a pre-defined user-agent.
    def randomly_select_user_agent(Self):
        return 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'    

    def create_header(self):
        return {
            'User-Agent' : self.randomly_select_user_agent()
        }
                