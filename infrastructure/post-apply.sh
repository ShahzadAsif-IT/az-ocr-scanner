# Empty the file first
#: > .env                                   # truncate .env

# Iterate over every defined output
for key in $(terraform output -json | jq -r 'keys[]'); do
  echo "${key}=""$(terraform output -raw "${key}")""" >> .env
done

mv .env ..\.env
