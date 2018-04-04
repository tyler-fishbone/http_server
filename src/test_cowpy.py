import requests
from cowpy import cow
import json



def test_server_sends_200_response():
    """tests 200 response"""
    response = requests.get('http://127.0.0.1:3000')
    assert response.status_code == 200


def test_server_sends_404_response():
    """ tests 404 endpoint not found"""
    response = requests.get('http://127.0.0.1:3000/monkey')
    assert response.status_code == 404
    assert response.text == 'Not Found'


def test_server_sends_qs_back():
    """ tests instructions endpoint"""
    response = requests.get('http://127.0.0.1:3000/cowsay')
    assert response.status_code == 200
    assert response.text == 'Helpful instructions about this application'

def test_server_looks_for_moose():
    """ tests input query string"""
    response = requests.get('http://127.0.0.1:3000/cow?msg=hellew world')
    assert response.status_code == 200
    assert response.text[:50] == ''' ______________ 
< hellew world >
 -------------- '''

def test_server_post_req():
    """ tests input query string"""
    response = requests.post('http://127.0.0.1:3000/cow?msg=hellew world')
    assert response.status_code == 200
    assert json.loads(response.text)['content'] == " ______________ \n< hellew world >\n -------------- \n  o\n   o   \\_\\_    _/_/\n    o      \\__/\n           (oo)\\_______\n           (__)\\       )\\/\\\n               ||----w |\n               ||     ||"