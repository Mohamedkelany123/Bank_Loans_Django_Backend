# Generated by Django 4.2.4 on 2023-08-07 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_loanfund_interest_rate_loanfund_loan_duration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customerName', models.CharField(max_length=100)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('duration', models.IntegerField()),
                ('status', models.CharField(choices=[('Requested', 'Requested'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Requested', max_length=20)),
                ('date_requested', models.DateField(auto_now_add=True)),
                ('date_approved', models.DateField(blank=True, null=True)),
                ('date_rejected', models.DateField(blank=True, null=True)),
                ('monthly_installment', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('loan_fund_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loanfund')),
            ],
        ),
    ]
