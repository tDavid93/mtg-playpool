from pydantic import BaseModel
from datetime import date
from typing import List

class MetaBase(BaseModel):
    date: date
    version: str

class MetaCreate(MetaBase):
    pass

class SetsBase(BaseModel):
    baseSetSize: int
    block: str
    cardsphereSetId: int
    code: str
    isFoilOnly: bool
    isForeignOnly: bool
    isNonFoilOnly: bool
    isOnlineOnly: bool
    isPartialPreview: bool
    keyruneCode: str
    languages: str
    mcmId: int
    mcmIdExtras: int
    mcmName: str
    mtgoCode: str
    name: str
    parentCode: str
    releaseDate: str
    tcgplayerGroupId: int
    tokenSetCode: str
    totalSetSize: int
    type: str

class SetsCreate(SetsBase):
    pass

class CardsBase(BaseModel):
    artist: str
    artistIds: str
    asciiName: str
    attractionLights: str
    availability: str
    boosterTypes: str
    borderColor: str
    cardParts: str
    colorIdentity: str
    colorIndicator: str
    colors: str
    defense: str
    duelDeck: str
    edhrecRank: int
    edhrecSaltiness: float
    faceConvertedManaCost: float
    faceFlavorName: str
    faceManaValue: float
    faceName: str
    finishes: str
    flavorName: str
    flavorText: str
    frameEffects: str
    frameVersion: str
    hand: str
    hasAlternativeDeckLimit: bool
    hasContentWarning: bool
    hasFoil: bool
    hasNonFoil: bool
    isAlternative: bool
    isFullArt: bool
    isFunny: bool
    isOnlineOnly: bool
    isOversized: bool
    isPromo: bool
    isRebalanced: bool
    isReprint: bool
    isReserved: bool
    isStarter: bool
    isStorySpotlight: bool
    isTextless: bool
    isTimeshifted: bool
    keywords: str
    language: str
    layout: str
    leadershipSkills: str
    life: str
    loyalty: str
    manaCost: str
    manaValue: float
    name: str
    number: str
    originalPrintings: str
    originalReleaseDate: str
    originalText: str
    originalType: str
    otherFaceIds: str
    power: str
    printings: str
    promoTypes: str
    rarity: str
    rebalancedPrintings: str
    relatedCards: str
    securityStamp: str
    setCode: str
    side: str
    signature: str
    subsets: str
    subtypes: str
    supertypes: str
    text: str
    toughness: str
    type: str
    types: str
    uuid: str
    variations: str
    watermark: str

class CardsCreate(CardsBase):
    pass

class TokensBase(BaseModel):
    artist: str
    artistIds: str
    asciiName: str
    availability: str
    boosterTypes: str
    borderColor: str
    colorIdentity: str
    colors: str
    edhrecSaltiness: float
    faceName: str
    finishes: str
    flavorText: str
    frameEffects: str
    frameVersion: str
    hasFoil: bool
    hasNonFoil: bool
    isFullArt: bool
    isFunny: bool
    isPromo: bool
    isReprint: bool
    isTextless: bool
    keywords: str
    language: str
    layout: str
    name: str
    number: str
    orientation: str
    originalText: str
    originalType: str
    otherFaceIds: str
    power: str
    promoTypes: str
    relatedCards: str
    reverseRelated: str
    securityStamp: str
    setCode: str
    side: str
    signature: str
    subtypes: str
    supertypes: str
    text: str
    toughness: str
    type: str
    types: str
    uuid: str
    watermark: str

class TokensCreate(TokensBase):
    pass

class CardIdentifiersBase(BaseModel):
    cardKingdomEtchedId: str
    cardKingdomFoilId: str
    cardKingdomId: str
    cardsphereId: str
    mcmId: str
    mcmMetaId: str
    mtgArenaId: str
    mtgjsonFoilVersionId: str
    mtgjsonNonFoilVersionId: str
    mtgjsonV4Id: str
    mtgoFoilId: str
    mtgoId: str
    multiverseId: str
    scryfallId: str
    scryfallIllustrationId: str
    scryfallOracleId: str
    tcgplayerEtchedProductId: str
    tcgplayerProductId: str
    uuid: str

class CardIdentifiersCreate(CardIdentifiersBase):
    pass

class CardLegalitiesBase(BaseModel):
    alchemy: str
    brawl: str
    commander: str
    duel: str
    explorer: str
    future: str
    gladiator: str
    historic: str
    historicbrawl: str
    legacy: str
    modern: str
    oathbreaker: str
    oldschool: str
    pauper: str
    paupercommander: str
    penny: str
    pioneer: str
    predh: str
    premodern: str
    standard: str
    uuid: str
    vintage: str

class CardLegalitiesCreate(CardLegalitiesBase):
    pass

class CardRulingsBase(BaseModel):
    date: date
    text: str
    uuid: str

class CardRulingsCreate(CardRulingsBase):
    pass

class CardForeignDataBase(BaseModel):
    faceName: str
    flavorText: str
    language: str
    multiverseId: int
    name: str
    text: str
    type: str
    uuid: str

class CardForeignDataCreate(CardForeignDataBase):
    pass

class CardPurchaseUrlsBase(BaseModel):
    cardKingdom: str
    cardKingdomEtched: str
    cardKingdomFoil: str
    cardmarket: str
    tcgplayer: str
    tcgplayerEtched: str
    uuid: str

class CardPurchaseUrlsCreate(CardPurchaseUrlsBase):
    pass

class TokenIdentifiersBase(BaseModel):
    cardKingdomEtchedId: str
    cardKingdomFoilId: str
    cardKingdomId: str
    cardsphereId: str
    mcmId: str
    mcmMetaId: str
    mtgArenaId: str
    mtgjsonFoilVersionId: str
    mtgjsonNonFoilVersionId: str
    mtgjsonV4Id: str
    mtgoFoilId: str
    mtgoId: str
    multiverseId: str
    scryfallId: str
    scryfallIllustrationId: str
    scryfallOracleId: str
    tcgplayerEtchedProductId: str
    tcgplayerProductId: str
    uuid: str

class TokenIdentifiersCreate(TokenIdentifiersBase):
    pass

class SetTranslationsBase(BaseModel):
    language: str
    translation: str
    uuid: str

class SetTranslationsCreate(SetTranslationsBase):
    pass

class SetBoosterContentsBase(BaseModel):
    boosterIndex: int
    boosterName: str
    setCode: str
    sheetName: str
    sheetPicks: int

class SetBoosterContentsCreate(SetBoosterContentsBase):
    pass

class SetBoosterContentWeightsBase(BaseModel):
    boosterIndex: int
    boosterName: str
    boosterWeight: int
    setCode: str

class SetBoosterContentWeightsCreate(SetBoosterContentWeightsBase):
    pass

class SetBoosterSheetsBase(BaseModel):
    setCode: str
    sheetHasBalanceColors: bool
    sheetIsFoil: bool
    sheetName: str

class SetBoosterSheetsCreate(SetBoosterSheetsBase):
    pass

class SetBoosterSheetCardsBase(BaseModel):
    cardUuid: str
    cardWeight: int
    setCode: str
    sheetName: str

class SetBoosterSheetCardsCreate(SetBoosterSheetCardsBase):
    pass
