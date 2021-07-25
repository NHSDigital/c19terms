# Covid 19 Terms

json covid snomed codes from "COVID-19 Vaccination Codes"
[https://hscic.kahootz.com/connect.ti/t_c_home/view?objectId=16878800](https://hscic.kahootz.com/connect.ti/t_c_home/view?objectId=16878800)

# get latest terms.json


## curl
ensure to use `curl -L` to follow redirects
```bash

curl -sL "https://github.com/NHSDigital/c19terms/releases/download/$(curl -sL -H 'accept: application/json' https://github.com/NHSDigital/c19terms/releases/latest | jq -r '.tag_name')/terms.json"
```

## wget
```bash

wget "https://github.com/NHSDigital/c19terms/releases/download/$(curl -sL -H 'accept: application/json' https://github.com/NHSDigital/c19terms/releases/latest | jq -r '.tag_name')/terms.json"
```

## python
```python
import requests

repo_uri = "https://github.com/NHSDigital/c19terms"
latest_tag =  (
    requests.get(
        url=f"{repo_uri}/releases/latest", 
        headers={"accept": "application/json"}
    )
    .json()
    ['tag_name']
)

terms = (
    requests.get(
        url=f"{repo_uri}/releases/download/{latest_tag}/terms.json"
    )
    .json()
)

```

