from mtgjson_db.database import Base

#Fields named "type" are reserved in Python, so we use "card_type" instead
from sqlalchemy import Column, Integer, Float, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Meta(Base):
    __tablename__ = 'meta'

    date = Column(Date, primary_key=True)
    version = Column(String)

class Sets(Base):
    __tablename__ = 'sets'

    basesetsize = Column(Integer)
    block = Column(String)
    cardspheresetid = Column(Integer)
    code = Column(String(8), primary_key=True, unique=True, nullable=False)
    isfoilonly = Column(Boolean)
    isforeignonly = Column(Boolean)
    isnonfoilonly = Column(Boolean)
    isonlineonly = Column(Boolean)
    ispartialpreview = Column(Boolean)
    keyrunecode = Column(String)
    languages = Column(String)
    mcmid = Column(Integer)
    mcmidextras = Column(Integer)
    mcmname = Column(String)
    mtgocode = Column(String)
    name = Column(String)
    parentcode = Column(String)
    releasedate = Column(String)
    tcgplayergroupid = Column(Integer)
    tokensetcode = Column(String)
    totalsetsize = Column(Integer)
    type = Column(String)

class Cards(Base):
    __tablename__ = 'cards'

    artist = Column(String)
    artistids = Column(String)
    asciiname = Column(String)
    attractionlights = Column(String)
    availability = Column(String)
    boostertypes = Column(String)
    bordercolor = Column(String)
    cardparts = Column(String)
    coloridentity = Column(String)
    colorindicator = Column(String)
    colors = Column(String)
    defense = Column(String)
    dueldeck = Column(String)
    edhrecrank = Column(Integer)
    edhrecsaltiness = Column(Float)
    faceconvertedmanacost = Column(Float)
    faceflavorname = Column(String)
    facemanavalue = Column(Float)
    facename = Column(String)
    finishes = Column(String)
    flavorname = Column(String)
    flavortext = Column(String)
    frameeffects = Column(String)
    frameversion = Column(String)
    hand = Column(String)
    hasalternativedecklimit = Column(Boolean)
    hascontentwarning = Column(Boolean)
    hasfoil = Column(Boolean)
    hasnonfoil = Column(Boolean)
    isalternative = Column(Boolean)
    isfullart = Column(Boolean)
    isfunny = Column(Boolean)
    isonlineonly = Column(Boolean)
    isoversized = Column(Boolean)
    ispromo = Column(Boolean)
    isrebalanced = Column(Boolean)
    isreprint = Column(Boolean)
    isreserved = Column(Boolean)
    isstarter = Column(Boolean)
    isstoryspotlight = Column(Boolean)
    istextless = Column(Boolean)
    istimeshifted = Column(Boolean)
    keywords = Column(String)
    language = Column(String)
    layout = Column(String)
    leadershipskills = Column(String)
    life = Column(String)
    loyalty = Column(String)
    manacost = Column(String)
    manavalue = Column(Float)
    name = Column(String)
    number = Column(String)
    originalprintings = Column(String)
    originalreleasedate = Column(String)
    originaltext = Column(String)
    originaltype = Column(String)
    otherfaceids = Column(String)
    power = Column(String)
    printings = Column(String)
    promotypes = Column(String)
    rarity = Column(String)
    rebalancedprintings = Column(String)
    relatedcards = Column(String)
    securitystamp = Column(String)
    setcode = Column(String)
    side = Column(String)
    signature = Column(String)
    subsets = Column(String)
    subtypes = Column(String)
    supertypes = Column(String)
    text = Column(String)
    toughness = Column(String)
    type = Column(String)
    types = Column(String)
    uuid = Column(String(36), primary_key=True, nullable=False)
    variations = Column(String)
    watermark = Column(String)

class Tokens(Base):
    __tablename__ = 'tokens'

    artist = Column(String)
    artistids = Column(String)
    asciiname = Column(String)
    availability = Column(String)
    boostertypes = Column(String)
    bordercolor = Column(String)
    coloridentity = Column(String)
    colors = Column(String)
    edhrecsaltiness = Column(Float)
    facename = Column(String)
    finishes = Column(String)
    flavortext = Column(String)
    frameeffects = Column(String)
    frameversion = Column(String)
    hasfoil = Column(Boolean)
    hasnonfoil = Column(Boolean)
    isfullart = Column(Boolean)
    isfunny = Column(Boolean)
    ispromo = Column(Boolean)
    isreprint = Column(Boolean)
    istextless = Column(Boolean)
    keywords = Column(String)
    language = Column(String)
    layout = Column(String)
    name = Column(String)
    number = Column(String)
    orientation = Column(String)
    originaltext = Column(String)
    originaltype = Column(String)
    otherfaceids = Column(String)
    power = Column(String)
    promotypes = Column(String)
    relatedcards = Column(String)
    reverserelated = Column(String)
    securitystamp = Column(String)
    setcode = Column(String)
    side = Column(String)
    signature = Column(String)
    subtypes = Column(String)
    supertypes = Column(String)
    text = Column(String)
    toughness = Column(String)
    type = Column(String)
    types = Column(String)
    uuid = Column(String(36), primary_key=True, nullable=False)
    watermark = Column(String)

class CardIdentifiers(Base):
    __tablename__ = 'cardidentifiers'

    cardkingdometchedid = Column(String)
    cardkingdomfoilid = Column(String)
    cardkingdomid = Column(String)
    cardsphereid = Column(String)
    mcmid = Column(String)
    mcmmetaid = Column(String)
    mtgarenaid = Column(String)
    mtgjsonfoilversionid = Column(String)
    mtgjsonnonfoilversionid = Column(String)
    mtgjsonv4id = Column(String)
    mtgofoilid = Column(String)
    mtgoid = Column(String)
    multiverseid = Column(String)
    scryfallid = Column(String)
    scryfallillustrationid = Column(String)
    scryfalloracleid = Column(String)
    tcgplayeretchedproductid = Column(String)
    tcgplayerproductid = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class CardLegalities(Base):
    __tablename__ = 'cardlegalities'

    alchemy = Column(String)
    brawl = Column(String)
    commander = Column(String)
    duel = Column(String)
    explorer = Column(String)
    future = Column(String)
    gladiator = Column(String)
    historic = Column(String)
    historicbrawl = Column(String)
    legacy = Column(String)
    modern = Column(String)
    oathbreaker = Column(String)
    oldschool = Column(String)
    pauper = Column(String)
    paupercommander = Column(String)
    penny = Column(String)
    pioneer = Column(String)
    predh = Column(String)
    premodern = Column(String)
    standard = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)
    vintage = Column(String)

class CardRulings(Base):
    __tablename__ = 'cardrulings'

    date = Column(Date)
    text = Column(String)
    uuid = Column(String(36), primary_key=True, nullable=False)

class CardForeignData(Base):
    __tablename__ = 'cardforeignData'

    facename = Column(String)
    flavortext = Column(String)
    language = Column(String)
    multiverseid = Column(Integer)
    name = Column(String)
    text = Column(String)
    type = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class CardPurchaseUrls(Base):
    __tablename__ = 'cardpurchaseurls'

    cardkingdom = Column(String)
    cardkingdometched = Column(String)
    cardkingdomfoil = Column(String)
    cardmarket = Column(String)
    tcgplayer = Column(String)
    tcgplayeretched = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class TokenIdentifiers(Base):
    __tablename__ = 'tokenidentifiers'

    cardkingdometchedid = Column(String)
    cardkingdomfoilid = Column(String)
    cardkingdomid = Column(String)
    cardsphereid = Column(String)
    mcmid = Column(String)
    mcmmetaid = Column(String)
    mtgarenaid = Column(String)
    mtgjsonfoilversionid = Column(String)
    mtgjsonnonfoilversionid = Column(String)
    mtgjsonv4id = Column(String)
    mtgofoilid = Column(String)
    mtgoid = Column(String)
    multiverseid = Column(String)
    scryfallid = Column(String)
    scryfallillustrationid = Column(String)
    scryfalloracleid = Column(String)
    tcgplayeretchedproductid = Column(String)
    tcgplayerproductid = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class SetTranslations(Base):
    __tablename__ = 'settranslations'

    language = Column(String)
    translation = Column(String)
    uuid = Column(String(36), primary_key=True, nullable=False)

class SetBoosterContents(Base):
    __tablename__ = 'setboostercontents'

    boosterindex = Column(Integer)
    boostername = Column(String(255))
    setcode = Column(String(20), primary_key=True, nullable=False)
    sheetname = Column(String(255))
    sheetpicks = Column(Integer)

class SetBoosterContentWeights(Base):
    __tablename__ = 'setboostercontentweights'

    boosterindex = Column(Integer)
    boostername = Column(String(255))
    boosterweight = Column(Integer)
    setcode = Column(String(20), primary_key=True, nullable=False)

class SetBoosterSheets(Base):
    __tablename__ = 'setboostersheets'

    setcode = Column(String(20), primary_key=True, nullable=False)
    sheethasbalancecolors = Column(Boolean)
    sheetisfoil = Column(Boolean)
    sheetname = Column(String(255))

class SetBoosterSheetCards(Base):
    __tablename__ = 'setboostersheetcards'

    carduuid = Column(String(36), primary_key=True, nullable=False)
    cardweight = Column(Integer)
    setcode = Column(String(20))
    sheetname = Column(String(255))

# Create an SQLite database engine and create tables

class Collection(Base):
    __tablename__ = 'collection'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    owner = Column(String(255))
    
class CardCollection(Base):
    __tablename__ = 'cardcollection'
    
    id = Column(Integer,primary_key=True,autoincrement=True)
    collection_id = Column(Integer)
    card_uuid = Column(String(36))
    quantity = Column(Integer)

    