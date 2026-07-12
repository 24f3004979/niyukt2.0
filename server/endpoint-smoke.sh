echo "Firing User Creation Endpoint :)"

function user_smoke(){
for i in {1..100}; do
  rand=$(head /dev/urandom | tr -dc a-z0-9 | head -c 5)
  username="user_${i}_${rand}"
  email="user_${i}@gmail.com"

  curl -X POST http://127.0.0.1:5000/api/users \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"${username}\", \"email\": \"${email}\", \"password\": \"1212\"}"

done

echo "SMOKED USER INTO DB"
}

function create_user(){
	local username=$1
	local email=$2
	local role=$3
curl -X POST http://127.0.0.1:5000/api/auth/register \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"${username}\", \"email\": \"${email}\", \"password\": \"1212\", \"role\": \"${role}\"}"
}

create_user "Admin" "admin@example.com" "admin"
