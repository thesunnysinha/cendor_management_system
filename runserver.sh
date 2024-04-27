script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$script_directory"

# Navigate to the backend directory
cd "$script_directory/backend"

cp .envExample .env

python manage.py deletepycachemigrations

python manage.py makemigrations api authApp purchaseOrders vendors

python manage.py migrate

python manage.py runserver 0.0.0.0:8000