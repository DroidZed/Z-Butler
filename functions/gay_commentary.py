def gay_commentary(rate: int) -> str:
        if not rate:
            return "That's a real human 😉"
        elif rate < 10:
            return "Need purifying 😬"
        elif rate < 50:
            return 'What a shame...🙄'
        elif rate < 65:
            return 'Utterly disgusting...🤮'
        else:
            return '**YOU ARE AN ABOMINATION, YOU HAVE NO RIGHT TO LIVE !! DIE YOU MONSTER !!**'
