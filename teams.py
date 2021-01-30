import json, requests, bs4, time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

# Global Variables
server = "localhost"
league = "2500/"
minimumRating = 10
gradesDict = {"A" : "4", "B" : "3", "C" : "2", "D" : "1", "F" : "0"}
output = open("output.txt", "w")
roster = open("roster.json", "r")
roster = json.load(roster)
wd = webdriver.Firefox()

# Scrapes the data and assigns values then kicks off cleanup
def scrape(pokeList, teamList):
    rating = 0
    gradeList = []
    fullUrl = server + "/team-builder/all/" + league + teamList
    wd.get(fullUrl)
    WebDriverWait(wd, 300).until(EC.visibility_of_element_located((By.CLASS_NAME, "grade")))
    html_page = wd.page_source

    bs = bs4.BeautifulSoup(html_page, 'html.parser')
    grades = bs.select('div.grade')
    threatscore = bs.select('b.threat-score')
    
    for i in range(0, 4):
        grade = grades[i].get_text()
        gradeList.append(grade)
        rategrade = (int(gradesDict[grade]))
        rating += rategrade
    
    gradeList.append(threatscore[0].get_text())
    if rating >= minimumRating:
        cleanup(pokeList, gradeList, rating)

# Writes to console and appends to results
def cleanup(team, gradeList, rating):
    update = (f"Team Rating: {rating}, Threat Score: {gradeList[4]}, {team}, Grades : {gradeList[0]}, {gradeList[1]}, {gradeList[2]}, {gradeList[3]}")
    print(update)
    outputLog.append(update)

# Creates the list of teams and moves
def makeTeams(roster):
    poke = []
    moveList = []    
    teamList = []
    pokeList = []

    for pokemon in roster:
        fast = roster[pokemon]["fast"]
        chargedOne = roster[pokemon]["chargeOne"]
        chargedTwo = roster[pokemon]["chargeTwo"]
        poke.append(pokemon)
        moveList.append(f"{pokemon}-m-{fast}-{chargedOne}-{chargedTwo}")
    
    pokeTwo = poke
    pokeThree = poke
    moveTwo = moveList
    moveThree = moveList

    for pokemon in moveList:
        pokemonOne = pokemon
        
        for pokemon in moveTwo:
            if pokemon != pokemonOne:
                pokemonTwo = pokemon

                for pokemon in moveThree:
                    if((pokemon != pokemonTwo) and (pokemon != pokemonOne)):
                        pokemonThree = pokemon
                        moveList = [pokemonOne, pokemonTwo, pokemonThree]
                        moveList.sort()
                        pokeTeam = f"{moveList[0]}%2C{moveList[1]}%2C{moveList[2]}"
                        
                        if pokeTeam not in teamList:
                            teamList.append(pokeTeam)
                    else:
                        continue
            else:
                continue

    for pokemon in poke:
        pokemonOne = pokemon
        
        for pokemon in pokeTwo:
            if pokemon != pokemonOne:
                pokemonTwo = pokemon

                for pokemon in pokeThree:
                    if((pokemon != pokemonTwo) and (pokemon != pokemonOne)):
                        pokemonThree = pokemon
                        poke = [pokemonOne, pokemonTwo, pokemonThree]
                        poke.sort()
                        pokeTeam = f"{poke[0]}, {poke[1]}, {poke[2]}"

                        if pokeTeam not in pokeList:
                            pokeList.append(pokeTeam)
                    else:
                        continue
            else:
                continue
    return [pokeList, teamList]

# Drives the logic
def main():
    
    make = makeTeams(roster)
    pokeList = make[0]
    teamList = make[1]

    pokeList.sort()
    teamList.sort()
    
    i = 0
    for team in teamList:
        scrape(pokeList[i], team)
        i += 1
    
    outputLog.sort(reverse=True)

    for log in outputLog:
        output.write(log)
        output.write('\n')

    wd.quit()

outputLog = []
main()