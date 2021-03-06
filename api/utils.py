from models import *
from dota2api import api

d2api = api.Initialise()


def get_until_success(get_function):
    while True:
        try:
            import time

            time.sleep(1)
            return get_function()
        except Exception as e:
            import logging

            logging.exception(e)


def load_team(match, players):
    updated_accounts = get_until_success(lambda: d2api.get_player_summaries(*[p.account_id for p in players]))
    for player_response in players:
        hero, _ = Hero.objects.get_or_create(hero_id=player_response.hero.id,
                                             localized_name=player_response.hero.localized_name,
                                             name=player_response.hero.name,
                                             url_small_portrait=player_response.hero.url_small_portrait,
                                             url_large_portrait=player_response.hero.url_large_portrait,
                                             url_full_portrait=player_response.hero.url_full_portrait,
                                             url_vertical_portrait=player_response.hero.url_vertical_portrait)

        if player_response.account_id != 4294967295:
            updated_acc = [ua for ua in updated_accounts
                           if str(ua.steam_id) == str(api.convert_to_64_bit(player_response.account_id))][0]

            account, _ = Account.objects.get_or_create(account_id=player_response.account_id)
            account.steam_id = updated_acc.steam_id
            account.last_logoff = updated_acc.last_logoff
            account.profile_url = updated_acc.profile_url
            account.community_visibility_state = updated_acc.community_visibility_state
            account.time_created = updated_acc.time_created
            account.persona_state = updated_acc.persona_state
            account.profile_state = updated_acc.profile_state
            account.save()
            update, created = account.updates.get_or_create(account=account,
                                                            persona_name=updated_acc.persona_name,
                                                            url_avatar=updated_acc.url_avatar,
                                                            url_avatar_medium=updated_acc.url_avatar_medium,
                                                            url_avatar_full=updated_acc.url_avatar_full,
                                                            primary_clan_id=updated_acc.primary_clan_id,
                                                            persona_state_flags=updated_acc.persona_state_flags)
            if created:
                update.sequential = len(account.updates.all())
                update.save()
        else:
            account = None

        leaver_status, _ = LeaverStatus.objects.get_or_create(leaver_id=player_response.leaver_status.id,
                                                              name=player_response.leaver_status.name,
                                                              description=player_response.leaver_status.description)

        player = DetailMatchPlayer.objects.create(match=match, player_account=account,
                                                  account_id=player_response.account_id,
                                                  player_slot=player_response.player_slot,
                                                  hero=hero, kills=player_response.kills,
                                                  deaths=player_response.deaths, assists=player_response.assists,
                                                  leaver_status=leaver_status,
                                                  gold=player_response.gold,
                                                  last_hits=player_response.last_hits, denies=player_response.denies,
                                                  gold_per_min=player_response.gold_per_min,
                                                  xp_per_min=player_response.xp_per_min,
                                                  gold_spent=player_response.gold_spent,
                                                  hero_damage=player_response.hero_damage,
                                                  tower_damage=player_response.tower_damage,
                                                  hero_healing=player_response.hero_healing,
                                                  level=player_response.level)

        for additional_unit in player_response.additional_units:
            unit, unit_created = AdditionalUnit.objects.get_or_create(unit_name=additional_unit.unit_name,
                                                                      player=player)
            for index, item_response in enumerate(additional_unit.items):
                item, _ = Item.objects.get_or_create(item_id=item_response.id,
                                                     localized_name=item_response.localized_name,
                                                     name=item_response.name,
                                                     is_recipe=bool(item_response.is_recipe),
                                                     in_secret_shop=item_response.in_secret_shop,
                                                     cost=item_response.cost,
                                                     in_side_shop=item_response.in_side_shop,
                                                     url_image=item_response.url_image)

                DetailMatchOwnerItem.objects.create(owner=unit, slot=index, item=item)

        for index, item_response in enumerate(player_response.items):
            item, _ = Item.objects.get_or_create(item_id=item_response.id,
                                                 localized_name=item_response.localized_name,
                                                 name=item_response.name,
                                                 is_recipe=bool(item_response.is_recipe),
                                                 in_secret_shop=item_response.in_secret_shop,
                                                 cost=item_response.cost,
                                                 in_side_shop=item_response.in_side_shop,
                                                 url_image=item_response.url_image)

            DetailMatchOwnerItem.objects.create(owner=player, slot=index, item=item)

        for upgrade in player_response.ability_upgrades:
            ability, _ = Ability.objects.get_or_create(ability_id=upgrade.ability,
                                                       name=upgrade.ability_name)
            DetailMatchAbilityUpgrade.objects.create(player=player,
                                                     ability=ability,
                                                     time=upgrade.time,
                                                     upgraded_lvl=upgrade.level)


def parse_from_details_match(match_details):
    cluster, _ = Cluster.objects.get_or_create(cluster_id=match_details.cluster,
                                               name=match_details.cluster_name)

    game_mode, _ = GameMode.objects.get_or_create(game_mode_id=match_details.game_mode,
                                                  name=match_details.game_mode_name)

    lobby_type, _ = LobbyType.objects.get_or_create(lobby_type_id=match_details.lobby_type,
                                                    name=match_details.lobby_name)

    match = DetailMatch.objects.create(is_radiant_win=match_details.is_radiant_win, duration=match_details.duration,
                                       start_time=match_details.start_time, match_id=match_details.match_id,
                                       match_seq_num=match_details.match_seq_num,
                                       tower_status_radiant=match_details.tower_status_radiant,
                                       tower_status_dire=match_details.tower_status_dire,
                                       barracks_status_radiant=match_details.barracks_status_radiant,
                                       barracks_status_dire=match_details.barracks_status_dire,
                                       cluster=cluster,
                                       first_blood_time=match_details.first_blood_time,
                                       lobby_type=lobby_type,
                                       human_players=match_details.human_players, league_id=match_details.league_id,
                                       positive_votes=match_details.positive_votes,
                                       negative_votes=match_details.negative_votes,
                                       game_mode=game_mode)

    load_team(match, match_details.players)

    return match


def get_details_match(match_id):
    match = DetailMatch.objects.filter(match_id=match_id)
    if match:
        return match[0]
    else:
        details = get_until_success(lambda: d2api.get_match_details(match_id))
        return parse_from_details_match(details)
