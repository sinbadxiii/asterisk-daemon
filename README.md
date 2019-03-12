<p>
Демон для онлайн статуса пользователей АТС Asterisk
</p>

## Как использовать

<p>

Заполнить конфиг config.example.py

```python
connection = {
    'address': '',
    'port': 5038
}
login = {
    'username': '',
    'secret': ''
}
redisConf = {
    'host': '127.0.0.1',
    'port': 6379
}
```
Переименовать его в config.py
</p>

Запустить демон в фоне

```bash
$ sudo ./start
```