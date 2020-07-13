# PriceAlert
Track prices and receive an alert when it changes

# Configuration
Open the config.ini to change any settings to your liking. If you would like to use the program with mobile or desktop push notifications, enable Pushbullet from the config. You will need to register to Pushbullet and enter the API key for this to work. If looking to use it with mobile push alerts, you can download the Pushbullet app on the App Store or the Play store.

# Adding items to watch for price changes
In order to add items you would like to track to the program, you need to open the links.txt file. Once opened, enter the link of the item you are watching in the following format "link;xpath"

For an example, if you wanted to track a price of a specific Paper Towel product on Amazon, you would take the following steps:

Link for reference: https://www.amazon.com/Pacific-Multifold-Previously-Signature-21000/dp/B004YK2KSM/ref=sr_1_6?dchild=1&keywords=paper+towel&qid=1594678578&sr=8-6

- First, enter the link into the links.txt file and add a semicolon (;) at the end of the link
![Reference photo 1](https://i.imgur.com/zruhUvR.png)
- Right click the price of the item (Ex: $24.18 in this case) and click inspect

![Reference photo 2](https://i.imgur.com/fjRusA2.png)
- Once the list of elements come up on the right, right click the line that is highlighted and copy the xpath of the price
![Reference photo 3](https://i.imgur.com/gDFSLkM.png)
- Append the xpath to the link in the links.txt file. You can repeat the process and add new items to each line of the links.txt file to receive alerts for more than a single item
![Reference photo 4](https://i.imgur.com/XADvxr8.png)
