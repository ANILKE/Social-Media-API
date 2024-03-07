"""
Django Admin Actions Helpers.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from core import models
import openpyxl
from django.http import HttpResponse
from follower.serializers import FriendshipDetailSerializer
from comments.serializers import CommentSerializer
from posts.serializers import PostDetailSerializer
from django.contrib.auth import get_user_model



@admin.action(description="Download selected items as excel.")
def export_to_excel_friends(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Exported Followship Data'
    # Write headers
    headers = ['id', 'follower', 'following', 'since','user_profile']
    worksheet.append(headers)

    # Write data rows
    for obj in FriendshipDetailSerializer(queryset,many=True).data:
        print(obj)
        row = [
            obj['id'],
            obj['follower']['name'] if obj['follower'] else -1,
            obj['following'] if obj['following'] else -1,
            obj['since'],
            obj['follower']['user_profile']  if obj['follower'] else "",
        ]
        worksheet.append(row)

    workbook.save(response)
    return response

@admin.action(description="Download selected items as excel.")
def export_to_excel_post(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Exported Post Data'
    # Write headers
    headers = ['id', 'owner', 'content', 'likes','comments', 'liked_users']
    worksheet.append(headers)

    # Write data rows
    for obj in PostDetailSerializer(queryset,many=True).data:
        print(obj)
        row = [
            obj['id'],
            obj['owner']['name'] if obj['owner'] else "",
            obj['content'],
            obj['likes'],
            ', '.join([comment['content'] for comment in obj['comments']]) if obj['comments'] else '',
            ', '.join([user['name'] for user in obj['liked_users']]) if obj['liked_users'] else ''
        ]
        worksheet.append(row)

    workbook.save(response)
    return response


@admin.action(description="Download selected items as excel.")
def export_to_excel_comment(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Exported Comment Data'
    # Write headers
    headers = ['id', 'related_post_id', 'owner', 'content', 'likes', 'liked_users']
    worksheet.append(headers)

    # Write data rows
    for obj in CommentSerializer(queryset,many=True).data:
        print(obj)
        row = [
            obj['id'],
            obj['related_post_id'],
            obj['owner']['name'] if obj['owner'] else "",
            obj['content'],
            obj['likes'],
            ', '.join([user['name'] for user in obj['liked_users']]) if obj['liked_users'] else ''
        ]
        worksheet.append(row)

    workbook.save(response)
    return response