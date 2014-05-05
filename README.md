Flask Image Resizer
===================

Resizes images on-the-fly and caches them in redis for a variable amount
of seconds.


### Requirements (outside `requirements.txt`):

* redis
* libjpeg-dev (for PIL/Pillow)


###  Optional requirements (You may switch these out with whatever you want):

* uWSGI
* nginx


### Installation:

1. Make a new virtualenv and install the requirements
2. `pip install -r requirements.txt`
3. Edit the configuration in `config/config.py` to suit your needs
4. Run the app with `python app.py`/`python app.py dev` for dev-mode
	or use the uWSGI and nginx configuration files provided in the repo


### Usage:

It's quite simple really.
(URL's are from running locally in dev mode)

Possible arguments:

* Input file: `src` or `file`
* Value for width: `w` or `width`
* Value for height: `h` or `height`

Resize an image to desired size:

	GET
	http://0.0.0.0:5000/v1/resizer/?src=http://link.to/image.jpg&w=400&h=220

Resize an image keeping a fixed height (providing `0` in either `w` or `h`
	will resize it with that fixed size):

	GET
	http://0.0.0.0:5000/v1/resizer/?src=http://link.to/image.jpg&w=0&h=220
