# photobox
A web server that shows the latest photo of your camera
![Photobox setup](https://cdn.jsdelivr.net/gh/mathebox/photobox@1487b7b36c260cc7266e4b63f9e91b69d8030d31/app/static/img/setup.svg)

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


