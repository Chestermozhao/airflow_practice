<h1 align="center">Airflow practice</h1>

<p align="center">
<a href="https://github.com/psf/black">
<img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

1. Using Python3.6
2. Using black as tool of code pre-commit

```shell
python3 -m venv venv
source venv/bin/activate

# requirements with pip
pip install -r requirements.txt

# install pre-commit
pre-commit install

# set airflow config: need airflow.cfg in this directory
export AIRFLOW_HOME=~/airflow

# default: sqlite, if you wanna change to mysql, plz modify airflow.cfg before execute this command
airflow initdb

# activate webUI and scheduler
airflow webserver -p 8080
airflow scheduler

# if you use CeleryExecutor
airflow worker
```

# Problems you might encounter
1. [Timezone](https://blog.csdn.net/Crazy__Hope/article/details/83688986):
   - Reset timezone in airflow.cfg
   - Maybe you wanna modify timezone in WebUI template
2. [CeleryExecutor configs](https://zhuanlan.zhihu.com/p/42239805)
