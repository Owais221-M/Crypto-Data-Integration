# **Crypto Data Integration: A Real-Time Trade Processing System**

## **Project Overview**
This project integrates multiple technologies to receive, process, and store cryptocurrency trade data in real time. By using the **MQTT protocol**, **Python**, and **various databases** (MySQL, MongoDB, and Neo4j), it processes cryptocurrency trades (buy and sell), stores them in different platforms, and provides real-time updates.

- **Data Collection:** Uses MQTT to receive trade data.
- **Data Processing:** Trade data is processed, parsed, and then stored in **MySQL**, **MongoDB**, and **Neo4j** based on the topic of the trade.
- **Real-Time Integration:** The system integrates with MQTT for live data streaming, ensuring that all trades are updated in real-time.

---

## **Technologies Used**

- **MQTT** (Message Queuing Telemetry Transport): For receiving and publishing real-time trade data.
- **Python**: Main programming language used to process data.
- **MySQL**: For relational database management to store trade transactions.
- **MongoDB**: For document-based storage, focusing on flexibility for storing trade information.
- **Neo4j**: A graph database to store user-transaction relationships and cryptocurrency data in a graph format.

---

## **Project Features**

1. **Real-time Data Handling**: Trade data is fetched and stored in real-time using MQTT and Python.
2. **Multiple Database Storage**: Data is stored in MySQL (for structured storage), MongoDB (for document-oriented storage), and Neo4j (for graph-based relationships).
3. **Data Processing**: The system processes each trade and inserts the trade details into the databases.
4. **MQTT Subscriber**: Listens for trade updates and stores the data in databases.
5. **Data Analysis**: Supports queries to analyze trade actions, price, and amounts for specific cryptocurrency pairs.

---

## **Getting Started**

### **Prerequisites**

- **Python** 3.x
- **MySQL** (with a database set up)
- **MongoDB** (with the relevant collection created)
- **Neo4j** (with the necessary data models for users and trades)
- **MQTT Broker** (like Mosquitto or EMQ X)

### **Setting Up the Project**

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/crypto-data-integration.git
   cd crypto-data-integration
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the MySQL, MongoDB, and Neo4j databases:

   - Ensure that the **crypto_transaction** database exists in MySQL.
   - Set up a collection in MongoDB called **trades**.
   - Create necessary models and nodes in Neo4j for users and trades.

4. Run the **subscriber.py** to listen for incoming trade data:

   ```bash
   python mqtt_subscriber.py
   ```

5. (Optional) If you want to publish data to the MQTT topic, use **publish.php** to send trade data to the broker.

---

## **Database Source**

This project retrieves trade data from an existing project, which is uploaded on GitHub. The data is sourced from a **MySQL database** containing trade information, including user transactions, cryptocurrency pairs, amounts, and prices.

**GitHub Repository for Database Source:**  
[Link to Your Previous GitHub Project](https://github.com/yourusername/previous-project)

---

## **Running the Project**

1. Make sure that your MQTT broker is running and accessible.
2. Run the **subscriber.py** script to start listening for trade data and storing it in your databases.
3. You can query the **MySQL**, **MongoDB**, and **Neo4j** databases to see the processed data.

---

## **Example Queries**

### MySQL (for recent trades)
```sql
SELECT * FROM transactions WHERE created_at >= '2025-02-01 00:00:00';
```

### MongoDB (to get ETH trades)
```javascript
db.trades.find({ pair: "ETH" });
```

### Neo4j (to find all BTC trades)
```cypher
MATCH (t:Trade)-[:FOR]->(c:Crypto {name: "BTC"})
RETURN t;
```

---

## **Contributing**

Feel free to fork this project, open issues, or submit pull requests. Contributions are welcome!

---

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
