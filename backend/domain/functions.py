#функция калькуляции статистики


async def calculate_stat_all_matches(profile_data: list):
    # берём из переданных параметров нужные
    username = profile_data['id']
    all_matches_stat = profile_data['all_games_stat']
    total_games = all_matches_stat.all
    total_wins = all_matches_stat.win
    total_draws = all_matches_stat.draw
    total_losses =  all_matches_stat.loss


    # расчитываем статистику
    overall_winrate = await total_wins / (total_games(total_wins + total_losses + total_draws)) * 100

    # возвращаем
    return overall_winrate

