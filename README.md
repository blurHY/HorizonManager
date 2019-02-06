# HorizonPanel 
![](https://img.shields.io/badge/licence-GPL-brightgreen.svg) 
![](https://img.shields.io/badge/Project-Horizon-orange.svg) 
![](https://img.shields.io/badge/Network-ZeroNet-%237722df.svg)

A panel to manage HorizonSpiders and ZeroNet clients.

# Installing

```bash
yarn
yarn build
```

You can also use npm: 

```bash
npm i
npm run build
```

Install dependencies with pipenv:

```bash
pipenv install
```

Requires python >=3.6

## Installation script

For CentOS7:

Download [centos7.sh](./centos7.sh), and `sudo bash centos7.sh`

# Usage

```bash
pipenv run python run.py
```

You can define environment variables to configure the panel.

If you didn't specify a port, you can visit http://127.1:5000 to have a look.

## Nginx

I recommend that you should use nginx as reverse proxy for the panel.

And use https to keep it safe

## Better_exceptions

To enable better_exceptions:

```bash
export BETTER_EXCEPTIONS=1 
```