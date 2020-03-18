import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

with open('auth.json') as f:
  data = json.load(f)

authenticator = IAMAuthenticator(data['apikey'])
environmentId = data['environment_id']
collectionId = data['collection_id']
discovery = DiscoveryV1(
    version='2019-04-30',
    authenticator=authenticator
)
discovery.set_service_url(data['url'])
collection = discovery.get_collection(environmentId, collectionId).get_result()
print(collection)
# chunk_size=100
# response = discovery.query(environmentId,
#                            collectionId,
#                            count=chunk_size)
# print(response)