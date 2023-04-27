
## Как собрать?

```
docker-compose up
```
## Как сделать запрос?

### Если нужен конкретный формат сериализации (поддерживаются все из условия)
```
echo -n '{"type": "get_result", "format" : "NATIVE"}' | nc -u -w1 0.0.0.0 2000

echo -n '{"type": "get_result", "format" : "GOOGLE_BUFFER"}' | nc -u -w1 0.0.0.0 2000

echo -n '{"type": "get_result", "format" : "APACHE"}' | nc -u -w1 0.0.0.0 2000

echo -n '{"type": "get_result", "format" : "YAML"}' | nc -u -w1 0.0.0.0 2000

echo -n '{"type": "get_result", "format" : "MESSAGEPACK"}' | nc -u -w1 0.0.0.0 2000

echo -n '{"type": "get_result", "format" : "XML"}' | nc -u -w1 0.0.0.0 2000

echo -n '{"type": "get_result", "format" : "JSON"}' | nc -u -w1 0.0.0.0 2000

```

### Если нужны все форматы сериализации
```
echo -n '{"type": "get_result_all"}' | nc -u -w1 0.0.0.0 2000
```