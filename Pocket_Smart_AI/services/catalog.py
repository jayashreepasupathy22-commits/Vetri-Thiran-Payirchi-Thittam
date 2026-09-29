from urllib.parse import quote_plus


CATALOG = {

    "home": [

        (
            "LED Ceiling Light",
            "Lighting",
            "Amazon",
            1299
        ),

        (
            "Decorative Floor Lamp",
            "Lighting",
            "IKEA",
            3499
        ),

        (
            "Ceiling Fan",
            "Fan",
            "Amazon",
            2799
        ),

        (
            "Compact Dining Table",
            "Furniture",
            "IKEA",
            8999
        ),

        (
            "Minimal Wall Art Set",
            "Decor",
            "Amazon",
            1799
        ),

        (
            "Storage Cabinet",
            "Furniture",
            "Flipkart",
            5499
        )
    ],

    "party": [

        (
            "Party Catering Package",
            "Food",
            "Zomato",
            350
        ),

        (
            "Food Delivery Package",
            "Food",
            "Swiggy",
            325
        ),

        (
            "Budget Event Decor",
            "Decoration",
            "Amazon",
            2499
        ),

        (
            "Hotel / Stay Search",
            "Accommodation",
            "OYO",
            2500
        ),

        (
            "Table Decoration Set",
            "Decoration",
            "Flipkart",
            1599
        )
    ],

    "jewelry": [

        (
            "Minimal Pendant Necklace",
            "Necklace",
            "Amazon",
            999
        ),

        (
            "Classic Stud Earrings",
            "Earrings",
            "Flipkart",
            799
        ),

        (
            "Elegant Bracelet",
            "Bracelet",
            "Amazon",
            1199
        ),

        (
            "Statement Earrings",
            "Earrings",
            "Flipkart",
            1499
        ),

        (
            "Layered Necklace",
            "Necklace",
            "Amazon",
            1699
        )
    ]
}


PLATFORM_SEARCH = {

    "Amazon":
        "https://www.amazon.in/s?k=",

    "Flipkart":
        "https://www.flipkart.com/search?q=",

    "IKEA":
        "https://www.ikea.com/in/en/search/?q=",

    "Swiggy":
        "https://www.swiggy.com/search?query=",

    "Zomato":
        "https://www.zomato.com/search?query=",

    "OYO":
        "https://www.oyorooms.com/search?location="
}


def search_url(
    platform: str,
    query: str
) -> str:

    base_url = PLATFORM_SEARCH.get(
        platform,
        "https://www.google.com/search?q="
    )

    return (
        base_url
        + quote_plus(query)
    )


def fallback_items(
    planner: str,
    budget: float
):

    rows = sorted(
        CATALOG[planner],
        key=lambda item: item[3]
    )

    selected = []

    running_total = 0

    for (
        name,
        category,
        platform,
        price
    ) in rows:

        if running_total + price <= budget:

            selected.append(
                {
                    "name": name,
                    "category": category,
                    "platform": platform,
                    "estimated_price": float(price),
                    "reason": (
                        "Budget-friendly fallback "
                        "option from the local "
                        "demo catalog."
                    ),
                    "search_url": search_url(
                        platform,
                        name
                    )
                }
            )

            running_total += price

        if len(selected) >= 5:
            break

    return selected