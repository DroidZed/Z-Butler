
def gay_commentary(rate: int) -> str:

    match rate:

        case x if x < 0: return gay_commentary(rate * -1)

        case 0: return "That's a real human 😉"

        case r if r < 10: return "Need purifying 😬"

        case r if r < 50: return 'What a shame...🙄'

        case r if r < 65: return 'Utterly disgusting...🤮'

        case _: return '**YOU ARE AN ABOMINATION, YOU HAVE NO RIGHT TO LIVE !! DIE YOU MONSTER !!**'
