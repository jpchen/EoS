========================
EoS: Education. Realtime.
=========================
http://eosplus.herokuapp.com/

EoS is a educational video platform that allows professors and TAs to post videos of lectures, office hours, review sessions, and allows students to view course materials and easily collaborate through an integrated discussion system. EoS uses the [Ziggeo API] (http://ziggeo.com) to create a hybrid of a Piazza-like discussion environment and a video sharing platform.  Professors can easily manage their content, and students can easily navigate between classes they are enrolled in. With the advent of online education such as Coursera and edX, we believe that video engagement is the next step towards making education globally accessible.

#Development
Deployment: 

source venv/bin/activate

pip install Flask gunicorn

virtualenv --no-site-packages venv

git push heroku master

