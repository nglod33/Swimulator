import scrapy


#Crawls through the list of teams until it finds a matching one, then returns the url
class TeamCrawler(scrapy.Spider):
    name = "team"

    def __init__(self, search_name, **kwargs):
        super().__init__(**kwargs)
        self.search_name = search_name

    start_urls = ["https://www.swimcloud.com/team/?page=1"]

    def parse(self, response) -> str:
        print(response)
        teams = response.css('div.top-box')
        for team in teams:
            team_url = 'https://www.swimcloud.com' + team.css('a').xpath('@href').get()
            team_name = team.css('img').xpath('@alt').get()
            if team_name == self.search_name:
                return {"team_url": team_url}
        pagination = response.css('a.c-pagination__action').xpath('@href')
        next_url = 'https://www.swimcloud.com/team' + pagination[len(pagination) - 1].get()
        if next_url != response.url:
            return response.follow(next_url, callback=self.parse)
