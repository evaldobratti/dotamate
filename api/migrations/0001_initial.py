# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ability_id', models.SmallIntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_id', models.BigIntegerField(unique=True)),
                ('steam_id', models.BigIntegerField(null=True)),
                ('last_logoff', models.BigIntegerField(null=True)),
                ('profile_url', models.CharField(max_length=500, null=True)),
                ('community_visibility_state', models.IntegerField(null=True)),
                ('time_created', models.BigIntegerField(null=True)),
                ('persona_state', models.IntegerField(null=True)),
                ('profile_state', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AccountUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequential', models.IntegerField(null=True)),
                ('persona_name', models.CharField(max_length=500, null=True)),
                ('url_avatar', models.CharField(max_length=500, null=True)),
                ('url_avatar_medium', models.CharField(max_length=500, null=True)),
                ('url_avatar_full', models.CharField(max_length=500, null=True)),
                ('primary_clan_id', models.BigIntegerField(null=True)),
                ('persona_state_flags', models.BigIntegerField(null=True)),
                ('account', models.ForeignKey(related_name='updates', to='api.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Cluster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cluster_id', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='DetailMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_radiant_win', models.BooleanField()),
                ('duration', models.BigIntegerField()),
                ('start_time', models.BigIntegerField()),
                ('match_id', models.BigIntegerField(unique=True)),
                ('match_seq_num', models.BigIntegerField()),
                ('tower_status_radiant', models.SmallIntegerField()),
                ('tower_status_dire', models.SmallIntegerField()),
                ('barracks_status_radiant', models.SmallIntegerField()),
                ('barracks_status_dire', models.SmallIntegerField()),
                ('first_blood_time', models.IntegerField()),
                ('human_players', models.SmallIntegerField()),
                ('league_id', models.BigIntegerField()),
                ('positive_votes', models.IntegerField()),
                ('negative_votes', models.IntegerField()),
                ('cluster', models.ForeignKey(to='api.Cluster')),
            ],
        ),
        migrations.CreateModel(
            name='DetailMatchAbilityUpgrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('upgraded_lvl', models.SmallIntegerField()),
                ('ability', models.ForeignKey(to='api.Ability')),
            ],
        ),
        migrations.CreateModel(
            name='DetailMatchOwnerItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slot', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GameMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_mode_id', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Hero',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hero_id', models.SmallIntegerField()),
                ('localized_name', models.CharField(max_length=50)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('url_small_portrait', models.CharField(max_length=300)),
                ('url_large_portrait', models.CharField(max_length=300)),
                ('url_full_portrait', models.CharField(max_length=300)),
                ('url_vertical_portrait', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item_id', models.SmallIntegerField(unique=True)),
                ('localized_name', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=40)),
                ('is_recipe', models.BooleanField()),
                ('in_secret_shop', models.BooleanField()),
                ('cost', models.SmallIntegerField()),
                ('in_side_shop', models.BooleanField()),
                ('url_image', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='ItemOwner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='LeaverStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('leaver_id', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='LobbyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lobby_type_id', models.IntegerField()),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='AdditionalUnit',
            fields=[
                ('itemowner_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='api.ItemOwner')),
                ('unit_name', models.CharField(max_length=50)),
            ],
            bases=('api.itemowner',),
        ),
        migrations.CreateModel(
            name='DetailMatchPlayer',
            fields=[
                ('itemowner_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='api.ItemOwner')),
                ('account_id', models.BigIntegerField()),
                ('player_slot', models.SmallIntegerField()),
                ('kills', models.SmallIntegerField()),
                ('deaths', models.SmallIntegerField()),
                ('assists', models.SmallIntegerField()),
                ('gold', models.IntegerField()),
                ('last_hits', models.SmallIntegerField()),
                ('denies', models.SmallIntegerField()),
                ('gold_per_min', models.SmallIntegerField()),
                ('xp_per_min', models.SmallIntegerField()),
                ('gold_spent', models.IntegerField()),
                ('hero_damage', models.IntegerField()),
                ('tower_damage', models.IntegerField()),
                ('hero_healing', models.IntegerField()),
                ('level', models.IntegerField()),
                ('hero', models.ForeignKey(to='api.Hero')),
                ('leaver_status', models.ForeignKey(to='api.LeaverStatus')),
            ],
            bases=('api.itemowner',),
        ),
        migrations.AddField(
            model_name='detailmatchowneritem',
            name='item',
            field=models.ForeignKey(to='api.Item'),
        ),
        migrations.AddField(
            model_name='detailmatchowneritem',
            name='owner',
            field=models.ForeignKey(related_name='items', to='api.ItemOwner'),
        ),
        migrations.AddField(
            model_name='detailmatch',
            name='game_mode',
            field=models.ForeignKey(to='api.GameMode'),
        ),
        migrations.AddField(
            model_name='detailmatch',
            name='lobby_type',
            field=models.ForeignKey(to='api.LobbyType'),
        ),
        migrations.AddField(
            model_name='detailmatchplayer',
            name='match',
            field=models.ForeignKey(related_name='players', to='api.DetailMatch'),
        ),
        migrations.AddField(
            model_name='detailmatchplayer',
            name='player_account',
            field=models.ForeignKey(related_name='match_players', to='api.Account', null=True),
        ),
        migrations.AddField(
            model_name='detailmatchabilityupgrade',
            name='player',
            field=models.ForeignKey(related_name='abilities', to='api.DetailMatchPlayer'),
        ),
        migrations.AddField(
            model_name='additionalunit',
            name='player',
            field=models.ForeignKey(related_name='additional_units', to='api.DetailMatchPlayer'),
        ),
    ]
