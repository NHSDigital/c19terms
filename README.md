# Covid 19 Terms

json covid snomed codes from "COVID-19 Vaccination Codes"
[https://hscic.kahootz.com/connect.ti/t_c_home/view?objectId=16878800](https://hscic.kahootz.com/connect.ti/t_c_home/view?objectId=16878800)

# get latest terms.json


## curl
ensure to use `curl -L` to follow redirects
```bash

curl -sL $(curl -s https://api.github.com/repos/NHSDigital/c19terms/releases/latest \
| jq -r '.assets[] | select(.name="terms.json") | .browser_download_url')
```

## wget
```bash

wget $(curl -s https://api.github.com/repos/NHSDigital/c19terms/releases/latest \
| jq -r '.assets[] | select(.name="terms.json") | .browser_download_url')
```

## python
```python
import requests

terms_asset = next(
    filter(
        (lambda asset: asset['name'] == 'terms.json'), 
        requests.get(url="https://api.github.com/repos/NHSDigital/c19terms/releases/latest").json()['assets']
    )
)

terms = requests.get(url=terms_asset['browser_download_url']).json()


```

# get product terms as a dictionary
## build locally    
```shell
make dist products-as-dict
```

## read from latest release
```shell
curl -sL $(curl -s https://api.github.com/repos/NHSDigital/c19terms/releases/latest \
| jq -r '.assets[] | select(.name="terms.json") | .browser_download_url') \
| jq '[.products | to_entries[] | {key: .key, value: .value.term}] | from_entries'
```