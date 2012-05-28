import datetime
import hashlib
import logging
import urllib2
import json

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from facebookconnect.models import FacebookUser

def login_facebook_connect(request):
    status = reverse('userena_signup')
    try:
        expires = request.POST['expires']
        ss = request.POST['ss']
        session_key = request.POST['session_key']
        user = request.POST['user']
        sig = request.POST['sig']

        pre_hash_string = "expires=%ssession_key=%sss=%suser=%s%s" % (
            expires,
            session_key,
            ss,
            user,
            settings.FACEBOOK_APPLICATION_SECRET,
        )
        post_hash_string = hashlib.new('md5')
        post_hash_string.update(pre_hash_string)
        if post_hash_string.hexdigest() == sig:
            try:
                fb = FacebookUser.objects.get(facebook_id=user)
            except FacebookUser.DoesNotExist:
                fb = FacebookUser()
                fb.facebook_id = user
                temp = hashlib.new('sha1')
                temp.update(str(datetime.datetime.now()))
                #password = temp.hexdigest()
                #fb.contrib_password = password
                fb.save()
            if fb.contrib_user:
                fb.contrib_user.backend = 'django.contrib.auth.backends.ModelBackend'
                auth.login(request, fb.contrib_user)
                status = reverse("website-user-home")
            elif not request.user.is_anonymous():
                fb.contrib_user = request.user
                fb.save()
                status = reverse("website-user-home")
            else:
                request.session['fb_pk'] = fb.pk
        else:
            status = reverse("website-home")

            logging.debug("FBConnect: user %s with exit status %s" % (user, status))

    except Exception, e:
        status = reverse("website-home")
        logging.debug("Exception thrown in the FBConnect ajax call: %s" % e)
    return HttpResponse("%s" % status)

def xd_receiver(request):
        return render_to_response('facebookconnect/xd_receiver.html')
