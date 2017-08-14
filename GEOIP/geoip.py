import geoip2.database
import socket

reader = geoip2.database.Reader('Country.mmdb')
reader2 = geoip2.database.Reader('ASN.mmdb')

def get_country(ip):
    response = reader.country(ip)
    return response.country.iso_code

def get_asn(ip):
    response = reader2.asn(ip)
    return response.autonomous_system_number

def ptr(ip):
    try:
        name,_,_ = socket.gethostbyaddr(ip)
        if name != 'localhost':
           return 1
    except Exception as e:
        print(str(e))
    return 0
