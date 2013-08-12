from bs4 import BeautifulSoup
import json
import urllib

coursera_courses_json = json.loads(urllib.urlopen("https://www.coursera.org/maestro/api/topic/list?full=1").read())
coursera_class_base_url = "https://www.coursera.org/course/"

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
    for url in connections_url_list:#[:10]:
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
#psuedocode: go through each connection and get their skills.
#if there's at least one in common with yours then, add all their skills to personal[commonskill]
#add the skill to the inner dictionary, or if already present, increase weight by 1

def find_related_courses(skills_list):
    related_courses_list = []
    for skill in skills_list:
        if len(skill) <= 3:
            skill = " " + skill + " "
        for course in coursera_courses_json:
            if skill in course["name"] or skill in course["category-ids"] or skill in course["courses"][0]["certificate_description"]:
                if coursera_class_base_url + course["short_name"] not in related_courses_list:
                   related_courses_list.append(coursera_class_base_url + course["short_name"])
               # break
            for category in course["categories"]:
                if skill in category["name"]:
                    if coursera_class_base_url + course["short_name"] not in related_courses_list:
                        related_courses_list.append(coursera_class_base_url + course["short_name"])
                    #break
    return related_courses_list

#test script
#skills = ['neuroscience']
#skills2= ['machine learning', 'algorithms', 'databases', 'git', 'C', 'economics', #'neuroscience']
#p = find_related_courses(skills)
#for thing in p:
#   print thing
#print len(p)
