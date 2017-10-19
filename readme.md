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