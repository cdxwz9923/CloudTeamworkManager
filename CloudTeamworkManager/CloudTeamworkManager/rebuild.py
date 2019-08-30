from django.shortcuts import render, HttpResponse, get_object_or_404
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.models import User, Group, Permission
from guardian.shortcuts import assign_perm, remove_perm
from task.models import task as models_task
from task.forms import task as forms_task
from publisher.models import personal_comment, personal_progress, personal_shedule
from account.models import UserProfile
import re
import json
import time
import os

def join_task():
    pass

def create_personal_archive():
    pass

def recover_archive_edit_perm():
    pass

    