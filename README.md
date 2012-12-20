# pymailer.py

A simple python tls smtp command line mailer script that does what I need.

### Setup:

1. create settings.py file.
2. pipe plain text body content to pymailer.py, e.g. 
```
$ echo "e-mail body" | pymailer.py -s subject -t to@example.com -f to@example.com
```

### pymailer.py flags
```
usage: pymailer.py [-h] -s SUBJECT -t TO_ADDR -f FROM_ADDR [-v VERBOSITY]
```

