import scrapy
import json
import re


class RosterCrawler(scrapy.Spider):
    name = "roster"
    # Event numbers correspond to swimswam event designations

    def __init__(self, gender, team_url, season, team_name, **kwargs):
        super().__init__(**kwargs)
        self.gender = gender
        self.team_url = team_url
        self.swimmer_times = {}
        self.season = season
        self.team_name = team_name
        self.event_list = [150, 1100, 1200, 1500, 11000, 2100, 2200, 3100, 3200, 4100, 4200, 5200, 5400]
        self.file = open('teamFiles/' + team_name.replace(" ", "_") + "_" + str(season) + '_races.jl', 'w')
        for event in self.event_list:
            self.start_urls.append(f'{self.team_url}/times/?gender={self.gender}&event={event}&season={self.season}')

    def parse(self, response):
        event = re.search(r"\d+", re.search(r"&event=\d+&", response.url).group()).group()
        swimmers = response.css('tbody').css('tr')
        for swimmer in swimmers:
            line_dict = {'name': swimmer.css('td.u-text-semi').css('a::text').get(),
                         'time': swimmer.css('td.u-text-end').css('a::text').get(),
                         'season': self.season,
                         'team': self.team_name,
                         'event': event,
                         'gender': self.gender
                        }
            self.file.write(json.dumps(line_dict) + '\n')
        if event == "7400":
            self.file.close()
                

