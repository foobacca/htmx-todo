from django.http.response import HttpResponseRedirectBase


class HttpResponseSeeOther(HttpResponseRedirectBase):
    status_code = 303
