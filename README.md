# Autocomplete
If you have used Google, eBay, Bing or any major commercial search engine, then its likely that you have used autocomplete functionality. Autocomplete is a powerful feature which offers suggestions for query completion as user types his/her query. It enhances user experience and is especially useful while using mobile devices as it is not easy to type on mobile.

In this lab we will build autocomplete feature by applying what we have learned today about language models. We are going to use completion suggester
in elastic search for building this feature. We will also use KenLM as the language model library for this project. 

## Instructions
* Install Elastic Search
* Install Docker
  run `docker run -it utkarshp/kenlm`
  KenLM is already installed in this image
* Download `norvig.com/big.txt`. This is also present in docker image.
  We will train our language model on this. This is also present in docker image.
* Download http://boston.lti.cs.cmu.edu/Data/web08-bst/AOLQs.txt. We will use these queries to index for suggestions
* Add plugin **Sense** to Chrome

Goal of this exercise is to index some queries and give them some score. Indexed queries will be retrieved for auto-correct based on this score. In this lab we want to score these queries with a language model. To do that, run the docker image in an interactive mode as shown in step (1) of instructions. In `/home/data`, I have downloaded some AOL queries in `AOLQ.txt`. We would score these queries but we first need to train a language model. For that, in `/home/data` there is `big.txt` that we will use to train LM. You can train the LM using the following command.

```sh
bin/lmplz -o 5 < ../data/big.txt > ../data/big.arpa
```

Once, LM is trained we would convert the arpa file into a binary as it makes querying the LM faster. This can be done by following command.

```sh
bin/build_binary text.arpa text.binary
```

Once, binary is obtained, we are ready to query this LM. This can be done using the following command. Please using the options to query accordingly as we need scores at query (sentence level).

```sh
bin/query -s 1 ../data/big.binary < ../data/AOLqueries.txt > result.txt
```

However, as we saw in the lab we dont necessarily need a LM to score queries. We can score these queries in any way we see fir. We can even just use the query counts (third column in the AOL data) as scores.

### Indexing

Once queries and their respective scores are obtained. We can index them. Indexing has two steps. First is creating a mapping after stating elasticsearch engine. Mapping is a way of letting elasticsearch know about the format of our document. This can be done using sense plugin of chrome. We can do the following in the sense.

```sh
PUT /queries
{
  "mappings": {
    "query" : {
      "properties" : {
        "name" : { "type" : "string" },
        "name_suggest" : {
          "type" :     "completion"
        }
      } 
    }
  }
}
```

if successful, you'll see the following in the output panel

```sh
{
   "acknowledged": true,
   "shards_acknowledged": true
}
```

This is elasticsearch's way of acknowledging the meta data information about the structure of our documents. 

Here, queries is the name of our index. query is type and we have two fields in our document namely "name" and "name_suggest". We will use the `_suggest` end point of elasticsearch and it will use the name_suggest field for offering suggestions. More details about this can be found [here.](https://www.elastic.co/blog/you-complete-me)

Next we can index few queries in sense to get a better understanding. Do the following  

```sh
PUT queries/query/1
{
  "name" :         "hello kitty",
  "name_suggest" : { 
    "input" :  "hello kitty",
    "weight":      50
  }
}
```
```sh
PUT queries/query/2
{
  "name" :         "hello kitty bag",
  "name_suggest" : { 
    "input" :  "hello kitty bag",
    "weight":      60
  }
}
```

If successful, you'd see something like this in the output panel of sense

```sh
{
   "_index": "queries",
   "_type": "query",
   "_id": "2",
   "_version": 1,
   "result": "created",
   "_shards": {
      "total": 2,
      "successful": 1,
      "failed": 0
   },
   "created": true
}
```

Now we can use the `_suggest` end point to see some results; do the following
```sh
POST /queries/_suggest
{
  "countries" : {
    "prefix" : "h",
    "completion" : {
      "field" : "name_suggest"
    }
  }
}
```

and you'd see something like the following

```sh
{
   "_shards": {
      "total": 5,
      "successful": 5,
      "failed": 0
   },
   "countries": [
      {
         "text": "h",
         "offset": 0,
         "length": 1,
         "options": [
            {
               "text": "hello kitty bag",
               "_index": "queries",
               "_type": "query",
               "_id": "2",
               "_score": 60,
               "_source": {
                  "name": "hello kitty bag",
                  "name_suggest": {
                     "input": "hello kitty bag",
                     "weight": 60
                  }
               }
            },
            {
               "text": "hello kitty",
               "_index": "queries",
               "_type": "query",
               "_id": "1",
               "_score": 50,
               "_source": {
                  "name": "hello kitty",
                  "name_suggest": {
                     "input": "hello kitty",
                     "weight": 50
                  }
               }
            },
            {
               "text": "hello kitty shoes",
               "_index": "queries",
               "_type": "query",
               "_id": "3",
               "_score": 10,
               "_source": {
                  "name": "hello kitty shoes",
                  "name_suggest": {
                     "input": "hello kitty shoes",
                     "weight": 10
                  }
               }
            }
         ]
      }
   ]
}
```

Now, we need to index queries in bulk, for that we have to first create a json file with all the queries and weights as json objects. Please refer to `data/aol.json` to see what this will look like.
Once, this file is in place, run the following

```sh
curl -XPOST 'localhost:9200/bank/queries/_bulk?pretty&refresh' --data-binary "@aol.json"
```

Now, that all the queries are indexed, all we need to do is to post request to elasticsearch and process the json response. Code for doing this is provided in server.py.

Demo here is the most basic version of auto-correct and requires a lot more functionality to be complete. However, such bells and whistles can be added on top of this once we understand how to use elasticsearch. 
This is a small example of how powerful and useful elasticserach is. We can explore other features of elasticserach as well to build such cool features.    

