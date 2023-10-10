# Dowell RandomTable Documentation
## Insert Input Data
### URL

#### For Pandas Implementation
```json
http://127.0.0.1:8000/pandas/
```
#### For PySpark Implementation
```json
http://127.0.0.1:8000/spark/
```

### Request
```json
{
    "column": "field1",
    "regex": "^.{3}5",
    "size" : 1
}
```

### Response
```json
{
    "data": [
        {
            "field1": 21254974,
            "field10": 11033937,
            "field2": 22207488, 
            "field3": 54967693,
            "field4": 40902644,
            "field5": 17892489,
            "field6": 77579653,
            "field7": 61235139,
            "field8": 45364891,
            "field9": 93864305,
            "index": 1
        }
    ],
}
```