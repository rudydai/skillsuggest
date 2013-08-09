from bs4 import BeautifulSoup
import json
import urllib

#person based, or adjacency matrix of skills...store this matrix in DB for all to use??
# to make faster, could have entries to adjacency matrix from connections that have at least 1 in common
#or, adjacency matrix with entries on one row as only your skills
#so, more like a coincidence matrix, keys are your skills... add skills of people who have one in common

def get_url_list(xml):
    soup = BeautifulSoup(xml)
    person_list = soup.find_all("public-profile-url")
    url_list = []
    for person in person_list:
        if person.text != "":
            url_list.append(person.text)
    return url_list

def get_personal_skills(xml):
    soup = BeautifulSoup(xml)
    skill_list = soup.find_all("name")
    names = [skill.text for skill in skill_list]
    return names

def find_best_skills(connections_url_list,personal_skill_set):
    weighted_skills_dictionary = {}
    for url in connections_url_list[:10]:
        print "accessing url {0}".format(url)
        soup = BeautifulSoup(urllib.urlopen(url).read())
        skill_list = soup.find_all("li", class_="competency show-bean ")
        for i in range (0, len(skill_list)):
            skill_list[i] = skill_list[i].text.strip()   # getting a cleaned up list of connection's skills
        weight = len(set(skill_list) & set(personal_skill_set)) #number of skills in common
        if weight > 0:
            for element in skill_list:
                if element in weighted_skills_dictionary:
                    weighted_skills_dictionary[element] += weight
                elif element not in personal_skill_set and element not in weighted_skills_dictionary:
                    weighted_skills_dictionary[element] = weight
    return weighted_skills_dictionary
	#print (skill_list)
	#coursera url https://www.coursera.org/course/publicspeak
	#fetch from that JSON page, the names and descriptions.. look for hits and give links to the URL
	#using the shortname attribute
	#add some nice UI (twitter bootstrap)

#psuedocode: go through each connection and get their skills.
#if there's at least one in common with yours then, add all their skills to personal[commonskill]
#add the skill to the inner dictionary, or if already present, increase weight by 1
