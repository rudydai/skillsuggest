from bs4 import BeautifulSoup
import json
import urllib

#person based, or adjacency matrix of skills...store this matrix in DB for all to use??
# to make faster, could have entries to adjacency matrix from connections that have at least 1 in common
#or, adjacency matrix with entries on one row as only your skills
#so, more like a coincidence matrix, keys are your skills... add skills of people who have one in common

personal_skill_set = [] #fill this in with your skills, key is another empty dictionary
weightedSkillsDictionary = {}

connections_url_list = []

for url in connections_url_list:
	soup = BeautifulSoup(urllib.urlopen("http://www.linkedin.com/pub/rudy-dai/55/5a2/a57").read())
	skill_list = soup.find_all("a", class_="jellybean")
	for i in range (0, len(skill_list)):
		skill_list[i] = skill_list[i].string.strip()   # getting a cleaned up list of connection's skills

	weight = len(set(skill_list) & set(personal_skill_set)) #number of skills in common

	if weight > 0:
		for element in skill_list:
			if element in skillsDictionary:
				weightedSkillsDictionary[element] += weight
			elif element not in personal_skill_set and element not in skillsDictionary:
				weightedSkillsDictionary[element] = weight

	#print (skill_list)
	#coursera url https://www.coursera.org/course/publicspeak
	#fetch from that JSON page, the names and descriptions.. look for hits and give links to the URL
	#using the shortname attribute
	#add some nice UI (twitter bootstrap)

#psuedocode: go through each connection and get their skills.
#if there's at least one in common with yours then, add all their skills to personal[commonskill]
#add the skill to the inner dictionary, or if already present, increase weight by 1
