"""
API with JSON Validation using Pydantic
Product Listing Generator with ChatGPT Integration
"""

import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from pydantic import BaseModel, Field, ValidationError


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API Key Loaded Successfully!")
else:
    print("WARNING: API key missing")



# ==========================================
# PYDANTIC INPUT MODEL
# ==========================================

class ProductRequest(BaseModel):

    name: str = Field(
        min_length=2
    )

    price: float = Field(
        gt=0
    )

    category: str = Field(
        min_length=2
    )

    additional_info: str | None = None

    quantity: int = Field(
        default=1,
        gt=0
    )



# ==========================================
# PYDANTIC OUTPUT MODEL
# ==========================================

class ProductListingResponse(BaseModel):

    title: str = Field(
        min_length=5
    )

    description: str = Field(
        min_length=50
    )

    features: list[str]

    keywords: str



# ==========================================
# CHATGPT PRODUCT LISTING GENERATOR
# ==========================================

def generate_listing(product):

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )


    prompt = f"""

You are an expert e-commerce copywriter.

Create a professional product listing.

Product Information:

Name:
{product.name}

Price:
${product.price}

Category:
{product.category}

Additional Information:
{product.additional_info}


Return ONLY valid JSON.

Use exactly this format:

{{
"title": "",
"description": "",
"features": [],
"keywords": ""
}}

Requirements:

- SEO friendly title
- 150-200 word product description
- 5 product features
- 10 SEO keywords
- Professional e-commerce style

"""


    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )


    raw_response = response.choices[0].message.content


    try:

        cleaned_response = raw_response.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()


        listing_json = json.loads(
            cleaned_response
        )


        validated_listing = ProductListingResponse(
            **listing_json
        )


        print("✓ ChatGPT output validated")


        return validated_listing.model_dump()


    except Exception as e:

        print("✗ ChatGPT output validation failed")


        return {
            "error": str(e),
            "raw_output": raw_response
        }



# ==========================================
# STEP 2: TEST VALIDATION MODEL
# ==========================================

print("="*50)
print("PRODUCT DATA VALIDATION MODEL")
print("="*50)


print("\nValid product test:")

try:

    product = ProductRequest(
        name="Bluetooth Headphones",
        price=80,
        category="Electronics",
        additional_info="Noise cancelling headphones",
        quantity=10
    )

    print("✓ Product accepted")
    print(product)


except ValidationError as e:

    print(e)



print("\nInvalid product test:")

try:

    bad_product = ProductRequest(
        name="",
        price=-20,
        category=""
    )


except ValidationError as e:

    print("✓ Invalid data rejected")
    print(e)




# ==========================================
# STEP 3: VALIDATE JSON FILE
# ==========================================

def validate_json_file(filename):

    print("\n" + "="*50)
    print(f"VALIDATING: {filename}")
    print("="*50)


    with open(filename,"r") as file:

        data = json.load(file)


    valid_products = []


    for index, item in enumerate(data,start=1):

        try:

            product = ProductRequest(**item)

            print(
                f"✓ Product {index} valid"
            )

            valid_products.append(product)


        except ValidationError:

            print(
                f"✗ Product {index} invalid"
            )


    print("\nSUMMARY")

    print(
        "Valid products:",
        len(valid_products)
    )

    print(
        "Invalid products:",
        len(data)-len(valid_products)
    )


    return valid_products




# ==========================================
# STEP 4: GENERATE ONE LISTING
# ==========================================

products = validate_json_file(
    "valid_products.json"
)


if products:

    print("\nGenerating listing...")


    listing = generate_listing(
        products[0]
    )


    print(
        json.dumps(
            listing,
            indent=2
        )
    )




# ==========================================
# STEP 5: BATCH PROCESSING
# ==========================================

def process_batch_requests(filename):

    print("\n" + "="*50)
    print(
        f"BATCH PROCESSING: {filename}"
    )
    print("="*50)


    with open(filename,"r") as file:

        products = json.load(file)


    results = {

        "successful": [],

        "failed": []

    }


    for index,item in enumerate(products,start=1):

        try:

            product = ProductRequest(**item)

            print(
                f"✓ Product {index} validated"
            )


            results["successful"].append(
                product.model_dump()
            )


        except ValidationError as e:


            print(
                f"✗ Product {index} failed"
            )


            results["failed"].append(
                e.errors()
            )



    print("\nBATCH SUMMARY")
    print("----------------")


    print(
        "Successful:",
        len(results["successful"])
    )

    print(
        "Failed:",
        len(results["failed"])
    )


    return results




batch_result = process_batch_requests(
    "valid_products.json"
)


print(batch_result)




# ==========================================
# STEP 6: CLIENT REQUEST HANDLER
# ==========================================

def handle_client_request(payload):

    try:

        product = ProductRequest(**payload)


        print(
            "✓ Client request validated"
        )


        listing = generate_listing(
            product
        )


        print(
            "✓ Product listing generated"
        )


        return {

            "status": "success",

            "product":
                product.model_dump(),

            "listing":
                listing

        }



    except ValidationError as e:


        return {

            "status":"error",

            "message":
                "Validation failed",

            "errors":
                e.errors()

        }



    except Exception as e:


        return {

            "status":"error",

            "message":
                str(e)

        }




# ==========================================
# TEST CLIENT REQUEST
# ==========================================

client_payload = {

    "name":"Smart Watch",

    "price":150,

    "category":"Accessories",

    "additional_info":
        "Fitness tracking smartwatch",

    "quantity":3

}



client_response = handle_client_request(
    client_payload
)



print("\nCLIENT RESPONSE")
print("="*50)


print(
    json.dumps(
        client_response,
        indent=2
    )
)

