# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

VERSION = "1.0.0"

CFGVERSION = {
    "main.conf": (1, 0, 0),
    "options.conf": (1, 0, 1),
    "irc.conf": (1, 0, 0),
    "bans.meta": (1, 0, 0),
    "ranks.meta": (1, 0, 0),
    "lastseen.meta": (1, 0, 0),
    "spectators.meta": (1, 0, 0),
    "world.meta": (1, 5, 0),
    }

CONFIG = [
    # Format:
    #(attribute name, (file, section, option), prerequistics, dynamic, mode, callback function, required, default value)
    # prerequistics is a python expression in which self is the factory (lazy bum :P)
    # Callback function is the name of the function, the server will attempt to grab the function (self = ArcFactory)
    # Default value is the value used when required = False and user did not enter a value / the option is missing in the config.
    ("server_name", ("main.conf", "main", "name"), None, True, "get", None, True, None),
    ("server_port", ("main.conf", "network", "port"), None, False, "getint", None, True, None),
    ("max_clients", ("main.conf", "main", "max_clients"), None, True, "getint", None, True, None),
    ("server_message", ("main.conf", "main", "description"), None, True, "get", None, True, None),
    ("public", ("main.conf", "main", "public"), None, True, "getboolean", None, True, None),
    ("salt", ("main.conf", "main", "salt"), None, False, "get", "checkSalt", True, None),
    ("use_controller", ("main.conf", "network", "use_controller"), None, False, "getboolean", None, False, False),
    (
    "controller_port", ("main.conf", "network", "controller_port"), "self.use_controller == True", False, "getint", None
    , False, None),
    ("controller_password", ("main.conf", "network", "controller_port"), "self.use_controller == True", False, "get",
     None, False, None),
    ("hbs", ("main.conf", "heartbeatnames", None), None, False, "options", None, True, None),
    ("duplicate_logins", ("options.conf", "options", "duplicate_logins"), None, True, "getboolean", None, False, False),
    (
    "wom_heartbeat", ("options.conf", "options", "wom_heartbeat"), None, True, "getboolean", "modifyHeartbeatURL", False
    , False),
    ("enable_lowlag", ("options.conf", "options", "enable_lowlag"), None, True, "getboolean", None, False, False),
    ("lowlag_players", ("options.conf", "options", "lowlag_players"), None, True, "getint", None, False, 0),
    #("use_irc", ("irc.conf", "irc", "use_irc"), None, False, "getboolean", "initIRC", False, False),
    ("info_url", ("options.conf", "options", "info_url"), None, True, "get", None, False, ""),
    ("colors", ("options.conf", "options", "colors"), None, True, "getboolean", None, False, True),
    ("physics_limit", ("options.conf", "worlds", "physics_limit"), None, True, "getint", None, False, 5),
    ("default_name", ("options.conf", "worlds", "default_name"), None, False, "get", None, True, None),
    ("default_backup", ("options.conf", "worlds", "default_backup"), None, True, "get", None, False, "main"),
    ("asd_delay", ("options.conf", "worlds", "asd_delay"), None, True, "getint", "startASDLoop", False, 5),
    ("backup_auto", ("options.conf", "backups", "backup_auto"), None, True, "get", "initBackupLoop", False, True),
    ("backup_freq", ("options.conf", "backups", "backup_freq"), "self.backup_auto == True", True, "getint",
     "changeBackupFrequency", False, 10),
    ("backup_default", ("options.conf", "backups", "backup_default"), "self.backup_auto == True", True, "getboolean",
     None, False, False),
    ("backup_max", ("options.conf", "backups", "backup_max"), "self.backup_auto == True", True, "getint", None, False,
     50),
    ("enable_archives", ("options.conf", "archiver", "enable_archives"), None, True, "getboolean", "enableArchiver",
     False, False),
    ("currency", ("options.conf", "bank", "currency"), None, True, "get", None, False, "Minecash"),
    (
    "useblblimit", ("options.conf", "blb", "use_blb_limiter"), None, True, "getboolean", "initBLBLimiter", False, False)
    ,
    ]

INFO_VIPLIST = [
    # classicube people : ')
    "andrewph",
    "tyteen4a03",
    "scoot",
    "fragmer",
    "cat",
    "allie",
    "pyropyro",
]

FORMAT_LENGTHS = {
    "b": 1,
    "a": 1024,
    "s": 64,
    "h": 2,
    "i": 4,
    }

TYPE_INITIAL = 0
TYPE_KEEPALIVE = 1
TYPE_PRECHUNK = 2
TYPE_CHUNK = 3
TYPE_LEVELSIZE = 4
TYPE_BLOCKCHANGE = 5
TYPE_BLOCKSET = 6
TYPE_SPAWNPOINT = 7
TYPE_PLAYERPOS = 8
TYPE_NINE = 9
TYPE_TEN = 10
TYPE_PLAYERDIR = 11
TYPE_PLAYERLEAVE = 12
TYPE_MESSAGE = 13
TYPE_ERROR = 14
TYPE_EXTINFO = 16
TYPE_EXTENTRY = 17
TYPE_CUSTOMBLOCKSUPPORTLEVEL = 19
TYPE_ENVSETCOLOR = 25
TYPE_ENVSETWEATHER = 31

from arc.format import Format

TYPE_FORMATS = {
    TYPE_INITIAL: Format("bssb"),
    TYPE_KEEPALIVE: Format(""),
    TYPE_PRECHUNK: Format(""),
    TYPE_CHUNK: Format("hab"),
    TYPE_LEVELSIZE: Format("hhh"),
    TYPE_BLOCKCHANGE: Format("hhhbb"),
    TYPE_BLOCKSET: Format("hhhb"),
    TYPE_SPAWNPOINT: Format("bshhhbb"),
    TYPE_PLAYERPOS: Format("bhhhbb"),
    TYPE_NINE: Format("bbbbbb"),
    TYPE_TEN: Format("bbbb"),
    TYPE_PLAYERDIR: Format("bbb"),
    TYPE_PLAYERLEAVE: Format("b"),
    TYPE_MESSAGE: Format("bs"),
    TYPE_ERROR: Format("s"),
    TYPE_EXTINFO: Format("sh"),
    TYPE_EXTENTRY: Format("si"),
    TYPE_CUSTOMBLOCKSUPPORTLEVEL: Format("b"),
    TYPE_ENVSETCOLOR: Format("bhhh"),
    TYPE_ENVSETWEATHER: Format("b")
}

TASK_BLOCKSET = 1
TASK_PLAYERPOS = 2
TASK_MESSAGE = 3
TASK_NEWPLAYER = 4
TASK_PLAYERLEAVE = 5
TASK_PLAYERDIR = 6
TASK_WORLDCHANGE = 7
TASK_PHYSICSON = 8
TASK_PHYSICSOFF = 9
TASK_FLUSH = 10
TASK_BLOCKGET = 11
TASK_STOP = 12
TASK_PLAYERCONNECT = 13
TASK_UNFLOOD = 14
TASK_FWATERON = 15
TASK_FWATEROFF = 16
TASK_PLAYERRESPAWN = 17
TASK_INSTANTRESPAWN = 18

COLOUR_BLACK = "&0"
COLOUR_DARKBLUE = "&1"
COLOUR_DARKGREEN = "&2"
COLOUR_DARKCYAN = "&3"
COLOUR_DARKRED = "&4"
COLOUR_DARKPURPLE = "&5"
COLOUR_DARKYELLOW = "&6"
COLOUR_GREY = "&7"
COLOUR_DARKGREY = "&8"
COLOUR_BLUE = "&9"
COLOUR_GREEN = "&a"
COLOUR_CYAN = "&b"
COLOUR_RED = "&c"
COLOUR_PURPLE = "&d"
COLOUR_YELLOW = "&e"
COLOUR_WHITE = "&f"

IRCCOLOUR_BLACK = chr(3) + '1'
IRCCOLOUR_DARKBLUE = chr(3) + '2'
IRCCOLOUR_DARKGREEN = chr(3) + '3'
IRCCOLOUR_DARKCYAN = chr(3) + '10'
IRCCOLOUR_DARKRED = chr(3) + '5'
IRCCOLOUR_DARKPURPLE = chr(3) + '6'
IRCCOLOUR_DARKYELLOW = chr(3) + '7'
IRCCOLOUR_GREY = chr(3) + '15'
IRCCOLOUR_DARKGREY = chr(3) + '14'
IRCCOLOUR_BLUE = chr(3) + '12'
IRCCOLOUR_GREEN = chr(3) + '9'
IRCCOLOUR_CYAN = chr(3) + '11'
IRCCOLOUR_RED = chr(3) + '4'
IRCCOLOUR_PURPLE = chr(3) + '13'
IRCCOLOUR_YELLOW = chr(3) + '8'
IRCCOLOUR_WHITE = chr(3) + '0'

IRCCOLOUR_DEFAULT = chr(15)
IRCCOLOUR_BOLD = chr(2)
IRCCOLOUR_UNDERLINE = chr(31)

BLOCK_NOTHING = 0
BLOCK_NONE = 0
BLOCK_EMPTY = 0
BLOCK_AIR = 0
BLOCK_BLANK = 0
BLOCK_CLEAR = 0
BLOCK_ROCK = 1
BLOCK_STONE = 1
BLOCK_GRASS = 2
BLOCK_DIRT = 3
BLOCK_STONES = 4
BLOCK_COBBLESTONE = 4
BLOCK_COBBLESTONES = 4
BLOCK_COBBLE = 4
BLOCK_WOOD = 5
BLOCK_PLANK = 5
BLOCK_PLANKS = 5
BLOCK_PLANT = 6
BLOCK_SHRUB = 6
BLOCK_SAPLING = 6
BLOCK_ADMINIUM = 7
BLOCK_OPIUM = 7
BLOCK_ADMINCRETE = 7
BLOCK_BEDROCK = 7
BLOCK_SOLID = 7
BLOCK_WATER = 8
BLOCK_STILL_WATER = 9
BLOCK_STILLWATER = 9
BLOCK_WATERVATOR = 9
BLOCK_LAVA = 10
BLOCK_MAGMA = 10
BLOCK_STILL_LAVA = 11
BLOCK_STILLLAVA = 11
BLOCK_LAVAVATOR = 11
BLOCK_SAND = 12
BLOCK_GRAVEL = 13
BLOCK_GOLD_ORE = 14
BLOCK_GOLDORE = 14
BLOCK_IRON_ORE = 15
BLOCK_IRONORE = 15
BLOCK_COALORE = 16
BLOCK_COAL_ORE = 16
BLOCK_COAL = 16
BLOCK_LOG = 17
BLOCK_TRUNK = 17
BLOCK_STUMP = 17
BLOCK_LEAVES = 18
BLOCK_LEAF = 18
BLOCK_FOLIAGE = 18
BLOCK_SPONGE = 19
BLOCK_SPENG = 19
BLOCK_CHEESE = 19
BLOCK_GLASS = 20
BLOCK_RED_CLOTH = 21
BLOCK_RED = 21
BLOCK_ORANGE_CLOTH = 22
BLOCK_ORANGE = 22
BLOCK_YELLOW_CLOTH = 23
BLOCK_YELLOW = 23
BLOCK_LIME_CLOTH = 24
BLOCK_LIME = 24
BLOCK_LIGHTGREEN = 24
BLOCK_LIGHTGREEN_CLOTH = 24
BLOCK_LIGHT_GREEN = 24
BLOCK_LIGHT_GREEN_CLOTH = 24
BLOCK_GREEN_CLOTH = 25
BLOCK_GREEN = 25
BLOCK_TURQUOISE_CLOTH = 26
BLOCK_TURQUOISE = 26
BLOCK_TEAL = 26
BLOCK_TEAL_CLOTH = 26
BLOCK_AQUA = 27
BLOCK_AQUA_CLOTH = 27
BLOCK_CYAN = 28
BLOCK_CYAN_CLOTH = 28
BLOCK_DARKBLUE = 29
BLOCK_DARKBLUE_CLOTH = 29
BLOCK_BLUE = 29
BLOCK_BLUE_CLOTH = 29
BLOCK_INDIGO_CLOTH = 30
BLOCK_INDIGO = 30
BLOCK_VIOLET_CLOTH = 31
BLOCK_VIOLET = 31
BLOCK_MAGENTA_CLOTH = 32
BLOCK_MAGENTA = 32
BLOCK_PINK_CLOTH = 33
BLOCK_PINK = 33
BLOCK_DARKGREY_CLOTH = 34
BLOCK_DARKGREY = 34
BLOCK_DARKGRAY_CLOTH = 34
BLOCK_DARKGRAY = 34
BLOCK_DARK_GREY_CLOTH = 34
BLOCK_DARK_GREY = 34
BLOCK_DARK_GRAY_CLOTH = 34
BLOCK_DARK_GRAY = 34
BLOCK_BLACK = 34
BLOCK_BLACK_CLOTH = 34
BLOCK_GREY_CLOTH = 35
BLOCK_GRAY_CLOTH = 35
BLOCK_GREY = 35
BLOCK_GRAY = 35
BLOCK_WHITE_CLOTH = 36
BLOCK_WHITE = 36
BLOCK_YELLOW_FLOWER = 37
BLOCK_YELLOWFLOWER = 37
BLOCK_RED_FLOWER = 38
BLOCK_REDFLOWER = 38
BLOCK_BROWN_MUSHROOM = 39
BLOCK_BROWN_SHROOM = 39
BLOCK_BROWNMUSHROOM = 39
BLOCK_SHROOM = 39
BLOCK_MUSHROOM = 39
BLOCK_MUSHROOMS = 39
BLOCK_RED_MUSHROOM = 40
BLOCK_TOADSTOOL = 40
BLOCK_RED_SHROOM = 40
BLOCK_GOLD = 41
BLOCK_STEEL = 42
BLOCK_IRON = 42
BLOCK_SILVER = 42
BLOCK_METAL = 42
BLOCK_DOUBLE_STAIR = 43
BLOCK_DOUBLESTEP = 43
BLOCK_DOUBLE_STEP = 43
BLOCK_DOUBLESTAIR = 43
BLOCK_DOUBLESLAB = 43
BLOCK_DOUBLE_SLAB = 43
BLOCK_SLAB = 44
BLOCK_STAIR = 44
BLOCK_STEP = 44
BLOCK_HALFSTEP = 44
BLOCK_BRICK = 45
BLOCK_TNT = 46
BLOCK_DYNAMITE = 46
BLOCK_EXPLOSIVE = 46
BLOCK_BOOKCASE = 47
BLOCK_BOOKSHELF = 47
BLOCK_SHELF = 47
BLOCK_BOOKS = 47
BLOCK_MOSSY_COBBLESTONE = 48
BLOCK_MOSS = 48
BLOCK_MOSSY = 48
BLOCK_MOSSYCOBBLESTONE = 48
BLOCK_MOSSY_STONE = 48
BLOCK_MOSSYSTONE = 48
BLOCK_MOSSY_ROCK = 48
BLOCK_MOSSYROCK = 48
BLOCK_OBSIDIAN = 49

#cpe blocks
BLOCK_COBBLESTONESLAB = 50
BLOCK_COBBLESLAB = 50
BLOCK_COBBLESTONEHALFSTEP = 50
BLOCK_COBBLEHALFSTEP = 50

BLOCK_ROPE = 51

BLOCK_SANDSTONE = 52

BLOCK_SNOW = 53

BLOCK_FIRE = 54

BLOCK_LIGHTPINK = 55
BLOCK_LIGHTPINK_CLOTH = 55

BLOCK_FORESTGREEN = 56
BLOCK_FORESTGREEN_CLOTH = 56

BLOCK_BROWN = 57
BLOCK_BROWN_CLOTH = 57

BLOCK_DEEPBLUE = 58
BLOCK_DEEPBLUE_CLOTH = 58

BLOCK_TURQUOISE = 59
BLOCK_TURQUOISE_CLOTH = 59

BLOCK_ICE = 60

BLOCK_CERAMICTILE = 61
BLOCK_CERAMIC = 61
BLOCK_TILE = 61

BLOCK_MAGMA = 62

BLOCK_PILLAR = 63
BLOCK_QUARTZ = 63

BLOCK_CRATE = 64
BLOCK_BOX = 64

BLOCK_STONEBRICK = 65

CPE_FALLBACKS = {
    BLOCK_COBBLESTONESLAB: BLOCK_HALFSTEP,
    BLOCK_ROPE: BLOCK_BROWNMUSHROOM,
    BLOCK_SANDSTONE: BLOCK_SAND,
    BLOCK_SNOW: BLOCK_AIR,
    BLOCK_FIRE: BLOCK_LAVA,
    BLOCK_LIGHTPINK: BLOCK_PINK,
    BLOCK_FORESTGREEN: BLOCK_GREEN,
    BLOCK_BROWN: BLOCK_DIRT,
    BLOCK_DEEPBLUE: BLOCK_BLUE,
    BLOCK_TURQUOISE: BLOCK_CYAN,
    BLOCK_ICE: BLOCK_GLASS,
    BLOCK_CERAMICTILE: BLOCK_IRON,
    BLOCK_MAGMA: BLOCK_OBSIDIAN,
    BLOCK_PILLAR: BLOCK_WHITE,
    BLOCK_CRATE: BLOCK_PLANKS,
    BLOCK_STONEBRICK: BLOCK_STONE
}

BlockList = [
    "air",
    "rock",
    "grass",
    "dirt",
    "stone",
    "wood",
    "plant",
    "adminblock",
    "water",
    "still water",
    "lava",
    "still lava",
    "sand",
    "gravel",
    "goldore",
    "ironore",
    "coal",
    "log",
    "leaves",
    "sponge",
    "glass",
    "red",
    "orange",
    "yellow",
    "lime",
    "green",
    "turquoise",
    "cyan",
    "blue",
    "indigo",
    "violet",
    "purple",
    "magenta",
    "pink",
    "black",
    "grey",
    "white",
    "yellow flower",
    "red flower",
    "brown mushroom",
    "red mushroom",
    "gold",
    "iron",
    "step",
    "doublestep",
    "brick",
    "tnt",
    "bookcase",
    "moss",
    "obsidian",
    "cobblestone slab",
    "rope",
    "sandstone",
    "snow",
    "fire",
    "light pink",
    "forest green",
    "brown",
    "deep blue",
    "turquoise",
    "ice",
    "ceramic tile",
    "magma",
    "pillar",
    "crate",
    "stonebrick"
]
MSGLOGFORMAT = {
    "chat": "[%{time}s] %{username}s: %{text}s",
    "staff": "[%{time}s] #%{username}s: %{text}s",
    "irc": "[%{time}s] %{username}s %{text}s",
    "action": "[%{time}s] * %{username}s %{text}s",
    "whisper": "[%{time}s] %{self}s to %{other}s: %{text}s",
    "world": "[%{time}s] %{username}s in %{world}s: %{text}s",
    "main": "",
    "server": "[%{time}s] %{text}s"
}
MSGREPLACE = {
    "escape_commands": {"./": " /", ".!": " !"},
    }
MSGREPLACE["game_colour_to_irc"] = {
    COLOUR_BLACK: IRCCOLOUR_BLACK,
    COLOUR_DARKBLUE: IRCCOLOUR_DARKBLUE,
    COLOUR_DARKGREEN: IRCCOLOUR_DARKGREEN,
    COLOUR_DARKCYAN: IRCCOLOUR_DARKCYAN,
    COLOUR_DARKRED: IRCCOLOUR_DARKRED,
    COLOUR_DARKPURPLE: IRCCOLOUR_DARKPURPLE,
    COLOUR_DARKYELLOW: IRCCOLOUR_DARKYELLOW,
    COLOUR_GREY: IRCCOLOUR_GREY,
    COLOUR_DARKGREY: IRCCOLOUR_DARKGREY,
    COLOUR_BLUE: IRCCOLOUR_BLUE,
    COLOUR_GREEN: IRCCOLOUR_GREEN,
    COLOUR_CYAN: IRCCOLOUR_CYAN,
    COLOUR_RED: IRCCOLOUR_RED,
    COLOUR_PURPLE: IRCCOLOUR_PURPLE,
    COLOUR_YELLOW: IRCCOLOUR_YELLOW,
    COLOUR_WHITE: IRCCOLOUR_WHITE
}
MSGREPLACE["text_colour_to_game"] = {# % to &
                                     "%0": "&0",
                                     "%1": "&1",
                                     "%2": "&2",
                                     "%3": "&3",
                                     "%4": "&4",
                                     "%5": "&5",
                                     "%6": "&6",
                                     "%7": "&7",
                                     "%8": "&8",
                                     "%9": "&9",
                                     "%a": "&a",
                                     "%b": "&b",
                                     "%c": "&c",
                                     "%d": "&d",
                                     "%e": "&e",
                                     "%f": "&f"
}

WEATHER = {
    'none': 0,
    'rain': 1,
    'snow': 2
}

from arc.globals import invertDict

MSGREPLACE["irc_colour_to_game"] = invertDict(MSGREPLACE["game_colour_to_irc"])

import string
PRINTABLE = string.printable

class ServerFull(Exception):
    pass
