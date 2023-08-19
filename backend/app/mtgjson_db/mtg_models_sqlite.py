from mtgjson_db.database import Base

#Fields named "type" are reserved in Python, so we use "card_type" instead
from sqlalchemy import Column, Integer, Float, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base



class Meta(Base):
    __tablename__ = 'meta'

    date = Column(Date, primary_key=True)
    version = Column(String)

class Sets(Base):
    __tablename__ = 'sets'

    baseSetSize = Column(Integer)
    block = Column(String)
    cardsphereSetId = Column(Integer)
    code = Column(String(8), primary_key=True, unique=True, nullable=False)
    isFoilOnly = Column(Boolean)
    isForeignOnly = Column(Boolean)
    isNonFoilOnly = Column(Boolean)
    isOnlineOnly = Column(Boolean)
    isPartialPreview = Column(Boolean)
    keyruneCode = Column(String)
    languages = Column(String)
    mcmId = Column(Integer)
    mcmIdExtras = Column(Integer)
    mcmName = Column(String)
    mtgoCode = Column(String)
    name = Column(String)
    parentCode = Column(String)
    releaseDate = Column(String)
    tcgplayerGroupId = Column(Integer)
    tokenSetCode = Column(String)
    totalSetSize = Column(Integer)
    type = Column(String)

class Cards(Base):
    __tablename__ = 'cards'

    artist = Column(String)
    artistIds = Column(String)
    asciiName = Column(String)
    attractionLights = Column(String)
    availability = Column(String)
    boosterTypes = Column(String)
    borderColor = Column(String)
    cardParts = Column(String)
    colorIdentity = Column(String)
    colorIndicator = Column(String)
    colors = Column(String)
    defense = Column(String)
    duelDeck = Column(String)
    edhrecRank = Column(Integer)
    edhrecSaltiness = Column(Float)
    faceConvertedManaCost = Column(Float)
    faceFlavorName = Column(String)
    faceManaValue = Column(Float)
    faceName = Column(String)
    finishes = Column(String)
    flavorName = Column(String)
    flavorText = Column(String)
    frameEffects = Column(String)
    frameVersion = Column(String)
    hand = Column(String)
    hasAlternativeDeckLimit = Column(Boolean)
    hasContentWarning = Column(Boolean)
    hasFoil = Column(Boolean)
    hasNonFoil = Column(Boolean)
    isAlternative = Column(Boolean)
    isFullArt = Column(Boolean)
    isFunny = Column(Boolean)
    isOnlineOnly = Column(Boolean)
    isOversized = Column(Boolean)
    isPromo = Column(Boolean)
    isRebalanced = Column(Boolean)
    isReprint = Column(Boolean)
    isReserved = Column(Boolean)
    isStarter = Column(Boolean)
    isStorySpotlight = Column(Boolean)
    isTextless = Column(Boolean)
    isTimeshifted = Column(Boolean)
    keywords = Column(String)
    language = Column(String)
    layout = Column(String)
    leadershipSkills = Column(String)
    life = Column(String)
    loyalty = Column(String)
    manaCost = Column(String)
    manaValue = Column(Float)
    name = Column(String)
    number = Column(String)
    originalPrintings = Column(String)
    originalReleaseDate = Column(String)
    originalText = Column(String)
    originalType = Column(String)
    otherFaceIds = Column(String)
    power = Column(String)
    printings = Column(String)
    promoTypes = Column(String)
    rarity = Column(String)
    rebalancedPrintings = Column(String)
    relatedCards = Column(String)
    securityStamp = Column(String)
    setCode = Column(String)
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
    artistIds = Column(String)
    asciiName = Column(String)
    availability = Column(String)
    boosterTypes = Column(String)
    borderColor = Column(String)
    colorIdentity = Column(String)
    colors = Column(String)
    edhrecSaltiness = Column(Float)
    faceName = Column(String)
    finishes = Column(String)
    flavorText = Column(String)
    frameEffects = Column(String)
    frameVersion = Column(String)
    hasFoil = Column(Boolean)
    hasNonFoil = Column(Boolean)
    isFullArt = Column(Boolean)
    isFunny = Column(Boolean)
    isPromo = Column(Boolean)
    isReprint = Column(Boolean)
    isTextless = Column(Boolean)
    keywords = Column(String)
    language = Column(String)
    layout = Column(String)
    name = Column(String)
    number = Column(String)
    orientation = Column(String)
    originalText = Column(String)
    originalType = Column(String)
    otherFaceIds = Column(String)
    power = Column(String)
    promoTypes = Column(String)
    relatedCards = Column(String)
    reverseRelated = Column(String)
    securityStamp = Column(String)
    setCode = Column(String)
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
    __tablename__ = 'cardIdentifiers'

    cardKingdomEtchedId = Column(String)
    cardKingdomFoilId = Column(String)
    cardKingdomId = Column(String)
    cardsphereId = Column(String)
    mcmId = Column(String)
    mcmMetaId = Column(String)
    mtgArenaId = Column(String)
    mtgjsonFoilVersionId = Column(String)
    mtgjsonNonFoilVersionId = Column(String)
    mtgjsonV4Id = Column(String)
    mtgoFoilId = Column(String)
    mtgoId = Column(String)
    multiverseId = Column(String)
    scryfallId = Column(String)
    scryfallIllustrationId = Column(String)
    scryfallOracleId = Column(String)
    tcgplayerEtchedProductId = Column(String)
    tcgplayerProductId = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class CardLegalities(Base):
    __tablename__ = 'cardLegalities'

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
    __tablename__ = 'cardRulings'

    date = Column(Date)
    text = Column(String)
    uuid = Column(String(36), primary_key=True, nullable=False)

class CardForeignData(Base):
    __tablename__ = 'cardForeignData'

    faceName = Column(String)
    flavorText = Column(String)
    language = Column(String)
    multiverseId = Column(Integer)
    name = Column(String)
    text = Column(String)
    type = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class CardPurchaseUrls(Base):
    __tablename__ = 'cardPurchaseUrls'

    cardKingdom = Column(String)
    cardKingdomEtched = Column(String)
    cardKingdomFoil = Column(String)
    cardmarket = Column(String)
    tcgplayer = Column(String)
    tcgplayerEtched = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class TokenIdentifiers(Base):
    __tablename__ = 'tokenIdentifiers'

    cardKingdomEtchedId = Column(String)
    cardKingdomFoilId = Column(String)
    cardKingdomId = Column(String)
    cardsphereId = Column(String)
    mcmId = Column(String)
    mcmMetaId = Column(String)
    mtgArenaId = Column(String)
    mtgjsonFoilVersionId = Column(String)
    mtgjsonNonFoilVersionId = Column(String)
    mtgjsonV4Id = Column(String)
    mtgoFoilId = Column(String)
    mtgoId = Column(String)
    multiverseId = Column(String)
    scryfallId = Column(String)
    scryfallIllustrationId = Column(String)
    scryfallOracleId = Column(String)
    tcgplayerEtchedProductId = Column(String)
    tcgplayerProductId = Column(String)
    uuid = Column(String, primary_key=True, nullable=False)

class SetTranslations(Base):
    __tablename__ = 'setTranslations'

    language = Column(String)
    translation = Column(String)
    uuid = Column(String(36), primary_key=True, nullable=False)

class SetBoosterContents(Base):
    __tablename__ = 'setBoosterContents'

    boosterIndex = Column(Integer)
    boosterName = Column(String(255))
    setCode = Column(String(20), primary_key=True, nullable=False)
    sheetName = Column(String(255))
    sheetPicks = Column(Integer)

class SetBoosterContentWeights(Base):
    __tablename__ = 'setBoosterContentWeights'

    boosterIndex = Column(Integer)
    boosterName = Column(String(255))
    boosterWeight = Column(Integer)
    setCode = Column(String(20), primary_key=True, nullable=False)

class SetBoosterSheets(Base):
    __tablename__ = 'setBoosterSheets'

    setCode = Column(String(20), primary_key=True, nullable=False)
    sheetHasBalanceColors = Column(Boolean)
    sheetIsFoil = Column(Boolean)
    sheetName = Column(String(255))

class SetBoosterSheetCards(Base):
    __tablename__ = 'setBoosterSheetCards'

    cardUuid = Column(String(36), primary_key=True, nullable=False)
    cardWeight = Column(Integer)
    setCode = Column(String(20))
    sheetName = Column(String(255))

# Create an SQLite database engine and create tables
