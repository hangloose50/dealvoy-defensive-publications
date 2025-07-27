from fastapi import APIRouter, File, UploadFile
from app.services.scout_vision import identify_product_from_image

router = APIRouter()

@router.post("/identify-image/")
async def identify_image(file: UploadFile = File(...)):
    contents = await file.read()
    result = identify_product_from_image(contents)
    return {"result": result}
