import os
from app.common.ip2Region import Ip2Region

def ip2addr(ip):
    ip_db_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        r'static\ip2region\ip2region.db'
    )
    ip_to_addr=Ip2Region(ip_db_path)
    addr_info = ip_to_addr
    return addr_info