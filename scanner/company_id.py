"""
Module for turning Bluetooth manufacturer id's into human readable
names.
Master list available from the Bluetooth Special Interest Group:
https://www.bluetooth.com/specifications/assigned-numbers/company-identifiers/
"""


def lookup(company_id):
    """Utility function to easily lookup names of companies from identifier"""
    try:
        manufacturer = company_name[company_id]
    except IndexError:
        manufacturer = 'No name available'
    return manufacturer


company_name = [
    "Ericsson Technology Licensing",
    "Nokia Mobile Phones",
    "Intel Corp.",
    "IBM Corp.",
    "Toshiba Corp.",
    "3Com",
    "Microsoft",
    "Lucent",
    "Motorola",
    "Infineon Technologies AG",
    "Cambridge Silicon Radio",
    "Silicon Wave",
    "Digianswer A/S",
    "Texas Instruments Inc.",
    "Ceva, Inc. (formerly Parthus Technologies, Inc.)",
    "Broadcom Corporation",
    "Mitel Semiconductor",
    "Widcomm, Inc",
    "Zeevo, Inc.",
    "Atmel Corporation",
    "Mitsubishi Electric Corporation",
    "RTX Telecom A/S",
    "KC Technology Inc.",
    "NewLogic",
    "Transilica, Inc.",
    "Rohde & Schwarz GmbH & Co. KG",
    "TTPCom Limited",
    "Signia Technologies, Inc.",
    "Conexant Systems Inc.",
    "Qualcomm",
    "Inventel",
    "AVM Berlin",
    "BandSpeed, Inc.",
    "Mansella Ltd",
    "NEC Corporation",
    "WavePlus Technology Co., Ltd.",
    "Alcatel",
    "NXP Semiconductors (formerly Philips Semiconductors)",
    "C Technologies",
    "Open Interface",
    "R F Micro Devices",
    "Hitachi Ltd",
    "Symbol Technologies, Inc.",
    "Tenovis",
    "Macronix International Co. Ltd.",
    "GCT Semiconductor",
    "Norwood Systems",
    "MewTel Technology Inc.",
    "ST Microelectronics",
    "Synopsis",
    "Red-M (Communications) Ltd",
    "Commil Ltd",
    "Computer Access Technology Corporation (CATC)",
    "Eclipse (HQ Espana) S.L.",
    "Renesas Electronics Corporation",
    "Mobilian Corporation",
    "Terax",
    "Integrated System Solution Corp.",
    "Matsushita Electric Industrial Co., Ltd.",
    "Gennum Corporation",
    "BlackBerry Limited (formerly Research In Motion)",
    "IPextreme, Inc.",
    "Systems and Chips, Inc.",
    "Bluetooth SIG, Inc.",
    "Seiko Epson Corporation",
    "Integrated Silicon Solution Taiwan, Inc.",
    "CONWISE Technology Corporation Ltd",
    "PARROT SA",
    "Socket Mobile",
    "Atheros Communications, Inc.",
    "MediaTek, Inc.",
    "Bluegiga",
    "Marvell Technology Group Ltd.",
    "3DSP Corporation",
    "Accel Semiconductor Ltd.",
    "Continental Automotive Systems",
    "Apple, Inc.",
    "Staccato Communications, Inc.",
    "Avago Technologies",
    "APT Licensing Ltd.",
    "SiRF Technology",
    "Tzero Technologies, Inc.",
    "J&M Corporation",
    "Free2move AB",
    "3DiJoy Corporation",
    "Plantronics, Inc.",
    "Sony Ericsson Mobile Communications",
    "Harman International Industries, Inc.",
    "Vizio, Inc.",
    "Nordic Semiconductor ASA",
    "EM Microelectronic-Marin SA",
    "Ralink Technology Corporation",
    "Belkin International, Inc.",
    "Realtek Semiconductor Corporation",
    "Stonestreet One, LLC",
    "Wicentric, Inc.",
    "RivieraWaves S.A.S",
    "RDA Microelectronics",
    "Gibson Guitars",
    "MiCommand Inc.",
    "Band XI International, LLC",
    "Hewlett-Packard Company",
    "9Solutions Oy",
    "GN Netcom A/S",
    "General Motors",
    "A&D Engineering, Inc.",
    "MindTree Ltd.",
    "Polar Electro OY",
    "Beautiful Enterprise Co., Ltd.",
    "BriarTek, Inc.",
    "Summit Data Communications, Inc.",
    "Sound ID",
    "Monster, LLC",
    "connectBlue AB",
    "ShangHai Super Smart Electronics Co. Ltd.",
    "Group Sense Ltd.",
    "Zomm, LLC",
    "Samsung Electronics Co. Ltd.",
    "Creative Technology Ltd.",
    "Laird Technologies",
    "Nike, Inc.",
    "lesswire AG",
    "MStar Semiconductor, Inc.",
    "Hanlynn Technologies",
    "A & R Cambridge",
    "Seers Technology Co. Ltd",
    "Sports Tracking Technologies Ltd.",
    "Autonet Mobile",
    "DeLorme Publishing Company, Inc.",
    "WuXi Vimicro",
    "Sennheiser Communications A/S",
    "TimeKeeping Systems, Inc.",
    "Ludus Helsinki Ltd.",
    "BlueRadios, Inc.",
    "equinox AG",
    "Garmin International, Inc.",
    "Ecotest",
    "GN ReSound A/S",
    "Jawbone",
    "Topcorn Positioning Systems, LLC",
    "Gimbal Inc.",
    "Zscan Software",
    "Quintic Corp.",
    "Stollman E+V GmbH",
    "Funai Electric Co., Ltd.",
    "Advanced PANMOBIL Systems GmbH & Co. KG",
    "ThinkOptics, Inc.",
    "Universal Electronics, Inc.",
    "Airoha Technology Corp.",
    "NEC Lighting, Ltd.",
    "ODM Technology, Inc.",
    "ConnecteDevice Ltd.",
    "zer01.tv GmbH",
    "i.Tech Dynamic Global Distribution Ltd.",
    "Alpwise",
    "Jiangsu Toppower Automotive Electronics Co., Ltd.",
    "Colorfy, Inc.",
    "Geoforce Inc.",
    "Bose Corporation",
    "Suunto Oy",
    "Kensington Computer Products Group",
    "SR-Medizinelektronik",
    "Vertu Corporation Limited",
    "Meta Watch Ltd.",
    "LINAK A/S",
    "OTL Dynamics LLC",
    "Panda Ocean Inc.",
    "Visteon Corporation",
    "ARP Devices Limited",
    "Magneti Marelli S.p.A",
    "CAEN RFID srl",
    "Ingenieur-Systemgruppe Zahn GmbH",
    "Green Throttle Games",
    "Peter Systemtechnik GmbH",
    "Omegawave Oy",
    "Cinetix",
    "Passif Semiconductor Corp",
    "Saris Cycling Group, Inc",
    "​Bekey A/S",
    "​Clarinox Technologies Pty. Ltd.",
    "​BDE Technology Co., Ltd.",
    "Swirl Networks",
    "​Meso international",
    "​TreLab Ltd",
    "​Qualcomm Innovation Center, Inc. (QuIC)",
    "​​Johnson Controls, Inc.",
    "​Starkey Laboratories Inc.",
    "​​S-Power Electronics Limited",
    "​​Ace Sensor Inc",
    "​​Aplix Corporation",
    "​​AAMP of America",
    "​​Stalmart Technology Limited",
    "​​AMICCOM Electronics Corporation",
    "​​Shenzhen Excelsecu Data Technology Co.,Ltd",
    "​​Geneq Inc.",
    "​​adidas AG",
    "​​LG Electronics​",
    "​Onset Computer Corporation",
    "​Selfly BV",
    "​Quuppa Oy.",
    "GeLo Inc",
    "Evluma",
    "MC10",
    "Binauric SE",
    "Beats Electronics",
    "Microchip Technology Inc.",
    "Elgato Systems GmbH",
    "ARCHOS SA",
    "Dexcom, Inc.",
    "Polar Electro Europe B.V.",
    "Dialog Semiconductor B.V.",
    "Taixingbang Technology (HK) Co,. LTD.",
    "Kawantech",
    "Austco Communication Systems",
    "Timex Group USA, Inc.",
    "Qualcomm Technologies, Inc.",
    "Qualcomm Connected Experiences, Inc.",
    "Voyetra Turtle Beach",
    "txtr GmbH",
    "Biosentronics",
    "Procter & Gamble",
    "Hosiden Corporation",
    "Muzik LLC",
    "Misfit Wearables Corp",
    "Google",
    "Danlers Ltd",
    "Semilink Inc",
    "inMusic Brands, Inc",
    "L.S. Research Inc.",
    "Eden Software Consultants Ltd.",
    "Freshtemp",
    "​KS Technologies",
    "​ACTS Technologies",
    "​Vtrack Systems",
    "​Nielsen-Kellerman Company",
    "​Server Technology, Inc.",
    "​BioResearch Associates",
    "​Jolly Logic, LLC",
    "​Above Average Outcomes, Inc.",
    "​Bitsplitters GmbH",
    "​PayPal, Inc.",
    "​Witron Technology Limited",
    "​Aether Things Inc. (formerly Morse Project Inc.)",
    "​Kent Displays Inc.",
    "Nautilus Inc​.",
    "​Smartifier Oy",
    "​Elcometer Limited",
    "​VSN Technologies Inc.",
    "​AceUni Corp., Ltd.",
    "​StickNFind",
    "​Crystal Code AB",
    "​KOUKAAM a.s.",
    "Delphi Corporation",
    "​ValenceTech Limited",
    "Reserved",
    "​Typo Products, LLC",
    "​TomTom International BV",
    "​Fugoo, Inc",
    "​Keiser Corporation",
    "​Bang & Olufsen A/S",
    "​PLUS Locations Systems Pty Ltd",
    "​Ubiquitous Computing Technology Corporation",
    "​Innovative Yachtter Solutions",
    "​William Demant Holding A/S",
    "​Chicony Electronics Co., Ltd.",
    "​Atus BV",
    "​Codegate Ltd.",
    "ERi, Inc.",
    "​Transducers Direct, LLC",
    "​Fujitsu Ten Limited",
    "​Audi AG",
    "​HiSilicon Technologies Co., Ltd.",
    "​Nippon Seiki Co., Ltd.",
    "​Steelseries ApS",
    "​vyzybl Inc.",
    "​Openbrain Technologies, Co., Ltd.",
    "​Xensr",
    "e.solutions",
    "​1OAK Technologies",
    "​Wimoto Technologies Inc",
    "​Radius Networks, Inc.",
    "​Wize Technology Co., Ltd.",
    "​Qualcomm Labs, Inc.",
    "​Aruba Networks",
    "​Baidu",
    "​Arendi AG",
    "​Skoda Auto a.s.",
    "​Volkswagon AG",
    "​Porsche AG",
    "​Sino Wealth Electronic Ltd.",
    "​AirTurn, Inc.",
    "​Kinsa, Inc.",
    "​HID Global",
    "​SEAT es",
    "​Promethean Ltd.",
    "​Salutica Allied Solutions",
    "​GPSI Group Pty Ltd",
    "​Nimble Devices Oy",
    "​Changzhou Yongse Infotech Co., Ltd",
    "​SportIQ",
    "​TEMEC Instruments B.V.",
    "​Sony Corporation",
    "​ASSA ABLOY",
    "​Clarion Co., Ltd.",
    "​Warehouse Innovations",
    "​Cypress Semiconductor Corporation",
    "​MADS Inc",
    "​Blue Maestro Limited",
    "​Resolution Products, Inc.",
    "​Airewear LLC",
    "Seed Labs, Inc. (formerly ETC sp. z.o.o.)​",
    "​Prestigio Plaza Ltd.",
    "​NTEO Inc.",
    "​Focus Systems Corporation",
    "​Tencent Holdings Limited",
    "​Allegion",
    "​Murata Manufacuring Co., Ltd.",
    "​Nod, Inc.",
    "​B&B Manufacturing Company",
    "​Alpine Electronics (China) Co., Ltd",
    "​FedEx Services",
    "​Grape Systems Inc.",
    "​Bkon Connect",
    "​Lintech GmbH",
    "​Novatel Wireless",
    "​Ciright",
    "​Mighty Cast, Inc.",
    "​Ambimat Electronics",
    "​Perytons Ltd.",
    "​Tivoli Audio, LLC",
    "​Master Lock",
    "​Mesh-Net Ltd",
    "​Huizhou Desay SV Automotive CO., LTD.",
    "Tangerine, Inc.",
    "B&W Group Ltd.",
    "​Pioneer Corporation",
    "​OnBeep",
    "​Vernier Software & Technology",
    "​ROL Ergo",
    "​Pebble Technology",
    "​NETATMO",
    "​Accumulate AB",
    "​Anhui Huami Information Technology Co., Ltd.",
    "​Inmite s.r.o.",
    "​ChefSteps, Inc.",
    "​micas AG",
    "​Biomedical Research Ltd.",
    "Pitius Tec S.L.",
    "Estimote, Inc.",
    "Unikey Technologies, Inc.",
    "Timer Cap Co.",
    "AwoX",
    "yikes",
    "MADSGlobal NZ Ltd.",
    "PCH International",
    "Qingdao Yeelink Information Technology Co., Ltd.",
    "Milwaukee Tool (formerly Milwaukee Electric Tools)",
    "MISHIK Pte Ltd",
    "Bayer HealthCare",
    "Spicebox LLC",
    "emberlight",
    "Cooper-Atkins Corporation",
    "Qblinks",
    "MYSPHERA",
    "LifeScan Inc",
    "Volantic AB",
    "Podo Labs, Inc",
    "Roche Diabetes Care AG",
    "Amazon Fulfillment Service",
    "Connovate Technology Private Limited",
    "Kocomojo, LLC",
    "Everykey LLC",
    "Dynamic Controls",
    "SentriLock",
    "I-SYST inc.",
    "CASIO COMPUTER CO., LTD.",
    "LAPIS Semiconductor Co., Ltd.",
    "Telemonitor, Inc.",
    "taskit GmbH",
    "Daimler AG",
    "BatAndCat",
    "BluDotz Ltd",
    "XTel ApS",
    "Gigaset Communications GmbH",
    "Gecko Health Innovations, Inc.",
    "HOP Ubiquitous",
    "To Be Assigned",
    "Nectar",
    "bel’apps LLC",
    "CORE Lighting Ltd",
    "Seraphim Sense Ltd",
    "Unico RBC",
    "Physical Enterprises Inc.",
    "Able Trend Technology Limited",
    "Konica Minolta, Inc.",
    "Wilo SE",
    "Extron Design Services",
    "Fitbit, Inc.",
    "Fireflies Systems",
    "Intelletto Technologies Inc.",
    "FDK CORPORATION",
    "Cloudleaf, Inc",
    "Maveric Automation LLC",
    "Acoustic Stream Corporation",
    "Zuli",
    "Paxton Access Ltd",
    "WiSilica Inc",
    "Vengit Limited",
    "SALTO SYSTEMS S.L.",
    "TRON Forum (formerly T-Engine Forum)",
    "CUBETECH s.r.o.",
    "Cokiya Incorporated",
    "CVS Health",
    "Ceruus",
    "Strainstall Ltd",
    "Channel Enterprises (HK) Ltd.",
    "FIAMM",
    "GIGALANE.CO.,LTD",
    "EROAD",
    "Mine Safety Appliances",
    "Icon Health and Fitness",
    "Asandoo GmbH",
    "ENERGOUS CORPORATION",
    "Taobao",
    "Canon Inc.",
    "Geophysical Technology Inc.",
    "Facebook, Inc.",
    "Nipro Diagnostics, Inc.",
    "FlightSafety International",
    "Earlens Corporation",
    "Sunrise Micro Devices, Inc.",
    "Star Micronics Co., Ltd.",
    "Netizens Sp. z o.o.",
    "Nymi Inc.",
    "Nytec, Inc.",
    "Trineo Sp. z o.o.",
    "Nest Labs Inc.",
    "LM Technologies Ltd",
    "General Electric Company",
    "i+D3 S.L.",
    "HANA Micron",
    "Stages Cycling LLC",
    "Cochlear Bone Anchored Solutions AB",
    "SenionLab AB",
    "Syszone Co., Ltd",
    "Pulsate Mobile Ltd.",
    "Hong Kong HunterSun Electronic Limited",
    "pironex GmbH",
    "BRADATECH Corp.",
    "Transenergooil AG",
    "Bunch",
    "DME Microelectronics",
    "Bitcraze AB",
    "HASWARE Inc.",
    "Abiogenix Inc.",
    "Poly-Control ApS",
    "Avi-on",
    "Laerdal Medical AS",
    "Fetch My Pet",
    "Sam Labs Ltd.",
    "Chengdu Synwing Technology Ltd",
    "HOUWA SYSTEM DESIGN, k.k.",
    "BSH",
    "Primus Inter Pares Ltd",
    "August",
    "Gill Electronics",
    "Sky Wave Design",
    "Newlab S.r.l.",
    "ELAD srl​",
    "​G-wearables inc.",
    "​Squadrone Systems Inc.",
    "​Code Corporation",
    "​Savant Systems LLC",
    "​Logitech International SA",
    "​Innblue Consulting",
    "​iParking Ltd.",
    "​Koninklijke Philips Electronics N.V.",
    "​Minelab Electronics Pty Limited",
    "​Bison Group Ltd.",
    "​Widex A/S",
    "​Jolla Ltd",
    "​Lectronix, Inc.",
    "​Caterpillar Inc",
    "​Freedom Innovations",
    "​Dynamic Devices Ltd",
    "​Technology Solutions (UK) Ltd",
    "​IPS Group Inc.",
    "​STIR",
    "Sano, Inc​",
    "Advanced Application Design, Inc.​",
    "AutoMap LLC​",
    "​Spreadtrum Communications Shanghai Ltd",
    "​CuteCircuit LTD",
    "​Valeo Service",
    "​Fullpower Technologies, Inc.",
    "​KloudNation",
    "​Zebra Technologies Corporation",
    "​Itron, Inc.",
    "​The University of Tokyo",
    "​UTC Fire and Security",
    "​Cool Webthings Limited",
    "​DJO Global",
    "​Gelliner Limited",
    "​Anyka (Guangzhou) Microelectronics Technology Co, LTD",
    "​Medtronic, Inc.",
    "​Gozio, Inc.",
    "​Form Lifting, LLC",
    "​Wahoo Fitness, LLC",
    "​Kontakt Micro-Location Sp. z o.o.",
    "​Radio System Corporation",
    "​Freescale Semiconductor, Inc.",
    "​Verifone Systems PTe Ltd. Taiwan Branch",
    "​AR Timing",
    "​Rigado LLC",
    "​Kemppi Oy",
    "​Tapcentive Inc.",
    "Smartbotics Inc.​",
    "Otter Products, LLC​",
    "​STEMP Inc.",
    "​LumiGeek LLC",
    "​InvisionHeart Inc.",
    "Macnica Inc. ​",
    "​Jaguar Land Rover Limited",
    "​CoroWare Technologies, Inc",
    "​Simplo Technology Co., LTD",
    "​Omron Healthcare Co., LTD",
    "​Comodule GMBH",
    "​ikeGPS",
    "​Telink Semiconductor Co. Ltd",
    "Interplan Co., Ltd",
    "​Wyler AG",
    "​IK Multimedia Production srl",
    "​Lukoton Experience Oy",
    "​MTI Ltd",
    "​Tech4home, Lda",
    "​Hiotech AB",
]
