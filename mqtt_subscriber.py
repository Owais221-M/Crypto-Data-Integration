import pymysql
import pymongo
from neo4j import GraphDatabase
import logging
import time

logging.basicConfig(level=logging.INFO)

# MySQL connection
try:
    mysql_conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Ansari_221",
        database="crypto_transaction", 
        port=3308,
    )
    mysql_cursor = mysql_conn.cursor()
    logging.info("Connected to MySQL successfully.")
except Exception as e:
    logging.error(f"Error connecting to MySQL: {e}")
    raise

# MongoDB connection
try:
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["crypto_transaction"]
    mongo_collection = mongo_db["trades"]
    logging.info("Connected to MongoDB successfully.")
except Exception as e:
    logging.error(f"Error connecting to MongoDB: {e}")
    raise

# Neo4j connection
try:
    neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "9792609977"))
    logging.info("Connected to Neo4j successfully.")
except Exception as e:
    logging.error(f"Error connecting to Neo4j: {e}")
    raise

# Function to fetch the latest trade from MySQL (from 'transactions' table)
def fetch_latest_trade():
    try:
        mysql_query = "SELECT user_id, type AS action, coin AS pair, amount, price, created_at FROM transactions ORDER BY created_at DESC LIMIT 10"
        mysql_cursor.execute(mysql_query)
        trades = mysql_cursor.fetchall()
        
        if trades:
            trade_data = []
            for trade in trades:
                trade_data.append({
                    "user_id": trade[0],
                    "action": trade[1],
                    "pair": trade[2],
                    "amount": trade[3],
                    "price": trade[4],
                    "created_at": trade[5]
                })
            logging.info(f"Fetched {len(trade_data)} trades from MySQL.")
            return trade_data  # Return a list of trade data
        return None  # If no trade found
    except Exception as e:
        logging.error(f"Error fetching data from MySQL: {e}")
        return None

# Function to process and store the trade data
def process_trade(trade_data):
    try:
        for trade in trade_data:
            logging.info(f"Processing Trade: {trade}")

            user_id = trade.get("user_id")
            action = trade.get("action")
            pair = trade.get("pair")
            amount = float(trade.get("amount", 0))
            price = float(trade.get("price", 0))
            created_at = trade.get("created_at")

            logging.info(f"Trade Details - user_id: {user_id}, action: {action}, pair: {pair}, amount: {amount}, price: {price}, created_at: {created_at}")

            # Store in MongoDB
            mongo_trade = {
                "user_id": user_id,
                "action": action,
                "pair": pair,
                "amount": amount,
                "price": price,
                "created_at": created_at
            }
            mongo_collection.insert_one(mongo_trade)
            logging.info(f"Stored in MongoDB: {mongo_trade}")

            # Store in Neo4j
            with neo4j_driver.session() as session:
                session.run(
                    """
                    MERGE (u:User  {id: $user_id})
                    MERGE (c:Crypto {name: $pair})
                    CREATE (t:Trade {action: $action, amount: $amount, price: $price, created_at: $created_at})
                    CREATE (u)-[:EXECUTED]->(t)
                    CREATE (t)-[:FOR]->(c)
                    """,
                    user_id=user_id, action=action, pair=pair, amount=amount, price=price, created_at=created_at
                )
            logging.info("Stored in Neo4j!")

    except Exception as e:
        logging.error(f"Error processing trade: {e}")

try:
    while True:
        trade_data = fetch_latest_trade()
        if trade_data:
            process_trade(trade_data)
        else:
            logging.info("No new trade data found in MySQL.")

        time.sleep(10)
except Exception as e:
    logging.error(f"Error in main loop: {e}")

finally:
    mysql_conn.close()
    logging.info("MySQL connection closed.")
    neo4j_driver.close()
    logging.info("Neo4j driver closed.")
