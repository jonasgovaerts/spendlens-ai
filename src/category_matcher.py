import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CategoryMatcher:
    def __init__(self):
        # Define keyword mappings for categories
        self.category_keywords = {
            # ======================
            # INCOME
            # ======================
            "Income": [
                "loon",
                "loons",
                "consultancy",
                "jonas govaerts consultancy",
                "HEILIGHARTZIEKENHUIS",
                "ZORGGROEP ZUSTERS VAN BERLAAR",
                "parentia",
                "groeipakket",
                "kleutertoeslag",
                "vakantiegeld",
                "ziekenfonds",
                "uitk.",
                "uitk",
                "terugbetaling",
                "mangopay",
                "vinted",
                "instantoverschrijving",
                "p2p mobile",
                "van:",
            ],
            # ======================
            # GROCERIES & DAILY FOOD
            # ======================
            "Groceries": [
                "colruyt",
                "delhaize",
                "aldi",
                "lidl",
                "jumbo",
                "okay",
                "comarkt",
                "albert heijn",
                "expressmarkt",
                "dillen groenten",
                "panos",
                "NYX*DavidRoelRousseau",
                "bakkerij",
                "banketbakkerij",
                "den tro",
                "ijsboerke",
                "ad herenthout",
                "bij stephanie"
            ],
            # ======================
            # EATING OUT & TAKEAWAY
            # ======================
            "Food & Dining": [
                "restaurant",
                "resto",
                "nethe en drinke",
                "tante trien",
                "psc resto",
                "de kloek",
                "boshuis",
                "mcdonalds",
                "frituur",
                "poke bowl",
                "charlies chicken",
                "hawaiian",
                "foodmaker",
                "cafe",
                "bar",
                "moment",
                "dokape",
                "mo made bvb antwerpen"
            ],
            # ======================
            # TRANSPORT & MOBILITY
            # ======================
            "Transport": [
                "q8",
                "total",
                "tinq",
                "maes",
                "dats 24",
                "auto 5",
                "banden",
                "garage",
                "fiets",
                "ciclobility",
                "parking",
                "JBN COMM V"
            ],
            # ======================
            # HOUSING & UTILITIES
            # ======================
            "Housing": [
                "triodos",
                "saldo hl",
                "electrabel",
                "pidpa",
                "diftar",
                "gemeente",
                "gem.bestuur",
                "flitsbak",
            ],
            # ======================
            # INSURANCE & PENSIONS
            # ======================
            "Insurance": [
                "dvv cocoon",
                "dvv verzekeringen",
                "allianz",
                "plan for life",
                "nn insurance",
                "zorgpremie",
                "ziekenfonds",
            ],
            # ======================
            # HEALTHCARE
            # ======================
            "Healthcare": [
                "apotheek",
                "kruidvat",
                "healthcorner",
            ],
            # ======================
            # CHILDREN & FAMILY
            # ======================
            "Children": [
                "huis van het kind",
                "heilig hart",
                "zwemclub",
                "ijshockey",
                "sportoase",
                "technopolis",
                "kinderboerderij",
            ],
            # ======================
            # CLOTHING & SHOES
            # ======================
            "Clothing": [
                "zara",
                "vero moda",
                "only",
                "jbc",
                "zeeman",
                "takko",
                "bel&bo",
                "torfs",
                "vanharen",
                "hunkemoller",
                "modemakers",
                "america today"
            ],
            # ======================
            # PERSONAL CARE & BEAUTY
            # ======================
            "Personal Care": [
                "kapper",
                "rituals",
                "ici paris",
                "kruidvat",
            ],
            # ======================
            # LEISURE, CULTURE & EVENTS
            # ======================
            "Leisure": [
                "ticketmaster",
                "sportpaleis",
                "concert",
                "center parcs",
                "weekend",
                "ice skating",
                "maple leaf sport",
                "zwembad",
                "amacx"
            ],
            # ======================
            # SHOPPING & HOUSEHOLD
            # ======================
            "Household": [
                "ikea",
                "ygo interieur",
                "mondi",
                "easykit",
                "tuin",
                "hobbycenter",
                "ohgreen",
                "technopolis",
                "megekko",
                "zippit",
                "homewizard",
                "windocare",
                "action",
                "joruca"
            ],
            # ======================
            # SUBSCRIPTIONS & DIGITAL
            # ======================
            "Subscriptions": [
                "apple.com",
                "paypal",
                "klarna",
                "hellofresh",
            ],
            # ======================
            # BANKING & ADMIN
            # ======================
            "Banking": [
                "eurocent/verrichting",
                "bankkosten",
                "visa card",
                "domiciliation visa",
            ],
            # ======================
            # TAXES & GOVERNMENT
            # ======================
            "Taxes": [
                "fod financien",
                "vlaamse belastingsdienst",
                "provincie antwerpen",
            ],
            # ======================
            # TRANSFERS
            # ======================
            "Transfers": [
                "spaarrekening",
                "sparen",
                "overschrijving",
                "instantoverschrijving",
            ],
            # ======================
            # GIFTS & MISC
            # ======================
            "Gifts & Donations": [
                "verrassingsfeest",
                "gift",
                "donatie",
            ],
            "Miscellaneous": [
                "divers",
                "onbekend",
            ],
        }

    def get_category_from_keywords(self, description, account):
        """Match description and account against predefined keywords"""
        # Convert to lowercase for case-insensitive matching
        desc_lower = description.lower()
        acc_lower = account.lower() if account else ""

        # Check for matches in description first
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in desc_lower:
                    return category

        # If no match in description, check account
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword.lower() in acc_lower:
                    return category

        # If no matches found, return None
        return None
