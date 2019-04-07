> simple program to automate creating user accounts in DHIS

# Input format
We expect a csv file with the format (double quoted strings and comma separated):
```
"first-name",org-unit","username","password"
```

For example:
```
"Ilemela MC","TgDak3kasdf","user1","password1"
"Nyamagana CC","aase84asdfx","user2","pas$w0rd2"
"Sengerema DC","aw3e4skdfjL","user3","P4ssword3"
```

# Quickstart

  1. install deps
      ```bash
      pip install -r requirements.txt
      ```
  1. create your CSV file
  1. run the script and pipe your CSV into stdin
      ```bash
      cat your-file.csv | python main.py \
        --user-role TMK9CMZ2V98 \
        --user-group aGgeJJhuJgU \
        --server https://dev.dhis.local \
        --admin-user admin \
        --admin-pass password
      ```
