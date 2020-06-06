
# Network Connection Checker

Checks if the network can connect to the Internet.

## Motivation

My Wi-Fi stops frequently so I wanted to know when I can use it (or not).  
So I diceded to create a progran which checks the connection.

## Requirements

- docker
- docker-compose

## Usage

```console
    docker-compose build
    docker-compose up
```

Change the values in `check_network_connection.py`'s `__main__` to customize.

If you want messages when the network recovered  
create a file `line_token.py` which has a `LINE_TOKEN` variable inside.  
You can register the token from [LINE Notify](https://notify-bot.line.me/ja/) for free if you have an acount.

## Note

I recommend setting the `connection_interval` for a bigger number than 20 or so.  
Your IP might get blocked for continuous and frequent connections.

## Reference

The code for checking the connection is from [a question in stack-overflow](https://stackoverflow.com/questions/3764291/checking-network-connection)

## Author

[Sawada Tomoya](https://github.com/STomoya/)
