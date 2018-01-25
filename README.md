# threeyourmind-challenge

### Install
```
pip install -r requirements.txt
```

### Run
```
python manage.py runserver
```

### Endpoint (/printers/) - (GET; POST; PUT; PATCH; DELETE)
```
http://127.0.0.1:8000/printers/
```

### POST Payload Example
```
{
	"name": "Printer A",
	"productionTime": {"minimum": 10, "maximum": 15}
}
```
