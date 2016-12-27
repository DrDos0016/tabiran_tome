# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals


from django.db import models

# Create your models here.
class Team(models.Model):
    name            = models.CharField(max_length=100)
    joined          = models.DateField()
    favor_earned    = models.IntegerField(default=0)
    favor_spent     = models.IntegerField(default=0)
    rep_keepers     = models.IntegerField(default=0)
    rep_trackers    = models.IntegerField(default=0)
    rep_scholars    = models.IntegerField(default=0)
    rep_artisans    = models.IntegerField(default=0)
    teammates       = models.ManyToManyField("Pokemon", related_name="team_id")
    authors         = models.ManyToManyField("User", related_name="team_id")
    logbooks        = models.ManyToManyField("Logbook", related_name="team_id")
    
    cameos          = models.CharField(max_length=12, default="No")
    type            = models.CharField(max_length=12, default="Drawn", blank=True) # Drawn/Written/Hybrid
    tumblr          = models.URLField(default="", blank=True)
    verified        = models.BooleanField(default=False)
    
    def __unicode__(self):
        output = self.name + str(self.joined)
        return output
    
    def favor(self):
        return self.favor_earned - self.favor_spent
    
class Pokemon(models.Model):
    status          = models.CharField(default="Active", max_length=20) # Activate/Retired/Deceased/Whatever you want
    species         = models.IntegerField()
    species_line    = models.IntegerField()
    shiny           = models.BooleanField(default=False)
    name            = models.CharField(max_length=80)
    gender          = models.CharField(max_length=20, default="", blank=True)
    
    def __unicode__(self):
        output = "Name: " + self.name + "\n"
        output += "Species: " + str(self.species) + "\n"
        return output
        
    def species_name(self):
        NUM_TO_NAME     = {-2:"Other", -1:"Egg", 1:"Bulbasaur", 2:"Ivysaur", 3:"Venusaur", 4:"Charmander", 5:"Charmeleon", 6:"Charizard", 7:"Squirtle", 8:"Wartortle", 9:"Blastoise", 10:"Caterpie", 11:"Metapod", 12:"Butterfree", 13:"Weedle", 14:"Kakuna", 15:"Beedrill", 16:"Pidgey", 17:"Pidgeotto", 18:"Pidgeot", 19:"Rattata", 20:"Raticate", 21:"Spearow", 22:"Fearow", 23:"Ekans", 24:"Arbok", 25:"Pikachu", 26:"Raichu", 27:"Sandshrew", 28:"Sandslash", 29:u"Nidoran?", 30:"Nidorina", 31:"Nidoqueen", 32:u"Nidoran?", 33:"Nidorino", 34:"Nidoking", 35:"Clefairy", 36:"Clefable", 37:"Vulpix", 38:"Ninetales", 39:"Jigglypuff", 40:"Wigglytuff", 41:"Zubat", 42:"Golbat", 43:"Oddish", 44:"Gloom", 45:"Vileplume", 46:"Paras", 47:"Parasect", 48:"Venonat", 49:"Venomoth", 50:"Diglett", 51:"Dugtrio", 52:"Meowth", 53:"Persian", 54:"Psyduck", 55:"Golduck", 56:"Mankey", 57:"Primeape", 58:"Growlithe", 59:"Arcanine", 60:"Poliwag", 61:"Poliwhirl", 62:"Poliwrath", 63:"Abra", 64:"Kadabra", 65:"Alakazam", 66:"Machop", 67:"Machoke", 68:"Machamp", 69:"Bellsprout", 70:"Weepinbell", 71:"Victreebel", 72:"Tentacool", 73:"Tentacruel", 74:"Geodude", 75:"Graveler", 76:"Golem", 77:"Ponyta", 78:"Rapidash", 79:"Slowpoke", 80:"Slowbro", 81:"Magnemite", 82:"Magneton", 83:"Farfetch'd", 84:"Doduo", 85:"Dodrio", 86:"Seel", 87:"Dewgong", 88:"Grimer", 89:"Muk", 90:"Shellder", 91:"Cloyster", 92:"Gastly", 93:"Haunter", 94:"Gengar", 95:"Onix", 96:"Drowzee", 97:"Hypno", 98:"Krabby", 99:"Kingler", 100:"Voltorb", 101:"Electrode", 102:"Exeggcute", 103:"Exeggutor", 104:"Cubone", 105:"Marowak", 106:"Hitmonlee", 107:"Hitmonchan", 108:"Lickitung", 109:"Koffing", 110:"Weezing", 111:"Rhyhorn", 112:"Rhydon", 113:"Chansey", 114:"Tangela", 115:"Kangaskhan", 116:"Horsea", 117:"Seadra", 118:"Goldeen", 119:"Seaking", 120:"Staryu", 121:"Starmie", 122:"Mr. Mime", 123:"Scyther", 124:"Jynx", 125:"Electabuzz", 126:"Magmar", 127:"Pinsir", 128:"Tauros", 129:"Magikarp", 130:"Gyarados", 131:"Lapras", 132:"Ditto", 133:"Eevee", 134:"Vaporeon", 135:"Jolteon", 136:"Flareon", 137:"Porygon", 138:"Omanyte", 139:"Omastar", 140:"Kabuto", 141:"Kabutops", 142:"Aerodactyl", 143:"Snorlax", 144:"Articuno", 145:"Zapdos", 146:"Moltres", 147:"Dratini", 148:"Dragonair", 149:"Dragonite", 150:"Mewtwo", 151:"Mew ", 152:"Chikorita", 153:"Bayleef", 154:"Meganium", 155:"Cyndaquil", 156:"Quilava", 157:"Typhlosion", 158:"Totodile", 159:"Croconaw", 160:"Feraligatr", 161:"Sentret", 162:"Furret", 163:"Hoothoot", 164:"Noctowl", 165:"Ledyba", 166:"Ledian", 167:"Spinarak", 168:"Ariados", 169:"Crobat", 170:"Chinchou", 171:"Lanturn", 172:"Pichu", 173:"Cleffa", 174:"Igglybuff", 175:"Togepi", 176:"Togetic", 177:"Natu", 178:"Xatu", 179:"Mareep", 180:"Flaaffy", 181:"Ampharos", 182:"Bellossom", 183:"Marill", 184:"Azumarill", 185:"Sudowoodo", 186:"Politoed", 187:"Hoppip", 188:"Skiploom", 189:"Jumpluff", 190:"Aipom", 191:"Sunkern", 192:"Sunflora", 193:"Yanma", 194:"Wooper", 195:"Quagsire", 196:"Espeon", 197:"Umbreon", 198:"Murkrow", 199:"Slowking", 200:"Misdreavus", 201:"Unown", 202:"Wobbuffet", 203:"Girafarig", 204:"Pineco", 205:"Forretress", 206:"Dunsparce", 207:"Gligar", 208:"Steelix", 209:"Snubbull", 210:"Granbull", 211:"Qwilfish", 212:"Scizor", 213:"Shuckle", 214:"Heracross", 215:"Sneasel", 216:"Teddiursa", 217:"Ursaring", 218:"Slugma", 219:"Magcargo", 220:"Swinub", 221:"Piloswine", 222:"Corsola", 223:"Remoraid", 224:"Octillery", 225:"Delibird", 226:"Mantine", 227:"Skarmory", 228:"Houndour", 229:"Houndoom", 230:"Kingdra", 231:"Phanpy", 232:"Donphan", 233:"Porygon2", 234:"Stantler", 235:"Smeargle", 236:"Tyrogue", 237:"Hitmontop", 238:"Smoochum", 239:"Elekid", 240:"Magby", 241:"Miltank", 242:"Blissey", 243:"Raikou", 244:"Entei", 245:"Suicune", 246:"Larvitar", 247:"Pupitar", 248:"Tyranitar", 249:"Lugia", 250:"Ho-Oh", 251:"Celebi ", 252:"Treecko", 253:"Grovyle", 254:"Sceptile", 255:"Torchic", 256:"Combusken", 257:"Blaziken", 258:"Mudkip", 259:"Marshtomp", 260:"Swampert", 261:"Poochyena", 262:"Mightyena", 263:"Zigzagoon", 264:"Linoone", 265:"Wurmple", 266:"Silcoon", 267:"Beautifly", 268:"Cascoon", 269:"Dustox", 270:"Lotad", 271:"Lombre", 272:"Ludicolo", 273:"Seedot", 274:"Nuzleaf", 275:"Shiftry", 276:"Taillow", 277:"Swellow", 278:"Wingull", 279:"Pelipper", 280:"Ralts", 281:"Kirlia", 282:"Gardevoir", 283:"Surskit", 284:"Masquerain", 285:"Shroomish", 286:"Breloom", 287:"Slakoth", 288:"Vigoroth", 289:"Slaking", 290:"Nincada", 291:"Ninjask", 292:"Shedinja", 293:"Whismur", 294:"Loudred", 295:"Exploud", 296:"Makuhita", 297:"Hariyama", 298:"Azurill", 299:"Nosepass", 300:"Skitty", 301:"Delcatty", 302:"Sableye", 303:"Mawile", 304:"Aron", 305:"Lairon", 306:"Aggron", 307:"Meditite", 308:"Medicham", 309:"Electrike", 310:"Manectric", 311:"Plusle", 312:"Minun", 313:"Volbeat", 314:"Illumise", 315:"Roselia", 316:"Gulpin", 317:"Swalot", 318:"Carvanha", 319:"Sharpedo", 320:"Wailmer", 321:"Wailord", 322:"Numel", 323:"Camerupt", 324:"Torkoal", 325:"Spoink", 326:"Grumpig", 327:"Spinda", 328:"Trapinch", 329:"Vibrava", 330:"Flygon", 331:"Cacnea", 332:"Cacturne", 333:"Swablu", 334:"Altaria", 335:"Zangoose", 336:"Seviper", 337:"Lunatone", 338:"Solrock", 339:"Barboach", 340:"Whiscash", 341:"Corphish", 342:"Crawdaunt", 343:"Baltoy", 344:"Claydol", 345:"Lileep", 346:"Cradily", 347:"Anorith", 348:"Armaldo", 349:"Feebas", 350:"Milotic", 351:"Castform", 352:"Kecleon", 353:"Shuppet", 354:"Banette", 355:"Duskull", 356:"Dusclops", 357:"Tropius", 358:"Chimecho", 359:"Absol", 360:"Wynaut", 361:"Snorunt", 362:"Glalie", 363:"Spheal", 364:"Sealeo", 365:"Walrein", 366:"Clamperl", 367:"Huntail", 368:"Gorebyss", 369:"Relicanth", 370:"Luvdisc", 371:"Bagon", 372:"Shelgon", 373:"Salamence", 374:"Beldum", 375:"Metang", 376:"Metagross", 377:"Regirock", 378:"Regice", 379:"Registeel", 380:"Latias", 381:"Latios", 382:"Kyogre", 383:"Groudon", 384:"Rayquaza", 385:"Jirachi", 386:"Deoxys ", 387:"Turtwig", 388:"Grotle", 389:"Torterra", 390:"Chimchar", 391:"Monferno", 392:"Infernape", 393:"Piplup", 394:"Prinplup", 395:"Empoleon", 396:"Starly", 397:"Staravia", 398:"Staraptor", 399:"Bidoof", 400:"Bibarel", 401:"Kricketot", 402:"Kricketune", 403:"Shinx", 404:"Luxio", 405:"Luxray", 406:"Budew", 407:"Roserade", 408:"Cranidos", 409:"Rampardos", 410:"Shieldon", 411:"Bastiodon", 412:"Burmy", 413:"Wormadam", 414:"Mothim", 415:"Combee", 416:"Vespiquen", 417:"Pachirisu", 418:"Buizel", 419:"Floatzel", 420:"Cherubi", 421:"Cherrim", 422:"Shellos", 423:"Gastrodon", 424:"Ambipom", 425:"Drifloon", 426:"Drifblim", 427:"Buneary", 428:"Lopunny", 429:"Mismagius", 430:"Honchkrow", 431:"Glameow", 432:"Purugly", 433:"Chingling", 434:"Stunky", 435:"Skuntank", 436:"Bronzor", 437:"Bronzong", 438:"Bonsly", 439:"Mime Jr.", 440:"Happiny", 441:"Chatot", 442:"Spiritomb", 443:"Gible", 444:"Gabite", 445:"Garchomp", 446:"Munchlax", 447:"Riolu", 448:"Lucario", 449:"Hippopotas", 450:"Hippowdon", 451:"Skorupi", 452:"Drapion", 453:"Croagunk", 454:"Toxicroak", 455:"Carnivine", 456:"Finneon", 457:"Lumineon", 458:"Mantyke", 459:"Snover", 460:"Abomasnow", 461:"Weavile", 462:"Magnezone", 463:"Lickilicky", 464:"Rhyperior", 465:"Tangrowth", 466:"Electivire", 467:"Magmortar", 468:"Togekiss", 469:"Yanmega", 470:"Leafeon", 471:"Glaceon", 472:"Gliscor", 473:"Mamoswine", 474:"Porygon-Z", 475:"Gallade", 476:"Probopass", 477:"Dusknoir", 478:"Froslass", 479:"Rotom", 480:"Uxie", 481:"Mesprit", 482:"Azelf", 483:"Dialga", 484:"Palkia", 485:"Heatran", 486:"Regigigas", 487:"Giratina", 488:"Cresselia", 489:"Phione", 490:"Manaphy", 491:"Darkrai", 492:"Shaymin", 493:"Arceus ", 494:"Victini", 495:"Snivy", 496:"Servine", 497:"Serperior", 498:"Tepig", 499:"Pignite", 500:"Emboar", 501:"Oshawott", 502:"Dewott", 503:"Samurott", 504:"Patrat", 505:"Watchog", 506:"Lillipup", 507:"Herdier", 508:"Stoutland", 509:"Purrloin", 510:"Liepard", 511:"Pansage", 512:"Simisage", 513:"Pansear", 514:"Simisear", 515:"Panpour", 516:"Simipour", 517:"Munna", 518:"Musharna", 519:"Pidove", 520:"Tranquill", 521:"Unfezant", 522:"Blitzle", 523:"Zebstrika", 524:"Roggenrola", 525:"Boldore", 526:"Gigalith", 527:"Woobat", 528:"Swoobat", 529:"Drilbur", 530:"Excadrill", 531:"Audino", 532:"Timburr", 533:"Gurdurr", 534:"Conkeldurr", 535:"Tympole", 536:"Palpitoad", 537:"Seismitoad", 538:"Throh", 539:"Sawk", 540:"Sewaddle", 541:"Swadloon", 542:"Leavanny", 543:"Venipede", 544:"Whirlipede", 545:"Scolipede", 546:"Cottonee", 547:"Whimsicott", 548:"Petilil", 549:"Lilligant", 550:"Basculin", 551:"Sandile", 552:"Krokorok", 553:"Krookodile", 554:"Darumaka", 555:"Darmanitan", 556:"Maractus", 557:"Dwebble", 558:"Crustle", 559:"Scraggy", 560:"Scrafty", 561:"Sigilyph", 562:"Yamask", 563:"Cofagrigus", 564:"Tirtouga", 565:"Carracosta", 566:"Archen", 567:"Archeops", 568:"Trubbish", 569:"Garbodor", 570:"Zorua", 571:"Zoroark", 572:"Minccino", 573:"Cinccino", 574:"Gothita", 575:"Gothorita", 576:"Gothitelle", 577:"Solosis", 578:"Duosion", 579:"Reuniclus", 580:"Ducklett", 581:"Swanna", 582:"Vanillite", 583:"Vanillish", 584:"Vanilluxe", 585:"Deerling", 586:"Sawsbuck", 587:"Emolga", 588:"Karrablast", 589:"Escavalier", 590:"Foongus", 591:"Amoonguss", 592:"Frillish", 593:"Jellicent", 594:"Alomomola", 595:"Joltik", 596:"Galvantula", 597:"Ferroseed", 598:"Ferrothorn", 599:"Klink", 600:"Klang", 601:"Klinklang", 602:"Tynamo", 603:"Eelektrik", 604:"Eelektross", 605:"Elgyem", 606:"Beheeyem", 607:"Litwick", 608:"Lampent", 609:"Chandelure", 610:"Axew", 611:"Fraxure", 612:"Haxorus", 613:"Cubchoo", 614:"Beartic", 615:"Cryogonal", 616:"Shelmet", 617:"Accelgor", 618:"Stunfisk", 619:"Mienfoo", 620:"Mienshao", 621:"Druddigon", 622:"Golett", 623:"Golurk", 624:"Pawniard", 625:"Bisharp", 626:"Bouffalant", 627:"Rufflet", 628:"Braviary", 629:"Vullaby", 630:"Mandibuzz", 631:"Heatmor", 632:"Durant", 633:"Deino", 634:"Zweilous", 635:"Hydreigon", 636:"Larvesta", 637:"Volcarona", 638:"Cobalion", 639:"Terrakion", 640:"Virizion", 641:"Tornadus", 642:"Thundurus", 643:"Reshiram", 644:"Zekrom", 645:"Landorus", 646:"Kyurem", 647:"Keldeo", 648:"Meloetta", 649:"Genesect ", 650:"Chespin", 651:"Quilladin", 652:"Chesnaught", 653:"Fennekin", 654:"Braixen", 655:"Delphox", 656:"Froakie", 657:"Frogadier", 658:"Greninja", 659:"Bunnelby", 660:"Diggersby", 661:"Fletchling", 662:"Fletchinder", 663:"Talonflame", 664:"Scatterbug", 665:"Spewpa", 666:"Vivillon", 667:"Litleo", 668:"Pyroar", 669:u"Flabébé", 670:"Floette", 671:"Florges", 672:"Skiddo", 673:"Gogoat", 674:"Pancham", 675:"Pangoro", 676:"Furfrou", 677:"Espurr", 678:"Meowstic", 679:"Honedge", 680:"Doublade", 681:"Aegislash", 682:"Spritzee", 683:"Aromatisse", 684:"Swirlix", 685:"Slurpuff", 686:"Inkay", 687:"Malamar", 688:"Binacle", 689:"Barbaracle", 690:"Skrelp", 691:"Dragalge", 692:"Clauncher", 693:"Clawitzer", 694:"Helioptile", 695:"Heliolisk", 696:"Tyrunt", 697:"Tyrantrum", 698:"Amaura", 699:"Aurorus", 700:"Sylveon", 701:"Hawlucha", 702:"Dedenne", 703:"Carbink", 704:"Goomy", 705:"Sliggoo", 706:"Goodra", 707:"Klefki", 708:"Phantump", 709:"Trevenant", 710:"Pumpkaboo", 711:"Gourgeist", 712:"Bergmite", 713:"Avalugg", 714:"Noibat", 715:"Noivern", 716:"Xerneas", 717:"Yveltal", 718:"Zygarde", 719:"Diancie", 720:"Hoopa", 721:"Volcanion", 722:"Rowlet", 723:"Dartrix", 724:"Decidueye", 725:"Litten", 726:"Torracat", 727:"Torracat", 728:"Popplio", 729:"Brionne", 730:"Primarina", 731:"Pikipek", 732:"Trumbeak", 733:"Toucannon", 734:"Yungoos", 735:"Gumshoos", 736:"Grubbin", 737:"Charjabug", 738:"Vikavolt", 739:"Crabrawler", 740:"Crabominable", 741:"Oricorio", 742:"Cutiefly", 743:"Ribombee", 744:"Rockruff", 745:"Lycanroc", 746:"Wishiwashi", 747:"Mareanie", 748:"Toxapex", 749:"Mudbray", 750:"Mudsdale", 751:"Dewpider", 752:"Araquanid", 753:"Fomantis", 754:"Lurantis", 755:"Morelull", 756:"Shiinotic", 757:"Salandit", 758:"Salazzle", 759:"Stufful", 760:"Bewear", 761:"Bounsweet", 762:"Steenee", 763:"Tsareena", 764:"Comfey", 765:"Oranguru", 766:"Passimian", 767:"Wimpod", 768:"Golisopod", 769:"Sandygast", 770:"Palossand", 771:"Pyukumuku", 772:"Type:@Null", 773:"Silvally", 774:"Minior", 775:"Komala", 776:"Turtonator", 777:"Togedemaru", 778:"Mimikyu", 779:"Bruxish", 780:"Drampa", 781:"Dhelmise", 782:"Jangmo-o", 783:"Hakamo-o", 784:"Kommo-o", 785:"Tapu Koko", 786:"Tapu Lele", 787:"Tapu Bulu", 788:"Tapu Fini", 789:"Cosmog", 790:"Cosmoem", 791:"Solgaleo", 792:"Lunala", 793:"Nihilego", 794:"Buzzwole", 795:"Pheromosa", 796:"Xurkitree", 797:"Celesteela", 798:"Kartana", 799:"Guzzlord", 800:"Necrozma", 801:"Magearna", 802:"Marshadow"}
        return NUM_TO_NAME.get(self.species, "MISSINGNO.")
        
    def update_species_line(self):
        PKMN_TO_CHAIN   = {-1:-1, 1:1, 2:1, 3:1, 4:2, 5:2, 6:2, 7:3, 8:3, 9:3, 10:4, 11:4, 12:4, 13:5, 14:5, 15:5, 16:6, 17:6, 18:6, 19:7, 20:7, 21:8, 22:8, 23:9, 24:9, 25:10, 26:10, 172:10, 27:11, 28:11, 29:12, 30:12, 31:12, 32:13, 33:13, 34:13, 35:14, 36:14, 173:14, 37:15, 38:15, 39:16, 40:16, 174:16, 41:17, 42:17, 169:17, 43:18, 44:18, 45:18, 182:18, 46:19, 47:19, 48:20, 49:20, 50:21, 51:21, 52:22, 53:22, 54:23, 55:23, 56:24, 57:24, 58:25, 59:25, 60:26, 61:26, 62:26, 186:26, 63:27, 64:27, 65:27, 66:28, 67:28, 68:28, 69:29, 70:29, 71:29, 72:30, 73:30, 74:31, 75:31, 76:31, 77:32, 78:32, 79:33, 80:33, 199:33, 81:34, 82:34, 462:34, 83:35, 84:36, 85:36, 86:37, 87:37, 88:38, 89:38, 90:39, 91:39, 92:40, 93:40, 94:40, 95:41, 208:41, 96:42, 97:42, 98:43, 99:43, 100:44, 101:44, 102:45, 103:45, 104:46, 105:46, 106:47, 107:47, 236:47, 237:47, 108:48, 463:48, 109:49, 110:49, 111:50, 112:50, 464:50, 113:51, 242:51, 440:51, 114:52, 465:52, 115:53, 116:54, 117:54, 230:54, 118:55, 119:55, 120:56, 121:56, 122:57, 439:57, 123:58, 212:58, 124:59, 238:59, 125:60, 239:60, 466:60, 126:61, 240:61, 467:61, 127:62, 128:63, 129:64, 130:64, 131:65, 132:66, 133:67, 134:67, 135:67, 136:67, 196:67, 197:67, 470:67, 471:67, 700:67, 137:68, 233:68, 474:68, 138:69, 139:69, 140:70, 141:70, 142:71, 143:72, 446:72, 144:73, 145:74, 146:75, 147:76, 148:76, 149:76, 150:77, 151:78, 152:79, 153:79, 154:79, 155:80, 156:80, 157:80, 158:81, 159:81, 160:81, 161:82, 162:82, 163:83, 164:83, 165:84, 166:84, 167:85, 168:85, 170:86, 171:86, 175:87, 176:87, 468:87, 177:88, 178:88, 179:89, 180:89, 181:89, 183:90, 184:90, 298:90, 185:91, 438:91, 187:92, 188:92, 189:92, 190:93, 424:93, 191:94, 192:94, 193:95, 469:95, 194:96, 195:96, 198:97, 430:97, 200:98, 429:98, 201:99, 202:100, 360:100, 203:101, 204:102, 205:102, 206:103, 207:104, 472:104, 209:105, 210:105, 211:106, 213:107, 214:108, 215:109, 461:109, 216:110, 217:110, 218:111, 219:111, 220:112, 221:112, 473:112, 222:113, 223:114, 224:114, 225:115, 226:116, 458:116, 227:117, 228:118, 229:118, 231:119, 232:119, 234:120, 235:121, 241:122, 243:123, 244:124, 245:125, 246:126, 247:126, 248:126, 249:127, 250:128, 251:129, 252:130, 253:130, 254:130, 255:131, 256:131, 257:131, 258:132, 259:132, 260:132, 261:133, 262:133, 263:134, 264:134, 265:135, 266:135, 267:135, 268:135, 269:135, 270:136, 271:136, 272:136, 273:137, 274:137, 275:137, 276:138, 277:138, 278:139, 279:139, 280:140, 281:140, 282:140, 475:140, 283:141, 284:141, 285:142, 286:142, 287:143, 288:143, 289:143, 290:144, 291:144, 292:144, 293:145, 294:145, 295:145, 296:146, 297:146, 299:147, 476:147, 300:148, 301:148, 302:149, 303:150, 304:151, 305:151, 306:151, 307:152, 308:152, 309:153, 310:153, 311:154, 312:155, 313:156, 314:157, 315:158, 406:158, 407:158, 316:159, 317:159, 318:160, 319:160, 320:161, 321:161, 322:162, 323:162, 324:163, 325:164, 326:164, 327:165, 328:166, 329:166, 330:166, 331:167, 332:167, 333:168, 334:168, 335:169, 336:170, 337:171, 338:172, 339:173, 340:173, 341:174, 342:174, 343:175, 344:175, 345:176, 346:176, 347:177, 348:177, 349:178, 350:178, 351:179, 352:180, 353:181, 354:181, 355:182, 356:182, 477:182, 357:183, 358:184, 433:184, 359:185, 361:186, 362:186, 478:186, 363:187, 364:187, 365:187, 366:188, 367:188, 368:188, 369:189, 370:190, 371:191, 372:191, 373:191, 374:192, 375:192, 376:192, 377:193, 378:194, 379:195, 380:196, 381:197, 382:198, 383:199, 384:200, 385:201, 386:202, 387:203, 388:203, 389:203, 390:204, 391:204, 392:204, 393:205, 394:205, 395:205, 396:206, 397:206, 398:206, 399:207, 400:207, 401:208, 402:208, 403:209, 404:209, 405:209, 408:211, 409:211, 410:212, 411:212, 412:213, 413:213, 414:213, 415:214, 416:214, 417:215, 418:216, 419:216, 420:217, 421:217, 422:218, 423:218, 425:219, 426:219, 427:220, 428:220, 431:221, 432:221, 434:223, 435:223, 436:224, 437:224, 441:228, 442:229, 443:230, 444:230, 445:230, 447:232, 448:232, 449:233, 450:233, 451:234, 452:234, 453:235, 454:235, 455:236, 456:237, 457:237, 459:239, 460:239, 479:240, 480:241, 481:242, 482:243, 483:244, 484:245, 485:246, 486:247, 487:248, 488:249, 489:250, 490:250, 491:252, 492:253, 493:254, 494:255, 495:256, 496:256, 497:256, 498:257, 499:257, 500:257, 501:258, 502:258, 503:258, 504:259, 505:259, 506:260, 507:260, 508:260, 509:261, 510:261, 511:262, 512:262, 513:263, 514:263, 515:264, 516:264, 517:265, 518:265, 519:266, 520:266, 521:266, 522:267, 523:267, 524:268, 525:268, 526:268, 527:269, 528:269, 529:270, 530:270, 531:271, 532:272, 533:272, 534:272, 535:273, 536:273, 537:273, 538:274, 539:275, 540:276, 541:276, 542:276, 543:277, 544:277, 545:277, 546:278, 547:278, 548:279, 549:279, 550:280, 551:281, 552:281, 553:281, 554:282, 555:282, 556:283, 557:284, 558:284, 559:285, 560:285, 561:286, 562:287, 563:287, 564:288, 565:288, 566:289, 567:289, 568:290, 569:290, 570:291, 571:291, 572:292, 573:292, 574:293, 575:293, 576:293, 577:294, 578:294, 579:294, 580:295, 581:295, 582:296, 583:296, 584:296, 585:297, 586:297, 587:298, 588:299, 589:299, 590:300, 591:300, 592:301, 593:301, 594:302, 595:303, 596:303, 597:304, 598:304, 599:305, 600:305, 601:305, 602:306, 603:306, 604:306, 605:307, 606:307, 607:308, 608:308, 609:308, 610:309, 611:309, 612:309, 613:310, 614:310, 615:311, 616:312, 617:312, 618:313, 619:314, 620:314, 621:315, 622:316, 623:316, 624:317, 625:317, 626:318, 627:319, 628:319, 629:320, 630:320, 631:321, 632:322, 633:323, 634:323, 635:323, 636:324, 637:324, 638:325, 639:326, 640:327, 641:328, 642:329, 643:330, 644:331, 645:332, 646:333, 647:334, 648:335, 649:336, 650:337, 651:337, 652:337, 653:338, 654:338, 655:338, 656:339, 657:339, 658:339, 659:340, 660:340, 661:341, 662:341, 663:341, 664:342, 665:342, 666:342, 667:343, 668:343, 669:344, 670:344, 671:344, 672:345, 673:345, 674:346, 675:346, 676:347, 677:348, 678:348, 679:349, 680:349, 681:349, 682:350, 683:350, 684:351, 685:351, 686:352, 687:352, 688:353, 689:353, 690:354, 691:354, 692:355, 693:355, 694:356, 695:356, 696:357, 697:357, 698:358, 699:358, 701:359, 702:360, 703:361, 704:362, 705:362, 706:362, 707:363, 708:364, 709:364, 710:365, 711:365, 712:366, 713:366, 714:367, 715:367, 716:368, 717:369, 718:370, 719:371, 720:372, 721:373, 722:374, 723:374, 724:374, 725:375, 726:375, 727:375, 728:376, 729:376, 730:376, 731:377, 732:377, 733:377, 734:378, 735:378, 736:379, 737:379, 738:379, 739:380, 740:380, 741:381, 742:382, 743:382, 744:383, 745:383, 746:384, 747:385, 748:385, 749:386, 750:386, 751:387, 752:387, 753:388, 754:388, 755:389, 756:389, 757:390, 758:390, 759:391, 760:391, 761:392, 762:392, 763:392, 764:393, 765:394, 766:395, 767:396, 768:396, 769:397, 770:397, 771:398, 772:399, 773:399, 774:400, 775:401, 776:402, 777:403, 778:404, 779:405, 780:406, 781:407, 782:408, 783:408, 784:408, 785:409, 786:410, 787:411, 788:412, 789:413, 790:413, 791:413, 792:413, 793:414, 794:415, 795:416, 796:417, 797:418, 798:419, 799:420, 800:421, 801:422, 802:423}
        return PKMN_TO_CHAIN.get(self.species, -1)
        
    def bubble(self):
        output = '<div class="pokemon-bubble'+(" shiny"*(self.shiny))+(" grayscale"*(self.status.lower() != "active"))+' col">'
        output += '<img src="/assets/images/sprites/icons/'+str(self.species)+'.png" alt="'+self.species_name()+'" title="'+self.species_name()+'"></div>'
        return output
    
class Item(models.Model):
    name        = models.CharField(max_length=80)           # The name of the item
    image       = models.CharField(max_length=40)           # The image filename of the item.
    active      = models.BooleanField(default=False)        # If this item can be added to inventories by members
    url         = models.URLField(default="http://www.talesoftabira.com/wiki/Items", blank=True)   # URL containing an explanation of the item

class Inventory(models.Model):
    team        = models.ForeignKey(Team)                   # The teamID that owns an item.
    item        = models.ForeignKey(Item)                   # The itemID of what the team now has.
    
    def url(self):
        return self.custom_url if custom_url else self.item.url
    
class User(models.Model):
    username        = models.CharField(max_length=20, db_index=True)        # The user's DeviantArt username
    icon            = models.CharField(max_length=70, default="")           # The user's DeviantArt avatar url
    ip              = models.GenericIPAddressField(default="")              # The IP address that last logged with this information
    admin           = models.BooleanField(default=False)                    # Is this account an admin? Yes/No
    beta            = models.BooleanField(default=False)                    # Allow beta features?
    da_id           = models.CharField(max_length=38)                       # DeviantArt API UUID
    
    def image_link(self):
        return '<a href="http://'+self.username+'.deviantart.com" target="_blank"><img src="'+self.icon+'" alt="'+self.username+'" title="'+self.username+'"></a>'
    
class Feed(models.Model):
    team            = models.ForeignKey("Team")
    user            = models.ForeignKey("User")
    type            = models.CharField(max_length=20, default="", blank=True)
    status          = models.TextField()
    timestamp       = models.DateTimeField(auto_now=True)
    
class Event(models.Model):    
    key             = models.CharField(max_length=8, unique=True) # The event key (C1T1 for Chapter 1 Trackers 1)
    name            = models.CharField(max_length=40)
    image           = models.CharField(default="", blank=True, max_length=20)
    active          = models.BooleanField(default=False)
    timestamp       = models.IntegerField()
    #folder          = models.ForeignKey("Gallery", null=True, blank=True, default=None)               # The Gallery entries for this event will be submitted
    order           = models.IntegerField(default=999)
    max_submissions = models.IntegerField(default=1)                                                   # The number of submissions a tema can make under this event)
    
    def guild(self):
        if "T" in self.key:
            return "Trackers"
        elif "A" in self.key:
            return "Artisans"
        elif "S" in self.key:
            return "Scholars"
        elif "K" in self.key:
            return "Keepers"
        else:
            return None

# Pull folders every hour, have site use ajax to also call for anything not yet stored
class Logbook(models.Model):
    event           = models.ForeignKey("Event")
    custom_name     = models.CharField(max_length=80, default="", blank=True)
    order           = models.IntegerField(default=9999)
    deviation       = models.ForeignKey("Deviation", null=True, blank=True)
    
    def __unicode__(self):
        output = "Logbook - " + self.event.name + "\n"
        return output
    
class Gallery(models.Model):
    folder_id       = models.CharField(max_length=36)
    parent          = models.CharField(max_length=36, blank=True, default="", null=True)
    name            = models.CharField(max_length=80)
    monitor         = models.BooleanField(default=False, db_index=True)

class Deviation(models.Model):
    deviation_id    = models.CharField(max_length=38)
    gallery         = models.ForeignKey("Gallery")
    da_url          = models.URLField(default="")
    fav_me_url      = models.URLField(default="", blank=True)
    title           = models.CharField(max_length=80)
    author_name     = models.CharField(max_length=20)
    author_id       = models.CharField(max_length=38)
    timestamp       = models.IntegerField(default=0)
    
    def __unicode__(self):
        output = "#"*40
        id = str(self.id) if self.id else "?"
        output += "DEVIATION: " + id + "\n"
        output += "DA ID    : " + self.deviation_id + "\n"
        output += "TITLE    : " + self.title + "\n"
        output += "DA URL   : " + self.da_url + "\n"
        output += "FAVME URL: " + self.fav_me_url + "\n"
        output += "AUTHOR   : " + self.author_name + "\n"
        output += "AUTHOR ID: " + self.author_id + "\n"
        output += "TIMESTAMP: " + str(self.timestamp) + "\n"
        return output
    
    def url(self):
        if self.fav_me_url:
            return self.fav_me_url
        else:
            return self.da_url

class Token(models.Model):
    value           = models.CharField(max_length=50)
    updated         = models.DateTimeField(auto_now=True)