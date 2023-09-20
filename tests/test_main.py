from app.main import host, port, reload, log_level
from app.routers.health import health_check


def test_main_host():
    assert host == '127.0.0.1'

def test_main_port():
    assert port == 8000
    
def test_main_reload():
    assert reload == True

def test_main_host():
    assert log_level == 'info'
