from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json
import codecs
import MySQLdb


def test(request):
    content = {"a": 1}
    return render_to_response('test.html', content);


if __name__ == '__main__':
    pass
