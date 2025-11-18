"""
Database Schemas for NFT Marketplace

Each Pydantic model represents a MongoDB collection.
Collection name is the lowercase class name.
"""

from pydantic import BaseModel, Field
from typing import Optional, List


class UserProfile(BaseModel):
    """
    Collection: "userprofile"
    Represents a user in the marketplace.
    """
    username: str = Field(..., description="Unique display name")
    wallet_address: str = Field(..., description="Public wallet address")
    avatar_url: Optional[str] = Field(None, description="Profile image URL")
    bio: Optional[str] = Field(None, description="Short bio")
    verified: bool = Field(False, description="Whether the profile is verified")


class NftCollection(BaseModel):
    """
    Collection: "nftcollection"
    A collection that groups NFTs.
    """
    name: str = Field(..., description="Collection name")
    description: Optional[str] = Field(None, description="Collection description")
    banner_url: Optional[str] = Field(None, description="Banner/cover image")
    creator_wallet: str = Field(..., description="Creator wallet address")


class NftItem(BaseModel):
    """
    Collection: "nftitem"
    Single NFT item metadata.
    """
    name: str = Field(..., description="NFT name")
    description: Optional[str] = Field(None, description="NFT description")
    image_url: str = Field(..., description="NFT image URL")
    collection_id: Optional[str] = Field(None, description="Associated collection id (string)")
    owner_wallet: str = Field(..., description="Current owner wallet address")
    attributes: Optional[List[dict]] = Field(default_factory=list, description="Trait list")


class Listing(BaseModel):
    """
    Collection: "listing"
    Marketplace listing for an NFT.
    """
    nft_id: str = Field(..., description="ID of the NFT item (string)")
    seller_wallet: str = Field(..., description="Seller wallet address")
    price_eth: float = Field(..., ge=0, description="Price in ETH")
    currency: str = Field("ETH", description="Currency code")
    status: str = Field("active", description="Listing status: active|sold|cancelled")
