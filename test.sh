script_directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$script_directory"

# Navigate to the backend directory
cd "$script_directory/backend"


# Execute tests for the vendors app
python manage.py test vendors

# Execute tests for the purchaseOrders app
python manage.py test purchaseOrders
