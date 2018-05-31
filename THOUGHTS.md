1. How would your design change if the data was not static (i.e updated frequently
during the day)?
If the csv files were to change during the day I will implement a lock mechanism to update the values every time the csv was updated. Depending on the frequency of the changes and If if will only change some values of most of them, I will load the files and recreate the data each time or just the updated records.

2. Do you think your design can handle 1000 concurrent requests per second? If not, what
would you change?
No, I don't it can handel 1000 concurrent requests per second. I would try to use more than one process for flask. To improve the result I would try to denormalize even more the data estructure to remove transformation steps to accommodate the data to the format needed from start. It would cost more RAM but will increase de response time.  You could also cache the response in order to answers whenever possible from cache specially if the information is static.
