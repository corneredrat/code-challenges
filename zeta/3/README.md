# autocomplete

## Setup

#### prerequisites
- need docker installed in the system.

### building docker image
```
sudo docker build . -t autocomplete:v1
```

### running docker container
```
sudo docker run -itd -p 5000:5000 --name autocomplete autocomplete:v1
```

## Test api 

### add words
```
curl -X POST localhost:5000/add_word/word=foo
curl -X POST localhost:5000/add_word/word=example
curl -X POST localhost:5000/add_word/word=foobar
curl -X POST localhost:5000/add_word/word=exam
```
### check autocomplete feature
```
curl localhost:5000/autocomplete/query=fo
```

### clean up 
```
sudo docker rm -f autocomplete
```