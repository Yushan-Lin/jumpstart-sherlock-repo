import json
from datetime import datetime

from dateutil.relativedelta import relativedelta
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import csv

#address = [country,state,city]
def getScore(name, age, address):
    with open('auth.json') as f:
      data = json.load(f)

    authenticator = IAMAuthenticator(data['apikey'])
    environmentId = data['environment_id']
    collectionId = data['collection_id']
    discovery = DiscoveryV1(
        version='2019-04-30',
        authenticator=authenticator
    )
    country,state,city = address[0],address[1],address[2]
    discovery.set_service_url(data['url'])

    filter = '(enriched_text.entities.type::"Person",enriched_text.keywords.text:"'+name+'"),' + \
            '(cps_enriched_text.entities.type::Age,cps_enriched_text.entities.text::"'+str(age)+'"),' +\
            '(cps_enriched_text.entities.type:Location,cps_enriched_text.entities.text:"' + country + '"),' +\
            '(cps_enriched_text.entities.type:Location,cps_enriched_text.entities.text:"' + state + '")'
            # '(cps_enriched_text.entities.type:Location,cps_enriched_text.entities.text:"' + city + '")'
    filter = '(enriched_text.entities.type::"Person",enriched_text.keywords.text::"'+name+'"),' + \
            '(cps_enriched_text.entities.type::Age),' + \
            '(cps_enriched_text.entities.type::Location)'
    csvWriter = csv.writer(open('results.csv', 'a+'))
    #labels

    chunksize=100
    csvWriter.writerow(['docID','Name','Location/address','Age','Name Match', 'Age Match', 'Location Match', 'Relevancy'])

    response = discovery.query(environmentId,collectionId,
                               filter=filter)
    #query through respons and get outputwriter = csv.writer(open('output.csv', 'a+'))
    currentdate = datetime.now()
    # print(response)
    for article in response.result['results']:
        score = 0 # relevancy
        name_found = 0
        age_found = 0
        addr_found = 0
        #check age
        #2018-02-01T07:55:00.000+02:00
        start_date = datetime.strptime(article['published'][:-10], '%Y-%m-%dT%H:%M:%S')
        difference_in_years = relativedelta(currentdate, start_date).years
        article_age = age - difference_in_years
        # print(article_age)
        for entity in article['cps_enriched_text']['entities']:
            if entity['type'] == "Person" and entity['text'].lower() == name.lower(): #found name
                name_found = 1
            elif entity['type'] == "Location" and (entity['text'].lower() == state.lower() or entity['text'].lower() == city.lower()):
                addr_found = 1
            #check date of article
            elif entity['type']== "Age" and str(article_age) in entity['text']:
                age_found = 1
            score = name_found and age_found and addr_found

        csvWriter.writerow([article['id'], name, state + ',' + city, age, name_found, age_found, addr_found, score])


address = ['U.S.','Michigan','Holt']
getScore('Larry Nassar',56,address)