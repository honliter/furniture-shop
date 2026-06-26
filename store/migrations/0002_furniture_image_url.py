from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='furniture',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
