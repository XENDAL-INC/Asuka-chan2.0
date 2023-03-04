def health_bar(health, max_health):
    """
    This function returns an ASCII health bar for the given health and maximum health.

    Parameters:
    health (int): The current health value.
    max_health (int): The maximum health value.

    Returns:
    str: The ASCII health bar.
    """
    health_percentage = health / max_health
    filled_blocks = int(health_percentage * 15)
    empty_blocks = 15 - filled_blocks
    health_bar = "[" + "█" * filled_blocks + "░" * empty_blocks + "]"
    health_bar += "\n" + str(health) + "/" + str(max_health)
    return health_bar


def combatVSPc(player_dmg,
               computer_dmg,
               playerTurn,
               player_health,
               computer_health,
               isWin=False,
               isLoss=False):
    if playerTurn:
        print("Player's turn:")
        #input("Press Enter to attack...")
        print("You attacked the computer and dealt", player_dmg, "damage.")
        computer_health -= player_dmg
        print("Computer's health is now", computer_health)
        if computer_health <= 0:
            isWin = True
            return playerTurn, player_health, computer_health, isWin, isLoss
        playerTurn = False

    if not playerTurn:
        # Computer's turn
        print("Computer's turn:")
        print("The computer attacked you and dealt", computer_dmg, "damage.")
        player_health -= computer_dmg
        if player_health <= 0:
            isLoss = True
            return playerTurn, player_health, computer_health, isWin, isLoss
        playerTurn = True
