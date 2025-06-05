db.createUser({
  user: "admin",
  pwd: "admin",
  roles: [
    {
      role: "readWrite",
      db: "strava",
    },
  ],
});

db = db.getSiblingDB("strava");

db.createCollection("test");

db.getCollection("test").insertOne({ name: "test", message: "Hello, world!" });

db.createCollection("users");
