# Zoekmachines Final Assignment
- Barry Servaas
- Buck Boon
- Mèir Noordermeer


## Setup
#### Run an ElasticSearch instance
Either run your own instance or start one using docker:
run `docker-compose up` in the root of this project. 
Press `ctl+c` to exit, or run `docker-compose down`.

#### Put your Elastic config in config.json, example:
``` json
{
	"host": "127.0.0.1",
	"port": "9200",
	"username": "elastic",
	"password": "changeme"
}
```

#### Setup data
- Make sure goeievraag .csv files are in `<root>/data`
- Run `load_data.py` to start loading data to elasticsearch

#### Start webserver
To start the webserver run either `run.bat` on Windows, or `run.sh` on Linux

#### Github Page
Please read our github page at https://github.com/MeirBon/Zoekmachines_Final and our github wiki at https://github.com/MeirBon/Zoekmachines_Final/wiki