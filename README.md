`Note Mills` is a scrambled version of the phrase "notes of motivationsl pills". To remind oneself about what drive the person to do something rewarding in the first place is the purpose of Note Mills. Mainly, I did this for personal use but should it seems valuable and worth exploring for others, I described below more details for the case of exploiting this repository.

Note Mills propose a `LINE` chat bot that picks a random note you had written on `Evernote` for yourself for you to read at when you need it.
Simply sending a note tag name to the bot will make it do its job. A random note with the specified tag will be delivered.
You can adapt it to your personal needs by categorise your notes using tags.

There's still a number of limitations due to large amount of extra work required by Evernote and LINE platforms to put it out of development mode.
The code is enough for anyone with moderate software development knowledge to make it run for your personal use, but it's still far from a product for general users.
It now only works on development environment. In other words, LINE's unpublished bot and Evernote's sandbox.

#### Setup and Run Locally
- execute `pip install -r requirements.txt`
- Obtain your Evernote's `sandbox access token`
- Obtain your LINE's `user id`, `channel access token`, and `channel secret`
- Set them as environment variable as described in `/self doc/configs_guide.md`
- You should be able to start the server by executing `python start.py` but with my knowledge, I am not sure how to let LINE platform access the webhook endpoint without deployment. So this will just make sure that it is runnable and it won't be functional.

#### Deploy to Heroku
Please see `/self doc/deployment.txt`

#### Reflection along the implementation
- Heroku is simple and convenient to use but actually not a good fit for this project. The only way to expose your code for testing publicly with Heroku (as te 3rd party platform cant find webhook endpoint when I run it locally) is by pushing your source to Heroku's repository. This takes at least a minute each time. Once I found a bug I didn't yet understand which needed a number of experimental trials, it suddenly became a vital bottle neck extending development time from an hour to several (thinking about a guitar with 1 second auditory delay when you strum, how long it would take to learn a song).

#### Some of the knowledge I harnessed along the way
- [Best Practices for Python Virtual Environment and Git Repos](https://libzx.so/main/learning/2016/03/13/best-practice-for-virtualenv-and-git-repos.html)
- [Deploying a Flask application on Heroku](https://medium.com/@gitaumoses4/deploying-a-flask-application-on-heroku-e509e5c76524).
- [Tutorial: LINE Bot With Python and Heroku](https://medium.com/better-programming/line-bot-with-python-and-heroku-tutorial-e8c296f3816f)
