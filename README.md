# photobox
A web server that shows the latest photo of your camera
![Photobox setup](https://cdn.rawgit.com/mathebox/photobox/master/app/static/img/setup.svg)

## Requirements
- **imagesnap** (via homebrew) for using the isight camera of your MacBook
- **gphoto2** (via homebrew) for controlling your DLSR camera
- **epeg** (via [source](https://github.com/mattes/epeg)) for scaling your photos

## How to install
```
pip install -r requirements.txt
bower install
```

## How to start
```
python run.py
```

## How to use
- localhost:5000/ -> shows latest photo and photo count
- localhost:5000/button -> shows additional trigger button


