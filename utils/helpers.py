"""
Helper functions for the gambling bot
"""
import random
from typing import Tuple, List
import config

def validate_bet(balance: int, bet: int) -> Tuple[bool, str]:
    """
    Validate if a bet is valid
    Returns (is_valid, error_message)
    """
    if bet < config.MIN_BET:
        return False, f"La mise minimum est de **{config.MIN_BET}** coins!"
    
    if bet > config.MAX_BET:
        return False, f"La mise maximum est de **{config.MAX_BET}** coins!"
    
    if bet > balance:
        return False, f"Vous n'avez pas assez de coins! Balance: **{balance}** coins"
    
    return True, ""

def coinflip(choice: str) -> Tuple[bool, str]:
    """
    Simulate a coinflip
    Returns (won, result)
    """
    result = random.choice(['pile', 'face'])
    won = result == choice.lower()
    return won, result

def roll_dice(num_dice: int = 2) -> List[int]:
    """Roll dice and return results"""
    return [random.randint(1, 6) for _ in range(num_dice)]

def spin_slots() -> Tuple[List[str], int]:
    """
    Spin slot machine
    Returns (symbols, multiplier)
    """
    symbols = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣']
    weights = [30, 25, 20, 15, 8, 2]  # Probability weights
    
    result = random.choices(symbols, weights=weights, k=3)
    
    # Calculate multiplier
    if result[0] == result[1] == result[2]:
        # All three match
        if result[0] == '7️⃣':
            multiplier = 50  # Jackpot!
        elif result[0] == '💎':
            multiplier = 20
        elif result[0] == '🍇':
            multiplier = 10
        elif result[0] == '🍊':
            multiplier = 5
        elif result[0] == '🍋':
            multiplier = 3
        else:  # 🍒
            multiplier = 2
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        # Two match
        multiplier = 1.5
    else:
        # No match
        multiplier = 0
    
    return result, multiplier

def spin_roulette(bet_type: str, bet_value: str = None) -> Tuple[bool, int, str]:
    """
    Spin roulette wheel
    Returns (won, multiplier, result_description)
    """
    number = random.randint(0, 36)
    
    # Determine color
    if number == 0:
        color = 'green'
    elif number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]:
        color = 'red'
    else:
        color = 'black'
    
    bet_type = bet_type.lower()
    
    # Check win conditions
    if bet_type == 'rouge' or bet_type == 'red':
        won = color == 'red'
        multiplier = 2 if won else 0
        result = f"🔴 {number} (Rouge)" if color == 'red' else f"⚫ {number} (Noir)" if color == 'black' else f"🟢 {number} (Vert)"
    
    elif bet_type == 'noir' or bet_type == 'black':
        won = color == 'black'
        multiplier = 2 if won else 0
        result = f"⚫ {number} (Noir)" if color == 'black' else f"🔴 {number} (Rouge)" if color == 'red' else f"🟢 {number} (Vert)"
    
    elif bet_type == 'vert' or bet_type == 'green':
        won = color == 'green'
        multiplier = 36 if won else 0
        result = f"🟢 {number} (Vert)"
    
    elif bet_type == 'pair' or bet_type == 'even':
        won = number % 2 == 0 and number != 0
        multiplier = 2 if won else 0
        result = f"Le numéro {number} est {'pair' if number % 2 == 0 else 'impair'}"
    
    elif bet_type == 'impair' or bet_type == 'odd':
        won = number % 2 == 1
        multiplier = 2 if won else 0
        result = f"Le numéro {number} est {'impair' if number % 2 == 1 else 'pair'}"
    
    else:
        won = False
        multiplier = 0
        result = f"Type de pari invalide"
    
    return won, multiplier, result

class BlackjackGame:
    """Simple Blackjack game logic"""
    
    def __init__(self):
        self.deck = self._create_deck()
        self.player_hand = []
        self.dealer_hand = []
    
    def _create_deck(self) -> List[Tuple[str, int]]:
        """Create a deck of cards"""
        suits = ['♠️', '♥️', '♦️', '♣️']
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        
        deck = []
        for suit in suits:
            for rank, value in zip(ranks, values):
                deck.append((f"{rank}{suit}", value))
        
        random.shuffle(deck)
        return deck
    
    def deal_card(self) -> Tuple[str, int]:
        """Deal a card from the deck"""
        return self.deck.pop()
    
    def calculate_hand_value(self, hand: List[Tuple[str, int]]) -> int:
        """Calculate the value of a hand"""
        value = sum(card[1] for card in hand)
        aces = sum(1 for card in hand if card[0].startswith('A'))
        
        # Adjust for aces
        while value > 21 and aces > 0:
            value -= 10
            aces -= 1
        
        return value
    
    def hand_to_string(self, hand: List[Tuple[str, int]]) -> str:
        """Convert hand to readable string"""
        return ' '.join(card[0] for card in hand)
    
    def play(self) -> Tuple[bool, str, int]:
        """
        Play a game of blackjack
        Returns (won, description, multiplier)
        """
        # Initial deal
        self.player_hand = [self.deal_card(), self.deal_card()]
        self.dealer_hand = [self.deal_card(), self.deal_card()]
        
        player_value = self.calculate_hand_value(self.player_hand)
        dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        description = f"**Votre main:** {self.hand_to_string(self.player_hand)} (Valeur: {player_value})\n"
        description += f"**Main du croupier:** {self.dealer_hand[0][0]} + ?\n\n"
        
        # Check for player blackjack
        if player_value == 21:
            description += f"**Main du croupier:** {self.hand_to_string(self.dealer_hand)} (Valeur: {dealer_value})\n"
            if dealer_value == 21:
                description += "**Égalité!** Vous et le croupier avez un Blackjack!"
                return False, description, 1  # Push, return bet
            else:
                description += "**BLACKJACK!** 🎉"
                return True, description, 2.5
        
        # Player hits until 17 or bust (simplified auto-play)
        while player_value < 17:
            card = self.deal_card()
            self.player_hand.append(card)
            player_value = self.calculate_hand_value(self.player_hand)
        
        description = f"**Votre main:** {self.hand_to_string(self.player_hand)} (Valeur: {player_value})\n"
        
        # Check for player bust
        if player_value > 21:
            description += f"**Main du croupier:** {self.hand_to_string(self.dealer_hand)} (Valeur: {dealer_value})\n"
            description += "**Vous avez dépassé 21!** Vous perdez."
            return False, description, 0
        
        # Dealer plays
        while dealer_value < 17:
            card = self.deal_card()
            self.dealer_hand.append(card)
            dealer_value = self.calculate_hand_value(self.dealer_hand)
        
        description += f"**Main du croupier:** {self.hand_to_string(self.dealer_hand)} (Valeur: {dealer_value})\n\n"
        
        # Determine winner
        if dealer_value > 21:
            description += "**Le croupier a dépassé 21!** Vous gagnez! 🎉"
            return True, description, 2
        elif player_value > dealer_value:
            description += "**Vous gagnez!** 🎉"
            return True, description, 2
        elif player_value < dealer_value:
            description += "**Le croupier gagne!** Vous perdez."
            return False, description, 0
        else:
            description += "**Égalité!** Votre mise est retournée."
            return False, description, 1  # Push, return bet

def crash_game(cashout_multiplier: float) -> Tuple[bool, float]:
    """
    Simulate a crash game
    Returns (won, crash_point)
    """
    # Generate crash point with weighted probability
    # Lower multipliers are more common
    rand = random.random()
    
    if rand < 0.33:
        crash_point = random.uniform(1.0, 2.0)
    elif rand < 0.66:
        crash_point = random.uniform(2.0, 5.0)
    elif rand < 0.90:
        crash_point = random.uniform(5.0, 10.0)
    else:
        crash_point = random.uniform(10.0, 50.0)
    
    won = cashout_multiplier <= crash_point
    return won, round(crash_point, 2)
