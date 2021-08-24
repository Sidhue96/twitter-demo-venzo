# Venzo assignment
## _Requirements_
User sign in with twitter
Application fetches users Twitter timeline and save it to the database
UI will display the tweets in chronological order from DB
Sort & filter based on the date on DB
Ability to search tweets on DB
Tweets are synced periodically to the database on an interval(crontab is fine)
If you can not do frontend, You can simply showcase the app with APIs.
Bonus points for end-to-end implementation:
- Deployed on any cloud services gcp/aws
- Test case validation
- Documentation

Preferred choice of tech (but not mandatory one): Docker + Python3 + Flask + sql alchemy.

## Installation
You need to install docker to run this demo
After you've installed docker:
- You need to rename the .environment file to .env
- In that file you need to add your twitter developer API key and API secret

Run

```sh
docker network create twitternet
docker-compose up -d --build
```
Make sure you don't have anything running on your port 80

## Features

### User sign in with twitter
(*Implemented*) It will prompt a login UI when you load it for the first time
### Application fetches users Twitter timeline and save it to the database
(*Implemented*) After successful signin, it will redirect to home page, fetch the latest timeline and add it to DataBase
### UI will display the tweets in chronological order from DB & ability to sort
> Note: `to view the results in table format add the key view=table in your url_params` (Ex: http://127.0.0.1/?sort=desc&view=table)

(*Implemented*) Since by default the tweets are fetched in chronological order, it will always return the results in chronological order
To sort the tweets in descending order:
http://127.0.0.1/?sort=desc
setting sort=_any other value_ will always sort the tweets in ascending order
### Filter based on the date on DB
> Note: `to view the results in table format add the key view=table in your url_params` (Ex: http://127.0.0.1/?start=2019-07-24&end=2021-01-01&view=table)

(*Implemented*) use key start=yyyy-mm-dd hh:mm:ss to filter based on start date
use key end=yyyy-mm-dd hh:mm:ss to filter based on end date
you can use either or both
### Ability to search tweets on DB
> Note: `to view the results in table format add the key view=table in your url_params` (Ex: http://127.0.0.1/search?query=friend&view=table)

(*Implemented*) use route /search and key query={search_key} to search db for given text
### Tweets are synced periodically to the database on an interval(crontab is fine)
(*Not Implemented*) However, you can fetch the latest tweets by reaching /sync-tweets (http://127.0.0.1/sync-tweets)
- it will automatically fetch the latest tweet after the last inserted tweet from twitter api

### If you can not do frontend, You can simply showcase the app with APIs.
APIs are done and table view is for frontend
Its not deployed in any cloud service

Used tech: Docker + Python3 + Flask + pymongo
