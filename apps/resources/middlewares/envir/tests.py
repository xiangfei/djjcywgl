#!/usr/bin/python

# -*- coding: utf-8 -*-

from django.test import TestCase
from rest_framework.test import APIRequestFactory
import pandas as pd

from .views import (
    EnvListView, EnvAddView, EnvInfoView,
    EnvDeleteView, EnvEditView, EnvUploadView,
    EnvDownloadView,
)


# Create your tests here.


class ServerTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.csrftoken = "1qaz@wsx3edc4rfv"

    def test_main(self):
        self._test_001_envlist()
        self._test_001_envadd()
        self._test_001_envinfo()
        self._test_001_envdelete()

    def _test_001_envlist(self):
        data = {"env_key": "", "page": 1, "page_size": 20}
        request = self.factory.post('/middlewares/env/search/', data, format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view = EnvListView.as_view()
        response = view(request)
        print(response.data)
        assert response.status_code == 200

    def _test_001_envadd(self):
        env_name = pd.Timestamp.now().strftime("%Y%m%d %H:%M:%S")
        data = {"env_name": env_name, "desc": env_name, "file_id": 1}
        request = self.factory.post('/middlewares/env/add/', data, format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view = EnvAddView.as_view()
        response = view(request)
        print(response.data)
        assert response.status_code == 200

    def _test_001_envinfo(self):
        data = {"env_id": 1}
        request = self.factory.post('/middlewares/env/info/', data, format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view = EnvAddView.as_view()
        response = view(request)
        print(response.data)
        assert response.status_code == 200

    def _test_001_envdelete(self):
        data = {"env_id": 1}
        request = self.factory.post('/middlewares/env/delete/', data, format='json')
        request.META['HTTP_ACCESSTOKEN'] = self.csrftoken
        view = EnvAddView.as_view()
        response = view(request)
        print(response.data)
        assert response.status_code == 200


