# Ascii_arts.py
# Compact, optimized, and warning-free weather ASCII arts for CLI-Mate.
# Colorized with standard Gruvbox colors using rich tags.

weather_arts = {
    # ==================== SUNNY ====================
    "sunny": [
        # Art 1. Braille Sun with Glasses (Kept exactly as requested)
        (
            "[bold #fabd2f]⠀⠀⠀⠀⠀⠀⠀⢴⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⢀⠀⠀⠀⠀⡇⢑⠀⠀⢀⡐⢱⠀⠀⠀⠀⠀⠀⠀\n"
            "⠀⠀⠈⢏⠢⣀⣘⠀⣀⣣⣔⣁⣀⡯⠀⣀⣀⣀⠀⠀⠀\n"
            "⠀⠀⠀⠈⡂⠔⠿⠉⠀⠈⠀⠀⠀⠉⠓⢄⡰⠋⠀⠀⠀\n"
            "⠀⢏⠈⠒⠷⣁⣀⡀⠀⠀⠀⣀⣀⠀⠀⠈⡗⠦⢄⠀⠀\n"
            "⠀⠀⠳⢄[/][bold #504945]⢘⢻⣴⣿⠥⢼⣽⣷⣿⠤⠖⠒[/][bold #fabd2f]⡇⠀⣀⣈⡇\n"
            "⠘⢗⠒⠛⢒⠙⠛⠁⠀⠀⠙⠛⠁⠀⠀⡸⠙⡍⠁⠀⠀\n"
            "⠀⠀⠁⠒⠄⢵⣀⠀⠀⠀⠀⠀⠀⡠⣾⣁⡀⠘⣄⠀⠀\n"
            "⠀⠀⠀⠀⣀⠴⠋⣑⣶⠒⢲⢮⠁⢰⠀⠀⠉⠓⠋⠀⠀\n"
            "⠀⠀⠀⣎⡡⠆⠋⠀⣏⣀⠎⠀⠘⣄⢀⡇⠀⠀⠀⠀⠀\n"
            "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀[/]"
        )
    ],

    # ==================== CLOUDY ====================
    "cloudy": [
        # Art 1. Compact Cloud
        (
            "[bold #a89984]     .--. \n"
            "  .-(    ). \n"
            " (___.___)_) [/]"
        ),
        # Art 2. Compact Cloud and Sun
        (
            "   [bold #fabd2f]\\\\ _ /[/]\n"
            " [bold #fabd2f]- ( ) -[/] [bold #a89984].--. [/]\n"
            "   [bold #fabd2f]/   \\\\[/] [bold #a89984](    )[/]\n"
            "       [bold #a89984](______)_)[/]"
        )
    ],

    # ==================== FOGGY ====================
    "foggy": [
        # Art 1. Compact Fog Lines
        (
            "[bold #928374]  ~ ~ ~ ~ ~ ~ ~\n"
            "   .-.-.-.-.-.\n"
            "  ~ ~ ~ ~ ~ ~ ~\n"
            "   - - - - - -[/]"
        ),
        # Art 2. Compact Sun behind Fog
        (
            "    [bold #fabd2f].--.[/]\n"
            "  [bold #928374]= = = = = = =[/]\n"
            "    [bold #fabd2f]'--'[/]\n"
            "  [bold #928374]= = = = = = =[/]"
        )
    ],

    # ==================== RAINY ====================
    "rainy": [
        # Art 1. Compact Cloud and Rain
        (
            "[bold #a89984]     .--.\n"
            "  .-(    ).-\n"
            " (___.___)_)[/]\n"
            "  [bold #83a598]/ / / / /\n"
            "   / / / /[/]"
        ),
        # Art 2. Compact Umbrella under Rain
        (
            "  [bold #83a598]/  /  /  /[/]\n"
            "  [bold #fe8019]  .-''-.[/]\n"
            "  [bold #fe8019] '======='[/]\n"
            "  [bold #fe8019]    | |[/]\n"
            "  [bold #fe8019]    J J[/]"
        )
    ],

    # ==================== SNOWY ====================
    "snowy": [
        # Art 1. Compact Cloud and Snow
        (
            "[bold #a89984]     .--.\n"
            "  .-(    ).-\n"
            " (___.___)_)[/]\n"
            "  [bold #8ec07c]*  *  *  *\n"
            "   *  *  *[/]"
        ),
        # Art 2. Compact Snowflake
        (
            "   [bold #8ec07c]\\\\  |  /[/]\n"
            "  [bold #8ec07c]-- * --[/]\n"
            "   [bold #8ec07c]/  |  \\\\[/]"
        )
    ],

    # ==================== SLEET ====================
    "sleet": [
        # Art 1. Compact Sleet Cloud
        (
            "[bold #a89984]     .--.\n"
            "  .-(    ).-\n"
            " (___.___)_)[/]\n"
            "  [bold #8ec07c]* [bold #83a598]/ [bold #8ec07c]* [bold #83a598]/ [bold #8ec07c]*\n"
            "   [bold #83a598]/ [bold #8ec07c]* [bold #83a598]/ [bold #8ec07c]*[/]"
        ),
        # Art 2. Sleet Pattern
        (
            "  [bold #8ec07c]* [bold #83a598]/[/] [bold #8ec07c]* [bold #83a598]/[/]\n"
            "  [bold #83a598]/[/] [bold #8ec07c]*[/] [bold #83a598]/[/] [bold #8ec07c]*[/]\n"
            "  [bold #8ec07c]* [bold #83a598]/[/] [bold #8ec07c]* [bold #83a598]/[/]"
        )
    ],

    # ==================== STORM ====================
    "storm": [
        # Art 1. Compact Storm Cloud and Lightning
        (
            "[bold #928374]     .--.\n"
            "  .-(    ).-\n"
            " (___.___)_)[/]\n"
            "   [bold #fabd2f]/_ /[/]\n"
            "    [bold #fabd2f]/_/[/]"
        ),
        # Art 2. Compact Double Lightning
        (
            "[bold #928374]     .-.-.\n"
            "    (     )\n"
            "   (_______)[/]\n"
            "    [bold #fabd2f]/\\\\  /[/]\n"
            "   [bold #fabd2f]/_/_/[/]\n"
            "    [bold #fabd2f]/_/[/]"
        )
    ],

    # ==================== WINDY ====================
    "windy": [
        # Art 1. Compact Wind Swirls
        (
            "[bold #83a598]  ~~ ~~~~ ~~\n"
            " ~~~~ ~~ ~~~~\n"
            "  ~~ ~~~~ ~~[/]"
        ),
        # Art 2. Compact Blowing Cloud
        (
            "   [bold #a89984].--.[/]\n"
            " [bold #83a598]~~[/] [bold #a89984](    )[/] [bold #83a598]~~[/]\n"
            "   [bold #a89984](______)[/]\n"
            " [bold #83a598]~~~~~~~~~~[/]"
        )
    ]
}