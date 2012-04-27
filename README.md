STATUS:

Authentication w/ OAuth is working. Basic project architecture is in place.

Just trying to hammer it out to work with the actual API, now.

TODO:

google docs api for listings.


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


