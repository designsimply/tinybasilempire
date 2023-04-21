rm -rf .venv/lib/python3.9/site-packages/psycopg2
# cp -pr .venv/lib/python3.9/site-packages/psycopg2-linux .venv/lib/python3.9/site-packages/psycopg2
svn export https://github.com/jkehler/awslambda-psycopg2/trunk/psycopg2-3.9 .venv/lib/python3.9/site-packages/psycopg2
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
zappa update