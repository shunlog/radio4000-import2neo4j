A python script that import data from [radio4000-api-node-firebase](https://github.com/internet4000/radio4000-api-node-firebase) to neo4j according to the models defined in models.py

## Usage

Export the credentials to neo4j:

``` sh
export NEO4J_USERNAME="neo4j"
export NEO4J_PASSWORD="password"
export NEO4J_BOLT_URL="bolt://${NEO4J_USERNAME}:${NEO4J_PASSWORD}@localhost:7687"
```

Run the script:

``` sh
python3 import.py
```
