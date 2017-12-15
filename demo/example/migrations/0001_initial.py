# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 14:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('viewflow', '0006_i18n'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTimesheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('code', models.CharField(choices=[('absent', 'Absent'), ('present', 'Present'), ('weekend', 'Weekend'), ('holiday', 'Holiday'), ('paid_leave', 'Paid Leave'), ('unpaid_leave', 'Unpaid Leave'), ('sick_leave', 'Sick Leave'), ('business_trip', 'Business Trip')], default='present', max_length=20)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='timesheet_approvals', to=settings.AUTH_USER_MODEL)),
                ('for_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sheets', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyTimesheetApproval',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('sheet', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='example.DailyTimesheet')),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('requested_on', models.DateField(auto_now=True)),
                ('details', models.CharField(default='vacation', max_length=300)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacation_approvals', to=settings.AUTH_USER_MODEL)),
                ('for_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VacationApproval',
            fields=[
                ('process_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='viewflow.Process')),
                ('vacation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval', to='example.Vacation')),
            ],
            options={
                'abstract': False,
            },
            bases=('viewflow.process',),
        ),
    ]
