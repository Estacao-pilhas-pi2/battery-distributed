# battery-distributed

# Instalação

## Dev
```bash
$ poetry install
$ poetry shell
$ python -m battery_distributed
```

## Prod Raspberry
```bash
$ pip install .
# configure the environment file before this
$ sudo ln -s battery_distributed.service /etc/system/systemd/system/
$ sudo systemctl daemon-reload
$ sudo systemctl restart battery_distributed.service
```
