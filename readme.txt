A python/django web-application project done for a recruitment process. Scrapes XHTML-data that updates every few seconds from a url, converts the data and uses functions
to calculate new data that is stored to a database. Then outputs the wanted data to a table that updates every few seconds. The main idea was that there is a birds nest 
in the origo and the XHTML-data presents fly-data from different drones. The goal was to scrape the fly-data, connect it to a user that the drone is registered to in 
case the drone is closer than 100 metres to the nest and then output the info of the owners that has been too close to the nest. Lastly the drones/users should be deleted
from the database after 10 minutes has gone. 
