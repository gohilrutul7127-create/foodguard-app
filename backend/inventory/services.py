import json
from datetime import date
import cv2
import numpy as np
from django.core.files.uploadedfile import UploadedFile

class QRDecodeError(ValueError): pass

def decode_qr(upload: UploadedFile) -> str:
    if upload.size > 8 * 1024 * 1024: raise QRDecodeError('Image must be smaller than 8 MB.')
    raw = upload.read(); image=cv2.imdecode(np.frombuffer(raw, np.uint8),cv2.IMREAD_COLOR)
    if image is None: raise QRDecodeError('This file is not a valid image.')
    value, _, _ = cv2.QRCodeDetector().detectAndDecode(image)
    if not value:
        try:
            from pyzbar.pyzbar import decode
            symbols=decode(image); value=symbols[0].data.decode('utf-8') if symbols else ''
        except (ImportError, OSError): pass
    if not value: raise QRDecodeError('No readable QR code was found. Use a sharper, well-lit image and try again.')
    return value.strip()

def parse_product_payload(value: str) -> dict:
    try: payload=json.loads(value)
    except json.JSONDecodeError: payload={'barcode':value}
    if not isinstance(payload,dict): raise QRDecodeError('The QR code does not contain supported product data.')
    product=payload.get('product',payload)
    barcode=str(product.get('barcode') or product.get('gtin') or value)[:512]
    return {'barcode':barcode,'name':str(product.get('name','')).strip(),'brand':str(product.get('brand','')).strip(),'manufacturing_date':product.get('manufacturing_date') or product.get('mfg_date'),'expiry_date':product.get('expiry_date') or product.get('expires_on'),'ingredients':product.get('ingredients',''),'storage_instructions':product.get('storage_instructions') or product.get('storage','')}
