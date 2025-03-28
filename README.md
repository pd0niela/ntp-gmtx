# Client NTP

Această aplicație permite obținerea orei exacte de la servere NTP și convertirea ei în diferite fusuri orare.

Instalare dependințe:
```
pip install ntplib pytz tzlocal
```

## Utilizare

### Obținerea orei locale

```
python ntp_client.py
```

### Specificarea unui server NTP

```
python ntp_client.py --server ntp.example.com
```

### Obținerea orei pentru un anumit fus orar

```
python ntp_client.py --timezone GMT+2
python ntp_client.py -t GMT-5
```

## Opțiuni disponibile

- `--server`, `-s`: Specifică serverul NTP de utilizat (implicit: pool.ntp.org)
- `--timezone`, `-t`: Specifică fusul orar în format GMT+X sau GMT-X (unde X este între 0 și 11)
