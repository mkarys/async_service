# Async Service
Created for Async challenge. It uses python asyncio.

It can work is async or sync way depending on `ASYNC` environmental variable

It creates images containing word cloud with synonyms and antonyms for every single word in given keyword


## How to get started

1. `cp docker/backend.env.example docker/backend.env`
2. Set `ASYNC` env to `true` or `false`
3. `docker-compose build`
4. `docker-compose up`
5. Service should be running on `http://localhost:8007`


## API

### /api/
* Method: POST
* Request body: [<string>, ...] (JSON array of strings)

it takes list of keywords and creates image for each one

example:

```
curl -X POST \
  http://localhost:8007/api/ \
  -H 'Content-Type: application/json' \
  -d '["bangkok", "miami vice", "mobbed by raccoons", "light it up", "rewind", "dumb ways to die", "Winnie the Pooh", "You talk the talk do you walk the walk", "banana split", "pseudopseudohypoparathyroidism", "how to make sushi", "come clean", "what does idk mean", "is this the reebok or the nike", "limitless", "it works on my machine", "beyond imagination", "tea time"]'
```

Response:
```
[
    {
        "keyword": "bangkok",
        "image": "http://localhost:8007/static/images/1610298025_XL5aqCjXWwu1rZBd.jpeg"
    },
    {
        "keyword": "miami vice",
        "image": "http://localhost:8007/static/images/1610298026_Wudu3BrWEyUgbM1f.jpeg"
    },
    ...
]
```