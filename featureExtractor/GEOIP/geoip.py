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

def get_all(ip):
    result = get_country(ip)+','+str(get_asn(ip))
    return result
