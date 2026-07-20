from pydantic import BaseModel, Field


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


class ProductListingResponse(BaseModel):

    title: str

    description: str

    features: list[str]

    keywords: str