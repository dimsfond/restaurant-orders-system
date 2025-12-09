# Restaurant Orders API

## Business Problem & Solution Mapping
Restaurants need a system to manage customer orders efficiently, track order statuses, and maintain a history of changes for auditing and operational purposes.  
This API allows staff to:
- Create and manage orders for customers
- Track items and total amounts in orders
- Update order statuses (pending → preparing → ready → served → paid)
- View the history of order status changes  

It solves the business problem by providing a reliable, testable backend that keeps all order data structured and accessible.

## Technical Decisions & Trade-offs
- **FastAPI**: lightweight, modern Python framework with strong validation and testing support.
- **SQLite**: simple, file-based database for easy setup; ideal for small-scale deployment.
- **SQLAlchemy ORM**: clear database models, type safety, and relationship management.
- **Docker & Docker Compose**: provides a reproducible, isolated environment without requiring Python or dependencies on the host machine.
- **Pydantic**: request and response validation, type enforcement.
- **Trade-offs**: 
  - Authentication not implemented:  
  For this assessment, the focus was on the core business workflow: managing orders, customers, menu items, and order history with validations and audit logs. Implementing authentication (API keys, OAuth, JWT, etc.) would have added complexity and required additional time to implement, test, and secure. Since the main goal was to demonstrate API structure, workflow logic, and testing strategy, authentication was intentionally left out.
  - SQLite chosen for simplicity; production systems may use PostgreSQL or MySQL.

## How the System Solves the Problem
- Orders are validated and stored in the database.
- Each order tracks its items, quantities, and total cost.
- Status updates are logged in a history table for auditing.
- Tests cover all major functionality to ensure reliability.

## API Endpoints
Main available endpoints (also visible in the interactive docs at `http://localhost:8000/docs`):

- `POST /orders/` — Create a new order
- `GET /orders/` — List all orders (optionally filter by status)
- `GET /orders/{id}` — Get details of a single order
- `PATCH /orders/{id}/status` — Update an order status
- `DELETE /orders/{id}` — Delete an order
- `GET /orders/{id}/history` — View order status change history

## Exploring & Debugging the System
- API endpoints are documented via FastAPI’s interactive docs at `http://localhost:8000/docs` when running the app.
- Logs provide info for order creation, status updates, and errors.
- Database can be inspected via SQLite tools if needed.

## Setup and Testing Instructions (Docker)
1. Clone the repository:
   ```bash
   git clone https://github.com/dimsfond/restaurant-orders-system
   cd restaurant-orders-system
   ```

2. Create a .env file in the project root with the following content:
   ```bash
   # .env
   DATABASE_URL=sqlite:///./restaurant.db
   TEST_DATABASE_URL=sqlite:///./test.db
   ```

3. Create an empty SQLite database file in the project root so you can open it later with DB Browser (SQLite).
   ```bash
   touch restaurant.db
   ```
   **Note**: SQLAlchemy will create the necessary tables automatically on first run. The file just needs to exist so Docker can mount it correctly and you can open it with DB Browser (SQLite).

4. Start your container in detached mode so it keeps running in the background:  
   **!!!Note**: Make sure Docker Desktop is running before executing this command.
   ```bash
   docker-compose up --build -d
   ```

5. The API will be available at http://localhost:8000.

6. Access API documentation and test endpoints interactively at:
   http://localhost:8000/docs

7. Inspect or insert data directly in the database. If you have SQLite Browser (or DB Browser for SQLite) installed, you can open the
   restaurant.db file in the project root. Insert initial data for customers or menu items to test the API.
   Example SQL commands:
   ```sql
   -- Insert 5 customers
   INSERT INTO customers (table_number, is_present) VALUES (1, 1);
   INSERT INTO customers (table_number, is_present) VALUES (2, 1);
   INSERT INTO customers (table_number, is_present) VALUES (3, 0);
   INSERT INTO customers (table_number, is_present) VALUES (4, 1);
   INSERT INTO customers (table_number, is_present) VALUES (5, 0);

   -- Insert 5 menu items
   INSERT INTO menu_items (name, price) VALUES ('Margherita Pizza', 8.50);
   INSERT INTO menu_items (name, price) VALUES ('Pepperoni Pizza', 9.50);
   INSERT INTO menu_items (name, price) VALUES ('Espresso', 2.50);
   INSERT INTO menu_items (name, price) VALUES ('Cappuccino', 3.00);
   INSERT INTO menu_items (name, price) VALUES ('Chocolate Cake', 4.50);
   ```

8. To run automated tests inside Docker, you can enter the container:
   ```bash
   docker-compose exec api python -m pytest -v
   ```

9. Stop the application:
   ```bash
   docker-compose down
   ```

10. If you want to wipe all local data and start with a fresh database after step 9 above:
   - Delete the existing database file:
   ```bash
    rm ./restaurant.db
   ```

   - Create a new empty database file with the same name (or another name if you update .env):
   ```bash
    touch restaurant.db
   ```

   - Make sure your .env points to the correct file:
   ```bash
    DATABASE_URL=sqlite:///./restaurant.db
   ```

   - Start the container again:
   ```bash
    docker-compose up --build -d
   ```