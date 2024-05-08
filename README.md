# Vendor Management System

# Setup
1. Clone the repository:
   - git clone https://github.com/Pranali2510/vendor_system.git

2. Create a virtual environment:
    - py -3 -m venv myenv

3. Activate the virtual environment:
    - myenv\Scripts\activate

4. Install dependencies:
    - pip install -r requirements.txt

5. Update database settings:
    Open vendor_manage_system/settings.py
    Update the DATABASES configuration to match your database settings

6. Running the Project
    Apply database migrations:
    - python manage.py makemigrations
    - python manage.py migrate

7. Create a superuser:
    - python manage.py createsuperuser

8. Run the development server:
    - python manage.py runserver

Access the admin panel at http://127.0.0.1:8000/admin/ and use the superuser credentials to log in.

# API Endpoints
1. Generate Token:
    - POST: /api/generate_token/: Generate access and refresh tokens for a vendor.
    - POST /api/token/refresh/: Refresh the access token.

2. Vendor Profile:
    - POST /api/vendors/: Create a new vendor profile.
    - GET /api/vendors/: List all vendors.
    - GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
    - PUT /api/vendors/{vendor_id}/: Update a vendor's details.
    - DELETE /api/vendors/{vendor_id}/: Delete a vendor.

3. Purchase Order:
    - POST /api/purchase_orders/: Create a new purchase order.
    - GET /api/purchase_orders/: List all purchase orders.
    - GET /api/purchase_orders/{po_number}: Retrieve a specific purchase order.
    - PUT /api/purchase_orders/{po_number}: Update a purchase order.
    - DELETE /api/purchase_orders/{po_number}: Delete a purchase order.

4. Acknowledge Purchase Order:
    - POST /api/purchase_orders/{po_number}/acknowledge: Acknowledge a purchase order.

5. Vendor Performance Metrics:
    - GET /api/vendors/{vendor_code}/performance: Retrieve vendor performance metrics.

# Note
1. Use 3.9 or higher python version for this requirements.txt
2. Ensure the virtual environment is activated whenever you work on the project.
3. Customize the DATABASES configuration in settings.py according to your database setup.

