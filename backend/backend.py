from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from Controller.header_cntrl import HeaderCntrl
from Controller.home_cntrl import HomeCntrl
from Controller.products_cntrl import ProductsCntrl
from Controller.product_details_cntrl import ProductDetailsCntrl
from Controller.category_cntrl import CategoryCntrl
from Controller.search_cntrl import SearchCntrl
from Controller.ingest_cntrl import IngestCntrl
from DAO.db_object import PostgresDB

app = Flask(__name__)
API = Api(app)
CORS(app)

PostgresDB().create_database()

API.add_resource(HeaderCntrl, "/")
API.add_resource(HomeCntrl, "/home/")
API.add_resource(ProductsCntrl, "/products")
API.add_resource(ProductDetailsCntrl, "/products/<product_ID>")
API.add_resource(CategoryCntrl, "/category")
API.add_resource(SearchCntrl, "/search")
API.add_resource(IngestCntrl, "/ingestion")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=3000)
