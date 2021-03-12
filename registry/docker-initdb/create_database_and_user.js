
db = db.getSiblingDB('registry')

db.createCollection('schema');

db.createUser({
    user: "registry_user",
    pwd: "registry_secret",
    roles: [
        {
            role: "readWrite", db: "registry"
        }
    ]
})
