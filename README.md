PURPOSE:
--------------------------------------------------------------------------------
Simple and quick Python Utility to parse and print JSON data from FILE, URL or STDIN

USAGE:
--------------------------------------------------------------------------------
$ json-parser.py -h
[json-parser, v0.13] /home/plsak/bin/json-parser.py [-h|-v] <-f FILE|-u URL|-s (read STDIN)> [KEY1] [KEY2] ...

OPTIONS:
--------------------------------------------------------------------------------

	-h			Print Help
	-v			Verbose mode

	-f FILE		Use FILE as source of JSON data
	-u URL		Use URL as source of JSON data
	-s STDIN	Use STDIN as source of JSON data

	KEYX		Don't print whole JSON doc but only content of KEY1->KEY2->KEY3->... (going into unlimited depth)

EXAMPLES:
--------------------------------------------------------------------------------

$ cat example-chef-node.json
{
  "name": "example-node.com",
  "chef_environment": "eu-prod-env",
  "run_list": [
        "role[linux_client]",
        "recipe[pd-chef-vault]",
        "recipe[pd-example-role]"
]
,
  "normal": {
    "tags": [

    ]
  }
}

----------------------------------------
FILE:
----------------------------------------
$ json-parser.py -f example-chef-node.json
{
    "chef_environment": "eu-prod-env",
    "name": "example-node.com",
    "normal": {
        "tags": []
    },
    "run_list": [
        "role[linux_client]",
        "recipe[pd-chef-vault]",
        "recipe[pd-example-role]"
    ]
}

--------------------
$ json-parser.py -f example-chef-node.json name
"example-node.com"

--------------------
$ json-parser.py -f example-chef-node.json run_list
[
    "role[linux_client]",
    "recipe[pd-chef-vault]",
    "recipe[pd-example-role]"
]

--------------------
$ json-parser.py -f example-chef-node.json run_list 0
"role[linux_client]"

----------------------------------------
URL:
----------------------------------------
$ json-parser.py -u http://localhost/example-chef-node.json
{
    "chef_environment": "eu-prod-env",
    "name": "example-node.com",
    "normal": {
        "tags": []
    },
    "run_list": [
        "role[linux_client]",
        "recipe[pd-chef-vault]",
        "recipe[pd-example-role]"
    ]
}

--------------------
$ json-parser.py -u http://localhost/example-chef-node.json name
"example-node.com"

--------------------
$ json-parser.py -u http://localhost/example-chef-node.json run_list
[
    "role[linux_client]",
    "recipe[pd-chef-vault]",
    "recipe[pd-example-role]"
]

--------------------
$ json-parser.py -u http://localhost/example-chef-node.json run_list 1
"recipe[pd-chef-vault]"

----------------------------------------
STDIN:
----------------------------------------
$ cat example-chef-node.json | json-parser.py -s
{
    "chef_environment": "eu-prod-env",
    "name": "example-node.com",
    "normal": {
        "tags": []
    },
    "run_list": [
        "role[linux_client]",
        "recipe[pd-chef-vault]",
        "recipe[pd-example-role]"
    ]
}

--------------------
$ cat example-chef-node.json | json-parser.py -s chef_environment
"eu-prod-env"

--------------------
$ cat example-chef-node.json | json-parser.py -s run_list
[
    "role[linux_client]",
    "recipe[pd-chef-vault]",
    "recipe[pd-example-role]"
]

--------------------
$ cat example-chef-node.json | json-parser.py -s run_list 2
"recipe[pd-example-role]"
