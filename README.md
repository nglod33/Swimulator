# Swimulator
Use the collegeswimming database to simulate a meet between two teams of a given year, using the fastest times of that team in that year

# Scraping
To get the link for the team, use this

```scrapy runspider -a search_name=<team> -a out_file=<output_file> teamCrawler.py```

To get the full roster for the team use this command:

```scrapy runspider -a gender=<gender> -a team_url=<team_url> -a season=<season> -a team_name=<team_name> rosterCrawler.py```

Gender will either be M or F, team URL can be obtained from the team crawler, Team name is the full official name of the team, season is 
the last two digits in the ending year plus 3 (ex, 2021-2022 season is season 25)

# Simulating

To simulate, run this command:

```python3 swimulator.py <team1_racefile>, <team2_racefile>, <gender>```