import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import UserProfile, NftCollection, NftItem, Listing

app = FastAPI(title="NFT Marketplace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "NFT Marketplace Backend is running"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


# --------- API: Collections ---------
@app.get("/api/collections")
def list_collections(limit: int = Query(12, ge=1, le=100)):
    try:
        docs = get_documents("nftcollection", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CreateCollectionRequest(NftCollection):
    pass


@app.post("/api/collections")
def create_collection(payload: CreateCollectionRequest):
    try:
        new_id = create_document("nftcollection", payload)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- API: NFTs ---------
@app.get("/api/nfts")
def list_nfts(limit: int = Query(16, ge=1, le=100), collection_id: Optional[str] = None):
    try:
        filter_dict = {"collection_id": collection_id} if collection_id else {}
        docs = get_documents("nftitem", filter_dict=filter_dict, limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CreateNftRequest(NftItem):
    pass


@app.post("/api/nfts")
def create_nft(payload: CreateNftRequest):
    try:
        new_id = create_document("nftitem", payload)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- API: Listings ---------
@app.get("/api/listings")
def list_listings(limit: int = Query(20, ge=1, le=100), status: Optional[str] = None):
    try:
        filter_dict = {"status": status} if status else {}
        docs = get_documents("listing", filter_dict=filter_dict, limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return {"items": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CreateListingRequest(Listing):
    pass


@app.post("/api/listings")
def create_listing(payload: CreateListingRequest):
    try:
        new_id = create_document("listing", payload)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
