from fastapi import FastAPI, Query
 
app = FastAPI()
 
# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
    
    #Q1 - new products added
    {'id': 5, 'name': 'Laptop Stand',       'price':  799, 'category': 'Electronics',  'in_stock': True },
    {'id': 6, 'name': 'Mechanical Keyboard',       'price':  3499, 'category': 'Electronics',  'in_stock': True },
    {'id': 7, 'name': 'Webcam',       'price':  2999, 'category': 'Electronics',  'in_stock': False }
]
 
# ── Endpoint 0 — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint 1 — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}

@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    result = products          # start with all products
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
 
    return {'filtered_products': result, 'count': len(result)}

# ── Endpoint 2 — Return products by its category ──────────────────
# Q2 - Filter by category
@app.get("/products/category/{category_name}")

def get_by_category(category_name: str):
    result = [p for p in products if p["category"] == category_name] 

    if not result:
        return {"error": "No products found in this category"} 
    
    return {"category": category_name, "products": result, "total": len(result)}

# ── Endpoint 3 — Return products by stock availability ──────────────────
# Q3 - Display products if in-stock
@app.get("/products/instock")

def get_instock(): 
    available = [p for p in products if p["in_stock"]] 

    return {"in_stock_products": available, "count": len(available)}

# ── Endpoint 4 — Return summary of the store ──────────────────
# Q4 - Store summary
@app.get("/store/summary")
def store_summary(): 
    in_stock_count = len([p for p in products if p["in_stock"]]) 
    out_stock_count = len(products) - in_stock_count 
    categories = list(set([p["category"] for p in products])) 
    return { 
        "store_name": "My E-commerce Store", 
        "total_products": len(products), 
        "in_stock": in_stock_count, 
        "out_of_stock": out_stock_count, 
        "categories": categories, 
        }

# ── Endpoint 5 — Return product by product name ──────────────────
# Q5 - Search Products by name
@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [
        p for p in products if keyword.lower() in p["name"].lower()
    ]
    if not results:
        return {"message": "No products matched your search"}
    
    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

#  ── Endpoint 6 — Return product by Best Deal and Premium Pick ──────────────────
# Bonus Q - Cheapest & Most Expensive Product
@app.get("/products/deals")
def get_deals():

    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }
