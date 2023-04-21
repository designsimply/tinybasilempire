#rm -rf .venv/lib/python3.9/site-packages/psycopg2
pip uninstall psycopg2
pip install psycopg2
python3.9 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
source .secrets
flask run --cert="cert.pem" --key="priv_key.pem"