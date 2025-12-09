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
- **Pydantic v2**: request and response validation, type enforcement.
- **Trade-offs**: 
  - Authentication not implemented.
  - SQLite chosen for simplicity; production systems may use PostgreSQL or MySQL.

## How the System Solves the Problem
- Orders are validated and stored in the database.
- Each order tracks its items, quantities, and total cost.
- Status updates are logged in a history table for auditing.
- Tests cover all major functionality to ensure reliability.

## Exploring & Debugging the System
- API endpoints are documented via FastAPI’s interactive docs at `http://localhost:8000/docs` when running the app.
- Logs provide info for order creation, status updates, and errors.
- Database can be inspected via SQLite tools if needed.

## Setup and Testing Instructions (Docker)
1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd restaurant-orders-system

2. Create a .env file with the following content:
   DATABASE_URL=<your-database-url>
   TEST_DATABASE_URL=<your-test-database-url>

3. Build and start the application using Docker Compose:
   docker-compose up --build

4. The API will be available at http://localhost:8000.

5. Access API documentation and test endpoints interactively at:
   http://localhost:8000/docs

6. To run tests inside Docker, you can enter the container:
   docker-compose exec api bash
   python -m pytest -v

7. Stop the application:
   docker-compose down