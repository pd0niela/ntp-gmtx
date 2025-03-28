import ntplib
import time
import datetime
import argparse
import re
import pytz
from tzlocal import get_localzone

class NTPClient:
    def __init__(self, server='pool.ntp.org'):
        """Inițializează clientul NTP cu un server."""
        self.server = server
        self.client = ntplib.NTPClient()
    
    def get_ntp_time(self):
        """Obține ora UTC curentă de la serverul NTP."""
        try:
            response = self.client.request(self.server, version=3)
            return response.tx_time
        except Exception as e:
            print(f"Eroare la obținerea orei de la serverul NTP: {e}")
            return None
    
    def get_local_time(self):
        """Obține ora locală curentă folosind NTP."""
        ntp_time = self.get_ntp_time()
        if ntp_time:
            # Convertește ora NTP (UTC) la fusul orar local
            utc_time = datetime.datetime.utcfromtimestamp(ntp_time)
            local_tz = get_localzone()
            local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
            return local_time
        return None
    
    def get_time_for_timezone(self, timezone_str):
        """
        Obține ora pentru un fus orar specificat în format GMT+X sau GMT-X.
        Args:
            timezone_str: String în format "GMT+X" sau "GMT-X" unde X este un număr între 0 și 11
        Returns:
            Obiect datetime reprezentând ora curentă în fusul orar specificat
        """
        # Parsarea șirului de fus orar
        match = re.match(r'^GMT([+-])(\d+)$', timezone_str)
        if not match:
            raise ValueError("Fusul orar trebuie să fie în format GMT+X sau GMT-X unde X este între 0 și 11")
        
        sign, hours = match.groups()
        hours = int(hours)
        if hours < 0 or hours > 11:
            raise ValueError("Diferența de ore trebuie să fie între 0 și 11")
        
        # Determinarea decalajului fusului orar
        if sign == '+':
            zone_name = f"Etc/GMT-{hours}"  # Semn opus pentru Etc/GMT
        else:
            zone_name = f"Etc/GMT+{hours}"  # Semn opus pentru Etc/GMT
        
        # Obține ora NTP (UTC)
        ntp_time = self.get_ntp_time()
        if ntp_time:
            utc_time = datetime.datetime.utcfromtimestamp(ntp_time)
            # Convertește la fusul orar specificat
            target_tz = pytz.timezone(zone_name)
            target_time = utc_time.replace(tzinfo=pytz.utc).astimezone(target_tz)
            return target_time
        return None

def main():
    parser = argparse.ArgumentParser(description='Client NTP pentru a obține ora exactă pentru diferite fusuri orare')
    parser.add_argument('--timezone', '-t', type=str,
                      help='Fus orar în format GMT+X sau GMT-X unde X este între 0 și 11')
    parser.add_argument('--server', '-s', type=str, default='pool.ntp.org',
                      help='Serverul NTP de utilizat (implicit: pool.ntp.org)')
    args = parser.parse_args()
    
    ntp_client = NTPClient(server=args.server)
    
    # Obține și afișează ora locală
    local_time = ntp_client.get_local_time()
    if local_time:
        print(f"Ora locală: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z (%z)')}")
    else:
        print("Nu s-a putut obține ora locală")
    
    # Dacă a fost specificat un fus orar, obține și afișează ora pentru acel fus orar
    if args.timezone:
        try:
            timezone_time = ntp_client.get_time_for_timezone(args.timezone)
            if timezone_time:
                print(f"Ora pentru {args.timezone}: {timezone_time.strftime('%Y-%m-%d %H:%M:%S %Z (%z)')}")
            else:
                print(f"Nu s-a putut obține ora pentru {args.timezone}")
        except ValueError as e:
            print(f"Eroare: {str(e)}")

if __name__ == "__main__":
    main()