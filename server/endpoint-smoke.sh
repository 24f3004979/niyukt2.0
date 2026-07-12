echo "Firing User Creation Endpoint :)"

for i in {1..100}; do
  rand=$(head /dev/urandom | tr -dc a-z0-9 | head -c 5)
  username="user_${i}_${rand}"
  email="user_${i}@gmail.com"

  curl -X POST http://127.0.0.1:5000/api/users \
    -H "Content-Type: application/json" \
    -d "{\"username\": \"${username}\", \"email\": \"${email}\", \"password\": \"1212\"}"

done
