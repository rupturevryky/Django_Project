python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# tests
python -m pytest tests/ -v

# Start App
flask run