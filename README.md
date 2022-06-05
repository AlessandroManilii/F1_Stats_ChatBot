# F1_Stats_ChatBot
Chatbot implemented through RASA framework on F1 statistics and generic info about races, pilots, circuits from 1950 season up to now.

Data retrival is made through 2 API:
 - Fast-F1: 
   - *pip install fastf1*
   - more info and code at:
      - https://github.com/theOehrly/Fast-F1 
      - https://theoehrly.github.io/Fast-F1/examples/index.html
 - Ergast:
   - more info at: http://ergast.com/mrd/
 
External library used:
- Request cache: *pip install requests-cache*
- Flask: *pip install flask*
  - run server through *python app.py*
- Spacy Model:
  - *pip install -U pip setuptools wheel*
  - *pip install -U spacy*
  - python -m spacy download en_core_web_md
