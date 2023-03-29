#!/bin/bash
python3 -c "import string; import secrets; print(''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(12)))"
