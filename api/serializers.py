from rest_framework import serializers
from models import DetailMatch, DetailMatchPlayer, Hero, Account, Item, DetailMatchAbilityUpgrade, DetailMatchOwnerItem, Cluster, LobbyType, GameMode, AccountUpdate


class ClusterSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = Cluster


class LobbyTypeSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = LobbyType


class GameModeSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = GameMode


class DetailMatchAbilityUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailMatchAbilityUpgrade


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item


class DetailMatchOwnerItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = DetailMatchOwnerItem

class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero

class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountUpdate


class AccountSerializer(serializers.ModelSerializer):
    current_update = AccountUpdateSerializer()

    class Meta:
        model = Account


class PlayerSerializer(serializers.ModelSerializer):
    hero = HeroSerializer()
    player_account = AccountSerializer()
    items = DetailMatchOwnerItemSerializer(many=True)
    abilities = DetailMatchAbilityUpgradeSerializer(many=True)

    class Meta:
        model = DetailMatchPlayer


class DetailMatchSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True)
    lobby_type = LobbyTypeSerialiazer()
    game_mode = GameModeSerialiazer()
    cluster = ClusterSerialiazer()

    class Meta:
        model = DetailMatch
