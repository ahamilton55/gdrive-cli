STATUS:

* Authentication w/ OAuth is working. It opens your browser.
* Basic project architecture is in place.
* Insert file is working!
* Show is working!

TODO:

* local sqlite database to keep track of inserted files

To use this project, you will need to be signed up for the Google Chrome Web 
Store and for the Google Drive SDK and API. At the worst, this means you
will have to sacrifice a few minutes of your time and pay google five
dollars. At the best, you've already done this, and you're ready to dive
in!

Authentication happens locally, through your browser! Launch it from the command line
with gdrive --authenticate and it will persist your credentials so that you can
issue other commands. Just remember to click the dialog in your browser.

See https://developers.google.com/drive/ --- lots of attention is required here.

Command line interface to Google Drive

Dependencies:

sudo pip install google-api-python-client
sudo pip install httplib2


