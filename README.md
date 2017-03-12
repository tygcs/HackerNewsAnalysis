# SentimentAnalysis


### Team Members

- Yuan Gao
- Yao Tan
- Mingwei Tang
- Xinyue Zheng
- Jingyi Li


### Database

MySQL 5.7.11

fields in local table *comtab*:

- id: comment id
- textcon: comment content
- timems: time in ms
- timesp: timestamp
- author: author of the article
- byw: author of the comment
- parent: parent
- ranking: ranking
- dead: dead
- seti_score: sentiment value in [0, 1]

### Run the project

```
cd ./SentimentAnalysis/SAWeb/
python manage.py runserver
```



